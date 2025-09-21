import streamlit as st
from src.utils.config import config


def show_settings_interface():
    """Display the settings interface."""

    st.header("⚙️ Settings")
    st.markdown("Configure your Lega.AI experience")

    # Tabs for different settings categories
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔑 API Keys", "🎨 Preferences", "📊 Usage", "ℹ️ About"]
    )

    with tab1:
        show_api_settings()

    with tab2:
        show_preference_settings()

    with tab3:
        show_usage_stats()

    with tab4:
        show_about_info()


def show_api_settings():
    """Display API key configuration."""
    st.subheader("🔑 API Configuration")

    # Check current API key status
    api_key_configured = bool(
        config.GOOGLE_API_KEY and config.GOOGLE_API_KEY != "your-google-api-key-here"
    )

    if api_key_configured:
        st.success("✅ Google AI API key is configured")
    else:
        st.warning("⚠️ Google AI API key not configured")
        st.markdown(
            """
        To use Lega.AI's AI features, you need to configure your Google AI API key:
        
        1. Go to [Google AI Studio](https://makersuite.google.com/)
        2. Create a new API key
        3. Copy the key and add it to your `.env` file
        4. Set `GOOGLE_API_KEY=your_actual_api_key`
        5. Restart the application
        """
        )

    # API key input (for demonstration)
    st.markdown("---")
    st.subheader("🔧 Update API Key")

    with st.form("api_key_form"):
        new_api_key = st.text_input(
            "Google AI API Key",
            type="password",
            placeholder="Enter your Google AI API key",
            help="This will be saved to your environment configuration",
        )

        submitted = st.form_submit_button("Update API Key")

        if submitted:
            if new_api_key.strip():
                st.success(
                    "✅ API key updated! Please restart the application for changes to take effect."
                )
                st.info("💡 Don't forget to update your `.env` file with the new key.")
            else:
                st.error("❌ Please enter a valid API key")


