---
title: Lega.AI
emoji: ⚖️
colorFrom: pink
colorTo: indigo
sdk: docker
pinned: false
---

# Lega.AI

AI-powered legal document analysis and simplification platform that makes complex legal documents accessible to everyone.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.49+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [🚀 Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📋 Prerequisites](#-prerequisites)
- [🚀 Quick Start](#-quick-start)
- [🐳 Docker Deployment](#-docker-deployment)
- [📁 Project Structure](#-project-structure)
- [🎯 Usage Guide](#-usage-guide)
- [📄 Sample Documents](#-sample-documents)
- [🚨 Document Types Supported](#-document-types-supported)
- [⚡ Key Features Deep Dive](#-key-features-deep-dive)
- [🔧 Configuration Options](#-configuration-options)
- [🔒 Privacy & Security](#-privacy--security)
- [🤝 Contributing](#-contributing)
- [🆘 Support](#-support)
- [🎯 Roadmap](#-roadmap)

## 🚀 Features

- **🔍 Advanced Document Analysis**: Upload PDF/DOCX/TXT files and get comprehensive AI-powered analysis using Google's Gemini
- **📝 Plain Language Translation**: Convert complex legal jargon into clear, understandable language with context-aware explanations
- **⚠️ Intelligent Risk Assessment**: Multi-dimensional risk scoring with color-coded severity levels and detailed explanations
- **💬 Interactive Q&A Assistant**: Ask specific questions about your documents and get instant, context-aware AI responses
- **🎯 Smart Clause Highlighting**: Visual highlighting of risky clauses with interactive tooltips and improvement suggestions
- **📊 Vector-Powered Similarity Search**: Find similar clauses across documents using Chroma vector database
- **📚 Persistent Document Library**: Organize, search, and manage all analyzed documents with metadata
- **⚠️ Risk Visualization**: Interactive charts and gauges showing risk distribution and severity
- **🗓️ Key Information Extraction**: Automatically identify important dates, deadlines, and financial terms
- **💾 Local Data Persistence**: Secure local storage of analysis results and vector embeddings
- **🎨 Modern UI/UX**: Responsive Streamlit interface with custom CSS and intuitive navigation

## 🛠️ Tech Stack

- **Frontend**: Streamlit with multi-page navigation and custom CSS styling
- **AI/ML**: LangChain + Google Generative AI (Gemini Pro)
- **Embeddings**: Google Generative AI Embeddings (models/text-embedding-004)
- **Vector Store**: Chroma for document similarity search and persistence
- **Document Processing**: PyPDF for PDF extraction, python-docx for Word documents
- **Package Management**: UV (modern Python package manager)
- **Configuration**: Python-dotenv for environment management
- **Visualization**: Plotly for interactive charts and analytics
- **UI Components**: Streamlit-option-menu for enhanced navigation

## 📋 Prerequisites

- Python 3.13+ (required for latest features and performance)
- Google AI API key (get from [Google AI Studio](https://aistudio.google.com/))
- UV package manager (recommended for fast, reliable dependency management)

## 🚀 Quick Start

### 1. **Clone and navigate to the project**:

```bash
git clone <repository-url>
cd Lega.AI
```

### 2. **Install UV (if not already installed)**:

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

### 3. **Set up environment and install dependencies**:

```bash
# Create and activate virtual environment with dependencies
uv sync

# Or if you prefer traditional approach:
# uv venv
# source .venv/bin/activate  # On Windows: .venv\Scripts\activate
# uv pip install -r pyproject.toml
```

### 4. **Configure environment**:

```bash
# Copy the template file
cp .env.example .env

# Edit .env file and update the following required settings:
```

**Required Configuration:**

```env
# Get your API key from: https://aistudio.google.com/
GOOGLE_API_KEY=your-google-api-key-here
```

**Optional Configuration (with sensible defaults):**

```env
# Application Settings
DEBUG=True
LOG_LEVEL=INFO
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost

# File Upload Settings
MAX_FILE_SIZE_MB=10
SUPPORTED_FILE_TYPES=pdf,docx,txt

# AI Model Settings
TEMPERATURE=0.2
MAX_TOKENS=2048
EMBEDDING_MODEL=models/text-embedding-004

# Storage Configuration
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
UPLOAD_DIR=./uploads
DATA_DIR=./data
LOG_FILE=./data/app.log

# Security Settings
SECRET_KEY=your-secret-key-here
SESSION_TIMEOUT_MINUTES=60
```

### 5. **Run the application**:

```bash
# If using UV (recommended)
uv run streamlit run main.py

# Or with activated virtual environment
streamlit run main.py
```

### 6. **Open your browser** to `http://localhost:8501`

### 🎯 Try the Demo

Once running, you can immediately test the application with the included sample documents:

- Navigate to **📄 Upload** page
- Try the sample documents: Employment contracts, NDAs, Lease agreements, Service agreements
- Experience the full analysis workflow without needing your own documents

## 🐳 Docker Deployment

### Local Docker Deployment

```bash
# Build the Docker image
docker build -t lega-ai .

# Run the container
docker run -p 7860:7860 -e GOOGLE_API_KEY=your_api_key_here lega-ai
```

### Hugging Face Spaces Deployment

Deploy Lega.AI to Hugging Face Spaces with one click!

[![Deploy to Hugging Face Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/deploy-to-spaces-md.svg)](https://huggingface.co/spaces)

**Quick Setup:**

1. Create a new [Hugging Face Space](https://huggingface.co/spaces) with SDK: Docker
2. Upload this repository to your Space
3. Set `GOOGLE_API_KEY` in Space Settings → Variables
4. Your app will be live at `https://huggingface.co/spaces/[username]/[space-name]`

📋 **Detailed Instructions**: See [HUGGINGFACE_DEPLOYMENT.md](./HUGGINGFACE_DEPLOYMENT.md) for complete setup guide.

## 📁 Project Structure

```
Lega.AI/
├── main.py                 # Main Streamlit application entry point
├── pyproject.toml          # UV/pip package configuration and dependencies
├── requirements.txt        # Docker-compatible requirements file
├── uv.lock                 # UV lockfile for reproducible builds
├── setup.py                # Legacy Python package setup
├── Dockerfile              # Docker container configuration
├── .dockerignore          # Docker build optimization
├── start.sh               # Hugging Face Spaces startup script
├── .env.example           # Environment variables template
├── .env.hf                # Hugging Face Spaces configuration
├── README.md              # Project documentation
├── HUGGINGFACE_DEPLOYMENT.md # HF Spaces deployment guide
├── src/                   # Main application source code
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py    # Document data models and schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_processor.py  # PDF/DOCX text extraction
│   │   ├── ai_analyzer.py         # AI analysis and risk assessment
│   │   └── vector_store.py        # Chroma vector database management
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── upload.py      # Document upload interface
│   │   ├── analysis.py    # Document analysis dashboard
│   │   ├── qa_assistant.py # Interactive Q&A chat interface
│   │   ├── library.py     # Document library management
│   │   └── settings.py    # Application settings and configuration
│   └── utils/
│       ├── __init__.py
│       ├── config.py      # Environment configuration management
│       ├── logger.py      # Logging utilities and setup
│       └── helpers.py     # Common helper functions
├── sample/                # Sample legal documents for testing
│   ├── Employment_Offer_Letter.pdf
│   ├── Master_Services_Agreement.pdf
│   ├── Mutual_NDA.pdf
│   └── Residential_Lease_Agreement.pdf
├── data/                  # Local data storage and persistence
│   ├── app.log           # Application logs
│   └── chroma_db/        # Vector database storage
└── uploads/              # Temporary file uploads directory
```

## 🎯 Usage Guide

### 1. Document Upload & Processing

- Navigate to **📄 Upload** page
- Upload PDF, DOCX, or TXT files (max 10MB per file)
- Try the included sample documents for immediate testing
- Automatic document type detection and text extraction

### 2. Comprehensive Analysis Dashboard

Visit **📊 Analysis** to explore:

- **Risk Score Gauge**: Interactive 0-100 risk assessment with color coding
- **Side-by-Side Comparison**: Original text vs. simplified plain language
- **Risk Factor Breakdown**: Detailed explanations of identified risks with severity levels
- **Interactive Clause Highlighting**: Hover over highlighted text for tooltips with suggestions
- **Financial & Date Extraction**: Automatic identification of monetary amounts and key dates
- **Risk Visualization Charts**: Visual distribution of risk categories and severity

### 3. Interactive Q&A Assistant

- Use **💬 Q&A** for document-specific questions and analysis
- Get context-aware answers powered by vector similarity search
- Access suggested questions based on document type and content
- Chat history preservation for reference and record-keeping

### 4. Document Library Management

- **📚 Library** provides persistent storage of all analyzed documents
- Advanced filtering by document type, risk level, upload date
- Full-text search across document content and analysis results
- Quick re-analysis and direct access to Q&A for stored documents
- Document metadata and analysis summary views

### 5. Settings & Configuration

- **⚙️ Settings** for API key management and validation
- Application configuration and performance monitoring
- Usage statistics and system health information

## 🔧 Configuration Options

The application uses environment variables for configuration. All settings can be customized in the `.env` file based on the `.env.example` template.

### 🔑 Required Settings

| Variable         | Description                      | Example                       |
| ---------------- | -------------------------------- | ----------------------------- |
| `GOOGLE_API_KEY` | Google AI API key for Gemini Pro | `xyz` (from AI Studio) |

### ⚙️ Application Settings

| Variable                   | Default        | Description                        |
| -------------------------- | -------------- | ---------------------------------- |
| `DEBUG`                    | `True`         | Enable debug mode and verbose logs |
| `LOG_LEVEL`                | `INFO`         | Logging level (DEBUG/INFO/WARNING) |
| `STREAMLIT_SERVER_PORT`    | `8501`         | Port for Streamlit server          |
| `STREAMLIT_SERVER_ADDRESS` | `localhost`    | Server address binding             |
| `MAX_FILE_SIZE_MB`         | `10`           | Maximum upload file size           |
| `SUPPORTED_FILE_TYPES`     | `pdf,docx,txt` | Allowed file extensions            |

### 🤖 AI Model Settings

| Variable          | Default                | Description                      |
| ----------------- | ---------------------- | -------------------------------- |
| `TEMPERATURE`     | `0.2`                  | AI response creativity (0.0-1.0) |
| `MAX_TOKENS`      | `2048`                 | Maximum response length          |
| `EMBEDDING_MODEL` | `models/embedding-001` | Google AI embedding model        |

### 💾 Storage Configuration

| Variable                   | Default            | Description                  |
| -------------------------- | ------------------ | ---------------------------- |
| `CHROMA_PERSIST_DIRECTORY` | `./data/chroma_db` | Vector database storage path |
| `UPLOAD_DIR`               | `./uploads`        | Temporary file uploads       |
| `DATA_DIR`                 | `./data`           | Application data directory   |
| `LOG_FILE`                 | `./data/app.log`   | Application log file path    |

### 🔒 Security Settings

| Variable                  | Default | Description              |
| ------------------------- | ------- | ------------------------ |
| `SECRET_KEY`              | None    | Application secret key   |
| `SESSION_TIMEOUT_MINUTES` | `60`    | Session timeout duration |

### Example .env configuration:

```bash
# Required
GOOGLE_API_KEY=your-google-ai-api-key

# Optional (with defaults shown)
DEBUG=True
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=10
SUPPORTED_FILE_TYPES=pdf,docx,txt
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
TEMPERATURE=0.2
```

## � Sample Documents

The project includes professionally-crafted sample legal documents for testing and demonstration:

| Document Type                | Filename                          | Purpose                                  |
| ---------------------------- | --------------------------------- | ---------------------------------------- |
| **Employment Contract**      | `Employment_Offer_Letter.pdf`     | Test employment-related clause analysis  |
| **Service Agreement**        | `Master_Services_Agreement.pdf`   | Demonstrate commercial contract analysis |
| **Non-Disclosure Agreement** | `Mutual_NDA.pdf`                  | Show confidentiality clause assessment   |
| **Lease Agreement**          | `Residential_Lease_Agreement.pdf` | Test rental/property contract analysis   |

These documents are located in the `sample/` directory and can be uploaded directly through the application to:

- Experience the complete analysis workflow
- Test different document types and complexity levels
- Understand risk assessment capabilities
- Explore Q&A functionality with real legal content

## �🚨 Document Types Supported

Currently optimized for:

- **🏠 Rental/Lease Agreements**
- **💰 Loan Contracts**
- **💼 Employment Contracts**
- **🤝 Service Agreements**
- **🔒 Non-Disclosure Agreements (NDAs)**
- **📄 General Legal Documents**

## ⚡ Key Features Deep Dive

### 🔍 Advanced Risk Assessment Engine

- **Multi-dimensional Analysis**: Evaluates financial, legal commitment, and rights-related risks
- **Intelligent Severity Classification**: Categorizes risks as Low, Medium, High, or Critical
- **Contextual Risk Scoring**: Dynamic 0-100 scale based on document type and complexity
- **Actionable Recommendations**: Specific suggestions for improving problematic clauses

### 📝 AI-Powered Plain Language Translation

- **Context-Aware Simplification**: Maintains legal accuracy while improving readability
- **Jargon Definition System**: Interactive tooltips for complex legal terms
- **Document Type Optimization**: Tailored simplification based on contract category
- **Preservation of Legal Intent**: Ensures meaning is not lost in translation

### 🎯 Interactive Clause Analysis

- **Smart Highlighting System**: Visual identification of risky and important clauses
- **Hover Tooltips**: Immediate access to explanations and suggestions
- **Clause Categorization**: Organized by risk type and legal significance
- **Improvement Suggestions**: Specific recommendations for clause modifications

### 🔍 Vector-Powered Document Intelligence

- **Semantic Search**: Find similar clauses across your document library
- **Context-Aware Q&A**: Answers grounded in actual document content
- **Document Similarity**: Compare clauses against known patterns and standards
- **Persistent Knowledge Base**: Chroma vector database for fast, accurate retrieval

### 📊 Advanced Visualization & Analytics

- **Interactive Risk Gauges**: Real-time visual risk assessment
- **Risk Distribution Charts**: Breakdown of risk categories and severity
- **Financial Terms Extraction**: Automatic identification of monetary obligations
- **Timeline Analysis**: Key dates and deadline extraction with visualization

### 💾 Enterprise-Grade Data Management

- **Local Data Persistence**: Secure storage of documents and analysis results
- **Document Library**: Organized management with search and filtering
- **Analysis History**: Complete audit trail of document processing
- **Metadata Extraction**: Automatic tagging and categorization

## 🔒 Privacy & Security

### 🛡️ Data Protection

- **Local Processing**: Documents analyzed locally with secure API calls to Google AI
- **No Data Sharing**: Zero third-party data sharing or storage outside your environment
- **Secure Storage**: Vector embeddings and analysis results stored locally in Chroma database
- **Environment Security**: API keys managed through secure environment variables

### 🔐 Security Best Practices

- **API Key Protection**: Secure credential management with environment-based configuration
- **Local Vector Storage**: Document embeddings stored exclusively on your local system
- **Session Management**: Configurable session timeouts and secure state management
- **Input Validation**: Comprehensive file type and size validation for uploads

### 📋 Data Handling

- **Temporary Upload Storage**: Uploaded files processed and optionally removed from temp storage
- **Persistent Analysis**: Analysis results retained locally for document library functionality
- **User Control**: Complete control over data retention and deletion
- **Audit Trail**: Transparent logging of all document processing activities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

### 📚 Documentation & Resources

- **In-Code Documentation**: Comprehensive docstrings and code comments throughout the project
- **Configuration Guide**: Detailed environment setup and configuration options above
- **Sample Documents**: Use included sample contracts to understand features and capabilities

### 🐛 Issues & Bug Reports

- **GitHub Issues**: Report bugs, request features, or ask questions via [GitHub Issues](https://github.com/your-repo/Lega.AI/issues)
- **Bug Reports**: Include system info, error logs, and steps to reproduce
- **Feature Requests**: Describe use cases and expected functionality

### 🛠️ Development & API References

- **Google AI Documentation**: [Google AI Developer Guide](https://ai.google.dev/) for Gemini API details
- **LangChain Documentation**: [LangChain Docs](https://python.langchain.com/) for framework reference
- **Streamlit Documentation**: [Streamlit Docs](https://docs.streamlit.io/) for UI framework guidance
- **Chroma Documentation**: [Chroma Docs](https://docs.trychroma.com/) for vector database operations

### 💡 Getting Help

1. **Check Documentation**: Review this README and in-code comments first
2. **Try Sample Documents**: Use provided samples to test functionality
3. **Check Logs**: Review `data/app.log` for detailed error information
4. **Environment Issues**: Verify `.env` configuration and API key validity
5. **Community Support**: Open GitHub discussions for general questions

---

**Made with ❤️ using Streamlit, LangChain, and Google AI**
