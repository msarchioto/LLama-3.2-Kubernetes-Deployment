from pathlib import Path

# Model Configuration
MODEL_PATH = Path("meta-llama/Llama-3.2-1B-Instruct")
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7
TOP_P = 0.95

# API Configuration
HOST = "0.0.0.0"
PORT = 8000

# System prompt for the chatbot
SYSTEM_PROMPT = """You are a helpful and friendly AI assistant. 
You aim to provide accurate and helpful responses while maintaining a conversational tone.
You should be direct in your responses and acknowledge when you're not sure about something."""

# Memory Configuration
MAX_HISTORY_LENGTH = 5  # Number of conversation turns to remember 