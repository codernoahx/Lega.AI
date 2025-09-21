import logging
import os
from datetime import datetime
from src.utils.config import config


def setup_logging():
    """Set up logging configuration."""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(config.LOG_FILE), logging.StreamHandler()],
    )

    return logging.getLogger(__name__)


def log_document_upload(filename: str, file_size: int) -> None:
    """Log document upload event."""
    logger = logging.getLogger(__name__)
    logger.info(f"Document uploaded: {filename} ({file_size} bytes)")


def log_analysis_start(document_id: str) -> None:
    """Log analysis start event."""
    logger = logging.getLogger(__name__)
    logger.info(f"Starting analysis for document: {document_id}")


def log_analysis_complete(document_id: str, processing_time: float) -> None:
    """Log analysis completion event."""
    logger = logging.getLogger(__name__)
    logger.info(
        f"Analysis completed for document: {document_id} in {processing_time:.2f}s"
    )


def log_error(error_message: str, document_id: str = None) -> None:
    """Log error event."""
    logger = logging.getLogger(__name__)
    if document_id:
        logger.error(f"Error processing document {document_id}: {error_message}")
    else:
        logger.error(f"Application error: {error_message}")


def log_qa_interaction(document_id: str, question: str) -> None:
    """Log Q&A interaction."""
    logger = logging.getLogger(__name__)
    logger.info(f"Q&A interaction for document {document_id}: {question[:100]}...")


# Initialize logging when module is imported
setup_logging()
