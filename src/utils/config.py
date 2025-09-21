import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    # =============================================================================
    # GOOGLE AI API CONFIGURATION
    # =============================================================================
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    # =============================================================================
    # APPLICATION SETTINGS
    # =============================================================================
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    STREAMLIT_SERVER_PORT: int = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    STREAMLIT_SERVER_ADDRESS: str = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    SUPPORTED_FILE_TYPES: list = os.getenv(
        "SUPPORTED_FILE_TYPES", "pdf,docx,txt"
    ).split(",")

    # =============================================================================
    # LOGGING
    # =============================================================================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./data/app.log")

    # =============================================================================
    # SECURITY
    # =============================================================================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development-key-change-in-production")
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))

    # =============================================================================
    # AI MODEL SETTINGS
    # =============================================================================
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gemini-1.5-flash")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/embedding-001")

    # =============================================================================
    # VECTOR STORE CONFIGURATION
    # =============================================================================
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")

    # =============================================================================
    # STORAGE CONFIGURATION
    # =============================================================================
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/lega.db")

    # =============================================================================
    # PERFORMANCE SETTINGS
    # =============================================================================
    MAX_CONCURRENT_UPLOADS: int = int(os.getenv("MAX_CONCURRENT_UPLOADS", "5"))
    DOCUMENT_PROCESSING_TIMEOUT: int = int(
        os.getenv("DOCUMENT_PROCESSING_TIMEOUT", "300")
    )
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "True").lower() == "true"
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

    # =============================================================================
    # FEATURE FLAGS
    # =============================================================================
    ENABLE_DOCUMENT_LIBRARY: bool = (
        os.getenv("ENABLE_DOCUMENT_LIBRARY", "True").lower() == "true"
    )
    ENABLE_QA_ASSISTANT: bool = (
        os.getenv("ENABLE_QA_ASSISTANT", "True").lower() == "true"
    )
    ENABLE_MARKET_COMPARISON: bool = (
        os.getenv("ENABLE_MARKET_COMPARISON", "True").lower() == "true"
    )
    ENABLE_TIMELINE_TRACKER: bool = (
        os.getenv("ENABLE_TIMELINE_TRACKER", "True").lower() == "true"
    )
    ENABLE_EXPORT_FEATURES: bool = (
        os.getenv("ENABLE_EXPORT_FEATURES", "True").lower() == "true"
    )

    # =============================================================================
    # ANALYTICS & MONITORING
    # =============================================================================
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "False").lower() == "true"
    ANALYTICS_API_KEY: str = os.getenv("ANALYTICS_API_KEY", "")
    ENABLE_ERROR_TRACKING: bool = (
        os.getenv("ENABLE_ERROR_TRACKING", "False").lower() == "true"
    )
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")

    # =============================================================================
    # REGIONAL SETTINGS
    # =============================================================================
    DEFAULT_REGION: str = os.getenv("DEFAULT_REGION", "India")
    DEFAULT_CURRENCY: str = os.getenv("DEFAULT_CURRENCY", "INR")
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata")

    # =============================================================================
    # ADVANCED AI SETTINGS
    # =============================================================================
    RISK_SENSITIVITY: int = int(os.getenv("RISK_SENSITIVITY", "3"))
    SIMPLIFICATION_LEVEL: str = os.getenv("SIMPLIFICATION_LEVEL", "intermediate")
    MAX_RISK_FACTORS: int = int(os.getenv("MAX_RISK_FACTORS", "10"))

    # =============================================================================
    # API RATE LIMITING
    # =============================================================================
    API_REQUESTS_PER_MINUTE: int = int(os.getenv("API_REQUESTS_PER_MINUTE", "60"))
    API_REQUESTS_PER_DAY: int = int(os.getenv("API_REQUESTS_PER_DAY", "1000"))

    # =============================================================================
    # BACKUP & MAINTENANCE
    # =============================================================================
    ENABLE_AUTO_BACKUP: bool = (
        os.getenv("ENABLE_AUTO_BACKUP", "False").lower() == "true"
    )
    BACKUP_INTERVAL_HOURS: int = int(os.getenv("BACKUP_INTERVAL_HOURS", "24"))
    BACKUP_RETENTION_DAYS: int = int(os.getenv("BACKUP_RETENTION_DAYS", "30"))
    AUTO_CLEANUP_TEMP_FILES: bool = (
        os.getenv("AUTO_CLEANUP_TEMP_FILES", "True").lower() == "true"
    )
    CLEANUP_INTERVAL_HOURS: int = int(os.getenv("CLEANUP_INTERVAL_HOURS", "6"))

    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        required_vars = ["GOOGLE_API_KEY"]

        missing_vars = []
        for var in required_vars:
            value = getattr(cls, var, "")
            if not value or value == "your_google_ai_api_key_here":
                missing_vars.append(var)

        if missing_vars:
            print(
                f"⚠️  Missing required environment variables: {', '.join(missing_vars)}"
            )
            print("📝 Please update your .env file with valid values")
            return False

        return True

    @classmethod
    def get_config_summary(cls) -> dict:
        """Get a summary of current configuration for debugging."""
        return {
            "api_configured": bool(
                cls.GOOGLE_API_KEY
                and cls.GOOGLE_API_KEY != "your_google_ai_api_key_here"
            ),
            "debug_mode": cls.DEBUG,
            "features_enabled": {
                "document_library": cls.ENABLE_DOCUMENT_LIBRARY,
                "qa_assistant": cls.ENABLE_QA_ASSISTANT,
                "market_comparison": cls.ENABLE_MARKET_COMPARISON,
                "timeline_tracker": cls.ENABLE_TIMELINE_TRACKER,
                "export_features": cls.ENABLE_EXPORT_FEATURES,
            },
            "supported_file_types": cls.SUPPORTED_FILE_TYPES,
            "max_file_size_mb": cls.MAX_FILE_SIZE_MB,
            "risk_sensitivity": cls.RISK_SENSITIVITY,
            "region": cls.DEFAULT_REGION,
            "currency": cls.DEFAULT_CURRENCY,
        }


# Create singleton instance
config = Config()
