#!/usr/bin/env python3
"""
Lega.AI Setup Script
===================
Interactive setup script to help configure your Lega.AI environment.
"""

import os
import sys
from pathlib import Path


def main():
    print("🚀 Welcome to Lega.AI Setup!")
    print("=" * 50)
    print()

    # Check if .env exists
    env_file = Path(".env")
    if env_file.exists():
        print("📋 Found existing .env file")
        overwrite = input("Do you want to update it? (y/N): ").lower().strip()
        if overwrite != "y":
            print("Setup cancelled.")
            return
    else:
        print("📋 Creating new .env file...")

    # Copy from template
    template_file = Path(".env.example")
    if not template_file.exists():
        print("❌ .env.example template not found!")
        return

    # Get API key from user
    print()
    print("🔑 Google AI API Key Setup")
    print("-" * 30)
    print("Get your API key from: https://makersuite.google.com/app/apikey")
    print()

    api_key = input("Enter your Google AI API key: ").strip()

    if not api_key:
        print("❌ No API key provided. You can add it later to the .env file.")
        api_key = "your_google_ai_api_key_here"
    else:
        print("✅ API key received")

    # Read template and replace API key
    with open(template_file, "r") as f:
        content = f.read()

    # Replace the API key placeholder
    content = content.replace(
        "GOOGLE_API_KEY=your-google-api-key-here", f"GOOGLE_API_KEY={api_key}"
    )

    # Write to .env
    with open(env_file, "w") as f:
        f.write(content)

    print()
    print("✅ Environment file created successfully!")
    print()

    # Optional configuration
    print("⚙️  Optional Configuration")
    print("-" * 25)

    # File size limit
    max_size = input("Maximum file size in MB (default: 10): ").strip()
    if max_size and max_size.isdigit():
        content = content.replace("MAX_FILE_SIZE_MB=10", f"MAX_FILE_SIZE_MB={max_size}")

    # Risk sensitivity
    print()
    print("Risk sensitivity (1-5, where 5 is most sensitive):")
    risk_sens = input("Enter risk sensitivity (default: 3): ").strip()
    if risk_sens and risk_sens.isdigit() and 1 <= int(risk_sens) <= 5:
        content = content.replace("RISK_SENSITIVITY=3", f"RISK_SENSITIVITY={risk_sens}")

    # Write updated content
    with open(env_file, "w") as f:
        f.write(content)

    print()
    print("🎉 Setup Complete!")
    print("=" * 20)
    print()
    print("Next steps:")
    print(
        "1. Install dependencies: uv add streamlit 'langchain[google-genai]' langchain-google-genai langchain-chroma"
    )
    print("2. Run the application: streamlit run main.py")
    print("3. Open your browser to: http://localhost:8501")
    print()
    print("Need help? Check the README.md file for detailed instructions.")


if __name__ == "__main__":
    main()
