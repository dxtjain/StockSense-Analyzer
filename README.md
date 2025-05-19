# StockSense Analyzer

A professional financial analytics platform for stock market analysis using natural language queries powered by AI.

![StockSense Analyzer](https://img.icons8.com/fluency/96/financial-analytics.png)

## Features

- **Natural Language Queries**: Ask questions about stock data in plain English
- **Interactive Dashboard**: Visualize market trends and sector performance
- **Data Explorer**: Filter and analyze stock data with an intuitive interface
- **AI-Powered Analysis**: Get instant insights from Groq LLM
- **Modern UI/UX**: Clean, responsive interface built with Streamlit

## Live Demo

[View the StockSense Analyzer Demo](https://stocksense-analyzer.streamlit.app/) (Add your deployed app link here)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/stocksense-analyzer.git
   cd stocksense-analyzer
   ```

2. Create and activate a virtual environment:
   ```
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure API access:
   - Obtain a Groq API key from [Groq's platform](https://console.groq.com/)
   - Create `.env` file and add your API key:
     ```
     GROQ_API_KEY=your_api_key_here
     CSV_FILE_PATH=data/stocks.csv
     RESULTS_FILE_PATH=results/analysis_results.csv
     ```

## Usage

### Run the Streamlit Web App

```
streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.

### Command-line Analysis (Optional)

For headless analysis without the web interface:

```
python main.py --query "What is the average P/E ratio of technology stocks?"
```

Available options:
- `--data PATH`: Path to stock data CSV file
- `--api-key KEY`: Groq API key (if not set in environment)
- `--query "QUERY1" "QUERY2"`: Custom queries to run
- `--visualize`: Generate data visualizations
- `--interactive`: Run in interactive mode

## Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Sharing](https://streamlit.io/sharing)
3. Connect your GitHub repository
4. Add your Groq API key as a secret
5. Deploy the app

### Alternative Deployment Options

- **Heroku**: Use the provided Procfile to deploy on Heroku
- **AWS/GCP/Azure**: Deploy using cloud platform services
- **Docker**: Use the included Dockerfile for containerized deployment

## Project Structure

```
stocksense-analyzer/
│
├── data/                    # Stock data files
│   └── stocks.csv           # Sample stock dataset
│
├── results/                 # Analysis results
│   ├── analysis_results.csv # Query results
│   └── plots/               # Generated visualizations
│
├── app.py                   # Streamlit web application
├── config.py                # Configuration settings
├── data_processor.py        # Data loading and processing
├── analyzer.py              # LangChain and Groq integration
├── visualizer.py            # Data visualization functions
├── main.py                  # CLI entry point
│
├── requirements.txt         # Project dependencies
└── README.md                # This file
```

## Technology Stack

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **LangChain**: Framework for LLM applications
- **Groq**: Large Language Model provider
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Data visualization
- **Scikit-learn**: Machine learning utilities (for extensions)

## Potential Extensions

- **Portfolio Optimization**: Add portfolio construction features
- **Predictive Analytics**: Implement machine learning for predictions
- **Real-time Data**: Connect to live market data APIs
- **Sentiment Analysis**: Analyze news sentiment for stocks
- **Advanced Visualization**: Add interactive charting with Plotly

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Stock data curated for educational purposes
- Icons by [Icons8](https://icons8.com/)