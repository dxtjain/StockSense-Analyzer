"""
Configuration module for the Stock Analysis project.
Loads environment variables and provides configuration settings.
"""

import os
from dotenv import load_dotenv
import streamlit as st

# Try to load environment variables from .env file
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

# API Configuration - Try to get from Streamlit secrets first, then environment
try:
    # Check if running in Streamlit Cloud
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
except Exception:
    # Fallback to environment variable
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# File paths
DATA_FILE = os.getenv("CSV_FILE_PATH", "data/stocks.csv")
RESULTS_FILE = os.getenv("RESULTS_FILE_PATH", "results/analysis_results.csv")

# Default model settings
MODEL_TEMPERATURE = 0.5

# Define standard queries
STANDARD_QUERIES = [
    "What is the stock price of AAPL?",
    "What is the performance of TSLA?",
    "What is the PE ratio of MSFT?",
    "Which stock has the highest price?",
    "What is the average stock price?",
    "Which sector has the most stocks?",
    "What is the market cap of AMZN?",
    "Which technology stock has the lowest P/E ratio?",
] 