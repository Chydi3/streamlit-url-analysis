import streamlit as st
import requests
import socket
from urllib.parse import urlparse
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# --- Your Existing URL Report Function ---
def get_url_report(url):
    # Ensure the URL has a scheme
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    report = {}
    try:
        # Use a custom user-agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # --- Basic Response Information ---
        report['Response Code'] = response.status_code
        report['Final URL'] = response.url
        report['Response Headers'] = dict(response.headers)
        
        # --- Security Headers ---
        sec_headers = {}
        for header in ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Content-Type-Options', 'X-Frame-Options']:
            if header in response.headers:
                sec_headers[header] = response.headers[header]
        report['Security Headers'] = sec_headers
        
        # --- Caching and Expiration ---
        caching = {}
        for header in ['Cache-Control', 'Expires']:
            if header in response.headers:
                caching[header] = response.headers[header]
        report['Caching and Expiration'] = caching
        
        # --- Redirects ---
        redirects = []
        if response.history:
            for resp in response.history:
                redirects.append({
                    'url': resp.url,
                    'status_code': resp.status_code
                })
        report['Redirects'] = redirects
        
        # --- Resource Information ---
        resource_info = {}
        for header in ['Content-Type', 'Content-Length']:
            if header in response.headers:
                resource_info[header] = response.headers[header]
        report['Resource Information'] = resource_info
        
        # --- IP Address and Location ---
        parsed_url = urlparse(response.url)
        domain = parsed_url.netloc.split(':')[0]  # Remove port if present
        
        try:
            ip_address = socket.gethostbyname(domain)
            report['IP Address'] = ip_address
            
            # Get geolocation details from ipinfo.io (free tier)
            ipinfo_url = f"https://ipinfo.io/{ip_address}/json"
            ipinfo_response = requests.get(ipinfo_url, timeout=10)
            if ipinfo_response.status_code == 200:
                report['IP Location'] = ipinfo_response.json()
            else:
                report['IP Location'] = {"error": "Unable to fetch location details"}
        except Exception as e:
            report['IP Address'] = "Could not resolve domain"
            report['IP Location'] = {"error": str(e)}
    
    except Exception as e:
        report['error'] = str(e)
    
    return report

def display_url_report():
    st.title("Live URL Report - Tabular View")
    
    url_input = st.text_input("Enter a URL to get a live report:")
    
    # Initialize session state for the report if not already set
    if "report" not in st.session_state:
        st.session_state.report = None

    # Fetch report on button click
    if st.button("Fetch Report"):
        if url_input:
            with st.spinner("Fetching data..."):
                st.session_state.report = get_url_report(url_input)
        else:
            st.error("Please enter a valid URL")
    
    # Display the report if it exists in session state
    if st.session_state.report is not None:
        report = st.session_state.report
        
        # Create Tabs for different sections of the report
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Basic Info", 
            "Response Headers", 
            "Security Headers", 
            "Resource Info", 
            "IP & Location", 
            "Additional Info"
        ])
        
        # Tab 1: Basic Info
        with tab1:
            st.subheader("Basic Information")
            basic_info = {
                "Response Code": report.get("Response Code"),
                "Final URL": report.get("Final URL")
            }
            st.table(pd.DataFrame(list(basic_info.items()), columns=["Property", "Value"]))
        
        # Tab 2: Response Headers
        with tab2:
            st.subheader("Response Headers")
            headers = report.get("Response Headers", {})
            if headers:
                st.table(pd.DataFrame(list(headers.items()), columns=["Header", "Value"]))
            else:
                st.write("No Response Headers available.")
        
        # Tab 3: Security Headers
        with tab3:
            st.subheader("Security Headers")
            sec_headers = report.get("Security Headers", {})
            if sec_headers:
                st.table(pd.DataFrame(list(sec_headers.items()), columns=["Header", "Value"]))
            else:
                st.write("No Security Headers available.")
        
        # Tab 4: Resource Information
        with tab4:
            st.subheader("Resource Information")
            resource_info = report.get("Resource Information", {})
            if resource_info:
                st.table(pd.DataFrame(list(resource_info.items()), columns=["Property", "Value"]))
            else:
                st.write("No Resource Information available.")
        
        # Tab 5: IP & Location with Map Integration
        with tab5:
            st.subheader("IP Address and Location")
            ip_address = report.get("IP Address", "N/A")
            st.write("**IP Address:**", ip_address)
            ip_location = report.get("IP Location", {})
            if ip_location:
                st.table(pd.DataFrame(list(ip_location.items()), columns=["Property", "Value"]))
                # If coordinates are available, display an interactive map
                if "loc" in ip_location:
                    loc_str = ip_location["loc"]  # expected format "lat,lon"
                    try:
                        lat, lon = map(float, loc_str.split(","))
                        m = folium.Map(location=[lat, lon], zoom_start=10)
                        # Add a marker with a popup containing the IP address
                        folium.Marker([lat, lon], popup=f"IP: {ip_address}").add_to(m)
                        st.markdown("### Map View")
                        st_folium(m, width=700, height=450)
                    except Exception as e:
                        st.error("Error parsing location coordinates: " + str(e))
                else:
                    st.write("Location coordinates not available.")
            else:
                st.write("No IP Location data available.")
        
        # Tab 6: Additional Information (Caching & Redirects)
        with tab6:
            st.subheader("Additional Information")
            caching = report.get("Caching and Expiration", {})
            st.write("**Caching and Expiration Headers:**")
            if caching:
                st.table(pd.DataFrame(list(caching.items()), columns=["Header", "Value"]))
            else:
                st.write("No caching headers provided.")
            st.write("**Redirects:**")
            redirects = report.get("Redirects", [])
            if redirects:
                st.table(pd.DataFrame(redirects))
            else:
                st.write("No redirects encountered.")

# --- New SERP API Integration for Google Ranking Information ---
def get_google_ranking(query, api_key):
    """
    Fetch Google ranking data from SERP API based on the search query.
    """
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "google_domain": "google.com",
        "hl": "en"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data from SERP API. Check your API key and query.")
        return None

def display_google_ranking_info():
    st.title("Google Ranking Information via SERP API")
    
    # User input for search query and SERP API key
    query = st.text_input("Enter your search query:")
    api_key = st.text_input("Enter your SERP API key:", type="password")
    
    if st.button("Get Ranking Info"):
        data = get_google_ranking(query, api_key)
        if data:
            # Display the entire JSON response for debugging/overview
            st.json(data)
            
            # Optionally, extract and display top organic results if available
            if "organic_results" in data:
                st.subheader("Top Organic Results")
                for result in data["organic_results"][:5]:
                    title = result.get('title', 'N/A')
                    link = result.get('link', 'N/A')
                    snippet = result.get('snippet', 'No description available.')
                    
                    st.markdown(f"**Title:** {title}")
                    st.markdown(f"**Link:** {link}")
                    st.markdown(f"**Description:** {snippet}")
                    st.markdown("---")

# --- Main Navigation ---
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["Live URL Report", "Google Ranking Info"])
    
    if page == "Live URL Report":
        display_url_report()
    elif page == "Google Ranking Info":
        display_google_ranking_info()

if __name__ == "__main__":
    main()

