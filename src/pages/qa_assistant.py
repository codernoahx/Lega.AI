import streamlit as st
from typing import List, Dict
import time

from ..services.ai_analyzer import AIAnalyzer
from ..services.vector_store import VectorStoreService


def show_qa_interface():
    """Display the Q&A assistant interface."""

    if not st.session_state.get("current_document"):
        st.warning("⚠️ No document loaded. Please upload and analyze a document first.")
        if st.button("📄 Go to Upload"):
            st.session_state.page = "📄 Upload"
            st.rerun()
        return

    doc = st.session_state.current_document

    # Header
    st.header("💬 Q&A Assistant")
    st.markdown(f"Ask questions about **{doc.get('filename', 'your document')}**")

    # Initialize chat history
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    # Chat interface
    chat_container = st.container()

    with chat_container:
        # Display chat history
        for i, qa in enumerate(st.session_state.qa_history):
            # User message
            with st.chat_message("user"):
                st.markdown(qa["question"])

            # Assistant response
            with st.chat_message("assistant"):
                st.markdown(qa["answer"])

    # Suggested questions
    st.markdown("### 💡 Suggested Questions")

    doc_type = doc.get("document_type", "other")
    suggested_questions = get_suggested_questions(doc_type)

    col1, col2 = st.columns(2)

    for i, question in enumerate(suggested_questions):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(question, key=f"suggested_{i}", use_container_width=True):
                ask_question(question, doc)

    # Chat input
    st.markdown("### ❓ Ask Your Question")

    with st.form("question_form", clear_on_submit=True):
        user_question = st.text_input(
            "Type your question here...",
            placeholder="e.g., What happens if I terminate this contract early?",
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button("Send", use_container_width=True)

        if submitted and user_question.strip():
            ask_question(user_question, doc)

    # Quick actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Back to Analysis", use_container_width=True):
            st.session_state.page = "📊 Analysis"
            st.rerun()

    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.qa_history = []
            st.rerun()

    with col3:
        if st.button("📥 Export Chat", use_container_width=True):
            export_chat_history()


def ask_question(question: str, doc: Dict):
    """Process a question and get AI response."""
    try:
        # Show thinking indicator
        with st.spinner("🤔 Thinking..."):
            # Initialize AI analyzer
            ai_analyzer = AIAnalyzer()

            # Get document type
            from ..models.document import DocumentType

            doc_type = DocumentType(doc.get("document_type", "other"))

            # Get answer from AI
            answer = ai_analyzer.answer_question(
                question=question,
                document_text=doc.get("original_text", ""),
                document_type=doc_type,
            )

            # Add to chat history
            st.session_state.qa_history.append(
                {"question": question, "answer": answer, "timestamp": time.time()}
            )

            # Rerun to show the new Q&A
            st.rerun()

    except Exception as e:
        st.error(f"❌ Error processing question: {str(e)}")


def get_suggested_questions(doc_type: str) -> List[str]:
    """Get suggested questions based on document type."""

    questions_by_type = {
        "rental": [
            "What is the monthly rent amount?",
            "What happens if I pay rent late?",
            "How much is the security deposit?",
            "Can I terminate the lease early?",
            "Who is responsible for repairs?",
            "What are the landlord's obligations?",
            "Are pets allowed in the property?",
            "What happens if I damage the property?",
        ],
        "loan": [
            "What is the total amount I will repay?",
            "What is the effective interest rate?",
            "What happens if I miss a payment?",
            "What collateral is required?",
            "Can I repay the loan early?",
            "What are the processing fees?",
            "How is the interest calculated?",
            "What happens in case of default?",
        ],
        "employment": [
            "What is my total compensation package?",
            "How many hours am I expected to work?",
            "Can the company terminate me without notice?",
            "What are the non-compete restrictions?",
            "Am I allowed to work other jobs?",
            "What benefits am I entitled to?",
            "How much notice must I give to resign?",
            "Who owns the intellectual property I create?",
        ],
        "nda": [
            "What information is considered confidential?",
            "How long does the confidentiality last?",
            "What are the penalties for disclosure?",
            "Can I discuss this agreement with others?",
            "What happens after the agreement ends?",
            "Are there any exceptions to confidentiality?",
        ],
        "service": [
            "What services are included in this agreement?",
            "What is the payment schedule?",
            "How can this agreement be terminated?",
            "What are the deliverables and deadlines?",
            "Who is responsible for what costs?",
            "What happens if the work is unsatisfactory?",
        ],
    }

    return questions_by_type.get(
        doc_type,
        [
            "What are the main obligations for each party?",
            "What are the key financial terms?",
            "How can this agreement be terminated?",
            "What are the potential risks for me?",
            "What should I be most careful about?",
            "Are there any unusual or concerning clauses?",
        ],
    )


def export_chat_history():
    """Export the chat history as a text file."""
    if not st.session_state.qa_history:
        st.warning("No chat history to export.")
        return

    doc = st.session_state.current_document

    # Create chat export
    export_text = f"""
LEGA.AI Q&A SESSION EXPORT
{'='*50}

Document: {doc.get('filename', 'Unknown')}
Document Type: {doc.get('document_type', 'Unknown').title()}
Export Date: {time.strftime('%Y-%m-%d %H:%M:%S')}

QUESTIONS & ANSWERS:
{'='*50}

"""

    for i, qa in enumerate(st.session_state.qa_history):
        export_text += f"""
Q{i+1}: {qa['question']}

A{i+1}: {qa['answer']}

{'-'*30}

"""

    export_text += "\nGenerated by Lega.AI - Making legal documents accessible"

    # Clean filename - remove .pdf extension if present
    filename = doc.get("filename", "document")
    if filename.endswith(".pdf"):
        filename = filename[:-4]
    if filename.endswith(".docx"):
        filename = filename[:-5]
    if filename.endswith(".txt"):
        filename = filename[:-4]

    # Offer download
    st.download_button(
        label="📥 Download Chat History",
        data=export_text,
        file_name=f"lega_ai_qa_{filename}.pdf",
        mime="application/pdf",
    )

    st.success("✅ Chat history prepared for download!")
