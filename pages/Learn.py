import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse
from datetime import datetime
import csv
import os
import time

# --- Ensure session_state variables exist ---
if "player_name" not in st.session_state:
    st.session_state.player_name = "Guest"
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

# Session state tracking for learning metrics
if "learn_start_time" not in st.session_state:
    st.session_state.learn_start_time = time.time()
if "learn_clicks" not in st.session_state:
    st.session_state.learn_clicks = 0

def count_click():
    st.session_state.learn_clicks += 1

# ====================== GOLD THEME DESIGN ======================
st.markdown("""
<style>
/* Global Theme */
html, body, [class*="css"] {
    background: linear-gradient(to bottom right, #0a0a1a, #121230, #1a1a40);
    color: #f1f1f1;
    font-family: 'Segoe UI', sans-serif;
}

/* Gold Headers */
h1 {
    color: #FFD700;
    animation: gold-glow 2s ease-in-out infinite alternate;
    text-shadow: 0 0 10px #FFD700;
    border-bottom: 2px solid #FFD700;
    padding-bottom: 8px;
    text-align: center;
}

h2 {
    color: #FFA500;
    border-bottom: 1px solid #FFA500;
    padding-bottom: 6px;
}

h3 {
    color: #1E90FF;
}

/* Gold Button Styles */
.stButton>button {
    background-color: rgba(0,0,0,0.3);
    border: 2px solid #FFD700;
    color: #FFD700;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #FFD700;
    color: #0a0a1a;
    transform: scale(1.05);
    box-shadow: 0 0 15px #FFD700;
}

/* Checkbox Styles */
.stCheckbox label {
    color: #FFA500 !important;
    font-weight: bold;
    font-size: 1.1rem;
}

.stCheckbox input:checked + label {
    color: #FF6B6B !important;
}

/* Table Styles */
.stTable {
    background-color: rgba(0,0,0,0.3) !important;
    border: 1px solid #FFD700;
}

.stTable th {
    background-color: rgba(255, 215, 0, 0.2) !important;
    color: #FFA500 !important;
}

.stTable td {
    background-color: rgba(0,0,0,0.3) !important;
    color: #f1f1f1 !important;
}

/* Text Area Styles */
.stTextArea textarea {
    background-color: rgba(30,30,30,0.5) !important;
    color: #f1f1f1 !important;
    border: 1px solid #1E90FF;
}

/* Radio Button Styles */
.stRadio label {
    color: #f1f1f1 !important;
    font-weight: normal;
}

.stRadio input:checked + label {
    color: #FFA500 !important;
    font-weight: bold;
}

/* Gold Glow Animation */
@keyframes gold-glow {
    from { text-shadow: 0 0 5px #FFD700, 0 0 10px #FFD700; }
    to   { text-shadow: 0 0 20px #FFD700, 0 0 30px #FFD700; }
}

/* Badge Styles */
.badge {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: rgba(0,0,0,0.5);
    padding: 0.5rem 1.2rem;
    border-radius: 20px;
    color: #FFD700;
    border: 1px solid #FFD700;
    font-weight: bold;
    font-size: 1.1rem;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    z-index: 100;
}

/* Section Styles */
.section {
    background-color: rgba(0,0,0,0.3);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1.5rem 0;
    border: 1px solid #1E90FF;
}

/* Tab Styles */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(0,0,0,0.3) !important;
    border: 1px solid #FFA500 !important;
    color: #f1f1f1 !important;
    border-radius: 8px !important;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background-color: #FFA500 !important;
    color: #0a0a1a !important;
    font-weight: bold !important;
}

/* Success/Error Messages */
.stSuccess {
    background-color: rgba(0, 100, 0, 0.3) !important;
    border: 1px solid #00ff00 !important;
    color: #00ff00 !important;
}

.stError {
    background-color: rgba(100, 0, 0, 0.3) !important;
    border: 1px solid #ff0000 !important;
    color: #ff0000 !important;
}

/* URL Hover Effect */
.url-part:hover {
    background-color: rgba(255, 165, 0, 0.3) !important;
    cursor: help;
    text-shadow: 0 0 10px #FFA500;
}

/* Sidebar Styles */
.stSidebar {
    background-color: rgba(10, 10, 30, 0.8) !important;
    border-right: 2px solid #FFD700;
}

.stRadio label {
    color: #FFD700 !important;
}
</style>
""", unsafe_allow_html=True)

