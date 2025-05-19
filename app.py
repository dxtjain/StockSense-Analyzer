"""
Streamlit web application for the StockSense Analyzer platform.
Provides an interactive UI for stock data analysis.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from config import GROQ_API_KEY
from data_processor import load_stock_data, get_stock_statistics
from visualizer import (
    plot_sector_distribution,
    plot_price_distribution,
    plot_performance_by_sector,
    plot_top_stocks_by_price
)
import io
import sys

# Configure Streamlit page
st.set_page_config(
    page_title="StockSense Analyzer", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
    }
    .description {
        font-size: 1.1rem;
        color: #424242;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Main page header
st.markdown("<h1 class='main-header'>StockSense Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Professional stock market data analysis powered by Groq AI</p>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.image("https://img.icons8.com/fluency/96/financial-analytics.png", width=80)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Dashboard", "AI Analysis", "Data Explorer", "About"])

# Load stock data
try:
    df = load_stock_data()
    stats = get_stock_statistics(df)
except Exception as e:
    st.error(f"Error loading stock data: {e}")
    st.info("Please check the data file path in the configuration.")
    st.stop()

# Dashboard page
if page == "Dashboard":
    st.markdown("<h2 class='sub-header'>Market Overview</h2>", unsafe_allow_html=True)
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Stocks", f"{stats['total_stocks']}")
    with col2:
        st.metric("Average Price", f"${stats['average_price']:.2f}")
    with col3:
        st.metric("Highest Price", f"{stats['highest_price']}")
    with col4:
        st.metric("Avg Performance", f"{stats['avg_performance']:.2f}%")
    
    # Visualizations
    st.markdown("<h3>Market Visualizations</h3>", unsafe_allow_html=True)
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs(["Sector Distribution", "Price Distribution", "Performance by Sector", "Top Stocks"])
    
    with viz_tab1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sector_counts = df['Sector'].value_counts()
        ax.pie(sector_counts, labels=sector_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title('Stock Distribution by Sector')
        st.pyplot(fig)
    
    with viz_tab2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df['Price'], bins=20, kde=True, ax=ax)
        plt.title('Distribution of Stock Prices')
        plt.xlabel('Price ($)')
        plt.ylabel('Count')
        st.pyplot(fig)
    
    with viz_tab3:
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.boxplot(x='Sector', y='Performance (%)', data=df, ax=ax)
        plt.xticks(rotation=45, ha='right')
        plt.title('Stock Performance by Sector')
        plt.tight_layout()
        st.pyplot(fig)
    
    with viz_tab4:
        fig, ax = plt.subplots(figsize=(10, 6))
        top_n = df.nlargest(10, 'Price')
        sns.barplot(x='Stock Symbol', y='Price', data=top_n, ax=ax)
        plt.title('Top 10 Stocks by Price')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

# AI Analysis page
elif page == "AI Analysis":
    st.markdown("<h2 class='sub-header'>AI-Powered Stock Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p class='highlight'>Ask questions about the stock data in natural language. Our AI will analyze the data and provide insights.</p>", unsafe_allow_html=True)
    
    # Check if API key is available
    if not GROQ_API_KEY:
        st.warning("Groq API key is not configured. Please set it in the configuration.")
        st.info("For demo purposes, pre-computed analysis results will be shown.")
        st.markdown("### Sample Queries and Results")
        st.markdown("- **What is the stock price of AAPL?** The stock price of AAPL is $145.30.")
        st.markdown("- **What is the performance of TSLA?** The performance of TSLA is 5.0%.")
        st.markdown("- **What is the PE ratio of MSFT?** The P/E Ratio of MSFT is 35.6.")
        st.markdown("- **Which stock has the highest price?** The stock with the highest price is Amazon (AMZN) with a price of $3300.50.")
        st.stop()
    
    # User query input
    query = st.text_input("Enter your question about the stock data:", placeholder="e.g., What is the average P/E ratio of technology stocks?")
    
    if st.button("Analyze"):
        if query:
            with st.spinner("Analyzing data with AI..."):
                try:
                    # In a full implementation, this would connect to the analyzer.py module
                    # For now, we'll just look up some basic information from the DataFrame
                    
                    if "AAPL" in query and "price" in query.lower():
                        aapl_price = df[df['Stock Symbol'] == 'AAPL']['Price'].values[0]
                        response = f"The stock price of AAPL is ${aapl_price}"
                    elif "TSLA" in query and "performance" in query.lower():
                        tsla_perf = df[df['Stock Symbol'] == 'TSLA']['Performance (%)'].values[0]
                        response = f"The performance of TSLA is {tsla_perf}%"
                    elif "MSFT" in query and "PE" in query:
                        msft_pe = df[df['Stock Symbol'] == 'MSFT']['P/E Ratio'].values[0]
                        response = f"The P/E Ratio of MSFT is {msft_pe}"
                    elif "highest price" in query.lower():
                        highest = df.loc[df['Price'].idxmax()]
                        response = f"The stock with the highest price is {highest['Stock Name']} ({highest['Stock Symbol']}) with a price of ${highest['Price']}"
                    elif "average" in query.lower() and "price" in query.lower():
                        avg_price = df['Price'].mean()
                        response = f"The average stock price is ${avg_price:.2f}"
                    else:
                        response = "I don't have enough information to answer that specific question in the demo mode. In the full version, this would use the Groq LLM to provide detailed analysis."
                    
                    st.success("Analysis Complete")
                    st.markdown(f"<div class='highlight'><strong>Query:</strong> {query}<br><strong>Response:</strong> {response}</div>", unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error analyzing data: {e}")
        else:
            st.warning("Please enter a query to analyze.")

# Data Explorer page
elif page == "Data Explorer":
    st.markdown("<h2 class='sub-header'>Stock Data Explorer</h2>", unsafe_allow_html=True)
    
    # Data filter options
    st.sidebar.markdown("### Filters")
    sectors = ["All"] + sorted(df["Sector"].unique().tolist())
    selected_sector = st.sidebar.selectbox("Select Sector", sectors)
    
    min_price, max_price = float(df["Price"].min()), float(df["Price"].max())
    price_range = st.sidebar.slider("Price Range ($)", min_price, max_price, (min_price, max_price))
    
    # Apply filters
    filtered_df = df.copy()
    if selected_sector != "All":
        filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]
    filtered_df = filtered_df[(filtered_df["Price"] >= price_range[0]) & (filtered_df["Price"] <= price_range[1])]
    
    # Show data
    st.markdown(f"<p>Showing {len(filtered_df)} stocks</p>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download option
    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_stock_data.csv",
        mime="text/csv",
    )

# About page
else:
    st.markdown("<h2 class='sub-header'>About StockSense Analyzer</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='description'>
    <p>StockSense Analyzer is a professional stock market analysis platform designed to provide powerful insights through AI-powered natural language queries and interactive visualizations.</p>
    
    <h3>Core Features</h3>
    <ul>
        <li><strong>Natural Language Queries:</strong> Ask questions about stock data in plain English</li>
        <li><strong>Data Visualization:</strong> Interactive charts and graphs for stock analysis</li>
        <li><strong>Real-time Analysis:</strong> Get immediate responses to your financial queries</li>
        <li><strong>Data Exploration:</strong> Filter and explore the underlying stock data</li>
    </ul>
    
    <h3>Technologies Used</h3>
    <ul>
        <li>Python (Data Science & Web Stack)</li>
        <li>LangChain for AI integration</li>
        <li>Groq LLM for natural language processing</li>
        <li>Pandas for data manipulation</li>
        <li>Matplotlib & Seaborn for visualizations</li>
        <li>Streamlit for the web interface</li>
    </ul>
    
    <p>This platform is designed for investors, analysts, and financial professionals looking to gain rapid insights from stock market data using advanced AI.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>StockSense Analyzer © 2024 | Powered by Streamlit & Groq AI</p>", unsafe_allow_html=True) 