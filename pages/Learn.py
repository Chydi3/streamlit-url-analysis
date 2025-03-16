import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse
from datetime import datetime

def learn_about_phishing_urls():
    st.title("📢 Learn About Phishing URLs")
    
    st.header("1️⃣ How to Read URLs")
    with st.expander("🔍 Click to Expand: Understanding URL Components"):
        st.write("Understanding how to read a URL helps you identify legitimate websites and avoid phishing attempts. A URL consists of different parts, and phishing attacks often manipulate these to trick users.")
        url_table = """
        **URL Component** | **Definition** | **Example** | **Tip**  
        ------------------ | ------------ | ---------- | -------  
        **Protocol** | Specifies how your browser communicates with the site. | `https://` vs. `http://` | **Always look for HTTPS**, as it encrypts data.   
        **Domain** | The main website address, showing where the page is hosted. | `amazon.com` (Legit) vs. `amazon-login.com` (Fake) | Always check the main domain before clicking.  
        **Subdomain** | A prefix before the main domain, used to organize a website’s content. | `support.google.com` (Legit) vs. `google.secure-login.com` (Fake) | The real domain is **before the last dot** (e.g., `google.com`).  
        **Path** | The part after the domain, leading to a specific page. | `amazon.com/login` | Attackers mimic real website structures but change the domain.  
        **Query Parameters** | Extra information added to a URL, often seen after a `?`. | `example.com/search?q=free-gift` | Be cautious of **URLs with strange queries** leading to unexpected pages.  
        **Top-Level Domain (TLD)** | The ending of a domain name (.com, .org, .net, etc.). | `example.org` vs. `example.xyz` | Some phishing sites use uncommon TLDs.  
        """
        st.markdown(url_table)
        
        st.subheader("How to Analyze a URL Step by Step")
        st.markdown("""
        1️⃣ **Look for HTTPS** – A secure site should have `https://`, but be aware that some phishing sites also use HTTPS.
        
        2️⃣ **Identify the Main Domain** – Ignore everything before the **last two segments** (e.g., in `secure.paypal.com`, the real domain is `paypal.com`).
        
        3️⃣ **Check for Misspellings** – Fake websites often contain typos like `faceboook.com` instead of `facebook.com`.
        
        4️⃣ **Avoid Strange or Extra Subdomains** – A legitimate `google.com` URL should not contain subdomains like `secure-login.google.verify.com`.
        
        5️⃣ **Beware of Shortened URLs** – If you see `bit.ly/example`, use a URL expander to reveal the real link before clicking.
        """)
    
    st.header("2️⃣ How Attackers Manipulate URLs")
    with st.expander("⚠️ Click to Expand: Common Phishing Techniques"):
        phishing_table = """
        **Phishing Technique** | **Example** | **How It Tricks Users** | **Tip**  
        ------------------------ | ---------- | ---------------------- | ----  
        **Lookalike Domains** | `faceb00k.com` instead of `facebook.com` | Uses similar-looking characters to deceive users. | Always type URLs manually instead of clicking suspicious links.  
        **Misleading Subdomains** | `paypal.secure-login.com` instead of `paypal.com` | The real domain is `secure-login.com`, not `paypal.com`. | The **main domain is just before the last dot**.  
        **Fake HTTPS** | `https://secure-bank.com` (Fake) | Attackers buy SSL certificates to appear trustworthy. | HTTPS is necessary but not a guarantee of security.  
        **Shortened URLs** | `bit.ly/2Jj89XK` | Hides the real destination of the link. | Use URL expanders like **CheckShortURL** to reveal the full address.  
        **Homoglyph Attack** | `www.аpple.com` (Fake) vs. `www.apple.com` (Real) | Uses **foreign characters** that look identical to English letters. | Copy and paste the URL into a **plain text editor** to reveal hidden differences.  
        """
        st.markdown(phishing_table)
    
    st.header("3️⃣ Test a URL for Phishing Risk")
    url_input = st.text_input("🔗 Enter a URL to check:")
    if url_input:
        if "secure" in url_input or "login" in url_input or url_input.startswith("bit.ly"):
            st.warning("⚠️ This URL looks suspicious! Double-check before clicking.")
        else:
            st.success("✅ This URL does not appear suspicious, but always be cautious.")
    
    st.header("4️⃣ How to Spot a Phishing URL Before Clicking")
    st.markdown("""
    ✅ **Hover Over the Link** – Check the real destination before clicking.  
    ✅ **Look at the Main Domain** – Ignore the subdomain and focus on what’s before `.com`, `.org`, etc.  
    ✅ **Check for Misspellings** – Fake sites often have typos or extra letters.  
    ✅ **Be Wary of Urgency** – Phishing emails create panic (e.g., "Your account will be suspended in 24 hours!").  
    """)
    
    st.header("5️⃣ What to Do If You Click a Phishing Link")
    st.markdown("""
    - ❌ **Do NOT enter any information.**  
    - 🔄 **Close the browser immediately.**  
    - 🔑 **Change your password** (if you entered login details).  
    - 📢 **Report the phishing site** (Google Safe Browsing, IT support, or your security team).  
    """)
    
    st.header("6️⃣ Interactive Learning Module")
    st.markdown("This module provides hands-on learning about URL structure through three interactive tabs.")
    # Create tabs for the interactive learning module
    tab_hover, tab_feedback, tab_reflection = st.tabs(["Hover Over URL", "Real-Time URL Feedback", "Post-Quiz Reflection"])
    
    with tab_hover:
        st.subheader("Hover Over URL")
        st.write("Move your mouse over the parts of the URL to see explanations.")
        st.markdown(
            """
            <style>
            .url-part:hover {
                background-color: yellow;
                cursor: help;
            }
            </style>
            <p>
                <span class="url-part" title="Protocol: Indicates how the resource is accessed (e.g., https://)">https://</span>
                <span class="url-part" title="Domain: The main website domain where resources are hosted (e.g., example.com)">example.com</span>
                <span class="url-part" title="Path: Specific resource or page on the website (e.g., /login)">/login</span>
            </p>
            """,
            unsafe_allow_html=True
        )
    
    with tab_feedback:
        st.subheader("Real-Time URL Feedback")
        user_url = st.text_input("Enter a URL to analyze:", placeholder="https://example.com/login")
        if user_url:
            try:
                parsed = urlparse(user_url)
                st.write("### Parsed URL Components")
                st.write(f"**Scheme:** {parsed.scheme}")
                st.write(f"**Netloc (Domain):** {parsed.netloc}")
                st.write(f"**Path:** {parsed.path}")
            except Exception as e:
                st.error(f"Error parsing URL: {e}")
    
    with tab_reflection:
        st.subheader("Post-Quiz Reflection")
        reflection = st.text_area("What strategies did you use to determine where the URL goes?", height=150)
        if st.button("Submit Reflection"):
            st.success("Thank you for your input!")
            st.write("Your Reflection:", reflection)
    
    st.header("7️⃣ Quick Quiz: Test Your Knowledge")
    question = "Which of these URLs is safe to click?"
    options = ["paypal.security-login.com", "amazon-support.co", "support.google.com"]
    answer = st.radio(question, options)
    
    if st.button("Check Answer"):
        if answer == "support.google.com":
            st.success("✅ Correct! 'support.google.com' is a legitimate Google subdomain.")
        else:
            st.error("❌ Incorrect! The other options use misleading subdomains to trick users.")
    
    st.success("✅ Now that you've learned about phishing URLs, always stay alert online! 🚀")

