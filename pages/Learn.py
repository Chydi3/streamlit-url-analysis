import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse
from datetime import datetime
import csv
import os
import time
from helpers import save_username_to_file, load_username_from_file

# --- New Click Logging Function ---
def log_click(element_id):
    """Log user interaction with element and timestamp"""
    if "player_name" in st.session_state and st.session_state.player_name:
        log_file = "click_logs.csv"
        header = ["User", "Element_ID", "Timestamp", "Human_Time"]
        exists = os.path.exists(log_file)
        
        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(header)
            writer.writerow([
                st.session_state.player_name,
                element_id,
                time.time(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

# --- Ensure session_state variables exist ---
# Preserve user-entered name from Home.py
if "player_name" not in st.session_state or not st.session_state.player_name.strip():
    st.session_state.player_name = load_username_from_file()
    print(f"Loaded player name: {st.session_state.player_name}")
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_page" not in st.session_state:
    st.session_state.current_page = ""
if "learn_metrics_logged" not in st.session_state:
    st.session_state.learn_metrics_logged = False

# Session state tracking for learning metrics
if "learn_start_time" not in st.session_state:
    st.session_state.learn_start_time = time.time()
if "learn_clicks" not in st.session_state:
    st.session_state.learn_clicks = 0
if "click_log" not in st.session_state:  # Added for click tracking
    st.session_state.click_log = []

# Track which checkboxes/radios have been interacted with
if "expander_read_urls" not in st.session_state:
    st.session_state.expander_read_urls = False
if "expander_phishing_techniques" not in st.session_state:
    st.session_state.expander_phishing_techniques = False
if "learn_url_input" not in st.session_state:
    st.session_state.learn_url_input = ""
if "feedback_url_input" not in st.session_state:
    st.session_state.feedback_url_input = ""
if "reflection_input" not in st.session_state:
    st.session_state.reflection_input = ""
if "quiz_safe_click" not in st.session_state:
    st.session_state.quiz_safe_click = None  # Changed to None
if "expander_report_components" not in st.session_state:
    st.session_state.expander_report_components = False
if "expander_report_guide" not in st.session_state:
    st.session_state.expander_report_guide = False
if "quiz_path_risk" not in st.session_state:
    st.session_state.quiz_path_risk = None  # Changed to None
if "expander_risk_breakdown" not in st.session_state:
    st.session_state.expander_risk_breakdown = False

def count_click():
    st.session_state.learn_clicks += 1

def log_learning_metrics():
    if not st.session_state.learn_metrics_logged:
        total_time = time.time() - st.session_state.learn_start_time
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
        st.session_state.learn_metrics_logged = True

# ====================== SYSTEM-COMPATIBLE THEME ======================
st.markdown("""
<style>
/* System-compatible base */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Red-glowing headers */
h1 {
    color: #FF4D4D;
    animation: red-glow 2s ease-in-out infinite alternate;
    text-shadow: 0 0 5px #FF4D4D;
    border-bottom: 2px solid #FF4D4D;
    padding-bottom: 8px;
    text-align: center;
}

h2 {
    color: #FF4D4D;
    border-bottom: 1px solid #FF4D4D;
    padding-bottom: 6px;
}

h3 {
    color: #1E90FF;
}

/* Buttons */
.stButton>button {
    background-color: transparent;
    border: 2px solid #FF4D4D;
    color: #FF4D4D;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #FF4D4D;
    color: white;
    transform: scale(1.05);
}

/* Tables */
.stTable {
    border: 1px solid var(--border-color);
}
.stTable th {
    background-color: rgba(255, 77, 77, 0.1) !important;
}
.stTable td {
    background-color: var(--background-color) !important;
}

/* Glow Animation */
@keyframes red-glow {
    from { text-shadow: 0 0 5px #FF4D4D; opacity: 0.9; }
    to { text-shadow: 0 0 15px #FF4D4D; opacity: 1; }
}

/* Theme Variables */
:root {
    --background-color: inherit;
    --text-color: inherit;
    --border-color: #FF4D4D;
}
@media (prefers-color-scheme: dark) {
    :root {
        --border-color: #FF6B6B;
    }
}
</style>
""", unsafe_allow_html=True)

# ====================== LEARN-PAGE PROGRESS CALCULATION ======================
def calculate_learn_progress():
    # 6 interactive items on "Learn About Phishing URLs" page:
    total_learn_items = 6
    completed = 0
    if st.session_state.expander_read_urls:
        completed += 1
    if st.session_state.expander_phishing_techniques:
        completed += 1
    if st.session_state.learn_url_input:
        completed += 1
    if st.session_state.feedback_url_input:
        completed += 1
    if st.session_state.reflection_input:
        completed += 1
    if st.session_state.quiz_safe_click is not None:  # Check for not None
        completed += 1
    return int((completed / total_learn_items) * 100)

# ====================== REPORT-PAGE PROGRESS CALCULATION ======================
def calculate_report_progress():
    # 4 interactive items on "Read URL Reports" page:
    total_report_items = 4
    completed = 0
    if st.session_state.expander_report_components:
        completed += 1
    if st.session_state.expander_report_guide:
        completed += 1
    if st.session_state.quiz_path_risk is not None:  # Check for not None
        completed += 1
    if st.session_state.expander_risk_breakdown:
        completed += 1
    return int((completed / total_report_items) * 100)

# ====================== MAIN CONTENT ======================
def learn_about_phishing_urls():
    # Add version badge
    st.markdown('<div class="badge">v2.1</div>', unsafe_allow_html=True)
    
    # Show progress bar for Learn page
    learn_pct = calculate_learn_progress()
    st.markdown(f"**Learning Progress: {learn_pct}%**")
    st.progress(learn_pct)

    st.title("📢 Learn About Phishing URLs")
    
    with st.container():
        st.header("1️⃣ How to Read URLs" + (" ✅" if st.session_state.expander_read_urls else ""))
        if st.checkbox(
            "🔍 Click to Expand: Understanding URL Components",
            key="expander_read_urls",
            on_change=lambda: [count_click(), log_click("expander_read_urls")]
        ):
            st.write("Understanding how to read a URL helps you identify legitimate websites and avoid phishing attempts. A URL consists of different parts, and phishing attacks often manipulate these to trick users.")
            url_table = """
            **URL Component** | **Definition** | **Example** | **Tip**  
            ------------------ | ------------ | ---------- | -------  
            **Protocol** | Specifies how your browser communicates with the site. | https:// vs. http:// | **Always look for HTTPS**, as it encrypts data.   
            **Domain** | The main website address, showing where the page is hosted. | amazon.com (Legit) vs. amazon-login.com (Fake) | Always check the main domain before clicking.  
            **Subdomain** | A prefix before the main domain, used to organize a website's content. | support.google.com (Legit) vs. google.secure-login.com (Fake) | The real domain is **before the last dot** (e.g., google.com).  
            **Path** | The part after the domain, leading to a specific page. | amazon.com/login | Attackers mimic real website structures but change the domain.  
            **Query Parameters** | Extra information added to a URL, often seen after a ?. | example.com/search?q=free-gift | Be cautious of **URLs with strange queries** leading to unexpected pages.  
            **Top-Level Domain (TLD)** | The ending of a domain name (.com, .org, .net, etc.). | example.org vs. example.xyz | Some phishing sites use uncommon TLDs.  
            """
            st.markdown(url_table)
            
            st.subheader("How to Analyze a URL Step by Step")
            st.markdown("""
            1️⃣ **Look for HTTPS** – A secure site should have https://, but be aware that some phishing sites also use HTTPS.
            
            2️⃣ **Identify the Main Domain** – Ignore everything before the **last two segments** (e.g., in secure.paypal.com, the real domain is paypal.com).
            
            3️⃣ **Check for Misspellings** – Fake websites often contain typos like faceboook.com instead of facebook.com.
            
            4️⃣ **Avoid Strange or Extra Subdomains** – A legitimate google.com URL should not contain subdomains like secure-login.google.verify.com.
            
            5️⃣ **Beware of Shortened URLs** – If you see bit.ly/example, use a URL expander to reveal the real link before clicking.
            """)

    with st.container():
        st.header("2️⃣ How Attackers Manipulate URLs" + (" ✅" if st.session_state.expander_phishing_techniques else ""))
        if st.checkbox(
            "⚠️ Click to Expand: Common Phishing Techniques",
            key="expander_phishing_techniques",
            on_change=lambda: [count_click(), log_click("expander_phishing_techniques")]
        ):
            phishing_table = """
            **Phishing Technique** | **Example** | **How It Tricks Users** | **Tip**  
            ------------------------ | ---------- | ---------------------- | ----  
            **Lookalike Domains** | faceb00k.com instead of facebook.com | Uses similar-looking characters to deceive users. | Always type URLs manually instead of clicking suspicious links.  
            **Misleading Subdomains** | paypal.secure-login.com instead of paypal.com | The real domain is secure-login.com, not paypal.com. | The **main domain is just before the last dot**.  
            **Fake HTTPS** | https://secure-bank.com (Fake) | Attackers buy SSL certificates to appear trustworthy. | HTTPS is necessary but not a guarantee of security.  
            **Shortened URLs** | bit.ly/2Jj89XK | Hides the real destination of the link. | Use URL expanders like **CheckShortURL** to reveal the full address.  
            **Homoglyph Attack** | www.аpple.com (Fake) vs. www.apple.com (Real) | Uses **foreign characters** that look identical to English letters. | Copy and paste the URL into a **plain text editor** to reveal hidden differences.  
            """
            st.markdown(phishing_table)
    
    with st.container():
        st.header("3️⃣ Test a URL for Phishing Risk" + (" ✅" if st.session_state.learn_url_input else ""))
        url_input = st.text_input(
            "Enter a URL to analyze:",
            key="learn_url_input",
            on_change=lambda: [count_click(), log_click("learn_url_input")]
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
        ✅ **Look at the Main Domain** – Ignore the subdomain and focus on what's before .com, .org, etc.  
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
        st.header("6️⃣ Interactive Learning Module" + (
            " ✅" if (st.session_state.feedback_url_input and st.session_state.reflection_input) else ""
        ))
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
                on_change=lambda: [count_click(), log_click("feedback_url_input")]
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
                on_change=lambda: [count_click(), log_click("reflection_input")]
            )
            if st.button("Submit Reflection", key="reflection_submit", on_click=lambda: log_click("reflection_submit")):
                st.success("Thank you for your input!")
                st.write("Your Reflection:", reflection)
    
    with st.container():
        st.header("7️⃣ Quick Quiz: Test Your Knowledge" + (" ✅" if st.session_state.quiz_safe_click is not None else ""))
        question = "Which of these URLs is safe to click?"
        options = ["paypal.security-login.com", "amazon-support.co", "support.google.com"]
        
        answer = st.radio(
            question,
            options,
            index=None,
            key="quiz_safe_click",
            on_change=lambda: [count_click(), log_click("quiz_safe_click")]
        )
        if st.button("Check Answer", key="quiz_check_answer", on_click=lambda: log_click("quiz_check_answer")):
            if answer == "support.google.com":
                st.success("✅ Correct! 'support.google.com' is a legitimate Google subdomain.")
            else:
                st.error("❌ Incorrect! The other options use misleading subdomains to trick users.")
    
    with st.container():
        st.success("✅ Now that you've learned about phishing URLs, always stay alert online! 🚀")

    if st.button("🧠 Start Quiz", on_click=lambda: [count_click(), log_click("start_quiz")]):
        log_learning_metrics()
        st.session_state.quiz_started = True
        st.switch_page("pages/Quiz.py")

def read_url_report():
    # Add version badge
    st.markdown('<div class="badge">v2.1</div>', unsafe_allow_html=True)
    
    # Show progress bar for Report page
    report_pct = calculate_report_progress()
    st.markdown(f"**Report Progress: {report_pct}%**")
    st.progress(report_pct)

    st.title("📊 How to Read URL Reports")
    
    with st.container():
        st.header("1️⃣ Understanding URL Reports" + (" ✅" if st.session_state.expander_report_components else ""))
        if st.checkbox(
            "🔍 Click to Expand: Components of a URL Report",
            key="expander_report_components",
            on_change=lambda: [count_click(), log_click("expander_report_components")]
        ):
            st.markdown("""
            A URL report contains various security assessments that help determine if a URL is safe. Here are the key components:
            
            - **Blacklist Status:** Checks if the URL is flagged for malware or phishing.
            - **SSL Certificate:** Determines if the website uses HTTPS for encryption.
            - **Domain Age:** Older domains are generally safer than newly registered ones.
            - **Suspicious Path Extensions:** Some file types, like .php, .exe, and .zip, may indicate a risk.
            - **Redirects:** Multiple redirects can hide a URL's real destination.
            - **Risk Score:** A numerical score evaluating different security factors.
            """)
    
    with st.container():
        st.header("2️⃣ How to Interpret a URL Report" + (" ✅" if st.session_state.expander_report_guide else ""))
        if st.checkbox(
            "📌 Click to Expand: Step-by-Step Guide",
            key="expander_report_guide",
            on_change=lambda: [count_click(), log_click("expander_report_guide")]
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
        st.header("3️⃣ Quick Quiz: Test Your Understanding" + (" ✅" if st.session_state.quiz_path_risk is not None else ""))
        question2 = "What does a high 'Path Risk Score' indicate?"
        options2 = [
            "The domain is blacklisted",
            "The URL contains a potentially risky file extension",
            "The website has an expired SSL certificate"
        ]
        
        answer2 = st.radio(
            question2,
            options2,
            index=None,
            key="quiz_path_risk",
            on_change=lambda: [count_click(), log_click("quiz_path_risk")]
        )
        if st.button("Check Answer (Report Quiz)", key="quiz_path_risk_button", on_click=lambda: log_click("quiz_path_risk_button")):
            if answer2 == "The URL contains a potentially risky file extension":
                st.success("✅ Correct! A high path risk score often means the URL has a suspicious extension.")
            else:
                st.error("❌ Incorrect! Review the explanation and try again.")

    with st.container():
        st.success("🚀 Now you know how to analyze a URL report! Stay cautious online.")

    with st.container():
        st.header("4️⃣ Comprehensive Risk Score Breakdown" + (" ✅" if st.session_state.expander_risk_breakdown else ""))
        if st.checkbox(
            "🔍 Click to Expand: Detailed Risk Score Information",
            key="expander_risk_breakdown",
            on_change=lambda: [count_click(), log_click("expander_risk_breakdown")]
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

    if st.button("🧠 Start Quiz", 
                key="report_start_quiz",
                on_click=lambda: log_click("report_start_quiz")):
        log_learning_metrics()
        st.session_state.quiz_started = True
        st.switch_page("pages/Quiz.py")

# This is where the read_url_report() function ends

def main():
    # if they've clicked "Start Quiz" already, drop into Quiz.py
    if st.session_state.get("quiz_started", False):
        st.stop()

    st.sidebar.title("Navigation")
    previous_page = st.session_state.current_page
    page = st.sidebar.radio("Go to:", ["Learn About Phishing URLs", "Read URL Reports"], 
                           on_change=lambda: log_click("sidebar_navigation"))
    
    # Detect navigation away from learning page
    if previous_page == "Learn About Phishing URLs" and page != "Learn About Phishing URLs":
        log_learning_metrics()
    
    # Update current page in session state
    st.session_state.current_page = page
    
    if page == "Learn About Phishing URLs":
        learn_about_phishing_urls()
    elif page == "Read URL Reports":
        read_url_report()

if __name__ == "__main__":
    main()
