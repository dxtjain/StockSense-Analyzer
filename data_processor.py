"""
Data processor module for the Stock Analysis project.
Handles loading, cleaning, and processing stock data.
"""

import pandas as pd
import os
from config import DATA_FILE, RESULTS_FILE

def load_stock_data():
    """
    Load stock data from CSV file and perform basic cleaning.
    
    Returns:
        pandas.DataFrame: Cleaned stock data
    """
    # Check if file exists
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Stock data file not found: {DATA_FILE}")
    
    # Load data
    df = pd.read_csv(DATA_FILE)
    
    # Basic cleaning
    # Remove duplicate rows based on Stock Symbol
    df = df.drop_duplicates(subset=['Stock Symbol'])
    
    return df

def save_analysis_results(results_df):
    """
    Save analysis results to CSV file.
    
    Args:
        results_df (pandas.DataFrame): DataFrame containing analysis results
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    
    # Save results
    results_df.to_csv(RESULTS_FILE, index=False)
    print(f"Analysis results saved to {RESULTS_FILE}")
    
    return RESULTS_FILE

def get_stock_statistics(df):
    """
    Calculate basic statistics for the stock data.
    
    Args:
        df (pandas.DataFrame): Stock data
        
    Returns:
        dict: Dictionary containing statistics
    """
    stats = {
        'total_stocks': len(df),
        'average_price': df['Price'].mean(),
        'highest_price': df.loc[df['Price'].idxmax()]['Stock Symbol'],
        'highest_pe': df.loc[df['P/E Ratio'].idxmax()]['Stock Symbol'],
        'sectors': df['Sector'].value_counts().to_dict(),
        'avg_performance': df['Performance (%)'].mean()
    }
    
    return stats 