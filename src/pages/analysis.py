import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any
import time

from ..utils.helpers import get_risk_color, extract_financial_terms, extract_key_dates


def create_advanced_highlighting(
    text: str, risk_factors: list, jargon_definitions: dict
) -> str:
    """Create advanced highlighting with hover tooltips for clauses and jargon."""
    import re
    
    highlighted_text = text
    processed_positions = []  # Track processed positions to avoid overlaps
    
    # First, collect all risk factors and their positions
    risk_replacements = []
    for i, factor in enumerate(risk_factors):
        clause_text = factor.get("clause_text", "")
        if not clause_text:
            continue
            
        # Clean and limit clause text
        clause_text = clause_text.strip()[:150]  # Increase limit slightly
        
        # Find the position in text
        start_pos = highlighted_text.find(clause_text)
        if start_pos != -1:
            end_pos = start_pos + len(clause_text)
            
            severity = factor.get("severity", "low")
            explanation = factor.get("explanation", "")[:200]  # Limit explanation
            suggestion = factor.get("suggestion", "")[:200]  # Limit suggestion
            
            # Clean the text content for HTML (escape quotes and special chars)
            clean_explanation = explanation.replace('"', "'").replace('<', '&lt;').replace('>', '&gt;')
            clean_suggestion = suggestion.replace('"', "'").replace('<', '&lt;').replace('>', '&gt;')
            
            tooltip_content = f"⚠️ Risk: {severity.upper()}<br>📝 {clean_explanation}"
            if clean_suggestion:
                tooltip_content += f"<br>💡 Suggestion: {clean_suggestion}"
            
            risk_replacements.append({
                'start': start_pos,
                'end': end_pos,
                'original': clause_text,
                'replacement': f'<span class="tooltip risk-{severity}" title="{tooltip_content}">{clause_text}</span>',
                'type': 'risk'
            })
    
    # Sort by position (reverse order to maintain positions when replacing)
    risk_replacements.sort(key=lambda x: x['start'], reverse=True)
    
    # Apply risk replacements
    for replacement in risk_replacements:
        start, end = replacement['start'], replacement['end']
        highlighted_text = (
            highlighted_text[:start] + 
            replacement['replacement'] + 
            highlighted_text[end:]
        )
        processed_positions.extend(range(start, end))
    
    # Then highlight jargon terms (but avoid areas already processed)
    jargon_replacements = []
    for term, definition in jargon_definitions.items():
        if len(term) < 3:  # Skip very short terms
            continue
            
        # Clean definition for HTML
        clean_definition = definition.replace('"', "'").replace('<', '&lt;').replace('>', '&gt;')[:150]
        
        # Find all occurrences of the term (case-insensitive)
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        
        for match in pattern.finditer(highlighted_text):
            start_pos, end_pos = match.span()
            
            # Check if this position overlaps with existing highlights
            if any(pos in processed_positions for pos in range(start_pos, end_pos)):
                continue
                
            # Check if we're inside an HTML tag
            before_text = highlighted_text[:start_pos]
            if before_text.count('<span') > before_text.count('</span>'):
                continue  # We're inside a span, skip
                
            jargon_replacements.append({
                'start': start_pos,
                'end': end_pos,
                'original': match.group(),
                'replacement': f'<span class="tooltip jargon-term" title="📚 {term}: {clean_definition}">{match.group()}</span>',
                'type': 'jargon'
            })
    
    # Sort jargon replacements by position (reverse order)
    jargon_replacements.sort(key=lambda x: x['start'], reverse=True)
    
    # Apply jargon replacements (limit to 5 to avoid clutter)
    for replacement in jargon_replacements[:5]:
        start, end = replacement['start'], replacement['end']
        highlighted_text = (
            highlighted_text[:start] + 
            replacement['replacement'] + 
            highlighted_text[end:]
        )
    
    return highlighted_text