def read_url_report():
    st.title("📊 How to Read URL Reports")
    
    st.header("1️⃣ Understanding URL Reports")
    with st.expander("🔍 Click to Expand: Components of a URL Report"):
        st.markdown("""
        A URL report contains various security assessments that help determine if a URL is safe. Here are the key components:
        
        - **Blacklist Status:** Checks if the URL is flagged for malware or phishing.
        - **SSL Certificate:** Determines if the website uses HTTPS for encryption.
        - **Domain Age:** Older domains are generally safer than newly registered ones.
        - **Suspicious Path Extensions:** Some file types, like `.php`, `.exe`, and `.zip`, may indicate a risk.
        - **Redirects:** Multiple redirects can hide a URL’s real destination.
        - **Risk Score:** A numerical score evaluating different security factors.
        """)
    
    st.header("2️⃣ How to Interpret a URL Report")
    with st.expander("📌 Click to Expand: Step-by-Step Guide"):
        st.markdown("""
        - **Blacklist Status:**  
          - *Not Blacklisted:* No known malicious activity.  
          - *Blacklisted:* Indicates a history of phishing or malware—avoid immediately.
        
        - **SSL Certificate:**  
          - *Valid:* Website uses HTTPS, ensuring data encryption.  
          - *Invalid/Expired:* A red flag that the connection may not be secure.
        
        - **Domain Age:**  
          - *Older Domains:* Generally more trustworthy.  
          - *New Domains (e.g., 0 days):* Could be used for short-term phishing campaigns.
        
        - **Suspicious Path Extension:**  
          - File types such as **.php**, **.exe**, or **.zip** can be associated with dynamic content or executables that might be risky.
        
        - **Redirects:**  
          - *Few or No Redirects:* Usually indicates a straightforward URL.  
          - *Multiple Redirects:* May be an attempt to hide the true destination.
        
        - **Risk Score:**  
          - A composite score derived from various factors.  
          - **Interpreting the Score:**  
            - **0-20:** Low risk (generally safe).  
            - **21-50:** Medium risk (caution advised).  
            - **51+:** High risk (likely unsafe).
        
        - **Final Decision:**  
          - Indicates the overall assessment. An “Allow” suggests the URL is safe despite minor concerns.
        """)
    
    st.header("3️⃣ Quick Quiz: Test Your Understanding")
    question = "What does a high 'Path Risk Score' indicate?"
    options = [
        "The domain is blacklisted",
        "The URL contains a potentially risky file extension",
        "The website has an expired SSL certificate"
    ]
    answer = st.radio(question, options)
    
    if st.button("Check Answer"):
        if answer == "The URL contains a potentially risky file extension":
            st.success("✅ Correct! A high path risk score often means the URL has a suspicious extension.")
        else:
            st.error("❌ Incorrect! Review the explanation and try again.")
    
    st.success("🚀 Now you know how to analyze a URL report! Stay cautious online.")

    st.header("4️⃣ Comprehensive Risk Score Breakdown")
    with st.expander("🔍 Click to Expand: Detailed Risk Score Information"):
        breakdown_data = [
            {
                "Risk Component": "Blacklist Status",
                "Explanation": "Indicates if the URL is flagged for malicious activity.",
                "Typical Values": "Not Blacklisted / Blacklisted",
                "Implications": "Blacklisted URLs are likely unsafe.",
                "Recommendations": "Avoid accessing if blacklisted."
            },
            {
                "Risk Component": "SSL Certificate",
                "Explanation": "Shows if the website uses HTTPS for encrypted communication.",
                "Typical Values": "Valid / Invalid / Expired",
                "Implications": "An invalid or expired certificate is a red flag.",
                "Recommendations": "Proceed only if certificate is valid."
            },
            {
                "Risk Component": "Domain Age",
                "Explanation": "Reflects the age of the domain; older domains tend to be more trustworthy.",
                "Typical Values": "0 days (new) to several years",
                "Implications": "New domains may be used for phishing.",
                "Recommendations": "Verify legitimacy for new domains."
            },
            {
                "Risk Component": "Suspicious Path Extension",
                "Explanation": "Checks for risky file extensions (e.g., .php, .exe, .zip) in the URL path.",
                "Typical Values": "Low risk: .html, .pdf; High risk: .php, .exe",
                "Implications": "Risk increases with suspicious extensions.",
                "Recommendations": "Exercise caution with high-risk file types."
            },
            {
                "Risk Component": "Redirects",
                "Explanation": "Number of times the URL redirects; excessive redirects may mask the final destination.",
                "Typical Values": "0-1 (normal) / 2+ (suspicious)",
                "Implications": "Multiple redirects can indicate malicious intent.",
                "Recommendations": "Investigate if too many redirects are present."
            },
            {
                "Risk Component": "Total Risk Score",
                "Explanation": "A composite score derived from all risk factors.",
                "Typical Values": "0-20: Low, 21-50: Medium, 51+: High",
                "Implications": "A higher score indicates greater overall risk.",
                "Recommendations": "Higher scores warrant increased caution."
            },
            {
                "Risk Component": "Final Decision",
                "Explanation": "The overall assessment based on the analysis.",
                "Typical Values": "Allow / Block",
                "Implications": "Indicates whether the URL is deemed safe.",
                "Recommendations": "Follow the final decision; if 'Block', do not proceed."
            }
        ]
        breakdown_df = pd.DataFrame(breakdown_data)
        st.table(breakdown_df)

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["Learn About Phishing URLs", "Read URL Reports"])
    
    if page == "Learn About Phishing URLs":
        learn_about_phishing_urls()
    elif page == "Read URL Reports":
        read_url_report()
    
if __name__ == "__main__":
    main()


