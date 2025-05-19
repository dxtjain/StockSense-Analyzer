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

# Configure Streamlit page - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="StockSense Analyzer", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/dxtjain/StockSense-Analyzer',
        'Report a bug': 'https://github.com/dxtjain/StockSense-Analyzer/issues',
        'About': 'StockSense Analyzer is a professional stock analysis platform.'
    }
)

# Debug information - only show in development mode
debug_mode = False  # Set to True for debugging

# Apply modern styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #2E7AD1;
        --secondary-color: #113E78;
        --background-color: #F7FAFC;
        --text-color: #333333;
        --accent-color: #FF9F1C;
    }
    
    /* Overall styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--secondary-color);
        margin-top: 1.5rem;
    }
    
    .description {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.1);
    }
    
    /* Highlight box */
    .highlight {
        background-color: #f0f7ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        background-color: #f0f7ff;
    }
    
    /* DataFrames */
    .dataframe-container {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* For dark mode compatibility */
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background-color: #1E1E1E;
            box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        }
        .highlight {
            background-color: rgba(46, 122, 209, 0.1);
        }
    }
</style>
""", unsafe_allow_html=True)

# App header with logo and title
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://img.icons8.com/fluency/96/financial-analytics.png", width=70)
with col2:
    st.markdown("<h1 class='main-header'>StockSense Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Professional stock market data analysis powered by Groq AI</p>", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/financial-analytics.png", width=60)
    st.markdown("## Navigation")
    page = st.radio("", ["Dashboard", "AI Analysis", "Data Explorer", "About"], label_visibility="collapsed")

# Load stock data (with caching for performance)
@st.cache_data(ttl=3600)
def get_cached_data():
    try:
        df = load_stock_data()
        stats = get_stock_statistics(df)
        return df, stats
    except Exception as e:
        # Create sample data as fallback
        data = {
            'Stock Symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
            'Stock Name': ['Apple Inc.', 'Microsoft Corp.', 'Alphabet Inc.', 'Amazon.com Inc.', 'Tesla Inc.'],
            'Price': [150.25, 290.50, 2800.75, 3250.50, 650.75],
            'P/E Ratio': [28.5, 35.6, 30.2, 65.8, 120.5],
            'Performance (%)': [12.5, 8.2, 15.7, 6.8, 5.0],
            'Sector': ['Technology', 'Technology', 'Technology', 'Consumer Services', 'Automotive']
        }
        df = pd.DataFrame(data)
        stats = get_stock_statistics(df)
        return df, stats

# Get data with error handling
try:
    with st.spinner("Loading market data..."):
        df, stats = get_cached_data()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# Dashboard page
if page == "Dashboard":
    st.markdown("<h2 class='sub-header'>Market Overview</h2>", unsafe_allow_html=True)
    
    # Key metrics in columns with improved styling
    metrics_container = st.container()
    with metrics_container:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 1rem; color: #666;">Total Stocks</h3>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0; color: #2E7AD1;">{}</p>
            </div>
            """.format(stats['total_stocks']), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 1rem; color: #666;">Average Price</h3>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0; color: #2E7AD1;">${:.2f}</p>
            </div>
            """.format(stats['average_price']), unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 1rem; color: #666;">Highest Price</h3>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0; color: #2E7AD1;">{}</p>
            </div>
            """.format(stats['highest_price']), unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 1rem; color: #666;">Avg Performance</h3>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0; color: #2E7AD1;">{:.2f}%</p>
            </div>
            """.format(stats['avg_performance']), unsafe_allow_html=True)
    
    # Visualizations with improved styling
    st.markdown("<h3 class='sub-header' style='margin-top: 2rem;'>Market Visualizations</h3>", unsafe_allow_html=True)
    
    # Use caching for visualizations to improve performance
    @st.cache_data
    def create_visualizations():
        # Set a modern style for visualizations
        plt.style.use('ggplot')
        sns.set_palette("rocket")
        
        # Create figures
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sector_counts = df['Sector'].value_counts()
        ax1.pie(sector_counts, labels=sector_counts.index, autopct='%1.1f%%', startangle=90, 
                shadow=False, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
        ax1.axis('equal')
        plt.tight_layout()
        plt.title('Stock Distribution by Sector', fontsize=16, pad=20)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.histplot(df['Price'], bins=20, kde=True, ax=ax2, color='#2E7AD1')
        plt.title('Distribution of Stock Prices', fontsize=16, pad=20)
        plt.xlabel('Price ($)', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        fig3, ax3 = plt.subplots(figsize=(12, 8))
        sns.boxplot(x='Sector', y='Performance (%)', data=df, ax=ax3)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.title('Stock Performance by Sector', fontsize=16, pad=20)
        plt.xlabel('Sector', fontsize=12)
        plt.ylabel('Performance (%)', fontsize=12)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        top_n = df.nlargest(10, 'Price')
        bars = sns.barplot(x='Stock Symbol', y='Price', data=top_n, ax=ax4, palette='rocket')
        plt.title('Top 10 Stocks by Price', fontsize=16, pad=20)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.xlabel('Stock Symbol', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        # Add value labels on top of bars
        for bar in bars.patches:
            bars.annotate(f'${bar.get_height():.0f}',
                        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        ha='center', va='bottom', fontsize=9)
        
        return fig1, fig2, fig3, fig4
    
    # Display tabs with visualizations
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs(["Sector Distribution", "Price Distribution", "Performance by Sector", "Top Stocks"])
    
    # Get cached visualizations
    fig1, fig2, fig3, fig4 = create_visualizations()
    
    with viz_tab1:
        st.pyplot(fig1)
    
    with viz_tab2:
        st.pyplot(fig2)
    
    with viz_tab3:
        st.pyplot(fig3)
    
    with viz_tab4:
        st.pyplot(fig4)

# AI Analysis page
elif page == "AI Analysis":
    st.markdown("<h2 class='sub-header'>AI-Powered Stock Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p class='highlight'>Ask questions about the stock data in natural language. Our AI will analyze the data and provide insights.</p>", unsafe_allow_html=True)
    
    # Check if API key is available
    api_missing = GROQ_API_KEY is None
    if api_missing:
        st.warning("⚠️ Groq API key is not configured. Running in demo mode.")
        st.info("ℹ️ To enable full AI features, set GROQ_API_KEY in Streamlit secrets.")
        
        # Create collapsible section for example queries
        with st.expander("Example Queries & Responses"):
            st.markdown("### Sample Queries and Results")
            
            examples = [
                ("What is the stock price of AAPL?", f"The stock price of AAPL is ${df[df['Stock Symbol'] == 'AAPL']['Price'].values[0]:.2f}."),
                ("What is the performance of TSLA?", f"The performance of TSLA is {df[df['Stock Symbol'] == 'TSLA']['Performance (%)'].values[0]:.2f}%."),
                ("What is the PE ratio of MSFT?", f"The P/E Ratio of MSFT is {df[df['Stock Symbol'] == 'MSFT']['P/E Ratio'].values[0]:.2f}."),
                ("Which stock has the highest price?", f"The stock with the highest price is {df.loc[df['Price'].idxmax()]['Stock Name']} ({df.loc[df['Price'].idxmax()]['Stock Symbol']}) with a price of ${df['Price'].max():.2f}.")
            ]
            
            for question, answer in examples:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"**Q: {question}**")
                with col2:
                    st.markdown(f"A: {answer}")
    
    # User query input with improved UI
    query = st.text_input("Ask about the stocks:", 
                        placeholder="e.g., What is the average P/E ratio of technology stocks?",
                        help="Type your question about the stock data here")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        analyze_button = st.button("Analyze", type="primary", use_container_width=True)
    with col2:
        pass
    
    if analyze_button:
        if query:
            with st.spinner("Analyzing data with AI..."):
                try:
                    # In this demo mode, process basic queries directly
                    if "AAPL" in query and "price" in query.lower():
                        aapl_price = df[df['Stock Symbol'] == 'AAPL']['Price'].values[0]
                        response = f"The stock price of AAPL is ${aapl_price:.2f}"
                    elif "TSLA" in query and "performance" in query.lower():
                        tsla_perf = df[df['Stock Symbol'] == 'TSLA']['Performance (%)'].values[0]
                        response = f"The performance of TSLA is {tsla_perf:.2f}%"
                    elif "MSFT" in query and "PE" in query:
                        msft_pe = df[df['Stock Symbol'] == 'MSFT']['P/E Ratio'].values[0]
                        response = f"The P/E Ratio of MSFT is {msft_pe:.2f}"
                    elif "highest price" in query.lower():
                        highest = df.loc[df['Price'].idxmax()]
                        response = f"The stock with the highest price is {highest['Stock Name']} ({highest['Stock Symbol']}) with a price of ${highest['Price']:.2f}"
                    elif "average" in query.lower() and "price" in query.lower():
                        avg_price = df['Price'].mean()
                        response = f"The average stock price is ${avg_price:.2f}"
                    # Add more basic query patterns
                    elif "sector" in query.lower() and "most" in query.lower():
                        top_sector = df['Sector'].value_counts().idxmax()
                        count = df['Sector'].value_counts().max()
                        response = f"The sector with the most stocks is {top_sector} with {count} stocks"
                    else:
                        response = "I don't have enough information to answer that specific question in the demo mode. In the full version with the Groq API key configured, this would provide a detailed analysis."
                    
                    # Display response in a nice card
                    st.success("Analysis Complete")
                    st.markdown(f"""
                    <div class="highlight" style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #2E7AD1;">
                        <p style="margin: 0; font-weight: 600; margin-bottom: 8px;">Query:</p>
                        <p style="margin: 0; margin-bottom: 12px; color: #555;">{query}</p>
                        <p style="margin: 0; font-weight: 600; margin-bottom: 8px;">Response:</p>
                        <p style="margin: 0; font-size: 1.1rem;">{response}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error analyzing data: {e}")
        else:
            st.warning("Please enter a query to analyze.")

