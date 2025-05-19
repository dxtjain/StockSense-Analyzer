"""
Main entry point for the Stock Analysis application.
"""

import os
import argparse
from config import DATA_FILE, GROQ_API_KEY, STANDARD_QUERIES
from data_processor import load_stock_data, save_analysis_results, get_stock_statistics
from analyzer import StockAnalyzer
from visualizer import (
    plot_sector_distribution,
    plot_price_distribution,
    plot_performance_by_sector,
    plot_top_stocks_by_price
)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Stock Data Analysis Tool')
    parser.add_argument('--data', type=str, default=DATA_FILE,
                        help='Path to stock data CSV file')
    parser.add_argument('--api-key', type=str, default=GROQ_API_KEY,
                        help='Groq API key (if not set in environment)')
    parser.add_argument('--query', type=str, nargs='+',
                        help='Custom queries to run (if not provided, standard queries will be used)')
    parser.add_argument('--visualize', action='store_true',
                        help='Generate visualizations')
    parser.add_argument('--interactive', action='store_true',
                        help='Run in interactive mode')
    
    return parser.parse_args()

def run_interactive_mode(analyzer, df):
    """Run the application in interactive mode."""
    print("\n=== Stock Analysis Interactive Mode ===")
    print("Type 'exit' to quit, 'stats' for basic statistics, 'viz' for visualizations")
    
    while True:
        query = input("\nEnter your query: ")
        
        if query.lower() == 'exit':
            break
        elif query.lower() == 'stats':
            stats = get_stock_statistics(df)
            for key, value in stats.items():
                print(f"{key}: {value}")
        elif query.lower() == 'viz':
            print("Generating visualizations...")
            plot_sector_distribution(df)
            plot_price_distribution(df)
            plot_performance_by_sector(df)
            plot_top_stocks_by_price(df)
        else:
            result = analyzer.analyze(query)
            print(f"\nQuery: {result['query']}")
            print(f"Response: {result['response']}")

def main():
    """Main function."""
    args = parse_args()
    
    # Check if API key is available
    if not args.api_key:
        print("Error: Groq API key is required. Set it in .env file or pass with --api-key")
        return
    
    try:
        # Load and clean data
        print(f"Loading stock data from {args.data}...")
        df = load_stock_data()
        print(f"Loaded {len(df)} stocks from {args.data}")
        
        # Create analyzer
        analyzer = StockAnalyzer(
            data_file=args.data,
            api_key=args.api_key
        )
        
        # Run queries
        if args.query:
            print("Running custom queries...")
            results_df = analyzer.run_custom_queries(args.query)
        else:
            print("Running standard queries...")
            results_df = analyzer.run_standard_queries()
        
        # Save results
        results_file = save_analysis_results(results_df)
        print(f"Analysis complete. Results saved to {results_file}")
        
        # Generate visualizations if requested
        if args.visualize:
            print("Generating visualizations...")
            os.makedirs('results/plots', exist_ok=True)
            plot_sector_distribution(df, 'results/plots/sector_distribution.png')
            plot_price_distribution(df, 'results/plots/price_distribution.png')
            plot_performance_by_sector(df, 'results/plots/performance_by_sector.png')
            plot_top_stocks_by_price(df, 'results/plots/top_stocks_by_price.png')
            print("Visualizations saved to results/plots/ directory")
        
        # Run interactive mode if requested
        if args.interactive:
            run_interactive_mode(analyzer, df)
            
        print("Stock analysis completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 