flowchart TD
    A[Start: Launch Streamlit App] --> B[main() Function]
    B --> C[Display Sidebar Navigation]
    C --> D{User Selects a Section}
    D -- "Learn About Phishing URLs" --> E[Call learn_about_phishing_urls()]
    D -- "Read URL Reports" --> F[Call read_url_report()]
    E --> G[Display Learn About Phishing URLs Content]
    F --> H[Display URL Reports Content]
    G --> I[User Interacts with Learning Materials]
    H --> J[User Interacts with Report Analysis]
    I --> K[Process Input (e.g., Quiz Answers, URL Checks)]
    J --> K
    K --> L[Update Display Based on User Input]
    L --> M[End/Loop for Further Interaction]
