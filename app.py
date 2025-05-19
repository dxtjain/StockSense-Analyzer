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

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# Debug information - only show in development mode
debug_mode = False  # Set to True for debugging

# Apply modern styling with dark theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4DA6FF;
        --secondary-color: #113E78;
        --background-color: #111827;
        --card-background: #242E42;
        --text-color: #FFFFFF;
        --text-secondary: #CCCCCC;
        --accent-color: #FF9F1C;
        --danger-color: #FF5252;
        --success-color: #4CAF50;
    }
    
    /* Overall streamlit overrides */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
    }
    
    .stApp {
        background-color: #111827;
        color: white;
    }
    
    /* Main elements styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.2rem;
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-top: 1.5rem;
    }
    
    .description {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background-color: var(--card-background);
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 15px;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
        border: 1px solid rgba(77, 166, 255, 0.3);
    }
    
    /* Highlight box */
    .highlight {
        background-color: rgba(77, 166, 255, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
    }
    
    /* Tabs styling */
    .stTabs {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        background-color: rgba(77, 166, 255, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(77, 166, 255, 0.2) !important;
        color: var(--primary-color) !important;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2E94FF;
        box-shadow: 0 5px 15px rgba(46, 148, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--card-background);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] .css-10y5sf6 {
        color: white !important;
    }
    
    [data-testid="stSidebarUserContent"] {
        padding-top: 1rem;
    }
    
    /* Slider and other widgets */
    .stSlider [data-baseweb="slider"] {
        margin-top: 0.5rem;
        margin-bottom: 2rem;
    }
    
    /* For DataFrames */
    [data-testid="stTable"] {
        background-color: var(--card-background);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe {
        background-color: var(--card-background);
        color: white;
        border-radius: 8px;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(36, 46, 66, 0.95);
        padding: 10px 0;
        text-align: center;
        font-size: 0.8rem;
        color: #9CA3AF;
        border-top: 1px solid rgba(77, 166, 255, 0.2);
        backdrop-filter: blur(10px);
        z-index: 999;
    }
    
    .footer a {
        color: #4DA6FF;
        text-decoration: none;
        margin: 0 10px;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* Headers styling */
    h1, h2, h3, h4, h5 {
        color: var(--primary-color);
    }
    
    /* Charts area */
    .chart-container {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(77, 166, 255, 0.1);
        border-radius: 8px;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #1A202C;
        color: white;
        border: 1px solid rgba(77, 166, 255, 0.3);
    }
    
    .stTextInput > div > div > input:focus {
        border: 1px solid var(--primary-color);
        box-shadow: 0 0 0 1px var(--primary-color);
    }
    
    /* Tooltips styling */
    [data-tooltip]:before {
        background-color: var(--card-background);
        color: white;
    }
    
    /* Fix for plotly charts */
    .js-plotly-plot .plotly {
        background-color: transparent !important;
    }
    
    .js-plotly-plot .bg {
        fill: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# App header with logo and title
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
        <div style="background-color: #4DA6FF; width: 60px; height: 60px; border-radius: 12px; display: flex; justify-content: center; align-items: center; box-shadow: 0 3px 10px rgba(77, 166, 255, 0.3);">
            <span style="font-size: 30px;">📊</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("<h1 class='main-header'>StockSense Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Professional stock market data analysis powered by Groq AI</p>", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div style="background-color: rgba(77, 166, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center; width: 90%;">
            <div style="background-color: #4DA6FF; width: 60px; height: 60px; border-radius: 12px; display: flex; justify-content: center; align-items: center; margin: 0 auto 15px auto; box-shadow: 0 3px 10px rgba(77, 166, 255, 0.3);">
                <span style="font-size: 30px;">📊</span>
            </div>
            <h2 style="margin: 0; color: #4DA6FF; font-size: 1.5rem; font-weight: 600;">StockSense</h2>
            <p style="margin: 5px 0 0 0; color: #9CA3AF; font-size: 0.9rem;">Intelligent Stock Analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: rgba(77, 166, 255, 0.05); padding: 10px 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid rgba(77, 166, 255, 0.1);">
        <h3 style="margin: 0 0 10px 0; color: #4DA6FF; font-size: 1.2rem;">Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom navigation buttons using session state
    options = ["Dashboard", "AI Analysis", "Data Explorer", "About"]
    icons = ["📈", "🤖", "🔍", "ℹ️"]
    
    # Function to change page
    def change_page(new_page):
        st.session_state.page = new_page
    
    for i, (option, icon) in enumerate(zip(options, icons)):
        if option == st.session_state.page:
            st.markdown(f"""
            <div style="background-color: rgba(77, 166, 255, 0.2); padding: 10px; border-radius: 8px; margin-bottom: 10px; cursor: pointer; border: 1px solid rgba(77, 166, 255, 0.3);">
                <div style="display: flex; align-items: center;">
                    <div style="background-color: #4DA6FF; color: white; border-radius: 8px; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                        <span>{icon}</span>
                    </div>
                    <span style="color: #4DA6FF; font-weight: 600;">{option}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            button_key = f"nav_button_{i}"
            if st.button(f"{icon} {option}", key=button_key, use_container_width=True):
                change_page(option)
    
    # Add additional information at the bottom of the sidebar
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: rgba(77, 166, 255, 0.05); padding: 15px; border-radius: 8px; margin-top: 20px; text-align: center;">
        <p style="margin: 0; color: #9CA3AF; font-size: 0.8rem;">StockSense Analyzer v1.0</p>
        <p style="margin: 5px 0 0 0; color: #9CA3AF; font-size: 0.8rem;">© 2024 All Rights Reserved</p>
        <div style="margin-top: 10px; display: flex; justify-content: center; gap: 10px;">
            <a href="https://github.com/dxtjain/StockSense-Analyzer" target="_blank" style="color: #4DA6FF; text-decoration: none; font-size: 0.9rem;">GitHub</a>
            <span style="color: #4DA6FF;">|</span>
            <a href="https://github.com/dxtjain/StockSense-Analyzer/issues" target="_blank" style="color: #4DA6FF; text-decoration: none; font-size: 0.9rem;">Support</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
if st.session_state.page == "Dashboard":
    st.markdown("<h2 class='sub-header'>Market Overview</h2>", unsafe_allow_html=True)
    
    # Key metrics in columns with improved styling
    metrics_container = st.container()
    with metrics_container:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 1rem; color: #9CA3AF;">Total Stocks</h3>
                <p style="font-size: 2.2rem; font-weight: 700; margin: 10px 0; color: #4DA6FF;">{}</p>
            </div>
            """.format(stats['total_stocks']), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 1rem; color: #9CA3AF;">Average Price</h3>
                <p style="font-size: 2.2rem; font-weight: 700; margin: 10px 0; color: #4DA6FF;">${:.2f}</p>
            </div>
            """.format(stats['average_price']), unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 1rem; color: #9CA3AF;">Highest Price</h3>
                <p style="font-size: 2.2rem; font-weight: 700; margin: 10px 0; color: #4DA6FF;">{}</p>
            </div>
            """.format(stats['highest_price']), unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 1rem; color: #9CA3AF;">Avg Performance</h3>
                <p style="font-size: 2.2rem; font-weight: 700; margin: 10px 0; color: #4DA6FF;">{:.2f}%</p>
            </div>
            """.format(stats['avg_performance']), unsafe_allow_html=True)
    
    # Visualizations with dark mode compatible styling
    st.markdown("<h3 class='sub-header' style='margin-top: 2rem;'>Market Visualizations</h3>", unsafe_allow_html=True)
    
    # Create a background container for the visualization tabs
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Use caching for visualizations to improve performance
    @st.cache_data
    def create_visualizations():
        # Set a dark theme for visualizations
        plt.style.use('dark_background')
        
        # Custom colors for charts
        colors = ['#4DA6FF', '#FF9F1C', '#4CAF50', '#F44336', '#9C27B0', '#3F51B5', 
                 '#00BCD4', '#FFEB3B', '#FF5722', '#795548']
        
        # Create figures
        fig1, ax1 = plt.subplots(figsize=(10, 6), facecolor='#242E42')
        ax1.set_facecolor('#242E42')
        sector_counts = df['Sector'].value_counts()
        wedges, texts, autotexts = ax1.pie(
            sector_counts, 
            labels=None,  # We'll add a legend instead
            autopct='%1.1f%%', 
            startangle=90, 
            shadow=False, 
            colors=colors,
            wedgeprops={'edgecolor': '#242E42', 'linewidth': 1, 'antialiased': True},
            textprops={'color': 'white', 'fontsize': 12, 'fontweight': 'bold'}
        )
        # Enhance the appearance of percentage text
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        # Add a legend
        ax1.legend(
            wedges, 
            sector_counts.index, 
            title="Sectors", 
            loc="center left", 
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=10
        )
        
        ax1.axis('equal')
        ax1.set_title('Stock Distribution by Sector', fontsize=16, color='white', pad=20)
        plt.tight_layout()
        
        # Second chart - price distribution
        fig2, ax2 = plt.subplots(figsize=(10, 6), facecolor='#242E42')
        ax2.set_facecolor('#242E42')
        sns.histplot(df['Price'], bins=20, kde=True, ax=ax2, color='#4DA6FF', edgecolor='#242E42', line_kws={'color': '#FF9F1C', 'lw': 2})
        plt.title('Distribution of Stock Prices', fontsize=16, color='white', pad=20)
        plt.xlabel('Price ($)', fontsize=12, color='white')
        plt.ylabel('Count', fontsize=12, color='white')
        plt.grid(alpha=0.2)
        ax2.tick_params(colors='white')
        for spine in ax2.spines.values():
            spine.set_color('#555555')
        plt.tight_layout()
        
        # Third chart - performance by sector
        fig3, ax3 = plt.subplots(figsize=(12, 8), facecolor='#242E42')
        ax3.set_facecolor('#242E42')
        box = sns.boxplot(x='Sector', y='Performance (%)', data=df, ax=ax3, palette=colors)
        plt.xticks(rotation=45, ha='right', fontsize=10, color='white')
        plt.title('Stock Performance by Sector', fontsize=16, color='white', pad=20)
        plt.xlabel('Sector', fontsize=12, color='white')
        plt.ylabel('Performance (%)', fontsize=12, color='white')
        plt.grid(axis='y', alpha=0.2)
        ax3.tick_params(colors='white')
        for spine in ax3.spines.values():
            spine.set_color('#555555')
        plt.tight_layout()
        
        # Fourth chart - top stocks by price
        fig4, ax4 = plt.subplots(figsize=(10, 6), facecolor='#242E42')
        ax4.set_facecolor('#242E42')
        top_n = df.nlargest(10, 'Price')
        bars = sns.barplot(x='Stock Symbol', y='Price', data=top_n, ax=ax4, palette=colors)
        plt.title('Top 10 Stocks by Price', fontsize=16, color='white', pad=20)
        plt.xticks(rotation=45, ha='right', fontsize=10, color='white')
        plt.xlabel('Stock Symbol', fontsize=12, color='white')
        plt.ylabel('Price ($)', fontsize=12, color='white')
        plt.grid(axis='y', alpha=0.2)
        ax4.tick_params(colors='white')
        for spine in ax4.spines.values():
            spine.set_color('#555555')
            
        # Add value labels on top of bars
        for i, bar in enumerate(bars.patches):
            bars.annotate(
                f'${bar.get_height():,.0f}',
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha='center', 
                va='bottom', 
                fontsize=9,
                color='white',
                fontweight='bold',
                xytext=(0, 5),  # 5 points vertical offset
                textcoords='offset points'
            )
        
        plt.tight_layout()
        
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
        
    # Close the chart container div
    st.markdown('</div>', unsafe_allow_html=True)

# AI Analysis page
elif st.session_state.page == "AI Analysis":
    st.markdown("<h2 class='sub-header'>AI-Powered Stock Analysis</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="highlight" style="background-color: rgba(77, 166, 255, 0.1); border-left: 4px solid #4DA6FF;">
        <h4 style="margin-top: 0; color: #4DA6FF;">Ask questions about your stock data</h4>
        <p style="margin-bottom: 0;">Get AI-powered insights by asking questions in natural language. Our system will analyze the data and provide detailed responses.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if API key is available
    api_missing = GROQ_API_KEY is None
    if api_missing:
        st.warning("⚠️ Groq API key is not configured. Running in demo mode.")
        st.info("ℹ️ To enable full AI features, set GROQ_API_KEY in Streamlit secrets.")
        
        # Create collapsible section for example queries
        with st.expander("Example Queries & Responses", expanded=True):
            st.markdown("<h4 style='color: #4DA6FF;'>Sample Queries and Results</h4>", unsafe_allow_html=True)
            
            examples = [
                ("What is the stock price of AAPL?", f"The stock price of AAPL is ${df[df['Stock Symbol'] == 'AAPL']['Price'].values[0]:.2f}."),
                ("What is the performance of TSLA?", f"The performance of TSLA is {df[df['Stock Symbol'] == 'TSLA']['Performance (%)'].values[0]:.2f}%."),
                ("What is the PE ratio of MSFT?", f"The P/E Ratio of MSFT is {df[df['Stock Symbol'] == 'MSFT']['P/E Ratio'].values[0]:.2f}."),
                ("Which stock has the highest price?", f"The stock with the highest price is {df.loc[df['Price'].idxmax()]['Stock Name']} ({df.loc[df['Price'].idxmax()]['Stock Symbol']}) with a price of ${df['Price'].max():.2f}.")
            ]
            
            for i, (question, answer) in enumerate(examples):
                st.markdown(f"""
                <div style="background-color: rgba(77, 166, 255, 0.05); padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <strong style="color: #4DA6FF;">Q: {question}</strong>
                    <p style="margin: 5px 0 0 0;">A: {answer}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # User query input with improved UI
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #4DA6FF;'>Ask Your Question:</h4>", unsafe_allow_html=True)
    
    query = st.text_input("", 
                         placeholder="e.g., What is the average P/E ratio of technology stocks?",
                         help="Type your question about the stock data here",
                         label_visibility="collapsed")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        analyze_button = st.button("Analyze", type="primary", use_container_width=True)
    with col2:
        pass
    
    if analyze_button:
        if query:
            with st.spinner("Analyzing stock data..."):
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
                        response = "I don't have enough information to answer that specific question in demo mode. With the Groq API key configured, this would provide a detailed analysis."
                    
                    # Display response in a nice card
                    st.markdown("""
                    <div class="metric-card" style="background-color: rgba(77, 166, 255, 0.1); border: 1px solid rgba(77, 166, 255, 0.3); padding: 20px;">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="background-color: #4DA6FF; color: white; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 14px;">❓</span>
                            </div>
                            <div style="font-weight: 600; color: #E2E8F0;">{}</div>
                        </div>
                        
                        <div style="display: flex; align-items: center;">
                            <div style="background-color: #4CAF50; color: white; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;">
                                <span style="font-size: 14px;">✓</span>
                            </div>
                            <div style="font-size: 1.1rem; color: white;">{}</div>
                        </div>
                    </div>
                    """.format(query, response), unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error analyzing data: {e}")
        else:
            st.warning("Please enter a query to analyze.")

# Data Explorer page
elif st.session_state.page == "Data Explorer":
    st.markdown("<h2 class='sub-header'>Stock Data Explorer</h2>", unsafe_allow_html=True)
    
    # Create a clean container for the explorer
    st.markdown("""
    <div style="background-color: #242E42; border-radius: 10px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
        <h4 style="color: #4DA6FF; margin-top: 0;">Explore and Filter Stock Data</h4>
        <p style="color: #ccc; margin-bottom: 20px;">Use the filters to narrow down the stock data and explore specific segments of the market.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create a two-column layout for filters and data
    filter_col, data_col = st.columns([1, 3])
    
    with filter_col:
        st.markdown("""
        <div style="background-color: #242E42; padding: 5px; border-radius: 8px; margin-bottom: 15px;">
            <h4 style="color: #4DA6FF; padding: 10px 15px; margin: 0; border-bottom: 1px solid rgba(77, 166, 255, 0.2);">Filters</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a card for filters
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
        
        # Add a reset filters button
        if st.button("Reset Filters", type="secondary", use_container_width=True):
            st.experimental_rerun()
            
    with data_col:
        # Create a header card for the data section
        st.markdown("""
        <div style="background-color: #242E42; padding: 5px; border-radius: 8px; margin-bottom: 15px;">
            <h4 style="color: #4DA6FF; padding: 10px 15px; margin: 0; border-bottom: 1px solid rgba(77, 166, 255, 0.2);">Stock Data</h4>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # Add a mini-dashboard with key stats about the filtered data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="background-color: rgba(77, 166, 255, 0.1); padding: 10px; border-radius: 5px; text-align: center;">
                <p style="margin: 0; color: #9CA3AF; font-size: 0.9rem;">Showing</p>
                <p style="margin: 0; font-weight: 700; font-size: 1.5rem; color: #4DA6FF;">{len(filtered_df)}</p>
                <p style="margin: 0; color: #9CA3AF; font-size: 0.9rem;">of {len(df)} stocks</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_price = filtered_df['Price'].mean() if not filtered_df.empty else 0
            st.markdown(f"""
            <div style="background-color: rgba(77, 166, 255, 0.1); padding: 10px; border-radius: 5px; text-align: center;">
                <p style="margin: 0; color: #9CA3AF; font-size: 0.9rem;">Avg Price</p>
                <p style="margin: 0; font-weight: 700; font-size: 1.5rem; color: #4DA6FF;">${avg_price:.2f}</p>
                <p style="margin: 0; color: #9CA3AF; font-size: 0.9rem;">in filtered data</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            avg_perf = filtered_df['Performance (%)'].mean() if 'Performance (%)' in filtered_df.columns and not filtered_df.empty else 0
            st.markdown(f"""
            <div style="background-color: rgba(77, 166, 255, 0.1); padding: 10px; border-radius: 5px; text-align: center;">
                <p style="margin: 0; color: #9CA3AF; font-size: 0.9rem;">Avg Performance</p>
                <p style="margin: 0; font-weight: 700; font-size: 1.5rem; color: #4DA6FF;">{avg_perf:.2f}%</p>
                <p style="margin: 0; color: #9CA3AF; font-size: 0.9rem;">in filtered data</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show data with improved styling for dark mode
        if filtered_df.empty:
            st.markdown("""
            <div style="background-color: rgba(255, 82, 82, 0.1); padding: 20px; border-radius: 8px; text-align: center; border: 1px solid rgba(255, 82, 82, 0.3);">
                <h4 style="margin: 0; color: #FF5252;">No Data Found</h4>
                <p style="margin: 10px 0 0 0;">Try adjusting your filters to see more results.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Improved styling for the dataframe
            st.markdown('<div style="background-color: #242E42; padding: 20px; border-radius: 8px;">', unsafe_allow_html=True)
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
            st.markdown("<br>", unsafe_allow_html=True)
            csv_buffer = io.StringIO()
            filtered_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.download_button(
                    label="📥 Download Filtered Data (CSV)",
                    data=csv_data,
                    file_name="filtered_stock_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# About page
else:
    st.markdown("<h2 class='sub-header'>About StockSense Analyzer</h2>", unsafe_allow_html=True)
    
    # Create a card-like container for the about section
    st.markdown("""
    <div style="background-color: #242E42; color: white; border-radius: 10px; padding: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); margin: 10px 0 30px 0;">
    <p style="font-size: 1.2rem; line-height: 1.6;">StockSense Analyzer is a professional stock market analysis platform designed to provide powerful insights through AI-powered natural language queries and interactive visualizations.</p>
    
    <h3 style="color: #4DA6FF; margin-top: 25px; font-size: 1.5rem;">Core Features</h3>
    <div style="margin-top: 20px;">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: #4DA6FF; color: white; border-radius: 50%; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;">1</div>
            <div style="flex: 1;"><strong style="color: #4DA6FF; font-size: 1.1rem;">Natural Language Queries:</strong><br>Ask questions about stock data in plain English</div>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: #4DA6FF; color: white; border-radius: 50%; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;">2</div>
            <div style="flex: 1;"><strong style="color: #4DA6FF; font-size: 1.1rem;">Data Visualization:</strong><br>Interactive charts and graphs for stock analysis</div>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: #4DA6FF; color: white; border-radius: 50%; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;">3</div>
            <div style="flex: 1;"><strong style="color: #4DA6FF; font-size: 1.1rem;">Real-time Analysis:</strong><br>Get immediate responses to your financial queries</div>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background-color: #4DA6FF; color: white; border-radius: 50%; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;">4</div>
            <div style="flex: 1;"><strong style="color: #4DA6FF; font-size: 1.1rem;">Data Exploration:</strong><br>Filter and explore the underlying stock data</div>
        </div>
    </div>
    
    <h3 style="color: #4DA6FF; margin-top: 30px; font-size: 1.5rem;">Technologies Used</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; margin-top: 20px;">
        <div style="background-color: rgba(77, 166, 255, 0.2); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid rgba(77, 166, 255, 0.3);">
            <strong style="color: #4DA6FF; font-size: 1.1rem;">Python</strong><br><span style="color: #ccc;">Data Science & Web Stack</span>
        </div>
        <div style="background-color: rgba(77, 166, 255, 0.2); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid rgba(77, 166, 255, 0.3);">
            <strong style="color: #4DA6FF; font-size: 1.1rem;">LangChain</strong><br><span style="color: #ccc;">AI integration</span>
        </div>
        <div style="background-color: rgba(77, 166, 255, 0.2); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid rgba(77, 166, 255, 0.3);">
            <strong style="color: #4DA6FF; font-size: 1.1rem;">Groq LLM</strong><br><span style="color: #ccc;">Natural Language Processing</span>
        </div>
        <div style="background-color: rgba(77, 166, 255, 0.2); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid rgba(77, 166, 255, 0.3);">
            <strong style="color: #4DA6FF; font-size: 1.1rem;">Pandas</strong><br><span style="color: #ccc;">Data manipulation</span>
        </div>
        <div style="background-color: rgba(77, 166, 255, 0.2); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid rgba(77, 166, 255, 0.3);">
            <strong style="color: #4DA6FF; font-size: 1.1rem;">Matplotlib</strong><br><span style="color: #ccc;">Visualizations</span>
        </div>
        <div style="background-color: rgba(77, 166, 255, 0.2); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid rgba(77, 166, 255, 0.3);">
            <strong style="color: #4DA6FF; font-size: 1.1rem;">Streamlit</strong><br><span style="color: #ccc;">Web interface</span>
        </div>
    </div>
    
    <p style="margin-top: 30px; font-style: italic; color: #ccc;">This platform is designed for investors, analysts, and financial professionals looking to gain rapid insights from stock market data using advanced AI.</p>
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
        background-color: rgba(36, 46, 66, 0.95);
        padding: 10px 0;
        text-align: center;
        font-size: 0.8rem;
        color: #9CA3AF;
        border-top: 1px solid rgba(77, 166, 255, 0.2);
        backdrop-filter: blur(10px);
        z-index: 999;
    }
    
    .footer a {
        color: #4DA6FF;
        text-decoration: none;
        margin: 0 10px;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
</style>
<div class="footer">
    <div>StockSense Analyzer © 2024 | Powered by <a href="https://streamlit.io" target="_blank">Streamlit</a> & <a href="https://groq.com" target="_blank">Groq AI</a></div>
</div>
""", unsafe_allow_html=True) 