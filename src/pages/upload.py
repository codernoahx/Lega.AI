import streamlit as st
import os
from typing import Optional
import time

from ..services.document_processor import DocumentProcessor
from ..services.ai_analyzer import AIAnalyzer
from ..services.vector_store import VectorStoreService
from ..models.document import DocumentType
from ..utils.helpers import generate_document_id, sanitize_filename, format_file_size
from ..utils.logger import log_document_upload


def show_upload_interface():
    """Display the document upload interface."""
    st.header("📄 Upload Legal Document")
    st.markdown(
        "Upload your legal document for instant AI analysis and risk assessment."
    )

    # Check if we should auto-load a sample document
    if st.session_state.get("load_sample"):
        filename = st.session_state.load_sample
        del st.session_state.load_sample  # Clear the flag
        load_sample_document_from_file(filename)
        return

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx"],  # Added docx support
        help="Supported formats: PDF, TXT, DOCX (Max 10MB)",
        key="document_uploader",
    )

    if uploaded_file is not None:
        # Display file info
        file_size = len(uploaded_file.getvalue())

        # Check file size limit
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            st.error(f"❌ File too large. Maximum size is {format_file_size(max_size)}")
            return

        st.success(f"📁 **{uploaded_file.name}** ({format_file_size(file_size)})")

        # Process button
        if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
            process_uploaded_document(uploaded_file)

    # Sample documents section
    st.markdown("---")
    st.subheader("📋 Try Sample Documents")
    st.markdown("Don't have a document handy? Try one of our real sample documents:")

    # Get available sample documents
    sample_dir = "./sample"
    sample_files = []
    if os.path.exists(sample_dir):
        sample_files = [f for f in os.listdir(sample_dir) if f.endswith(('.pdf', '.docx', '.txt'))]

    if sample_files:
        col1, col2 = st.columns(2)
        
        for i, filename in enumerate(sample_files):
            col = col1 if i % 2 == 0 else col2
            
            with col:
                # Create descriptive button names
                display_name = filename.replace('_', ' ').replace('.pdf', '').replace('.docx', '').replace('.txt', '')
                display_name = display_name.title()
                
                if st.button(f"📄 {display_name}", use_container_width=True, key=f"sample_{i}"):
                    load_sample_document_from_file(filename)
    else:
        st.info("No sample documents found in the sample directory.")


def process_uploaded_document(uploaded_file):
    """Process the uploaded document with AI analysis."""
    try:
        # Initialize processors
        doc_processor = DocumentProcessor()
        ai_analyzer = AIAnalyzer()
        vector_store = VectorStoreService()

        # Create progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Step 1: Extract text
        status_text.text("📄 Extracting text from document...")
        progress_bar.progress(20)

        file_content = uploaded_file.getvalue()
        text = doc_processor.extract_text(file_content, uploaded_file.name)

        if not text.strip():
            st.error(
                "❌ Could not extract text from the document. Please try a different file."
            )
            progress_bar.empty()
            status_text.empty()
            return

        progress_bar.progress(40)

        # Step 2: Detect document type
        status_text.text("🔍 Analyzing document type...")
        document_type = doc_processor.detect_document_type(text)
        progress_bar.progress(50)

        # Step 3: Risk analysis
        status_text.text("⚠️ Performing risk assessment...")
        risk_data = ai_analyzer.analyze_document_risk(text, document_type)
        progress_bar.progress(70)

        # Step 4: Text simplification
        status_text.text("💬 Simplifying legal language...")
        simplified_data = ai_analyzer.simplify_text(text, document_type)
        progress_bar.progress(85)

        # Step 5: Generate summary
        status_text.text("📋 Generating summary...")
        summary = ai_analyzer.generate_summary(text, document_type)

        # Step 6: Add to vector store
        status_text.text("💾 Storing document for search...")
        doc_id = generate_document_id()
        vector_store.add_document(
            document_id=doc_id,
            text=text,
            metadata={
                "filename": uploaded_file.name,
                "document_type": document_type.value,
                "upload_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

        progress_bar.progress(100)

        # Complete
        status_text.text("✅ Analysis complete!")
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()

        # Store results in session state
        st.session_state.current_document = {
            "id": doc_id,
            "filename": uploaded_file.name,
            "document_type": document_type.value,
            "original_text": text,
            "simplified_text": simplified_data.get("simplified_text", ""),
            "summary": summary,
            "risk_data": risk_data,
            "key_points": simplified_data.get("key_points", []),
            "jargon_definitions": simplified_data.get("jargon_definitions", {}),
            "analysis_timestamp": time.time(),
            "file_size": len(file_content),
        }

        # Add to documents library
        if "documents_library" not in st.session_state:
            st.session_state.documents_library = []

        st.session_state.documents_library.append(
            {
                "id": doc_id,
                "filename": uploaded_file.name,
                "document_type": document_type.value,
                "upload_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": len(file_content),
                "risk_score": len(risk_data.get("risk_factors", []))
                * 10,  # Simple risk score
            }
        )

        # Log the upload
        log_document_upload(uploaded_file.name, len(file_content))

        # Show success and redirect to analysis page
        st.success("🎉 Document analysis completed! Redirecting to results...")

        # Set page state for redirection
        st.session_state.page = "📊 Analysis"

        time.sleep(2)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
        progress_bar.empty()
        status_text.empty()


def load_sample_document_from_file(filename: str):
    """Load an actual sample document from the sample directory."""
    try:
        sample_path = os.path.join("./sample", filename)
        
        if not os.path.exists(sample_path):
            st.error(f"❌ Sample file not found: {filename}")
            return
        
        # Read the file
        with open(sample_path, 'rb') as f:
            file_content = f.read()
        
        # Create a mock uploaded file object
        class MockUploadedFile:
            def __init__(self, content, name):
                self._content = content
                self.name = name
            
            def getvalue(self):
                return self._content
        
        mock_file = MockUploadedFile(file_content, filename)
        
        st.success(f"📄 Loading sample document: **{filename}**")
        
        # Process the sample document
        process_uploaded_document(mock_file)
        
    except Exception as e:
        st.error(f"❌ Error loading sample document: {str(e)}")


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
            "filename": "sample_employment_contract.docx",  # Changed to DOCX
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
        from ..utils.helpers import generate_document_id

        # Store in session state
        doc_id = generate_document_id()
        st.session_state.current_document = {
            "id": doc_id,
            "filename": sample["filename"],
            "document_type": sample["type"],
            "original_text": sample["text"],
            "is_sample": True,
        }

        st.success(f"📄 Loaded sample {doc_type} document. Processing...")

        # Simulate processing for demo
        with st.spinner("Analyzing sample document..."):
            time.sleep(2)

        st.rerun()
