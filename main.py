import streamlit as st
from streamlit_option_menu import option_menu
import os
import sys

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.utils.config import config
from src.utils.logger import setup_logging

# Page config
st.set_page_config(
    page_title="Lega.AI", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded"
)

# Custom CSS for responsive dark/light theme
st.markdown(
    """
<style>
    /* Main header with gradient text */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f4e79, #2e86ab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Responsive feature cards that adapt to theme */
    .feature-card {
        background: var(--background-color);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #2e86ab;
        border: 1px solid var(--border-color);
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Risk color indicators */
    .risk-critical { color: #ff4444; font-weight: bold; }
    .risk-high { color: #ff6666; font-weight: bold; }
    .risk-medium { color: #ffaa00; font-weight: bold; }
    .risk-low { color: #ffcc00; font-weight: bold; }
    .risk-safe { color: #44aa44; font-weight: bold; }
    
    /* Responsive metric cards */
    .metric-card {
        background: var(--secondary-background-color);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        border: 1px solid var(--border-color);
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: var(--hover-background-color);
    }
    
    /* Enhanced button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2e86ab, #1f4e79);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1f4e79, #2e86ab);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Enhanced sidebar styling for dark/light theme */
    .css-1d391kg {
        background: var(--background-color) !important;
    }
    
    /* Streamlit sidebar container */
    section[data-testid="stSidebar"] {
        background: var(--background-color) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    /* Sidebar content */
    section[data-testid="stSidebar"] > div {
        background: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Sidebar header */
    section[data-testid="stSidebar"] .block-container {
        background: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Option menu in sidebar */
    section[data-testid="stSidebar"] .nav-link {
        background: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Active option in sidebar */
    section[data-testid="stSidebar"] .nav-link.active {
        background: linear-gradient(135deg, #2e86ab, #1f4e79) !important;
        color: white !important;
    }
    
    /* Streamlit Option Menu specific styling - Force override */
    .nav-link {
        background: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        margin: 2px 0 !important;
    }
    
    .nav-link:hover {
        background: var(--hover-background-color) !important;
        color: var(--text-color) !important;
    }
    
    .nav-link.active {
        background: linear-gradient(135deg, #2e86ab, #1f4e79) !important;
        color: white !important;
        border: 1px solid #2e86ab !important;
    }
    
    /* Option menu container */
    .nav {
        background: transparent !important;
    }
    
    /* Fix option menu wrapper */
    div[data-testid="stVerticalBlock"] > div > div {
        background: transparent !important;
    }
    
    /* More specific selectors for option menu */
    section[data-testid="stSidebar"] .nav-link {
        background-color: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    section[data-testid="stSidebar"] .nav-link:hover {
        background-color: var(--hover-background-color) !important;
    }
    
    section[data-testid="stSidebar"] .nav-link.active {
        background-color: #2e86ab !important;
        color: white !important;
    }
    
    /* Force override any white backgrounds in sidebar */
    section[data-testid="stSidebar"] * {
        background-color: inherit !important;
    }
    
    section[data-testid="stSidebar"] .nav-link {
        background-color: var(--secondary-background-color) !important;
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: var(--secondary-background-color) !important;
        border: 2px dashed var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-color) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--secondary-background-color);
        border-radius: 8px;
        color: var(--text-color);
        border: 1px solid var(--border-color);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2e86ab, #1f4e79) !important;
        color: white !important;
    }
    
    /* Tooltip styling for risk factors */
    .tooltip {
        position: relative;
        display: inline;
        cursor: help;
        border-radius: 4px;
        padding: 2px 4px;
        margin: 0 1px;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: var(--tooltip-background);
        color: var(--tooltip-text);
        text-align: left;
        border-radius: 8px;
        padding: 12px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s, visibility 0.3s;
        font-size: 13px;
        line-height: 1.4;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid var(--border-color);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Risk highlighting */
    .risk-critical { 
        background-color: rgba(255, 68, 68, 0.2); 
        border-left: 4px solid #ff4444; 
        padding: 4px 8px;
        border-radius: 4px;
    }
    .risk-high { 
        background-color: rgba(255, 136, 0, 0.2); 
        border-left: 4px solid #ff8800; 
        padding: 4px 8px;
        border-radius: 4px;
    }
    .risk-medium { 
        background-color: rgba(255, 204, 0, 0.2); 
        border-left: 4px solid #ffcc00; 
        padding: 4px 8px;
        border-radius: 4px;
    }
    .risk-low { 
        background-color: rgba(68, 170, 68, 0.2); 
        border-left: 4px solid #44aa44; 
        padding: 4px 8px;
        border-radius: 4px;
    }
    
    /* Jargon term highlighting */
    .jargon-term { 
        background-color: rgba(46, 134, 171, 0.2); 
        text-decoration: underline dotted #2e86ab;
        padding: 2px 4px;
        border-radius: 3px;
    }
    
    /* Dark theme variables */
    [data-theme="dark"] {
        --background-color: #0e1117;
        --secondary-background-color: #262730;
        --text-color: #fafafa;
        --border-color: #464a5a;
        --hover-background-color: #3d4354;
        --tooltip-background: #262730;
        --tooltip-text: #fafafa;
    }
    
    /* Light theme variables */
    [data-theme="light"], :root {
        --background-color: #ffffff;
        --secondary-background-color: #f8f9fa;
        --text-color: #262626;
        --border-color: #e0e0e0;
        --hover-background-color: #f0f0f0;
        --tooltip-background: #333333;
        --tooltip-text: #ffffff;
    }
    
    /* Auto-detect system theme */
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #0e1117;
            --secondary-background-color: #262730;
            --text-color: #fafafa;
            --border-color: #464a5a;
            --hover-background-color: #3d4354;
            --tooltip-background: #262730;
            --tooltip-text: #fafafa;
        }
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Fix all Streamlit components for dark theme */
    .stApp {
        background: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Main content area */
    .main .block-container {
        background: var(--background-color) !important;
        color: var(--text-color) !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Text input fields */
    .stTextInput > div > div > input {
        background: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        background: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div > select {
        background: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Info, warning, error boxes */
    .stAlert {
        background: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Columns */
    .element-container {
        background: transparent !important;
    }
    
    /* Status indicators */
    .status-success {
        background: rgba(68, 170, 68, 0.1);
        border: 1px solid #44aa44;
        border-radius: 6px;
        padding: 8px 12px;
        color: #44aa44;
    }
    
    .status-warning {
        background: rgba(255, 136, 0, 0.1);
        border: 1px solid #ff8800;
        border-radius: 6px;
        padding: 8px 12px;
        color: #ff8800;
    }
    
    .status-error {
        background: rgba(255, 68, 68, 0.1);
        border: 1px solid #ff4444;
        border-radius: 6px;
        padding: 8px 12px;
        color: #ff4444;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    # Initialize logging
    setup_logging()

    # Initialize session state
    if "current_document" not in st.session_state:
        st.session_state.current_document = None
    if "documents_library" not in st.session_state:
        st.session_state.documents_library = []

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### ⚖️ Lega.AI")
        st.markdown("*Making legal documents accessible*")

        selected = option_menu(
            menu_title=None,
            options=[
                "🏠 Home",
                "📄 Upload",
                "📊 Analysis",
                "💬 Q&A",
                "📚 Library",
                "⚙️ Settings",
            ],
            icons=["house", "upload", "graph-up", "chat-dots", "folder", "gear"],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent",
                },
                "icon": {"color": "#2e86ab", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "2px 0px",
                    "padding": "8px 12px",
                    "border-radius": "8px",
                    "background-color": "transparent",
                    "color": "inherit",
                    "border": "1px solid transparent",
                    "--hover-color": "transparent",
                },
                "nav-link-selected": {
                    "background-color": "#2e86ab",
                    "color": "white",
                    "border": "1px solid #2e86ab",
                },
            },
        )

    # Handle page redirections from session state
    if "page" in st.session_state and st.session_state.page:
        # Map the session state page to the selected value
        page_mapping = {
            "📄 Upload": "📄 Upload",
            "📊 Analysis": "📊 Analysis",
            "💬 Q&A": "💬 Q&A",
            "📚 Library": "📚 Library",
            "⚙️ Settings": "⚙️ Settings",
        }

        if st.session_state.page in page_mapping:
            selected = st.session_state.page
            # Clear the page state to prevent continuous redirections
            del st.session_state.page

    # Main content area
    if selected == "🏠 Home":
        show_home_page()
    elif selected == "📄 Upload":
        show_upload_page()
    elif selected == "📊 Analysis":
        show_analysis_page()
    elif selected == "💬 Q&A":
        show_qa_page()
    elif selected == "📚 Library":
        show_library_page()
    elif selected == "⚙️ Settings":
        show_settings_page()


def show_home_page():
    """Display the home page with overview and features."""
    st.markdown('<h1 class="main-header">⚖️ Lega.AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-powered legal document analysis and simplification</p>',
        unsafe_allow_html=True,
    )

    # Key benefits
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="feature-card">
            <h3>🚀 Instant Analysis</h3>
            <p>Upload any legal document and get comprehensive analysis in under 60 seconds using Google's Gemini AI.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="feature-card">
            <h3>🎯 Risk Assessment</h3>
            <p>Color-coded risk scoring helps you identify problematic clauses at a glance with detailed explanations.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="feature-card">
            <h3>💬 Plain Language</h3>
            <p>Convert complex legal jargon into clear, understandable language that anyone can comprehend.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Quick stats
    st.markdown("---")
    st.subheader("📊 Platform Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
        <div class="metric-card">
            <h2>1,247</h2>
            <p>Documents Analyzed</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="metric-card">
            <h2>95%</h2>
            <p>Accuracy Rate</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="metric-card">
            <h2>₹2,000</h2>
            <p>Avg. Saved per User</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
        <div class="metric-card">
            <h2>45 sec</h2>
            <p>Avg. Processing Time</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Getting started
    st.markdown("---")
    st.subheader("🎯 Getting Started")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
        **How to use Lega.AI:**
        
        1. **Upload** your legal document (PDF, DOCX, or TXT)
        2. **Wait** for AI analysis (typically 30-60 seconds)
        3. **Review** risk assessment and simplified explanations  
        4. **Ask questions** about specific clauses or terms
        5. **Export** summary for your records
        """
        )

    with col2:
        st.markdown("### 📄 Try Real Sample Documents")
        st.markdown("Get started with actual legal documents:")
        
        # Get available sample documents
        sample_dir = "./sample"
        sample_files = []
        if os.path.exists(sample_dir):
            sample_files = [f for f in os.listdir(sample_dir) if f.endswith(('.pdf', '.docx', '.txt'))]
        
        if sample_files:
            for i, filename in enumerate(sample_files[:4]):  # Show first 4
                display_name = filename.replace('_', ' ').replace('.pdf', '').replace('.docx', '').replace('.txt', '')
                display_name = display_name.title()
                
                if st.button(f"📄 {display_name}", key=f"home_sample_{i}"):
                    st.session_state.load_sample = filename
                    st.session_state.page = "📄 Upload"
                    st.rerun()
        else:
            st.info("Sample documents loading...")

    # CTA button
    st.markdown("---")
    if st.button("📄 Analyze Your First Document", type="primary"):
        st.session_state.page = "📄 Upload"
        st.rerun()


