import streamlit as st
import re
import ssl
import socket
import urllib.parse
import requests
import math
import datetime
import json
import sqlite3
import pandas as pd
from fpdf import FPDF
import io  # For handling in-memory PDF files
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import openai  # For AI-powered chatbot

# Optional: Install the python-whois package via pip: pip install python-whois
try:
    import whois
except ImportError:
    whois = None  # In production, ensure that the whois module is installed

###############################################
# CODE 1: URL Safety Analyzer (All Features) #
###############################################

class URLSafetyAnalyzer:
    def __init__(self, url, user_context=None):
        """
        Initializes the analyzer with the URL and optional user context.
        :param url: The URL to analyze.
        :param user_context: A dictionary containing context like region and browsing history.
        """
        self.original_url = url
        self.user_context = user_context
        self.normalized_url = self.normalize_url(url)
        self.parsed_url = self.parse_url(self.normalized_url)
        self.risk_scores = {}  # Holds risk scores from each analysis module
        self.total_risk_score = 0
        self.report = {}

    # 1. URL Parsing and Normalization
    def normalize_url(self, url):
        """Normalizes the URL by decoding URL-encoded characters."""
        return urllib.parse.unquote(url)

    def parse_url(self, url):
        """Decomposes the URL into its components."""
        parsed = urllib.parse.urlparse(url)
        domain = parsed.hostname
        port = parsed.port
        subdomain = self.extract_subdomain(domain)
        return {
            'protocol': parsed.scheme,
            'domain': domain,
            'subdomain': subdomain,
            'path': parsed.path,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'port': port
        }

    def extract_subdomain(self, hostname):
        """Extracts the subdomain (if any) from the hostname.
        Assumes that the main domain is the last two labels."""
        if hostname:
            parts = hostname.split('.')
            if len(parts) > 2:
                return '.'.join(parts[:-2])
        return ''

    # 2. Static Analysis
    def static_analysis(self):
        """Performs static analysis by checking domain reputation, path/query, and subdomain."""
        domain_risk = self.domain_reputation_check(self.parsed_url['domain'])
        path_risk = self.path_and_query_analysis(self.parsed_url['path'], self.parsed_url['query'])
        subdomain_risk = self.subdomain_analysis(self.parsed_url['subdomain'])
        self.risk_scores['static'] = domain_risk + path_risk + subdomain_risk

        self.report['static_analysis'] = {
            'domain_risk': domain_risk,
            'path_risk': path_risk,
            'subdomain_risk': subdomain_risk
        }
        return self.risk_scores['static']

    def domain_reputation_check(self, domain):
        """Checks the domain against blacklists, WHOIS details, and validates its SSL certificate."""
        risk = 0
        details = {}

        # a. Blacklist Check (using a dummy blacklist)
        blacklisted_domains = ['malicious.com', 'evil.com', 'badsite.net']
        if domain in blacklisted_domains:
            risk += 50
            details['blacklist'] = True
        else:
            details['blacklist'] = False

        # b. WHOIS Lookup: Check for recent creation
        if whois:
            try:
                domain_info = whois.whois(domain)
                creation_date = domain_info.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                if creation_date:
                    age_days = (datetime.datetime.now() - creation_date).days
                    if age_days < 180:
                        risk += 20
                        details['recently_created'] = True
                    else:
                        details['recently_created'] = False
                else:
                    details['creation_date_unknown'] = True
            except Exception as e:
                details['whois_lookup_failed'] = True
                risk += 10
        else:
            details['whois_not_available'] = True
            risk += 10

        # c. SSL/TLS Certificate Validation if using HTTPS
        if self.parsed_url['protocol'] == 'https':
            cert_valid, cert_details = self.validate_ssl_certificate(domain, self.parsed_url.get('port') or 443)
            details['ssl_certificate'] = cert_details
            if not cert_valid:
                risk += 20

        self.report['domain_reputation'] = details
        return risk

    def validate_ssl_certificate(self, domain, port=443):
        """Validates the SSL/TLS certificate for the given domain."""
        try:
            context = ssl.create_default_context()
            with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain) as conn:
                conn.settimeout(5.0)
                conn.connect((domain, port))
                cert = conn.getpeercert()
                not_after = cert.get('notAfter')
                expiry = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                if expiry < datetime.datetime.now():
                    return False, {'expired': True}
                else:
                    return True, {'expired': False}
        except Exception as e:
            return False, {'error': str(e)}

    def path_and_query_analysis(self, path, query):
        """Analyzes the URL path and query for phishing keywords, suspicious extensions, and risky parameters."""
        risk = 0
        details = {}

        phishing_keywords = ['login', 'verify', 'account', 'update', 'secure']
        for keyword in phishing_keywords:
            if keyword in path.lower():
                risk += 5
                details.setdefault('phishing_keywords', []).append(keyword)

        suspicious_extensions = ['.exe', '.php', '.js']
        for ext in suspicious_extensions:
            if path.lower().endswith(ext):
                risk += 10
                details.setdefault('suspicious_extension', []).append(ext)

        if query:
            params = urllib.parse.parse_qs(query)
            for param in params:
                if param.lower() in ['redirect', 'cmd']:
                    risk += 10
                    details.setdefault('risky_parameters', []).append(param)

        self.report['path_query_analysis'] = details
        return risk

    def subdomain_analysis(self, subdomain):
        """Analyzes the subdomain by calculating its entropy and checking for typosquatting."""
        risk = 0
        details = {}

        if subdomain:
            entropy = self.calculate_entropy(subdomain)
            details['entropy'] = entropy
            if entropy > 3.5:  # Threshold for suspecting algorithmically generated domains
                risk += 15
                details['dga_suspected'] = True

            # Typosquatting detection: check against common domains
            common_domains = ['google', 'facebook', 'amazon']
            for cd in common_domains:
                if cd in subdomain.lower() and subdomain.lower() != cd:
                    risk += 10
                    details.setdefault('typosquatting', []).append(subdomain)

        self.report['subdomain_analysis'] = details
        return risk

    def calculate_entropy(self, s):
        """Calculates the Shannon entropy of a string."""
        prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
        entropy = -sum([p * math.log(p, 2) for p in prob])
        return entropy

    # 3. Dynamic Analysis
    def dynamic_analysis(self):
        """Performs a simulated dynamic analysis by executing the URL and tracking redirects."""
        risk = 0
        details = {}
        try:
            session = requests.Session()
            response = session.get(self.normalized_url, timeout=5, allow_redirects=True)
            redirect_chain = [resp.url for resp in response.history] + [response.url]
            details['redirect_chain'] = redirect_chain
            if len(redirect_chain) > 3:
                risk += 10
        except Exception as e:
            details['error'] = str(e)
            risk += 10

        self.report['dynamic_analysis'] = details
        self.risk_scores['dynamic'] = risk
        return risk

    # 4. Machine Learning (ML) Models (Simulated)
    def ml_analysis(self):
        """Simulates ML-based risk scoring using lexical, host-based, and behavioral features."""
        risk = 0
        details = {}
        url_length = len(self.normalized_url)
        num_subdomains = len(self.parsed_url['subdomain'].split('.')) if self.parsed_url['subdomain'] else 0
        special_chars = len(re.findall(r'[^a-zA-Z0-9]', self.normalized_url))
        details['lexical'] = {
            'url_length': url_length,
            'num_subdomains': num_subdomains,
            'special_chars': special_chars
        }

        domain_age_days = 0
        if whois:
            try:
                domain_info = whois.whois(self.parsed_url['domain'])
                creation_date = domain_info.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                if creation_date:
                    domain_age_days = (datetime.datetime.now() - creation_date).days
            except Exception as e:
                domain_age_days = 0
        details['host_based'] = {
            'domain_age_days': domain_age_days
        }

        redirect_chain = self.report.get('dynamic_analysis', {}).get('redirect_chain', [])
        redirect_count = len(redirect_chain)
        details['behavioral'] = {
            'redirect_count': redirect_count
        }

        risk = (url_length / 100) + (num_subdomains * 2) + (special_chars / 50)
        if domain_age_days < 180:
            risk += 5
        if redirect_count > 3:
            risk += 5

        self.report['ml_analysis'] = details
        self.risk_scores['ml'] = risk
        return risk

    # 5. Threat Intelligence Integration
    def threat_intelligence_integration(self):
        """Simulates integration with threat intelligence APIs by checking the resolved IP."""
        risk = 0
        details = {}
        known_malicious_ips = ['192.168.1.100']  # Dummy list
        try:
            ip = socket.gethostbyname(self.parsed_url['domain'])
            details['resolved_ip'] = ip
            if ip in known_malicious_ips:
                risk += 30
        except Exception as e:
            details['ip_lookup_error'] = str(e)
        self.report['threat_intel'] = details
        self.risk_scores['threat_intel'] = risk
        return risk

    # 6. Obfuscation Detection
    def obfuscation_detection(self):
        """Detects URL obfuscation techniques such as hexadecimal encoding and use of shortened URL services."""
        risk = 0
        details = {}
        if re.search(r'%[0-9a-fA-F]{2}', self.original_url):
            details['hex_encoding'] = True
            risk += 5

        if self.parsed_url['domain'] and re.match(r'^\d{1,3}(\.\d{1,3}){3}$', self.parsed_url['domain']):
            details['ipv4_address'] = True
            risk += 10

        shortened_services = ['bit.ly', 'goo.gl', 'tinyurl.com']
        if self.parsed_url['domain'] in shortened_services:
            details['shortened_url'] = True
            risk += 10

        self.report['obfuscation_detection'] = details
        self.risk_scores['obfuscation'] = risk
        return risk

    # 7. User Context Analysis
    def user_context_analysis(self):
        """Analyzes user context (region and browsing history) to adjust risk scoring."""
        risk = 0
        details = {}
        if self.user_context and 'region' in self.user_context:
            if self.parsed_url['domain'] and self.parsed_url['domain'].endswith('.ru') and self.user_context['region'] != 'Russia':
                risk += 10
                details['geolocation_mismatch'] = True

        if self.user_context and 'history' in self.user_context:
            if self.parsed_url['domain'] not in self.user_context['history']:
                risk += 5
                details['new_domain'] = True

        self.report['user_context_analysis'] = details
        self.risk_scores['user_context'] = risk
        return risk

    # 8. Decision-Making Workflow
    def decision_making_workflow(self):
        """Combines all risk scores to decide whether to block or allow the URL."""
        total = 0
        component_scores = {}
        for key in self.risk_scores:
            component_scores[key] = self.risk_scores[key]
            total += self.risk_scores[key]
        self.report['component_scores'] = component_scores
        self.total_risk_score = total
        self.report['total_risk_score'] = total

        threshold = 50
        self.report['decision'] = 'block' if total >= threshold else 'allow'
        return self.report['decision']

    # Run Full Analysis
    def analyze(self):
        """Runs the complete analysis workflow and returns a detailed report."""
        self.static_analysis()
        self.dynamic_analysis()
        self.ml_analysis()
        self.threat_intelligence_integration()
        self.obfuscation_detection()
        self.user_context_analysis()
        self.decision_making_workflow()
        return self.report


