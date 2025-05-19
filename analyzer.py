"""
Stock analyzer module using LangChain and Groq.
Provides natural language querying capabilities for stock data.
"""

import os
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL_TEMPERATURE, STANDARD_QUERIES
from data_processor import load_stock_data, save_analysis_results

class StockAnalyzer:
    """
    Stock analyzer using LangChain and Groq LLM.
    Provides natural language interface for stock data analysis.
    """
    
    def __init__(self, data_file, api_key=None, temperature=None):
        """
        Initialize the stock analyzer.
        
        Args:
            data_file (str): Path to the stock data CSV file
            api_key (str, optional): Groq API key. Defaults to config value.
            temperature (float, optional): Model temperature. Defaults to config value.
        """
        self.data_file = data_file
        self.api_key = api_key or GROQ_API_KEY
        self.temperature = temperature or MODEL_TEMPERATURE
        
        # Check for API key
        if not self.api_key:
            raise ValueError("Groq API key is required. Set it in .env file or pass directly.")
        
        # Set up LLM
        self.llm = ChatGroq(
            api_key=self.api_key,
            temperature=self.temperature
        )
        
        # Create agent
        self.agent = create_csv_agent(
            self.llm,
            self.data_file,
            verbose=True,
            allow_dangerous_code=True
        )
    
    def analyze(self, query):
        """
        Analyze stock data with a natural language query.
        
        Args:
            query (str): Natural language query
            
        Returns:
            dict: Response from the agent
        """
        try:
            response = self.agent.invoke(query)
            return {
                "query": query,
                "response": response["output"]
            }
        except Exception as e:
            return {
                "query": query,
                "response": f"Error: {str(e)}"
            }
    
    def run_standard_queries(self):
        """
        Run standard predefined queries and return results.
        
        Returns:
            pandas.DataFrame: Results of standard queries
        """
        results = []
        for query in STANDARD_QUERIES:
            print(f"Running query: {query}")
            result = self.analyze(query)
            results.append(result)
        
        return pd.DataFrame(results)
    
    def run_custom_queries(self, queries):
        """
        Run custom queries provided by the user.
        
        Args:
            queries (list): List of query strings
            
        Returns:
            pandas.DataFrame: Results of custom queries
        """
        results = []
        for query in queries:
            print(f"Running query: {query}")
            result = self.analyze(query)
            results.append(result)
        
        return pd.DataFrame(results) 