# LangChain Anthropic Chatbot
# A comprehensive chatbot implementation using LangChain with Anthropic's Claude API

import os
from typing import List, Dict, Any
import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import asyncio

# Configuration
class ChatbotConfig:
    """Configuration settings for the chatbot"""
    def __init__(self):
        self.model_name = "claude-3-sonnet-20240229"  # or "claude-3-opus-20240229"
        self.temperature = 0.7
        self.max_tokens = 1000
        self.system_prompt = """You are a helpful AI assistant. You are knowledgeable, friendly, and aim to provide accurate and helpful responses. You can engage in conversations on a wide variety of topics."""

# Initialize the chatbot
class AnthropicChatbot:
    def __init__(self, config: ChatbotConfig):
        self.config = config
        self.setup_llm()
        self.setup_prompt_template()
        self.setup_chain()
    
    def setup_llm(self):
        """Initialize the Anthropic LLM"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.llm = ChatAnthropic(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            anthropic_api_key=api_key
        )
    
    def setup_prompt_template(self):
        """Setup the prompt template with system message and chat history"""
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.config.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
    
    def setup_chain(self):
        """Setup the LangChain chain"""
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def get_response(self, user_input: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Get response from the chatbot"""
        if chat_history is None:
            chat_history = []
        
        # Convert chat history to LangChain message format
        messages = []
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        response = self.chain.invoke({
            "input": user_input,
            "chat_history": messages
        })
        
        return response

# Streamlit UI
def main():
    st.set_page_config(
        page_title="LangChain Anthropic Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 LangChain Anthropic Chatbot")
    st.markdown("A chatbot powered by LangChain and Anthropic's Claude API")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            help="Enter your Anthropic API key"
        )
        
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key
        
        # Model selection
        model_choice = st.selectbox(
            "Select Model",
            ["claude-3-sonnet-20240229", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
            help="Choose the Claude model to use"
        )
        
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Controls randomness in responses"
        )
        
        # Max tokens
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=1000,
            help="Maximum number of tokens in response"
        )
        
        # System prompt
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful AI assistant. You are knowledgeable, friendly, and aim to provide accurate and helpful responses.",
            height=100,
            help="Define the chatbot's personality and behavior"
        )
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chatbot
    if api_key:
        try:
            config = ChatbotConfig()
            config.model_name = model_choice
            config.temperature = temperature
            config.max_tokens = max_tokens
            config.system_prompt = system_prompt
            
            chatbot = AnthropicChatbot(config)
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Display chat history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("What would you like to know?"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Get bot response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            response = chatbot.get_response(prompt, st.session_state.messages[:-1])
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
        except Exception as e:
            st.error(f"Failed to initialize chatbot: {str(e)}")
            st.info("Please check your API key and try again.")
    else:
        st.warning("Please enter your Anthropic API key in the sidebar to start chatting.")
        st.info("""
        To get started:
        1. Get your API key from https://console.anthropic.com/
        2. Enter it in the sidebar
        3. Start chatting!
        """)

# Command-line interface version
class CLIChatbot:
    def __init__(self):
        self.config = ChatbotConfig()
        self.chatbot = AnthropicChatbot(self.config)
        self.chat_history = []
    
    def run(self):
        """Run the CLI version of the chatbot"""
        print("🤖 LangChain Anthropic Chatbot")
        print("Type 'quit' to exit, 'clear' to clear history")
        print("-" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'clear':
                self.chat_history = []
                print("Chat history cleared.")
                continue
            elif not user_input:
                continue
            
            try:
                response = self.chatbot.get_response(user_input, self.chat_history)
                print(f"\nAssistant: {response}")
                
                # Update chat history
                self.chat_history.append({"role": "user", "content": user_input})
                self.chat_history.append({"role": "assistant", "content": response})
                
            except Exception as e:
                print(f"Error: {str(e)}")

# Advanced features
class AdvancedChatbot(AnthropicChatbot):
    """Extended chatbot with additional features"""
    
    def __init__(self, config: ChatbotConfig):
        super().__init__(config)
        self.setup_advanced_features()
    
    def setup_advanced_features(self):
        """Setup advanced features like memory and tools"""
        # You can add more advanced features here
        pass
    
    def get_response_with_sources(self, user_input: str, chat_history: List[Dict[str, str]] = None):
        """Get response with source information"""
        response = self.get_response(user_input, chat_history)
        
        # Add metadata or source information
        metadata = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "timestamp": "2024-01-15T10:30:00Z"  # You'd use actual timestamp
        }
        
        return {
            "response": response,
            "metadata": metadata
        }

if __name__ == "__main__":
    # Check if running in Streamlit
    try:
        import streamlit as st
        # If we can import streamlit and it's running, use Streamlit UI
        main()
    except ImportError:
        # If streamlit is not available, use CLI
        print("Streamlit not available. Using CLI version.")
        cli_bot = CLIChatbot()
        cli_bot.run()
    except Exception:
        # Fallback to CLI if there are any issues with Streamlit
        cli_bot = CLIChatbot()
        cli_bot.run()
