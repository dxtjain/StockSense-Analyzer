"""
Data visualization module for the Stock Analysis project.
Provides functions for creating charts and visualizations of stock data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_sector_distribution(df, save_path=None):
    """
    Create a pie chart showing distribution of stocks by sector.
    
    Args:
        df (pandas.DataFrame): Stock data
        save_path (str, optional): Path to save the plot. If None, plot is displayed.
    """
    plt.figure(figsize=(12, 8))
    sector_counts = df['Sector'].value_counts()
    plt.pie(sector_counts, labels=sector_counts.index, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Stock Distribution by Sector')
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Sector distribution plot saved to: {save_path}")
    else:
        plt.show()

def plot_price_distribution(df, save_path=None):
    """
    Create a histogram showing the distribution of stock prices.
    
    Args:
        df (pandas.DataFrame): Stock data
        save_path (str, optional): Path to save the plot. If None, plot is displayed.
    """
    plt.figure(figsize=(12, 6))
    sns.histplot(df['Price'], bins=20, kde=True)
    plt.title('Distribution of Stock Prices')
    plt.xlabel('Price ($)')
    plt.ylabel('Count')
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Price distribution plot saved to: {save_path}")
    else:
        plt.show()

def plot_performance_by_sector(df, save_path=None):
    """
    Create a box plot showing performance by sector.
    
    Args:
        df (pandas.DataFrame): Stock data
        save_path (str, optional): Path to save the plot. If None, plot is displayed.
    """
    plt.figure(figsize=(14, 8))
    sns.boxplot(x='Sector', y='Performance (%)', data=df)
    plt.xticks(rotation=45, ha='right')
    plt.title('Stock Performance by Sector')
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Performance by sector plot saved to: {save_path}")
    else:
        plt.show()

def plot_top_stocks_by_price(df, n=10, save_path=None):
    """
    Create a bar chart showing the top N stocks by price.
    
    Args:
        df (pandas.DataFrame): Stock data
        n (int): Number of top stocks to display
        save_path (str, optional): Path to save the plot. If None, plot is displayed.
    """
    top_n = df.nlargest(n, 'Price')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Stock Symbol', y='Price', data=top_n)
    plt.title(f'Top {n} Stocks by Price')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Top stocks plot saved to: {save_path}")
    else:
        plt.show() 