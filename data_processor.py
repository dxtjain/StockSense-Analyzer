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
    Tries multiple possible file locations to improve deployment compatibility.
    
    Returns:
        pandas.DataFrame: Cleaned stock data
    """
    # Try multiple possible file locations
    possible_paths = [
        DATA_FILE,
        "data/stocks.csv",
        "stocks.csv",
        "sample.csv"
    ]
    
    df = None
    errors = []
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                df = pd.read_csv(path)
                print(f"Successfully loaded data from {path}")
                break
        except Exception as e:
            errors.append(f"Error loading {path}: {str(e)}")
    
    if df is None:
        error_msg = "\n".join(errors)
        raise FileNotFoundError(f"Could not find or load stock data file. Tried: {possible_paths}. Errors: {error_msg}")
    
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