def show_preference_settings():
    """Display user preference settings."""
    st.subheader("🎨 User Preferences")

    # Language settings
    st.markdown("#### 🌐 Language & Region")

    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "Interface Language",
            ["English", "Hindi", "Tamil", "Telugu", "Gujarati"],
            help="Language for the user interface",
        )

    with col2:
        region = st.selectbox(
            "Legal Region",
            ["India", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu"],
            help="Legal jurisdiction for document analysis",
        )

    # Analysis preferences
    st.markdown("#### 📊 Analysis Preferences")

    risk_sensitivity = st.slider(
        "Risk Detection Sensitivity",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Only critical risks, 5 = All potential concerns",
    )

    simplification_level = st.selectbox(
        "Text Simplification Level",
        ["Basic", "Intermediate", "Advanced"],
        index=1,
        help="How much to simplify legal language",
    )

    show_suggestions = st.checkbox(
        "Show improvement suggestions",
        value=True,
        help="Display suggestions for problematic clauses",
    )

    # Notification preferences
    st.markdown("#### 🔔 Notifications")

    email_notifications = st.checkbox(
        "Email notifications for analysis completion", value=False
    )

    browser_notifications = st.checkbox("Browser notifications", value=True)

    # Save preferences
    if st.button("💾 Save Preferences", type="primary"):
        # In a real app, save to user profile/database
        st.success("✅ Preferences saved successfully!")


def show_usage_stats():
    """Display usage statistics."""
    st.subheader("📊 Usage Statistics")

    # Mock usage data
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Documents Analyzed", value="47", delta="12 this month")

    with col2:
        st.metric(label="Questions Asked", value="156", delta="23 this week")

    with col3:
        st.metric(label="Risks Identified", value="89", delta="High: 12, Medium: 31")

    # Usage by document type
    st.markdown("#### 📄 Analysis by Document Type")

    usage_data = {
        "Rental Agreements": 18,
        "Loan Contracts": 12,
        "Employment Contracts": 8,
        "Service Agreements": 6,
        "NDAs": 3,
    }

    for doc_type, count in usage_data.items():
        progress = count / max(usage_data.values())
        st.markdown(f"**{doc_type}**: {count} documents")
        st.progress(progress)

    # Storage usage
    st.markdown("#### 💾 Storage Usage")

    storage_used = 2.4  # GB
    storage_limit = 5.0  # GB

    st.progress(storage_used / storage_limit)
    st.markdown(
        f"**{storage_used:.1f} GB** used of **{storage_limit:.1f} GB** available"
    )

    # Account tier
    st.markdown("#### 👤 Account Information")

    col1, col2 = st.columns(2)

    with col1:
        st.info("**Plan**: Free Tier")
        st.markdown(
            """
        - 10 documents per month
        - Basic AI analysis
        - Email support
        """
        )

    with col2:
        st.markdown("**Upgrade Benefits**:")
        st.markdown(
            """
        - Unlimited documents
        - Advanced AI features
        - Priority support
        - Bulk processing
        """
        )

        if st.button("🚀 Upgrade to Pro", type="primary"):
            st.info("Upgrade functionality would be implemented here")


def show_about_info():
    """Display about information."""
    st.subheader("ℹ️ About Lega.AI")

    # App info
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
        **Lega.AI** is an AI-powered platform that makes legal documents accessible to everyone.
        
        ### 🎯 Mission
        To democratize legal document understanding by providing instant AI analysis,
        risk assessment, and plain language explanations.
        
        ### ✨ Features
        - **Document Analysis**: Upload and analyze any legal document
        - **Risk Assessment**: Color-coded risk scoring with explanations
        - **Plain Language**: Convert legal jargon to simple English
        - **Q&A Assistant**: Ask questions about your documents
        - **Smart Search**: Find similar clauses and documents
        - **Export Reports**: Generate comprehensive analysis reports
        
        ### 🛡️ Privacy & Security
        - Your documents are processed securely
        - No data is shared with third parties
        - Local vector storage for document similarity
        - GDPR compliant data handling
        """
        )

    with col2:
        st.markdown(
            """
        ### 📊 Version Info
        **Version**: 1.0.0  
        **Build**: 2025.09.21  
        **Engine**: Google Gemini
        
        ### 🔧 Tech Stack
        - **Frontend**: Streamlit
        - **AI/ML**: LangChain + Gemini
        - **Vector DB**: Chroma
        - **Embeddings**: Google Embeddings
        
        ### 📞 Support
        - **Email**: support@lega.ai
        - **Docs**: github.com/codernoahx/Lega.AI/README.md
        - **GitHub**: github.com/codernoahx/Lega.AI
        """
        )

    # Legal notice
    st.markdown("---")
    st.markdown(
        """
    ### ⚖️ Legal Notice
    
    **Disclaimer**: Lega.AI provides AI-powered analysis for informational purposes only. 
    This is not legal advice. Always consult with qualified legal professionals for 
    important legal matters.
    
    **Data Usage**: By using this service, you agree to our Terms of Service and Privacy Policy.
    Your documents are processed to provide analysis but are not used to train AI models.
    
    © 2025 Lega.AI. All rights reserved.
    """
    )

    # Feedback section
    st.markdown("---")
    st.subheader("💬 Feedback")

    with st.form("feedback_form"):
        feedback_type = st.selectbox(
            "Feedback Type",
            ["General Feedback", "Bug Report", "Feature Request", "Question"],
        )

        feedback_text = st.text_area(
            "Your Feedback",
            placeholder="Tell us what you think or report any issues...",
            height=100,
        )

        submitted = st.form_submit_button("Send Feedback")

        if submitted and feedback_text.strip():
            st.success("✅ Thank you for your feedback! We'll review it soon.")
        elif submitted:
            st.error("❌ Please enter your feedback before submitting.")
