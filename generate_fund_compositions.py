import json
import random
from datetime import datetime
import sys

# Fixed tickers for each fund
fund_tickers = {
    "Fund A": ["AAPL", "GOOG", "MSFT"],
    "Fund B": ["AMZN", "TSLA", "NVDA"],
    "Fund C": ["JPM", "BAC", "V"],
    "Fund D": ["XOM", "CVX", "COP"],
}

# Load funds from Portfolio 1 artifact
def load_portfolio_funds():
    with open("artifacts/portfolio.json", "r") as f:
        portfolio = json.load(f)
    return [fund["name"] for fund in portfolio["funds"]]

# Generate random proportions for each fund
def generate_fund_compositions(fund_names, date):
    compositions = {
        "date": date,
        "fund_compositions": []
    }
    
    for fund in fund_names:
        tickers = fund_tickers.get(fund, [])
        
        if not tickers:
            continue
        
        positions = []
        remaining_proportion = 1.0
        
        for ticker in tickers:
            # Randomize proportions while ensuring they sum to 1.0
            proportion = round(random.uniform(0.1, remaining_proportion), 2)
            positions.append({"ticker": ticker, "proportion": proportion})
            remaining_proportion -= proportion
            if remaining_proportion <= 0.1:
                break
        
        # Normalize proportions to exactly sum to 1.0
        total_proportion = sum(p["proportion"] for p in positions)
        for p in positions:
            p["proportion"] = round(p["proportion"] / total_proportion, 2)
        
        compositions["fund_compositions"].append({
            "name": fund,
            "positions": positions
        })
    
    return compositions

# Main execution
if __name__ == "__main__":
    # Accept date input or default to today
    input_date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    
    # Load funds from Portfolio 1
    fund_names = load_portfolio_funds()
    
    # Generate compositions
    fund_compositions = generate_fund_compositions(fund_names, input_date)
    
    # Write to JSON file
    output_file = "artifacts/fund_compositions.json"
    with open(output_file, "w") as f:
        json.dump(fund_compositions, f, indent=4)

    print(f"Generated fund compositions artifact for {input_date}: {output_file}")