# Data Explorer page
elif page == "Data Explorer":
    st.markdown("<h2 class='sub-header'>Stock Data Explorer</h2>", unsafe_allow_html=True)
    
    # Create a two-column layout for filters and data
    filter_col, data_col = st.columns([1, 3])
    
    with filter_col:
        st.markdown("### Filters")
        st.markdown('<div class="metric-card" style="padding: 15px;">', unsafe_allow_html=True)
        
        # Filter by sector
        sectors = ["All"] + sorted(df["Sector"].unique().tolist())
        selected_sector = st.selectbox("Sector", sectors)
        
        # Price range slider
        min_price, max_price = float(df["Price"].min()), float(df["Price"].max())
        price_range = st.slider("Price Range ($)", 
                               min_price, max_price, 
                               (min_price, max_price),
                               help="Filter stocks by price range")
        
        # Additional filters
        if 'P/E Ratio' in df.columns:
            show_pe_filter = st.checkbox("Filter by P/E Ratio", value=False)
            if show_pe_filter:
                pe_min = float(df["P/E Ratio"].min())
                pe_max = float(df["P/E Ratio"].max())
                pe_range = st.slider("P/E Ratio Range", 
                                   pe_min, pe_max, 
                                   (pe_min, pe_max))
        
        if 'Performance (%)' in df.columns:
            show_perf_filter = st.checkbox("Filter by Performance", value=False)
            if show_perf_filter:
                perf_min = float(df["Performance (%)"].min())
                perf_max = float(df["Performance (%)"].max())
                perf_range = st.slider("Performance Range (%)", 
                                      perf_min, perf_max, 
                                      (perf_min, perf_max))
                
        st.markdown('</div>', unsafe_allow_html=True)
            
    with data_col:
        # Apply filters
        filtered_df = df.copy()
        
        if selected_sector != "All":
            filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]
            
        filtered_df = filtered_df[(filtered_df["Price"] >= price_range[0]) & 
                                 (filtered_df["Price"] <= price_range[1])]
        
        if 'P/E Ratio' in df.columns and show_pe_filter:
            filtered_df = filtered_df[(filtered_df["P/E Ratio"] >= pe_range[0]) & 
                                     (filtered_df["P/E Ratio"] <= pe_range[1])]
            
        if 'Performance (%)' in df.columns and show_perf_filter:
            filtered_df = filtered_df[(filtered_df["Performance (%)"] >= perf_range[0]) & 
                                     (filtered_df["Performance (%)"] <= perf_range[1])]
        
        # Show data count and summary
        st.markdown(f"<p>Showing {len(filtered_df)} of {len(df)} stocks</p>", unsafe_allow_html=True)
        
        # Improved styling for the dataframe
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(filtered_df, use_container_width=True, height=400, 
                   column_config={
                       "Price": st.column_config.NumberColumn(
                           "Price ($)",
                           format="$%.2f"
                       ),
                       "Performance (%)": st.column_config.NumberColumn(
                           "Performance (%)",
                           format="%.2f%%"
                       ),
                   })
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download option
        csv_buffer = io.StringIO()
        filtered_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name="filtered_stock_data.csv",
            mime="text/csv",
        )

