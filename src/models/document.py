from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    RENTAL = "rental"
    LOAN = "loan"
    EMPLOYMENT = "employment"
    SERVICE = "service"
    NDA = "nda"
    OTHER = "other"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    FINANCIAL = "financial"
    COMMITMENT = "commitment"
    RIGHTS = "rights"
    STANDARD = "standard"


class ClausePosition(BaseModel):
    start_index: int
    end_index: int
    page_number: Optional[int] = None


class RiskFactor(BaseModel):
    id: str
    clause_text: str
    category: RiskCategory
    severity: RiskLevel
    explanation: str
    suggestion: Optional[str] = None
    position: Optional[ClausePosition] = None


class DocumentAnalysis(BaseModel):
    document_id: str
    document_type: DocumentType
    risk_score: int = Field(ge=0, le=100)
    summary: str
    simplified_text: str
    risk_factors: List[RiskFactor] = []
    key_dates: List[Dict[str, Any]] = []
    financial_terms: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.now)


class Document(BaseModel):
    id: str
    filename: str
    file_path: str
    document_type: Optional[DocumentType] = None
    file_size: int
    upload_timestamp: datetime = Field(default_factory=datetime.now)
    analysis: Optional[DocumentAnalysis] = None
    processed: bool = False


class QASession(BaseModel):
    id: str
    document_id: str
    question: str
    answer: str
    timestamp: datetime = Field(default_factory=datetime.now)
    confidence_score: Optional[float] = None


class SimplificationRequest(BaseModel):
    text: str
    context: Optional[str] = None
    document_type: Optional[DocumentType] = None


class SimplificationResponse(BaseModel):
    original_text: str
    simplified_text: str
    key_points: List[str] = []
    jargon_definitions: Dict[str, str] = {}