def show_analysis_interface():
    """Display the document analysis interface."""

    if not st.session_state.get("current_document"):
        st.info("📊 **Document Analysis Page**")
        st.markdown("### No document selected for analysis")
        st.markdown("""
        To view analysis results, you need to:
        1. **Upload a new document** for instant analysis, or
        2. **Check your library** for previously analyzed documents
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Upload Document", type="primary", use_container_width=True):
                st.session_state.page = "📄 Upload"
                st.rerun()
        
        with col2:
            if st.button("📚 View Library", use_container_width=True):
                st.session_state.page = "� Library"
                st.rerun()
                
        with col3:
            if st.button("🏠 Go Home", use_container_width=True):
                st.session_state.page = "🏠 Home"
                st.rerun()
        
        # Show recently analyzed documents if available
        if st.session_state.get("documents_library"):
            st.markdown("---")
            st.markdown("### 📋 Recently Analyzed Documents")
            st.markdown("Click on any document below to view its analysis:")
            
            for doc in st.session_state.documents_library[-3:]:  # Show last 3
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{doc.get('filename', 'Unknown')}** - {doc.get('document_type', 'Unknown').title()}")
                with col2:
                    if st.button(f"View Analysis", key=f"view_{doc.get('id')}", use_container_width=True):
                        # Load this document for analysis
                        st.session_state.current_document = doc
                        st.rerun()
        
        return

    doc = st.session_state.current_document

    # Header
    st.header("📊 Document Analysis")
    st.markdown(
        f"**File:** {doc.get('filename', 'Unknown')} | **Type:** {doc.get('document_type', 'Unknown').title()}"
    )

    # If it's a sample document, process it first
    if doc.get("is_sample") and not doc.get("processed"):
        process_sample_document(doc)
        return

    # Risk Score Dashboard
    show_risk_dashboard(doc)

    # Document Content Analysis
    col1, col2 = st.columns([1, 1])

    with col1:
        show_original_document(doc)

    with col2:
        show_simplified_version(doc)

    # Additional Analysis Sections
    st.markdown("---")

    # Tabs for different analysis views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 Summary",
            "⚠️ Risk Factors",
            "📅 Key Dates",
            "💰 Financial Terms",
            "📊 Market Comparison",
        ]
    )

    with tab1:
        show_document_summary(doc)

    with tab2:
        show_risk_factors(doc)

    with tab3:
        show_key_dates(doc)

    with tab4:
        show_financial_terms(doc)

    with tab5:
        show_market_comparison(doc)

    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💬 Ask Questions", use_container_width=True):
            st.session_state.page = "💬 Q&A"
            st.rerun()

    with col2:
        if st.button("📥 Export Report", use_container_width=True):
            export_report(doc)

    with col3:
        if st.button("📄 Analyze New Document", use_container_width=True):
            st.session_state.current_document = None
            st.session_state.page = "📄 Upload"
            st.rerun()


def process_sample_document(doc):
    """Process a sample document with simulated AI analysis."""
    st.info("🤖 Processing sample document with AI analysis...")

    progress_bar = st.progress(0)
    status_text = st.empty()

    # Simulate processing steps
    steps = [
        ("📄 Extracting text...", 20),
        ("🔍 Detecting document type...", 40),
        ("⚠️ Analyzing risks...", 60),
        ("💬 Simplifying language...", 80),
        ("📋 Generating summary...", 100),
    ]

    for step_text, progress in steps:
        status_text.text(step_text)
        progress_bar.progress(progress)
        time.sleep(0.5)

    # Generate mock analysis results
    doc_type = doc.get("document_type", "other")

    # Mock risk factors based on document type
    risk_factors = generate_mock_risk_factors(doc_type)
    simplified_text = generate_mock_simplified_text(
        doc.get("original_text", ""), doc_type
    )
    summary = generate_mock_summary(doc_type)

    # Update document with analysis
    doc.update(
        {
            "risk_data": {
                "risk_factors": risk_factors,
                "overall_assessment": f"This {doc_type} document contains several high-risk clauses.",
            },
            "simplified_text": simplified_text,
            "summary": summary,
            "key_points": [
                f"Key point 1 for {doc_type}",
                f"Key point 2 for {doc_type}",
                f"Key point 3 for {doc_type}",
            ],
            "jargon_definitions": {
                "Liability": "Legal responsibility for damages",
                "Arbitration": "Dispute resolution outside of court",
            },
            "processed": True,
            "analysis_timestamp": time.time(),
        }
    )

    st.session_state.current_document = doc

    progress_bar.empty()
    status_text.empty()
    st.success("✅ Analysis complete!")
    time.sleep(1)
    st.rerun()


def show_risk_dashboard(doc):
    """Display the risk assessment dashboard."""
    risk_data = doc.get("risk_data", {})
    risk_factors = risk_data.get("risk_factors", [])

    # Calculate risk score
    risk_score = min(len(risk_factors) * 15, 100)

    # Risk score gauge
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        # Create gauge chart
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=risk_score,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Risk Score"},
                delta={"reference": 50},
                gauge={
                    "axis": {"range": [None, 100]},
                    "bar": {"color": get_risk_color(risk_score)},
                    "steps": [
                        {"range": [0, 25], "color": "lightgray"},
                        {"range": [25, 50], "color": "gray"},
                        {"range": [50, 75], "color": "lightcoral"},
                        {"range": [75, 100], "color": "red"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 90,
                    },
                },
            )
        )

        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric(
            label="Risk Factors Found",
            value=len(risk_factors),
            delta=f"vs average: +{max(0, len(risk_factors) - 3)}",
        )

    with col3:
        risk_level = (
            "Low"
            if risk_score < 25
            else (
                "Medium"
                if risk_score < 50
                else "High" if risk_score < 75 else "Critical"
            )
        )
        st.metric(
            label="Risk Level",
            value=risk_level,
            delta_color="inverse" if risk_score > 50 else "normal",
        )

    # Risk assessment summary
    if risk_data.get("overall_assessment"):
        st.info(f"**Assessment:** {risk_data['overall_assessment']}")


def show_original_document(doc):
    """Display the original document with advanced highlighting and hover definitions."""
    st.subheader("📄 Original Document")

    original_text = doc.get("original_text", "")
    risk_factors = doc.get("risk_data", {}).get("risk_factors", [])
    jargon_definitions = doc.get("jargon_definitions", {})

    # Advanced highlighting with hover tooltips
    highlighted_text = create_advanced_highlighting(
        original_text, risk_factors, jargon_definitions
    )

    # Custom CSS for hover tooltips with responsive theming
    st.markdown(
        """
    <style>
    .tooltip {
        position: relative;
        display: inline;
        cursor: help;
        border-radius: 4px;
        padding: 2px 4px;
        margin: 0 1px;
    }
    
    /* Risk highlighting with theme-aware backgrounds */
    .risk-critical { 
        background-color: rgba(255, 68, 68, 0.2); 
        border-left: 4px solid #ff4444; 
        padding: 4px 8px;
        border-radius: 4px;
        cursor: help;
    }
    .risk-high { 
        background-color: rgba(255, 136, 0, 0.2); 
        border-left: 4px solid #ff8800; 
        padding: 4px 8px;
        border-radius: 4px;
        cursor: help;
    }
    .risk-medium { 
        background-color: rgba(255, 204, 0, 0.2); 
        border-left: 4px solid #ffcc00; 
        padding: 4px 8px;
        border-radius: 4px;
        cursor: help;
    }
    .risk-low { 
        background-color: rgba(68, 170, 68, 0.2); 
        border-left: 4px solid #44aa44; 
        padding: 4px 8px;
        border-radius: 4px;
        cursor: help;
    }
    
    /* Jargon term highlighting */
    .jargon-term { 
        background-color: rgba(46, 134, 171, 0.2); 
        text-decoration: underline dotted #2e86ab;
        padding: 2px 4px;
        border-radius: 3px;
        cursor: help;
    }
    
    /* Enhanced tooltips */
    .tooltip:hover {
        opacity: 0.8;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(highlighted_text, unsafe_allow_html=True)

    # Scroll area for long documents
    if len(original_text) > 1000:
        with st.expander("View Full Document"):
            st.text_area("Full Text", original_text, height=400, disabled=True)


def show_simplified_version(doc):
    """Display the simplified version of the document."""
    st.subheader("💬 Simplified Version")

    simplified_text = doc.get("simplified_text", "Processing...")
    st.markdown(simplified_text)

    # Key points
    key_points = doc.get("key_points", [])
    if key_points:
        st.markdown("**Key Points:**")
        for point in key_points:
            st.markdown(f"• {point}")

    # Jargon definitions
    jargon_definitions = doc.get("jargon_definitions", {})
    if jargon_definitions:
        st.markdown("**Legal Terms Explained:**")
        for term, definition in jargon_definitions.items():
            st.markdown(f"**{term}:** {definition}")


def show_document_summary(doc):
    """Display document summary."""
    summary = doc.get("summary", "Generating summary...")
    st.markdown(summary)

    # Document metadata
    st.markdown("### 📊 Document Information")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Type:** {doc.get('document_type', 'Unknown').title()}")
        st.markdown(f"**Filename:** {doc.get('filename', 'Unknown')}")

    with col2:
        if doc.get("file_size"):
            from ..utils.helpers import format_file_size

            st.markdown(f"**Size:** {format_file_size(doc['file_size'])}")

        if doc.get("analysis_timestamp"):
            import datetime

            analysis_time = datetime.datetime.fromtimestamp(doc["analysis_timestamp"])
            st.markdown(f"**Analyzed:** {analysis_time.strftime('%Y-%m-%d %H:%M')}")


def show_risk_factors(doc):
    """Display detailed risk factors."""
    risk_factors = doc.get("risk_data", {}).get("risk_factors", [])

    if not risk_factors:
        st.info("No significant risk factors identified in this document.")
        return

    for i, factor in enumerate(risk_factors):
        severity = factor.get("severity", "low")

        # Color coding based on severity
        if severity == "critical":
            st.error(f"🚨 **Critical Risk #{i+1}**")
        elif severity == "high":
            st.warning(f"⚠️ **High Risk #{i+1}**")
        elif severity == "medium":
            st.info(f"🟡 **Medium Risk #{i+1}**")
        else:
            st.success(f"🟢 **Low Risk #{i+1}**")

        st.markdown(f"**Clause:** {factor.get('clause_text', 'N/A')}")
        st.markdown(f"**Category:** {factor.get('category', 'N/A').title()}")
        st.markdown(f"**Explanation:** {factor.get('explanation', 'N/A')}")

        if factor.get("suggestion"):
            st.markdown(f"**Suggestion:** {factor['suggestion']}")

        st.markdown("---")


def show_key_dates(doc):
    """Display extracted key dates with timeline visualization."""
    original_text = doc.get("original_text", "")
    dates = extract_key_dates(original_text)

    if not dates:
        st.info("No specific dates found in this document.")
        return

    # Enhanced date analysis with timeline
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Important Dates Found:**")
        for date_info in dates:
            st.markdown(f"• **{date_info['date']}** - Context: {date_info['context']}")

    with col2:
        st.markdown("**Timeline & Obligations:**")

        # Mock timeline data based on document type
        doc_type = doc.get("document_type", "other")

        if doc_type == "rental":
            timeline_items = [
                {
                    "date": "1st of every month",
                    "event": "Rent Payment Due",
                    "type": "recurring",
                },
                {
                    "date": "30 days notice",
                    "event": "Termination Notice Required",
                    "type": "condition",
                },
                {
                    "date": "End of lease",
                    "event": "Security Deposit Return",
                    "type": "deadline",
                },
            ]
        elif doc_type == "loan":
            timeline_items = [
                {
                    "date": "15th of every month",
                    "event": "EMI Payment Due",
                    "type": "recurring",
                },
                {
                    "date": "7 days after due",
                    "event": "Late Fee Applicable",
                    "type": "penalty",
                },
                {"date": "24 months", "event": "Loan Maturity", "type": "deadline"},
            ]
        elif doc_type == "employment":
            timeline_items = [
                {
                    "date": "Last day of month",
                    "event": "Salary Payment",
                    "type": "recurring",
                },
                {
                    "date": "90 days",
                    "event": "Resignation Notice Period",
                    "type": "condition",
                },
                {
                    "date": "2 years post-termination",
                    "event": "Non-compete Expires",
                    "type": "deadline",
                },
            ]
        else:
            timeline_items = []

        for item in timeline_items:
            if item["type"] == "recurring":
                st.markdown(f"🔄 **{item['date']}**: {item['event']}")
            elif item["type"] == "penalty":
                st.markdown(f"⚠️ **{item['date']}**: {item['event']}")
            elif item["type"] == "deadline":
                st.markdown(f"📅 **{item['date']}**: {item['event']}")
            else:
                st.markdown(f"📌 **{item['date']}**: {item['event']}")

    # Visual timeline chart
    if timeline_items:
        st.markdown("---")
        st.markdown("**📊 Visual Timeline**")

        # Create timeline visualization
        timeline_df = []
        for i, item in enumerate(timeline_items):
            timeline_df.append(
                {
                    "Event": item["event"],
                    "Timeline": item["date"],
                    "Type": item["type"].title(),
                    "Order": i,
                }
            )

        if timeline_df:
            import pandas as pd

            df = pd.DataFrame(timeline_df)

            # Color code by type
            color_map = {
                "Recurring": "#2e86ab",
                "Penalty": "#ff4444",
                "Deadline": "#ff8800",
                "Condition": "#44aa44",
            }

            fig = px.timeline(
                df,
                x_start=[0] * len(df),
                x_end=[1] * len(df),
                y="Event",
                color="Type",
                color_discrete_map=color_map,
                title="Contract Timeline & Obligations",
            )
            st.plotly_chart(fig, use_container_width=True)


def show_financial_terms(doc):
    """Display extracted financial terms."""
    original_text = doc.get("original_text", "")
    financial_terms = extract_financial_terms(original_text)

    if not financial_terms:
        st.info("No financial terms identified in this document.")
        return

    col1, col2 = st.columns(2)

    with col1:
        if "amounts" in financial_terms:
            st.markdown("**Monetary Amounts:**")
            for amount in financial_terms["amounts"]:
                st.markdown(f"• {amount}")

    with col2:
        if "percentages" in financial_terms:
            st.markdown("**Percentages/Rates:**")
            for percentage in financial_terms["percentages"]:
                st.markdown(f"• {percentage}")

    if "interest_rates" in financial_terms:
        st.markdown("**Interest Rates:**")
        for rate in financial_terms["interest_rates"]:
            st.markdown(f"• {rate}")


def export_report(doc):
    """Export analysis report."""
    # Create a simple text report
    report = f"""
LEGA.AI DOCUMENT ANALYSIS REPORT
{'='*50}

Document: {doc.get('filename', 'Unknown')}
Type: {doc.get('document_type', 'Unknown').title()}
Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
{doc.get('summary', 'No summary available')}

RISK ASSESSMENT:
{doc.get('risk_data', {}).get('overall_assessment', 'No risk assessment available')}

RISK FACTORS:
"""

    risk_factors = doc.get("risk_data", {}).get("risk_factors", [])
    for i, factor in enumerate(risk_factors):
        report += f"""
{i+1}. {factor.get('severity', 'Unknown').upper()} RISK
   Category: {factor.get('category', 'N/A').title()}
   Clause: {factor.get('clause_text', 'N/A')}
   Explanation: {factor.get('explanation', 'N/A')}
"""

    report += f"""

SIMPLIFIED VERSION:
{doc.get('simplified_text', 'No simplified version available')}

KEY POINTS:
"""

    for point in doc.get("key_points", []):
        report += f"• {point}\n"

    report += "\n\nGenerated by Lega.AI - Making legal documents accessible"

    # Clean filename - remove .pdf extension if present
    filename = doc.get('filename', 'document')
    if filename.endswith('.pdf'):
        filename = filename[:-4]
    if filename.endswith('.docx'):
        filename = filename[:-5]
    if filename.endswith('.txt'):
        filename = filename[:-4]

    # Offer download
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name=f"lega_ai_report_{filename}.pdf",
        mime="application/pdf",
    )

    st.success("✅ Report prepared for download!")


def generate_mock_risk_factors(doc_type):
    """Generate mock risk factors for sample documents."""
    if doc_type == "rental":
        return [
            {
                "clause_text": "Late payments will incur a penalty of Rs. 1,000 per day",
                "category": "financial",
                "severity": "high",
                "explanation": "Daily penalties can quickly escalate to substantial amounts",
                "suggestion": "Negotiate a more reasonable penalty structure",
            },
            {
                "clause_text": "Tenant is responsible for all repairs and maintenance",
                "category": "financial",
                "severity": "medium",
                "explanation": "This places unusual burden on tenant for structural repairs",
                "suggestion": "Clarify that structural repairs remain landlord responsibility",
            },
        ]
    elif doc_type == "loan":
        return [
            {
                "clause_text": "24% per annum (APR 28.5% including processing fees)",
                "category": "financial",
                "severity": "critical",
                "explanation": "Interest rate is significantly above market rates",
                "suggestion": "Shop around for better rates from other lenders",
            },
            {
                "clause_text": "Lender may seize collateral immediately upon default",
                "category": "rights",
                "severity": "high",
                "explanation": "No grace period or notice before asset seizure",
                "suggestion": "Negotiate for notice period and cure opportunity",
            },
        ]
    elif doc_type == "employment":
        return [
            {
                "clause_text": "Employee shall not work for any competing company for 2 years",
                "category": "commitment",
                "severity": "high",
                "explanation": "Non-compete period is unusually long and broad",
                "suggestion": "Negotiate shorter period and narrower scope",
            },
            {
                "clause_text": "Company may terminate employment at any time without cause",
                "category": "rights",
                "severity": "medium",
                "explanation": "No job security or notice period for termination",
                "suggestion": "Request notice period and severance terms",
            },
        ]
    else:
        return []


def generate_mock_simplified_text(original_text, doc_type):
    """Generate mock simplified text."""
    if doc_type == "rental":
        return """
**What this rental agreement means in simple terms:**

You're renting a property in Mumbai for ₹25,000 per month. Here are the key things to know:

• **Payment:** You must pay rent by the 1st of each month. If you're late, you'll be charged ₹1,000 for each day you're late.

• **Security deposit:** You need to pay ₹75,000 upfront as security. This money is hard to get back.

• **Repairs:** You're responsible for fixing everything that breaks, even major structural problems.

• **Leaving early:** If you want to leave before the lease ends, you lose your security deposit.

**Watch out for:** The daily late fees and your responsibility for all repairs are unusual and costly.
        """
    elif doc_type == "loan":
        return """
**What this loan agreement means in simple terms:**

You're borrowing ₹2,00,000 but will pay back ₹3,00,000 total - that's ₹1,00,000 extra in interest and fees.

• **Monthly payment:** ₹12,500 every month for 2 years

• **Interest rate:** 24% per year (very high - normal rates are 10-15%)

• **Late fees:** ₹500 per day if you're late

• **Your gold jewelry:** The lender can take it immediately if you miss payments

• **Total cost:** You'll pay 50% more than you borrowed

**Warning:** This is an expensive loan. The interest rate is much higher than banks typically charge.
        """
    elif doc_type == "employment":
        return """
**What this employment contract means in simple terms:**

You're being hired as a Software Developer for ₹8,00,000 per year. Here's what you need to know:

• **Working hours:** 45 hours per week, including weekends when needed

• **Salary:** ₹66,667 per month

• **If you quit:** You must give 90 days notice

• **If they fire you:** They can fire you anytime without reason or notice

• **After leaving:** You can't work for competing companies for 2 years

• **Side work:** You can't do any other work while employed

**Concerns:** The 2-year non-compete and ability to fire without notice are harsh terms.
        """
    else:
        return "Document simplified version will appear here after analysis."


def show_market_comparison(doc):
    """Display market benchmarking and comparison data."""
    doc_type = doc.get("document_type", "other")

    st.markdown("**Market Context & Benchmarking**")

    if doc_type == "rental":
        show_rental_market_comparison(doc)
    elif doc_type == "loan":
        show_loan_market_comparison(doc)
    elif doc_type == "employment":
        show_employment_market_comparison(doc)
    else:
        st.info(
            "Market comparison data available for rental, loan, and employment contracts."
        )


def show_rental_market_comparison(doc):
    """Show rental market comparison."""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏠 Rental Market Analysis")
        st.markdown("**Security Deposit:** ₹75,000")
        st.success("✅ Standard: Typically 2-3 months rent")

        st.markdown("**Late Penalty:** ₹1,000/day")
        st.error("❌ Above Market: Typical penalties are ₹100-500/day")

        st.markdown("**Maintenance Responsibility:** Tenant")
        st.warning("⚠️ Unusual: Structural repairs typically landlord's responsibility")

    with col2:
        st.markdown("#### 📊 Mumbai Rental Benchmarks")

        # Mock market data
        market_data = {
            "Average Rent (2BHK)": "₹28,000",
            "Security Deposit Range": "₹50,000 - ₹84,000",
            "Standard Late Fee": "₹200/day",
            "Tenant Maintenance": "10% of agreements",
        }

        for metric, value in market_data.items():
            st.metric(metric, value)


def show_loan_market_comparison(doc):
    """Show loan market comparison."""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💰 Loan Market Analysis")
        st.markdown("**Interest Rate:** 24% per annum")
        st.error("❌ Well Above Market: Bank rates typically 10-15%")

        st.markdown("**Processing Fee:** ₹10,000")
        st.warning("⚠️ High: Typical processing fees 1-2% of loan amount")

        st.markdown("**Total Repayment:** ₹3,00,000 for ₹2,00,000")
        st.error("❌ Very High: 50% more than principal")

    with col2:
        st.markdown("#### 📊 Personal Loan Benchmarks")

        # Create comparison chart
        fig = px.bar(
            x=["Your Loan", "Bank Average", "NBFC Average"],
            y=[24, 12, 18],
            title="Interest Rate Comparison (%)",
            color=["red", "green", "orange"],
        )
        st.plotly_chart(fig, use_container_width=True)


def show_employment_market_comparison(doc):
    """Show employment market comparison."""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💼 Employment Market Analysis")
        st.markdown("**Non-compete Period:** 2 years")
        st.error("❌ Excessive: Typical non-compete is 6-12 months")

        st.markdown("**Notice Period:** 90 days")
        st.warning("⚠️ Long: Standard notice is 30-60 days")

        st.markdown("**At-will Termination:** Yes")
        st.error("❌ Unfavorable: Most contracts provide notice period")

    with col2:
        st.markdown("#### 📊 IT Industry Standards")

        standards = {
            "Average Salary (3-5 YOE)": "₹8-12 lakhs",
            "Standard Notice Period": "30-60 days",
            "Typical Non-compete": "6-12 months",
            "Weekend Work": "Occasionally, not mandatory",
        }

        for standard, value in standards.items():
            st.metric(standard, value)


def generate_mock_summary(doc_type):
    """Generate mock summary."""
    if doc_type == "rental":
        return "This is a residential lease agreement for a property in Mumbai with rent of ₹25,000/month. The agreement contains several tenant-unfavorable terms including high daily late fees, tenant responsibility for all repairs, and forfeiture of security deposit for early termination."
    elif doc_type == "loan":
        return "This is a personal loan agreement for ₹2,00,000 with very high interest rates (24% APR, 28.5% effective). The loan requires gold jewelry as collateral and includes harsh default terms with immediate asset seizure rights."
    elif doc_type == "employment":
        return "This is an employment contract for a Software Developer position with ₹8,00,000 annual salary. The contract includes restrictive terms like a 2-year non-compete clause, at-will termination by employer, and prohibition on side work."
    else:
        return "Document summary will appear here after analysis."
