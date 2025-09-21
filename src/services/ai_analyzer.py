from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import time

from src.utils.config import config
from src.utils.logger import log_error, log_analysis_start, log_analysis_complete
from src.models.document import (
    DocumentType,
    RiskLevel,
    RiskCategory,
    RiskFactor,
    ClausePosition,
)
from src.utils.helpers import (
    calculate_risk_score,
    extract_key_dates,
    extract_financial_terms,
)


class AIAnalyzer:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=config.CHAT_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=config.TEMPERATURE,
            max_output_tokens=config.MAX_TOKENS,
        )

        # Initialize prompt templates
        self._setup_prompts()

    def _setup_prompts(self):
        """Set up prompt templates for different analysis tasks."""

        # Risk analysis prompt
        self.risk_analysis_prompt = PromptTemplate(
            input_variables=["text", "document_type"],
            template="""
            Analyze the following {document_type} document for potential risks and problematic clauses.
            
            Document text:
            {text}
            
            Please identify:
            1. High-risk clauses that could be problematic for the signer
            2. Financial risks (hidden fees, penalties, high costs)
            3. Commitment risks (long-term obligations, difficult exit clauses)
            4. Rights risks (waived protections, limited recourse)
            
            For each risk, provide:
            - The exact clause text (keep it concise, max 100 words)
            - Risk category (financial, commitment, rights, or standard)
            - Severity level (low, medium, high, critical)
            - Clear explanation of why it's risky
            - Suggestion for improvement
            
            IMPORTANT: Return ONLY valid JSON in the exact format below. Do not include any explanatory text before or after the JSON:
            
            {{
                "risk_factors": [
                    {{
                        "clause_text": "exact text from document",
                        "category": "financial",
                        "severity": "medium",
                        "explanation": "why this is risky",
                        "suggestion": "how to improve or what to watch for"
                    }}
                ],
                "overall_assessment": "brief summary of document risk level"
            }}
            """,
        )

        # Plain language translation prompt
        self.simplification_prompt = PromptTemplate(
            input_variables=["text", "document_type"],
            template="""
            Convert the following legal text into plain, simple English that anyone can understand.
            
            Document type: {document_type}
            Legal text: {text}
            
            Rules for simplification:
            1. Use everyday language instead of legal jargon
            2. Break down complex sentences into shorter ones
            3. Explain what actions or obligations mean in practical terms
            4. Keep the essential meaning intact
            5. Use "you" to make it personal and clear
            6. Focus on the most important points
            
            IMPORTANT: Return ONLY valid JSON in the exact format below. Do not include any explanatory text:
            
            {{
                "simplified_text": "the simplified version in plain English",
                "key_points": ["main point 1", "main point 2", "main point 3"],
                "jargon_definitions": {{"legal term": "simple definition"}}
            }}
            """,
        )

        # Document summary prompt
        self.summary_prompt = PromptTemplate(
            input_variables=["text", "document_type"],
            template="""
            Create a concise summary of this {document_type} document.
            
            Document: {text}
            
            Provide a summary that includes:
            1. What type of agreement this is
            2. Who are the main parties involved
            3. Key obligations for each party
            4. Important terms (dates, amounts, conditions)
            5. Major benefits and risks
            
            Keep it under 200 words and focus on what matters most to the person signing.
            """,
        )

    def analyze_document_risk(
        self, text: str, document_type: DocumentType
    ) -> Dict[str, Any]:
        """Analyze document for risks and problematic clauses."""
        try:
            log_analysis_start("risk_analysis")
            start_time = time.time()

            # Create and run the risk analysis chain
            risk_chain = LLMChain(llm=self.llm, prompt=self.risk_analysis_prompt)

            result = risk_chain.run(
                text=text[:4000],  # Limit text size for API
                document_type=document_type.value,
            )

            # Parse JSON response with better error handling
            try:
                # Try to extract JSON from the response if it's wrapped in markdown
                if "```json" in result:
                    json_start = result.find("```json") + 7
                    json_end = result.find("```", json_start)
                    if json_end != -1:
                        result = result[json_start:json_end].strip()

                # Clean up the result string
                result = result.strip()
                if result.startswith("```") and result.endswith("```"):
                    result = result[3:-3].strip()

                risk_data = json.loads(result)

                # Validate the structure
                if not isinstance(risk_data, dict):
                    raise ValueError("Response is not a dictionary")

                if "risk_factors" not in risk_data:
                    risk_data["risk_factors"] = []

                if "overall_assessment" not in risk_data:
                    risk_data["overall_assessment"] = "Analysis completed"

            except (json.JSONDecodeError, ValueError) as e:
                log_error(f"JSON parsing error in risk analysis: {str(e)}")
                log_error(f"Raw AI response: {result[:500]}...")

                # Try to extract risk information manually if JSON fails
                risk_data = self._extract_risk_fallback(result, text)

            processing_time = time.time() - start_time
            log_analysis_complete("risk_analysis", processing_time)

            return risk_data

        except Exception as e:
            log_error(f"Error in risk analysis: {str(e)}")
            return {"risk_factors": [], "overall_assessment": "Analysis failed"}

    def _extract_risk_fallback(
        self, response: str, original_text: str
    ) -> Dict[str, Any]:
        """Fallback method to extract risk information when JSON parsing fails."""
        try:
            risk_factors = []

            # Look for common risk indicators in the response
            risk_keywords = [
                "risk",
                "problematic",
                "concern",
                "warning",
                "caution",
                "penalty",
                "fee",
            ]
            sentences = response.split(".")

            for i, sentence in enumerate(sentences):
                sentence = sentence.strip()
                if (
                    any(
                        keyword.lower() in sentence.lower() for keyword in risk_keywords
                    )
                    and len(sentence) > 20
                ):
                    risk_factors.append(
                        {
                            "clause_text": sentence[:200],  # Limit length
                            "category": "standard",
                            "severity": "medium",
                            "explanation": "Potential risk identified by text analysis",
                            "suggestion": "Review this clause carefully with legal counsel",
                        }
                    )

                    if len(risk_factors) >= 5:  # Limit to 5 fallback risks
                        break

            return {
                "risk_factors": risk_factors,
                "overall_assessment": "Risk analysis completed with limited parsing. Please review manually.",
            }

        except Exception as e:
            log_error(f"Error in fallback risk extraction: {str(e)}")
            return {
                "risk_factors": [],
                "overall_assessment": "Unable to analyze risks - please try again",
            }

    def simplify_text(self, text: str, document_type: DocumentType) -> Dict[str, Any]:
        """Convert legal text to plain language."""
        try:
            simplification_chain = LLMChain(
                llm=self.llm, prompt=self.simplification_prompt
            )

            result = simplification_chain.run(
                text=text[:3000], document_type=document_type.value  # Limit text size
            )

            # Parse JSON response with better error handling
            try:
                # Try to extract JSON from the response if it's wrapped in markdown
                if "```json" in result:
                    json_start = result.find("```json") + 7
                    json_end = result.find("```", json_start)
                    if json_end != -1:
                        result = result[json_start:json_end].strip()

                # Clean up the result string
                result = result.strip()
                if result.startswith("```") and result.endswith("```"):
                    result = result[3:-3].strip()

                simplified_data = json.loads(result)

                # Validate the structure
                if not isinstance(simplified_data, dict):
                    raise ValueError("Response is not a dictionary")

                # Ensure required keys exist
                if "simplified_text" not in simplified_data:
                    simplified_data["simplified_text"] = text[:500] + "..."
                if "key_points" not in simplified_data:
                    simplified_data["key_points"] = ["Unable to extract key points"]
                if "jargon_definitions" not in simplified_data:
                    simplified_data["jargon_definitions"] = {}

            except (json.JSONDecodeError, ValueError) as e:
                log_error(f"JSON parsing error in text simplification: {str(e)}")
                simplified_data = {
                    "simplified_text": text[:500]
                    + "... (Full simplification unavailable)",
                    "key_points": ["Document content requires legal review"],
                    "jargon_definitions": {},
                }

            return simplified_data

        except Exception as e:
            log_error(f"Error in text simplification: {str(e)}")
            return {
                "simplified_text": text[:500]
                + "...",  # Return truncated original if simplification fails
                "key_points": ["Simplification failed - showing original text"],
                "jargon_definitions": {},
            }

    def generate_summary(self, text: str, document_type: DocumentType) -> str:
        """Generate a concise document summary."""
        try:
            summary_chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)

            summary = summary_chain.run(
                text=text[:3000], document_type=document_type.value  # Limit text size
            )

            return summary.strip()

        except Exception as e:
            log_error(f"Error generating summary: {str(e)}")
            return "Unable to generate summary"

    def answer_question(
        self, question: str, document_text: str, document_type: DocumentType
    ) -> str:
        """Answer a question about the document."""
        try:
            qa_prompt = PromptTemplate(
                input_variables=["question", "document", "doc_type"],
                template="""
                Answer the following question about this {doc_type} document. 
                Be specific and cite relevant parts of the document.
                
                Document: {document}
                
                Question: {question}
                
                Provide a clear, helpful answer based only on the document content.
                If the answer isn't in the document, say so clearly.
                """,
            )

            qa_chain = LLMChain(llm=self.llm, prompt=qa_prompt)

            answer = qa_chain.run(
                question=question,
                document=document_text[:3000],  # Limit context size
                doc_type=document_type.value,
            )

            return answer.strip()

        except Exception as e:
            log_error(f"Error answering question: {str(e)}")
            return "Sorry, I couldn't process your question. Please try again."

    def create_risk_factors(
        self, risk_data: Dict[str, Any], text: str
    ) -> List[RiskFactor]:
        """Convert AI analysis results to RiskFactor objects."""
        risk_factors = []

        for factor_data in risk_data.get("risk_factors", []):
            try:
                # Find clause position in text
                clause_text = factor_data.get("clause_text", "")
                position = None

                if clause_text:
                    start_index = text.find(clause_text)
                    if start_index != -1:
                        position = ClausePosition(
                            start_index=start_index,
                            end_index=start_index + len(clause_text),
                        )

                risk_factor = RiskFactor(
                    id=f"risk_{len(risk_factors) + 1}",
                    clause_text=clause_text,
                    category=RiskCategory(factor_data.get("category", "standard")),
                    severity=RiskLevel(factor_data.get("severity", "low")),
                    explanation=factor_data.get("explanation", ""),
                    suggestion=factor_data.get("suggestion"),
                    position=position,
                )

                risk_factors.append(risk_factor)

            except Exception as e:
                log_error(f"Error creating risk factor: {str(e)}")
                continue

        return risk_factors