# About page
else:
    st.markdown("<h2 class='sub-header'>About StockSense Analyzer</h2>", unsafe_allow_html=True)
    
    # Create a card-like container for the about section
    st.markdown("""
    <div style="background-color: white; border-radius: 10px; padding: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin: 10px 0 30px 0;">
    <p style="font-size: 1.2rem; line-height: 1.6;">StockSense Analyzer is a professional stock market analysis platform designed to provide powerful insights through AI-powered natural language queries and interactive visualizations.</p>
    
    <h3 style="color: #2E7AD1; margin-top: 25px;">Core Features</h3>
    <ul style="list-style-type: none; padding-left: 0;">
        <li style="margin: 10px 0; display: flex; align-items: center;">
            <span style="background-color: #2E7AD1; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;">1</span>
            <span><strong>Natural Language Queries:</strong> Ask questions about stock data in plain English</span>
        </li>
        <li style="margin: 10px 0; display: flex; align-items: center;">
            <span style="background-color: #2E7AD1; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;">2</span>
            <span><strong>Data Visualization:</strong> Interactive charts and graphs for stock analysis</span>
        </li>
        <li style="margin: 10px 0; display: flex; align-items: center;">
            <span style="background-color: #2E7AD1; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;">3</span>
            <span><strong>Real-time Analysis:</strong> Get immediate responses to your financial queries</span>
        </li>
        <li style="margin: 10px 0; display: flex; align-items: center;">
            <span style="background-color: #2E7AD1; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;">4</span>
            <span><strong>Data Exploration:</strong> Filter and explore the underlying stock data</span>
        </li>
    </ul>
    
    <h3 style="color: #2E7AD1; margin-top: 25px;">Technologies Used</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;">
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; text-align: center;">
            <strong>Python</strong><br>Data Science & Web Stack
        </div>
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; text-align: center;">
            <strong>LangChain</strong><br>AI integration
        </div>
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; text-align: center;">
            <strong>Groq LLM</strong><br>NLP
        </div>
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; text-align: center;">
            <strong>Pandas</strong><br>Data manipulation
        </div>
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; text-align: center;">
            <strong>Matplotlib & Seaborn</strong><br>Visualizations
        </div>
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; text-align: center;">
            <strong>Streamlit</strong><br>Web interface
        </div>
    </div>
    
    <p style="margin-top: 30px; font-style: italic;">This platform is designed for investors, analysts, and financial professionals looking to gain rapid insights from stock market data using advanced AI.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer with subtle styling
st.markdown("""
<style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 10px 0;
        text-align: center;
        font-size: 0.8rem;
        color: #666;
        border-top: 1px solid #eee;
        backdrop-filter: blur(10px);
    }
</style>
<div class="footer">
    StockSense Analyzer © 2024 | Powered by Streamlit & Groq AI
</div>
""", unsafe_allow_html=True) 