#####################################################
# CODE 2: URL Report Generator, PDF & Chatbot Features #
#####################################################

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect("sunday.db")
    conn.row_factory = sqlite3.Row
    return conn

# Function to fetch URL details from the database
def get_url_details(url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls WHERE url = ?", (url,))
    result = cursor.fetchone()
    conn.close()
    return result

# Function to create a PDF report in memory
def generate_pdf_report(url_details):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "URL Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for key, value in url_details.items():
        pdf.multi_cell(0, 10, f"{key.capitalize()}: {value}")

    pdf_buffer = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer.write(pdf_bytes)
    pdf_buffer.seek(0)
    return pdf_buffer

# Function to send email with PDF attachment
def send_email(recipient_email, pdf_buffer):
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"         # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "URL Report"

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(pdf_buffer.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename="URL_Report.pdf")
    msg.attach(attachment)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Adjust SMTP server if needed
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Function for AI-powered chatbot response
def chatbot_response(user_input):
    openai.api_key = "your_openai_api_key"  # Replace with your OpenAI API key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate model
            prompt=user_input,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


#####################################################
# Main Page: All Functionalities (No Sidebar)      #
#####################################################

st.title("Merged URL Analyzer & Report Generator")

# SECTION 1: URL Safety Analyzer
st.header("🔒 URL Safety Analyzer")
url_input = st.text_input("Enter the URL to analyze:", key="analyzer_url")
st.markdown("**User Context:**")
region_input = st.text_input("Enter your region:", "USA", key="region")
history_input = st.text_area("Enter your browsing history (comma separated):", "example.com, trustedsite.com", key="history")

if st.button("Analyze URL"):
    if url_input:
        user_context = {
            'region': region_input,
            'history': [h.strip() for h in history_input.split(",") if h.strip()]
        }
        with st.spinner("Analyzing URL safety..."):
            analyzer = URLSafetyAnalyzer(url_input, user_context)
            report = analyzer.analyze()
        st.success("Analysis complete!")
        st.json(report)
    else:
        st.warning("Please enter a URL to analyze.")

st.markdown("---")

# SECTION 2: URL Report Generator
st.header("🔍 URL Report Generator")
search_query = st.text_input("Enter a URL to search in the database:", key="search_url")

if search_query:
    url_data = get_url_details(search_query)
    if url_data:
        st.subheader("URL Report")
        df = pd.DataFrame([dict(url_data)])
        # Transpose for vertical display
        df_vertical = df.T.reset_index()
        df_vertical.columns = ["Field", "Value"]
        st.dataframe(df_vertical, hide_index=True)
        
        # Generate and download PDF report
        pdf_buffer = generate_pdf_report(dict(url_data))
        st.download_button(
            label="Download Report as PDF",
            data=pdf_buffer,
            file_name="URL_Report.pdf",
            mime="application/pdf"
        )
        
        st.subheader("📧 Email Report")
        email = st.text_input("Enter your email to receive the report:", key="email")
        if email and st.button("Send Report via Email"):
            if send_email(email, pdf_buffer):
                st.success("Email sent successfully!")
            else:
                st.error("Failed to send email.")
    else:
        st.warning("🚨 URL not found in the database. Please try another one.")

st.markdown("---")

# SECTION 3: Chatbot
st.header("💬 Chatbot")
chat_input = st.text_area("Ask a question:")
if st.button("Submit Question"):
    if chat_input:
        with st.spinner("Getting chatbot response..."):
            response = chatbot_response(chat_input)
        st.write(f"**Chatbot:** {response}")
    else:
        st.warning("Please enter a question.")
