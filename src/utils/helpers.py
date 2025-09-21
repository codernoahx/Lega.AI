import hashlib
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re


def generate_document_id() -> str:
    """Generate a unique document ID."""
    return str(uuid.uuid4())


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def calculate_file_hash(file_content: bytes) -> str:
    """Calculate SHA-256 hash of file content."""
    return hashlib.sha256(file_content).hexdigest()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    # Remove or replace dangerous characters
    sanitized = re.sub(r"[^\w\-_\.]", "_", filename)
    # Ensure it's not too long
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[: 255 - len(ext)] + ext
    return sanitized


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"


def extract_key_dates(text: str) -> List[Dict[str, Any]]:
    """Extract dates and deadlines from text."""
    date_patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",  # MM/DD/YYYY
        r"\b\d{1,2}-\d{1,2}-\d{4}\b",  # MM-DD-YYYY
        r"\b\d{4}-\d{1,2}-\d{1,2}\b",  # YYYY-MM-DD
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
    ]

    dates = []
    for pattern in date_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            dates.append(
                {
                    "date": match.group(),
                    "position": match.start(),
                    "context": text[max(0, match.start() - 50) : match.end() + 50],
                }
            )

    return dates


def extract_financial_terms(text: str) -> Dict[str, Any]:
    """Extract financial information from text."""
    financial_info = {}

    # Extract monetary amounts (Indian Rupees and other currencies)
    money_patterns = [
        r"₹[\d,]+(?:\.\d{2})?",  # Indian Rupees
        r"Rs\.?\s*[\d,]+(?:\.\d{2})?",  # Rs. format
        r"\$[\d,]+(?:\.\d{2})?",  # USD
    ]

    amounts = []
    for pattern in money_patterns:
        amounts.extend(re.findall(pattern, text))

    if amounts:
        financial_info["amounts"] = amounts

    # Extract percentages
    percentage_pattern = r"\d+(?:\.\d+)?%"
    percentages = re.findall(percentage_pattern, text)
    if percentages:
        financial_info["percentages"] = percentages

    # Extract interest rates
    interest_pattern = (
        r"(?:interest rate|APR|annual percentage rate).*?(\d+(?:\.\d+)?%)"
    )
    interest_matches = re.findall(interest_pattern, text, re.IGNORECASE)
    if interest_matches:
        financial_info["interest_rates"] = interest_matches

    return financial_info


def calculate_risk_score(risk_factors: List[Dict[str, Any]]) -> int:
    """Calculate overall risk score from individual risk factors."""
    if not risk_factors:
        return 0

    risk_weights = {"critical": 25, "high": 15, "medium": 8, "low": 3}

    total_score = 0
    for factor in risk_factors:
        severity = factor.get("severity", "low").lower()
        total_score += risk_weights.get(severity, 0)

    # Cap at 100
    return min(total_score, 100)


def get_risk_color(risk_score: int) -> str:
    """Get color code based on risk score."""
    if risk_score >= 75:
        return "#FF4444"  # Red
    elif risk_score >= 50:
        return "#FF8800"  # Orange
    elif risk_score >= 25:
        return "#FFCC00"  # Yellow
    else:
        return "#44AA44"  # Green


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks for processing."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at sentence boundary
        if end < len(text):
            last_period = chunk.rfind(".")
            if last_period > chunk_size // 2:
                chunk = chunk[: last_period + 1]
                end = start + last_period + 1

        chunks.append(chunk)
        start = end - overlap

    return chunks


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display."""
    now = datetime.now()
    diff = now - timestamp

    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"
