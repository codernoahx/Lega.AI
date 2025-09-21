#!/bin/bash

# Hugging Face Spaces startup script for Lega.AI

echo "🚀 Starting Lega.AI on Hugging Face Spaces..."

# Create necessary directories if they don't exist
mkdir -p data/chroma_db
mkdir -p uploads
mkdir -p .streamlit

# Set default environment variables for Hugging Face deployment
export STREAMLIT_SERVER_PORT=${PORT:-7860}
export STREAMLIT_SERVER_ADDRESS="0.0.0.0"
export DEBUG=False
export LOG_LEVEL=INFO
export STREAMLIT_CONFIG_DIR=/app/.streamlit
export XDG_CONFIG_HOME=/app

# Check if GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  WARNING: GOOGLE_API_KEY environment variable is not set!"
    echo "Please set it in your Hugging Face Space settings for the app to work properly."
fi

# Start the Streamlit application
echo "🌐 Starting Streamlit on port $STREAMLIT_SERVER_PORT..."
exec streamlit run main.py \
    --server.port=$STREAMLIT_SERVER_PORT \
    --server.address=$STREAMLIT_SERVER_ADDRESS \
    --server.headless=true \
    --server.fileWatcherType=none \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false