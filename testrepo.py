import streamlit as st
import re
import ssl
import socket
import urllib.parse
import requests
import math
import datetime
import json

# Optional: Install the python-whois package via pip: pip install python-whois
try:
    import whois
except ImportError:
    whois = None  # In production, ensure that the whois module is installed


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

    # ----------------------------
    # 1. URL Parsing and Normalization
    # ----------------------------
    def normalize_url(self, url):
        """
        Normalizes the URL by decoding URL-encoded characters.
        """
        return urllib.parse.unquote(url)

    def parse_url(self, url):
        """
        Decomposes the URL into its components.
        Returns a dictionary containing protocol, domain, subdomain, path, query, fragment, and port.
        """
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
        """
        Extracts the subdomain (if any) from the hostname.
        Assumes that the main domain is the last two labels.
        """
        if hostname:
            parts = hostname.split('.')
            if len(parts) > 2:
                return '.'.join(parts[:-2])
        return ''

    # ----------------------------
    # 2. Static Analysis
    # ----------------------------
    def static_analysis(self):
        """
        Performs static analysis by checking domain reputation, path/query components, and subdomain.
        """
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
        """
        Checks the domain against blacklists, WHOIS details, and validates its SSL certificate if applicable.
        """
        risk = 0
        details = {}

        # a. Blacklist Check (using a dummy blacklist)
        blacklisted_domains = ['malicious.com', 'evil.com', 'badsite.net']
        if domain in blacklisted_domains:
            risk += 50
            details['blacklist'] = True
        else:
            details['blacklist'] = False

        # b. WHOIS Lookup: Check for recent creation (if WHOIS module is available)
        if whois:
            try:
                domain_info = whois.whois(domain)
                creation_date = domain_info.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                if creation_date:
                    age_days = (datetime.datetime.now() - creation_date).days
                    if age_days < 180:  # Less than 6 months old
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
        """
        Validates the SSL/TLS certificate for the given domain.
        Returns a tuple (is_valid, details_dict).
        """
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
        """
        Analyzes the URL path and query for phishing keywords, suspicious file extensions,
        and risky parameters (e.g., redirect=, cmd=).
        """
        risk = 0
        details = {}

        # Regex Pattern Matching for phishing keywords
        phishing_keywords = ['login', 'verify', 'account', 'update', 'secure']
        for keyword in phishing_keywords:
            if keyword in path.lower():
                risk += 5
                details.setdefault('phishing_keywords', []).append(keyword)

        # Check for suspicious file extensions
        suspicious_extensions = ['.exe', '.php', '.js']
        for ext in suspicious_extensions:
            if path.lower().endswith(ext):
                risk += 10
                details.setdefault('suspicious_extension', []).append(ext)

        # Parameter Inspection for risky parameters
        if query:
            params = urllib.parse.parse_qs(query)
            for param in params:
                if param.lower() in ['redirect', 'cmd']:
                    risk += 10
                    details.setdefault('risky_parameters', []).append(param)

        self.report['path_query_analysis'] = details
        return risk

    def subdomain_analysis(self, subdomain):
        """
        Analyzes the subdomain by calculating its entropy and checking for typosquatting.
        """
        risk = 0
        details = {}

        if subdomain:
            # Calculate Shannon entropy of the subdomain
            entropy = self.calculate_entropy(subdomain)
            details['entropy'] = entropy
            if entropy > 3.5:  # Arbitrary threshold for suspecting algorithmically generated domains
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
        """
        Calculates the Shannon entropy of a string.
        """
        prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
        entropy = -sum([p * math.log(p, 2) for p in prob])
        return entropy

    # ----------------------------
    # 3. Dynamic Analysis
    # ----------------------------
    def dynamic_analysis(self):
        """
        Performs a simulated dynamic analysis by executing the URL in an isolated manner,
        tracking its redirect chain.
        """
        risk = 0
        details = {}

        try:
            session = requests.Session()
            response = session.get(self.normalized_url, timeout=5, allow_redirects=True)
            # Build the redirect chain from the response history
            redirect_chain = [resp.url for resp in response.history] + [response.url]
            details['redirect_chain'] = redirect_chain
            if len(redirect_chain) > 3:  # Arbitrary threshold: many redirects may be suspicious
                risk += 10
        except Exception as e:
            details['error'] = str(e)
            risk += 10

        # Note: A real sandbox would monitor for drive-by downloads, exploit kits, and network traffic.
        self.report['dynamic_analysis'] = details
        self.risk_scores['dynamic'] = risk
        return risk

    # ----------------------------
    # 4. Machine Learning (ML) Models (Simulated)
    # ----------------------------
    def ml_analysis(self):
        """
        Extracts lexical, host-based, and behavioral features from the URL and computes
        a dummy risk score simulating a machine learning classifier.
        """
        risk = 0
        details = {}

        # Lexical Features
        url_length = len(self.normalized_url)
        num_subdomains = len(self.parsed_url['subdomain'].split('.')) if self.parsed_url['subdomain'] else 0
        special_chars = len(re.findall(r'[^a-zA-Z0-9]', self.normalized_url))
        details['lexical'] = {
            'url_length': url_length,
            'num_subdomains': num_subdomains,
            'special_chars': special_chars
        }

        # Host-Based Features: Domain age from WHOIS lookup (if available)
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

        # Behavioral Features: Number of redirects from dynamic analysis
        redirect_chain = self.report.get('dynamic_analysis', {}).get('redirect_chain', [])
        redirect_count = len(redirect_chain)
        details['behavioral'] = {
            'redirect_count': redirect_count
        }

        # Dummy risk scoring (weighted sum of features)
        risk = (url_length / 100) + (num_subdomains * 2) + (special_chars / 50)
        if domain_age_days < 180:
            risk += 5
        if redirect_count > 3:
            risk += 5

        self.report['ml_analysis'] = details
        self.risk_scores['ml'] = risk
        return risk

    # ----------------------------
    # 5. Threat Intelligence Integration
    # ----------------------------
    def threat_intelligence_integration(self):
        """
        Integrates threat intelligence by (simulated) API calls.
        Checks if the resolved IP address is known to be malicious.
        """
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

    # ----------------------------
    # 6. Obfuscation Detection
    # ----------------------------
    def obfuscation_detection(self):
        """
        Detects obfuscation techniques such as hexadecimal encoding in the URL,
        IPv4 encoding in the domain, and use of URL shortening services.
        """
        risk = 0
        details = {}

        # Check for hex-encoded characters
        if re.search(r'%[0-9a-fA-F]{2}', self.original_url):
            details['hex_encoding'] = True
            risk += 5

        # Check if the domain is an IPv4 address
        if self.parsed_url['domain'] and re.match(r'^\d{1,3}(\.\d{1,3}){3}$', self.parsed_url['domain']):
            details['ipv4_address'] = True
            risk += 10

        # Check for shortened URL services
        shortened_services = ['bit.ly', 'goo.gl', 'tinyurl.com']
        if self.parsed_url['domain'] in shortened_services:
            details['shortened_url'] = True
            risk += 10

        self.report['obfuscation_detection'] = details
        self.risk_scores['obfuscation'] = risk
        return risk

    # ----------------------------
    # 7. User Context Analysis
    # ----------------------------
    def user_context_analysis(self):
        """
        Analyzes user context (e.g., geolocation and browsing history) to determine if the URL
        is atypical for the user.
        """
        risk = 0
        details = {}

        # Geolocation check: For demonstration, flag if the URL's TLD implies a different region
        if self.user_context and 'region' in self.user_context:
            # Dummy rule: Domains ending with '.ru' are assumed to target Russia.
            if self.parsed_url['domain'] and self.parsed_url['domain'].endswith('.ru') and self.user_context['region'] != 'Russia':
                risk += 10
                details['geolocation_mismatch'] = True

        # User history analysis: If the domain is not in the user’s typical history, add slight risk.
        if self.user_context and 'history' in self.user_context:
            if self.parsed_url['domain'] not in self.user_context['history']:
                risk += 5
                details['new_domain'] = True

        self.report['user_context_analysis'] = details
        self.risk_scores['user_context'] = risk
        return risk

    # ----------------------------
    # 8. Decision-Making Workflow
    # ----------------------------
    def decision_making_workflow(self):
        """
        Combines all risk scores from the analysis components and determines
        whether to flag or block the URL.
        """
        total = 0
        component_scores = {}
        for key in self.risk_scores:
            component_scores[key] = self.risk_scores[key]
            total += self.risk_scores[key]
        self.report['component_scores'] = component_scores
        self.total_risk_score = total
        self.report['total_risk_score'] = total

        # Set an arbitrary threshold for blocking
        threshold = 50
        self.report['decision'] = 'block' if total >= threshold else 'allow'
        return self.report['decision']

    # ----------------------------
    # Run Full Analysis
    # ----------------------------
    def analyze(self):
        """
        Runs the complete analysis workflow and returns a detailed report.
        """
        self.static_analysis()
        self.dynamic_analysis()
        self.ml_analysis()
        self.threat_intelligence_integration()
        self.obfuscation_detection()
        self.user_context_analysis()
        self.decision_making_workflow()
        return self.report


# ----------------------------
# Streamlit UI
# ----------------------------
st.title("URL Safety Analyzer")

# URL input
url_input = st.text_input("Enter the URL to analyze:", "")

# User context inputs
st.subheader("User Context")
region_input = st.text_input("Enter your region:", "USA")
history_input = st.text_area("Enter your browsing history (comma separated):", "example.com, trustedsite.com")

# When the user clicks the "Analyze URL" button, perform the analysis.
if st.button("Analyze URL") and url_input:
    user_context = {
        'region': region_input,
        'history': [h.strip() for h in history_input.split(",") if h.strip()]
    }
    with st.spinner("Analyzing..."):
        analyzer = URLSafetyAnalyzer(url_input, user_context)
        report = analyzer.analyze()
    st.success("Analysis complete!")
    st.json(report)

