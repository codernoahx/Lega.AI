# Hugging Face Spaces Deployment Guide for Lega.AI

## 🚀 Quick Deployment to Hugging Face Spaces

### Step 1: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **Space name**: `lega-ai` (or your preferred name)
   - **License**: `MIT`
   - **SDK**: `Docker`
   - **Hardware**: `CPU basic` (sufficient for this app)

### Step 2: Upload the Code

1. Clone or download this repository
2. Upload all files to your Hugging Face Space repository
3. Ensure the `README.md` has the correct frontmatter:
   ```yaml
   ---
   title: Lega.AI
   emoji: ⚖️
   colorFrom: pink
   colorTo: indigo
   sdk: docker
   pinned: false
   ---
   ```

### Step 3: Configure Environment Variables

1. In your Space, go to **Settings** → **Variables**
2. Add the required environment variable:
   - **Name**: `GOOGLE_API_KEY`
   - **Value**: Your Google AI API key from [Google AI Studio](https://aistudio.google.com/)

### Step 4: Deploy

1. Commit and push your changes to the Space repository
2. Hugging Face will automatically build and deploy your Docker container
3. Wait for the build to complete (usually 5-10 minutes)
4. Your app will be available at `https://huggingface.co/spaces/[username]/[space-name]`

## 🔧 Customization Options

### Environment Variables You Can Set:

- `GOOGLE_API_KEY` (required)
- `MAX_FILE_SIZE_MB` (default: 5)
- `TEMPERATURE` (default: 0.2)
- `LOG_LEVEL` (default: INFO)

### Hardware Requirements:

- **CPU Basic**: Sufficient for most use cases
- **CPU Upgrade**: Recommended for heavy usage
- **GPU**: Not required for this application

## 📋 Troubleshooting

### Common Issues:

1. **Build fails**: Check that all files are uploaded correctly
2. **API errors**: Ensure `GOOGLE_API_KEY` is set correctly
3. **Timeout**: Consider upgrading to CPU Upgrade hardware

### Logs:

- Check the Space logs in the Hugging Face interface
- Look for startup messages and error information

## 🔒 Security Considerations

- Never commit your API key to the repository
- Use Hugging Face Spaces environment variables for sensitive data
- The application runs in a sandboxed environment on Hugging Face

## 📊 Usage Limits

- Hugging Face Spaces has usage limits for free tiers
- Consider upgrading for production use
- Monitor usage in your Hugging Face account dashboard