# ====================== MAIN CONTENT ======================
def learn_about_phishing_urls():
    # Add version badge
    st.markdown('<div class="badge">v2.1</div>', unsafe_allow_html=True)
    
    st.title("📢 Learn About Phishing URLs")
    
    with st.container():
        st.header("1️⃣ How to Read URLs")
        if st.checkbox(
            "🔍 Click to Expand: Understanding URL Components",
            key="expander_read_urls",
            on_change=count_click
        ):
            st.write("Understanding how to read a URL helps you identify legitimate websites and avoid phishing attempts. A URL consists of different parts, and phishing attacks often manipulate these to trick users.")
            url_table = """
            **URL Component** | **Definition** | **Example** | **Tip**  
            ------------------ | ------------ | ---------- | -------  
            **Protocol** | Specifies how your browser communicates with the site. | `https://` vs. `http://` | **Always look for HTTPS**, as it encrypts data.   
            **Domain** | The main website address, showing where the page is hosted. | `amazon.com` (Legit) vs. `amazon-login.com` (Fake) | Always check the main domain before clicking.  
            **Subdomain** | A prefix before the main domain, used to organize a website's content. | `support.google.com` (Legit) vs. `google.secure-login.com` (Fake) | The real domain is **before the last dot** (e.g., `google.com`).  
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
    
    with st.container():
        st.header("2️⃣ How Attackers Manipulate URLs")
        if st.checkbox(
            "⚠️ Click to Expand: Common Phishing Techniques",
            key="expander_phishing_techniques",
            on_change=count_click
        ):
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
    
    with st.container():
        st.header("3️⃣ Test a URL for Phishing Risk")
        url_input = st.text_input(
            "Enter a URL to analyze:",
            key="learn_url_input",
            on_change=count_click
        )
        if url_input:
            if "secure" in url_input or "login" in url_input or url_input.startswith("bit.ly"):
                st.warning("⚠️ This URL looks suspicious! Double-check before clicking.")
            else:
                st.success("✅ This URL does not appear suspicious, but always be cautious.")
    
    with st.container():
        st.header("4️⃣ How to Spot a Phishing URL Before Clicking")
        st.markdown("""
        ✅ **Hover Over the Link** – Check the real destination before clicking.  
        ✅ **Look at the Main Domain** – Ignore the subdomain and focus on what's before `.com`, `.org`, etc.  
        ✅ **Check for Misspellings** – Fake sites often have typos or extra letters.  
        ✅ **Be Wary of Urgency** – Phishing emails create panic (e.g., "Your account will be suspended in 24 hours!").  
        """)
    
    with st.container():
        st.header("5️⃣ What to Do If You Click a Phishing Link")
        st.markdown("""
        - ❌ **Do NOT enter any information.**  
        - 🔄 **Close the browser immediately.**  
        - 🔑 **Change your password** (if you entered login details).  
        - 📢 **Report the phishing site** (Google Safe Browsing, IT support, or your security team).  
        """)
    
    with st.container():
        st.header("6️⃣ Interactive Learning Module")
        st.markdown("This module provides hands-on learning about URL structure through three interactive tabs.")
        tab_hover, tab_feedback, tab_reflection = st.tabs([
            "Hover Over URL", 
            "Real-Time URL Feedback", 
            "Post-Quiz Reflection"
        ])
        
        with tab_hover:
            st.subheader("Hover Over URL")
            st.write("Move your mouse over the parts of the URL to see explanations.")
            st.markdown(
                """
                <style>
                .url-part:hover {
                    background-color: rgba(255, 165, 0, 0.3) !important;
                    cursor: help;
                    text-shadow: 0 0 10px #FFA500;
                }
                </style>
                <p>
                    <span class="url-part" title="Protocol: Indicates how the resource is accessed (e.g., https://)" style="color:#FF6B6B; font-weight:bold;">https://</span>
                    <span class="url-part" title="Domain: The main website domain where resources are hosted (e.g., example.com)" style="color:#1E90FF; font-weight:bold;">example.com</span>
                    <span class="url-part" title="Path: Specific resource or page on the website (e.g., /login)" style="color:#FFA500; font-weight:bold;">/login</span>
                </p>
                """,
                unsafe_allow_html=True
            )
        
        with tab_feedback:
            st.subheader("Real-Time URL Feedback")
            user_url = st.text_input(
                "Enter a URL to analyze:",
                placeholder="https://example.com/login",
                key="feedback_url_input",
                on_change=count_click
            )
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
            reflection = st.text_area(
                "What strategies did you use to determine where the URL goes?",
                height=150,
                key="reflection_input",
                on_change=count_click
            )
            if st.button("Submit Reflection", key="reflection_submit"):
                count_click()
                st.success("Thank you for your input!")
                st.write("Your Reflection:", reflection)
    
    with st.container():
        st.header("7️⃣ Quick Quiz: Test Your Knowledge")
        question = "Which of these URLs is safe to click?"
        options = ["paypal.security-login.com", "amazon-support.co", "support.google.com"]
        answer = st.radio(
            question,
            options,
            key="quiz_safe_click",
            on_change=count_click
        )
        if st.button("Check Answer", key="quiz_check_answer"):
            count_click()
            if answer == "support.google.com":
                st.success("✅ Correct! 'support.google.com' is a legitimate Google subdomain.")
            else:
                st.error("❌ Incorrect! The other options use misleading subdomains to trick users.")
    
    with st.container():
        st.success("✅ Now that you've learned about phishing URLs, always stay alert online! 🚀")

    # Properly placed "Start Quiz" button at the end of the learning module
    st.write("---")
    if st.button("🧠 Start Quiz"):
        # 1) compute total learn time
        total_time = time.time() - st.session_state.learn_start_time

        # 2) append to learn_logs.csv
        log_file = "learn_logs.csv"
        header = ["User", "Learn Time (s)", "Learn Clicks", "Timestamp"]
        exists = os.path.exists(log_file)
        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(header)
            writer.writerow([
                st.session_state.player_name,
                f"{total_time:.1f}",
                st.session_state.learn_clicks,
                time.strftime("%Y-%m-%d %H:%M:%S")
            ])

        # 3) flip into quiz mode
        st.session_state.quiz_started = True
        st.switch_page("pages/Quiz.py")

def read_url_report():
    # Add version badge
    st.markdown('<div class="badge">v2.1</div>', unsafe_allow_html=True)
    
    st.title("📊 How to Read URL Reports")
    
    with st.container():
        st.header("1️⃣ Understanding URL Reports")
        if st.checkbox(
            "🔍 Click to Expand: Components of a URL Report",
            key="expander_report_components",
            on_change=count_click
        ):
            st.markdown("""
            A URL report contains various security assessments that help determine if a URL is safe. Here are the key components:
            
            - **Blacklist Status:** Checks if the URL is flagged for malware or phishing.
            - **SSL Certificate:** Determines if the website uses HTTPS for encryption.
            - **Domain Age:** Older domains are generally safer than newly registered ones.
            - **Suspicious Path Extensions:** Some file types, like `.php`, `.exe`, and `.zip`, may indicate a risk.
            - **Redirects:** Multiple redirects can hide a URL's real destination.
            - **Risk Score:** A numerical score evaluating different security factors.
            """)
    
    with st.container():
        st.header("2️⃣ How to Interpret a URL Report")
        if st.checkbox(
            "📌 Click to Expand: Step-by-Step Guide",
            key="expander_report_guide",
            on_change=count_click
        ):
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
              - Indicates the overall assessment. An "Allow" suggests the URL is safe despite minor concerns.
            """)
    
    with st.container():
        st.header("3️⃣ Quick Quiz: Test Your Understanding")
        question2 = "What does a high 'Path Risk Score' indicate?"
        options2 = [
            "The domain is blacklisted",
            "The URL contains a potentially risky file extension",
            "The website has an expired SSL certificate"
        ]
        answer2 = st.radio(
            question2,
            options2,
            key="quiz_path_risk",
            on_change=count_click
        )
        if st.button("Check Answer (Report Quiz)", key="quiz_path_risk_button"):
            count_click()
            if answer2 == "The URL contains a potentially risky file extension":
                st.success("✅ Correct! A high path risk score often means the URL has a suspicious extension.")
            else:
                st.error("❌ Incorrect! Review the explanation and try again.")
    
    with st.container():
        st.success("🚀 Now you know how to analyze a URL report! Stay cautious online.")

    with st.container():
        st.header("4️⃣ Comprehensive Risk Score Breakdown")
        if st.checkbox(
            "🔍 Click to Expand: Detailed Risk Score Information",
            key="expander_risk_breakdown",
            on_change=count_click
        ):
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
    # if they've clicked "Start Quiz" already, drop into Quiz.py
    if st.session_state.get("quiz_started", False):
        st.stop()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["Learn About Phishing URLs", "Read URL Reports"])
    
    if page == "Learn About Phishing URLs":
        learn_about_phishing_urls()
    elif page == "Read URL Reports":
        read_url_report()

if __name__ == "__main__":
    main()