def load_sample_document(doc_type: str):
    """Load a sample document for demonstration."""
    sample_docs = {
        "rental": {
            "filename": "sample_rental_agreement.pdf",
            "type": "rental",
            "text": """
            RESIDENTIAL LEASE AGREEMENT
            
            This Lease Agreement is entered into between John Smith (Landlord) and Jane Doe (Tenant) 
            for the property located at 123 Main Street, Mumbai, Maharashtra.
            
            RENT: Tenant agrees to pay Rs. 25,000 per month, due on the 1st of each month. 
            Late payments will incur a penalty of Rs. 1,000 per day.
            
            SECURITY DEPOSIT: Tenant shall pay a security deposit of Rs. 75,000, which is 
            non-refundable except for damage assessment.
            
            TERMINATION: Either party may terminate this lease with 30 days written notice. 
            Early termination by Tenant results in forfeiture of security deposit.
            
            MAINTENANCE: Tenant is responsible for all repairs and maintenance, including 
            structural repairs, regardless of cause.
            
            The property is leased "as-is" with no warranties. Landlord is not liable for 
            any damages or injuries occurring on the premises.
            """,
        },
        "loan": {
            "filename": "sample_loan_agreement.pdf",
            "type": "loan",
            "text": """
            PERSONAL LOAN AGREEMENT
            
            Borrower: Rajesh Kumar
            Lender: QuickCash Financial Services Pvt Ltd
            Principal Amount: Rs. 2,00,000
            
            INTEREST RATE: 24% per annum (APR 28.5% including processing fees)
            
            REPAYMENT: 24 monthly installments of Rs. 12,500 each
            Total repayment amount: Rs. 3,00,000
            
            LATE PAYMENT PENALTY: Rs. 500 per day for any late payment
            
            DEFAULT: If payment is late by more than 7 days, the entire remaining 
            balance becomes immediately due and payable.
            
            COLLATERAL: Borrower pledges gold ornaments worth Rs. 2,50,000 as security.
            Lender may seize collateral immediately upon default.
            
            ARBITRATION: All disputes shall be resolved through binding arbitration. 
            Borrower waives right to jury trial.
            
            Processing fee: Rs. 10,000 (non-refundable)
            Documentation charges: Rs. 5,000
            """,
        },
        "employment": {
            "filename": "sample_employment_contract.pdf",
            "type": "employment",
            "text": """
            EMPLOYMENT CONTRACT
            
            Employee: Priya Sharma
            Company: TechCorp India Private Limited
            Position: Software Developer
            Start Date: January 1, 2024
            
            SALARY: Rs. 8,00,000 per annum, payable monthly
            
            WORKING HOURS: 45 hours per week, including mandatory weekend work when required
            
            NON-COMPETE: Employee shall not work for any competing company for 2 years 
            after termination, within India or globally.
            
            CONFIDENTIALITY: Employee agrees to maintain strict confidentiality of all 
            company information indefinitely, even after termination.
            
            TERMINATION: Company may terminate employment at any time without cause or notice. 
            Employee must provide 90 days notice to resign.
            
            NO MOONLIGHTING: Employee shall not engage in any other work or business 
            activities during employment.
            
            INTELLECTUAL PROPERTY: All work created by employee belongs entirely to company, 
            including personal projects done outside work hours.
            """,
        },
    }

    if doc_type in sample_docs:
        sample = sample_docs[doc_type]
        from src.utils.helpers import generate_document_id

        # Store in session state
        st.session_state.current_document = {
            "id": generate_document_id(),
            "filename": sample["filename"],
            "document_type": sample["type"],
            "original_text": sample["text"],
            "is_sample": True,
        }

        st.success(f"📄 Loaded sample {doc_type} document!")
        st.session_state.page = "📊 Analysis"
        st.rerun()


def show_upload_page():
    """Import and show the upload page."""
    try:
        from src.pages.upload import show_upload_interface

        show_upload_interface()
    except ImportError as e:
        st.error(f"Upload page not found: {e}")


def show_analysis_page():
    """Import and show the analysis page."""
    try:
        from src.pages.analysis import show_analysis_interface

        show_analysis_interface()
    except ImportError as e:
        st.error(f"Analysis page not found: {e}")


def show_qa_page():
    """Import and show the Q&A page."""
    try:
        from src.pages.qa_assistant import show_qa_interface

        show_qa_interface()
    except ImportError as e:
        st.error(f"Q&A page not found: {e}")


def show_library_page():
    """Import and show the library page."""
    try:
        from src.pages.library import show_library_interface

        show_library_interface()
    except ImportError as e:
        st.error(f"Library page not found: {e}")


def show_settings_page():
    """Import and show the settings page."""
    try:
        from src.pages.settings import show_settings_interface

        show_settings_interface()
    except ImportError as e:
        st.error(f"Settings page not found: {e}")


if __name__ == "__main__":
    main()
