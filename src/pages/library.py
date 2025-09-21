import streamlit as st
import pandas as pd
from typing import List, Dict
import time

from ..utils.helpers import format_file_size, format_timestamp


def show_library_interface():
    """Display the document library interface."""

    st.header("📚 Document Library")
    st.markdown("Manage and review all your analyzed documents")

    # Get documents from session state
    documents = st.session_state.get("documents_library", [])

    if not documents:
        show_empty_library()
        return

    # Library statistics
    show_library_stats(documents)

    # Filter and search
    show_library_filters(documents)

    # Document grid
    show_document_grid(documents)


def show_empty_library():
    """Show empty library state."""
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            """
        <div style="text-align: center; padding: 3rem;">
            <h3>📚 Your Library is Empty</h3>
            <p style="color: var(--text-color, #666); opacity: 0.7;">Upload and analyze documents to build your personal legal document library.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "📄 Upload Your First Document", type="primary", use_container_width=True
        ):
            st.session_state.page = "📄 Upload"
            st.rerun()

    # Add sample documents section
    st.markdown("---")
    show_sample_documents_section()


def show_library_stats(documents: List[Dict]):
    """Display library statistics."""
    # Calculate stats
    total_docs = len(documents)
    doc_types = {}
    high_risk_docs = 0

    for doc in documents:
        doc_type = doc.get("document_type", "other")
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1

        if doc.get("risk_score", 0) > 60:
            high_risk_docs += 1

    # Display stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Documents", value=total_docs)

    with col2:
        most_common_type = max(doc_types, key=doc_types.get) if doc_types else "None"
        st.metric(label="Most Common Type", value=most_common_type.title())

    with col3:
        st.metric(
            label="High Risk Documents",
            value=high_risk_docs,
            delta=(
                f"{high_risk_docs/total_docs*100:.0f}% of total"
                if total_docs > 0
                else "0%"
            ),
        )

    with col4:
        total_size = sum(doc.get("file_size", 0) for doc in documents)
        st.metric(label="Total Storage", value=format_file_size(total_size))


def show_library_filters(documents: List[Dict]):
    """Display filter and search options."""
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Document type filter
        doc_types = ["All"] + list(
            set(doc.get("document_type", "other") for doc in documents)
        )
        selected_type = st.selectbox("Filter by Type", doc_types)

    with col2:
        # Risk level filter
        risk_levels = [
            "All",
            "Low Risk (0-30)",
            "Medium Risk (31-60)",
            "High Risk (61+)",
        ]
        selected_risk = st.selectbox("Filter by Risk", risk_levels)

    with col3:
        # Search
        search_term = st.text_input(
            "Search documents", placeholder="Enter filename or content..."
        )

    # Apply filters
    filtered_docs = documents

    if selected_type != "All":
        filtered_docs = [
            doc for doc in filtered_docs if doc.get("document_type") == selected_type
        ]

    if selected_risk != "All":
        if "Low Risk" in selected_risk:
            filtered_docs = [
                doc for doc in filtered_docs if doc.get("risk_score", 0) <= 30
            ]
        elif "Medium Risk" in selected_risk:
            filtered_docs = [
                doc for doc in filtered_docs if 31 <= doc.get("risk_score", 0) <= 60
            ]
        elif "High Risk" in selected_risk:
            filtered_docs = [
                doc for doc in filtered_docs if doc.get("risk_score", 0) > 60
            ]

    if search_term:
        filtered_docs = [
            doc
            for doc in filtered_docs
            if search_term.lower() in doc.get("filename", "").lower()
        ]

    # Store filtered docs for grid display
    st.session_state.filtered_documents = filtered_docs


def show_document_grid(documents: List[Dict]):
    """Display documents in a grid layout."""
    filtered_docs = st.session_state.get("filtered_documents", documents)

    if not filtered_docs:
        st.info("No documents match your filter criteria.")
        return

    st.markdown("---")
    st.subheader(f"📄 Documents ({len(filtered_docs)})")

    # Display documents in cards
    for i in range(0, len(filtered_docs), 2):
        col1, col2 = st.columns(2)

        # First document
        with col1:
            if i < len(filtered_docs):
                show_document_card(filtered_docs[i])

        # Second document
        with col2:
            if i + 1 < len(filtered_docs):
                show_document_card(filtered_docs[i + 1])


def show_document_card(doc: Dict):
    """Display a single document card."""
    # Risk color
    risk_score = doc.get("risk_score", 0)
    if risk_score > 60:
        risk_color = "🔴"
        risk_label = "High Risk"
    elif risk_score > 30:
        risk_color = "🟠"
        risk_label = "Medium Risk"
    else:
        risk_color = "🟢"
        risk_label = "Low Risk"

    # Use container for card styling
    with st.container():
        # Header row with filename and risk
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📄 {doc.get('filename', 'Unknown')}**")
        with col2:
            st.markdown(f"{risk_color} {risk_label}")

        # Document details
        doc_type = doc.get("document_type", "other").title()
        upload_date = doc.get("upload_date", "Unknown")
        file_size = format_file_size(doc.get("file_size", 0))

        st.markdown(f"📋 {doc_type} • 📅 {upload_date} • 💾 {file_size}")

        # Add some spacing
        st.markdown("---")

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 View", key=f"view_{doc['id']}", use_container_width=True):
            load_document_for_analysis(doc["id"])

    with col2:
        if st.button("💬 Q&A", key=f"qa_{doc['id']}", use_container_width=True):
            load_document_for_qa(doc["id"])

    with col3:
        if st.button("🗑️ Delete", key=f"delete_{doc['id']}", use_container_width=True):
            delete_document(doc["id"])


def load_document_for_analysis(doc_id: str):
    """Load a document from library for analysis."""
    documents = st.session_state.get("documents_library", [])

    for doc in documents:
        if doc["id"] == doc_id:
            # Simulate loading the full document data
            st.session_state.current_document = {
                "id": doc["id"],
                "filename": doc["filename"],
                "document_type": doc["document_type"],
                "original_text": f"Sample content for {doc['filename']}...",  # In real app, load from storage
                "is_sample": True,  # Mark as sample for demo
                "risk_score": doc.get("risk_score", 0),
            }

            st.session_state.page = "📊 Analysis"
            st.rerun()
            break


def load_document_for_qa(doc_id: str):
    """Load a document from library for Q&A."""
    documents = st.session_state.get("documents_library", [])

    for doc in documents:
        if doc["id"] == doc_id:
            # Simulate loading the full document data
            st.session_state.current_document = {
                "id": doc["id"],
                "filename": doc["filename"],
                "document_type": doc["document_type"],
                "original_text": f"Sample content for {doc['filename']}...",  # In real app, load from storage
                "is_sample": True,  # Mark as sample for demo
            }

            st.session_state.page = "💬 Q&A"
            st.rerun()
            break


def delete_document(doc_id: str):
    """Delete a document from the library."""
    # Confirm deletion
    if st.session_state.get(f"confirm_delete_{doc_id}"):
        documents = st.session_state.get("documents_library", [])
        st.session_state.documents_library = [
            doc for doc in documents if doc["id"] != doc_id
        ]

        # Clear confirmation state
        del st.session_state[f"confirm_delete_{doc_id}"]

        st.success("✅ Document deleted from library")


def show_sample_documents_section():
    """Show available sample documents for testing."""
    import os

    st.subheader("🎯 Try Sample Documents")
    st.markdown("Get started by analyzing our sample legal documents:")

    # Get available sample documents
    sample_dir = "./sample"
    sample_files = []
    if os.path.exists(sample_dir):
        sample_files = [
            f for f in os.listdir(sample_dir) if f.endswith((".pdf", ".docx", ".txt"))
        ]

    if sample_files:
        # Create description mapping for better UX
        descriptions = {
            "Employment_Offer_Letter.pdf": "📋 Analyze employment terms, benefits, and obligations",
            "Master_Services_Agreement.pdf": "🤝 Review service agreements and contract terms",
            "Mutual_NDA.pdf": "🔒 Examine confidentiality and non-disclosure clauses",
            "Residential_Lease_Agreement.pdf": "🏠 Check rental terms, deposits, and tenant rights",
        }

        for filename in sample_files:
            with st.expander(
                f"📄 {filename.replace('_', ' ').replace('.pdf', '')}", expanded=False
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    description = descriptions.get(
                        filename, "📊 Analyze this legal document for risks and terms"
                    )
                    st.markdown(description)

                with col2:
                    if st.button(
                        "Analyze Now",
                        key=f"sample_lib_{filename}",
                        use_container_width=True,
                    ):
                        # Set this as the sample to load and redirect to upload page
                        st.session_state.load_sample = filename
                        st.session_state.page = "📄 Upload"
                        st.rerun()
    else:
        st.info("No sample documents available.")
