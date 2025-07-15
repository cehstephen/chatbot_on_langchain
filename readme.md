# LangChain Anthropic Chatbot Setup Guide

## Overview
This chatbot implementation uses LangChain with Anthropic's Claude API to create a conversational AI assistant. It includes both a Streamlit web interface and a command-line interface.

## Features
- **Multiple Interface Options**: Web UI (Streamlit) and CLI
- **Configurable Settings**: Model selection, temperature, max tokens, system prompt
- **Chat History Management**: Persistent conversation context
- **Error Handling**: Robust error handling and user feedback
- **Multiple Claude Models**: Support for Claude 3 Sonnet, Opus, and Haiku

## Requirements

### Python Dependencies
Create a `requirements.txt` file:

```txt
langchain==0.1.0
langchain-anthropic==0.1.0
langchain-core==0.1.0
langchain-community==0.0.13
streamlit==1.29.0
anthropic==0.8.0
python-dotenv==1.0.0
```

### Installation Commands

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Setup Instructions

### 1. Get Anthropic API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (keep it secure!)

### 2. Environment Configuration

Create a `.env` file in your project directory:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Running the Application

#### Option A: Streamlit Web Interface
```bash
streamlit run chatbot.py
```

#### Option B: Command Line Interface
```bash
python chatbot.py
```

## Usage Guide

### Web Interface (Streamlit)
1. Enter your Anthropic API key in the sidebar
2. Configure model settings (optional)
3. Start chatting in the main interface
4. Use "Clear Chat History" to reset conversation

### CLI Interface
- Type your messages and press Enter
- Use `quit` to exit
- Use `clear` to clear chat history

## Configuration Options

### Model Selection
- **claude-3-sonnet-20240229**: Balanced performance and speed
- **claude-3-opus-20240229**: Highest capability model
- **claude-3-haiku-20240307**: Fastest and most cost-effective

### Parameters
- **Temperature** (0.0-1.0): Controls response randomness
- **Max Tokens** (100-4000): Maximum response length
- **System Prompt**: Defines chatbot personality and behavior

## Advanced Usage

### Custom System Prompts
Modify the system prompt to create specialized chatbots:

```python
# Example: Technical Support Bot
system_prompt = """You are a technical support specialist. You help users troubleshoot software and hardware issues. Always ask clarifying questions and provide step-by-step solutions."""

# Example: Creative Writing Assistant
system_prompt = """You are a creative writing assistant. You help users brainstorm ideas, improve their writing, and overcome writer's block. Be encouraging and provide constructive feedback."""
```

### Integration with Other Systems
The chatbot can be integrated into other applications:

```python
from chatbot import AnthropicChatbot, ChatbotConfig

# Initialize chatbot
config = ChatbotConfig()
chatbot = AnthropicChatbot(config)

# Get response
response = chatbot.get_response("Hello, how are you?")
print(response)
```

## Error Handling

Common issues and solutions:

### API Key Issues
- **Error**: "ANTHROPIC_API_KEY environment variable is required"
- **Solution**: Ensure API key is set in environment or .env file

### Rate Limiting
- **Error**: API rate limit exceeded
- **Solution**: Implement exponential backoff or reduce request frequency

### Model Availability
- **Error**: Model not available
- **Solution**: Check model name and availability in Anthropic console

## File Structure

```
langchain-anthropic-chatbot/
├── chatbot.py              # Main chatbot implementation
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── README.md              # This file
└── .gitignore             # Git ignore file
```

## Security Best Practices

1. **Never commit API keys**: Use environment variables or .env files
2. **Validate inputs**: Sanitize user inputs to prevent injection attacks
3. **Rate limiting**: Implement rate limiting for production use
4. **Error handling**: Don't expose sensitive information in error messages

## Deployment Options

### Local Development
Use the provided Streamlit interface for local development and testing.

### Production Deployment
For production deployment, consider:
- Using a proper web framework (FastAPI, Flask)
- Implementing authentication and authorization
- Adding logging and monitoring
- Using containerization (Docker)
- Implementing proper error handling and recovery

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade langchain langchain-anthropic
   ```

2. **Streamlit Not Starting**
   ```bash
   pip install streamlit
   streamlit --version
   ```

3. **API Connection Issues**
   - Check internet connection
   - Verify API key is correct
   - Check Anthropic service status

### Debug Mode
Enable debug mode for detailed error information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review Anthropic API documentation
- Check LangChain documentation
- Create an issue in the project repository
