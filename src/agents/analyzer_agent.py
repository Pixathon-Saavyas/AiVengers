from uagents import Agent, Context, Model
from pydantic import BaseModel
import yfinance as yf
import numpy as np

# Define the Analyzer Agent
analyzer_agent = Agent(
    name="analyzer_agent",
    seed="analyzer_secret_phrase",
    port=8001,
    endpoint=["http://localhost:8001/submit"],
)

# Define the UserInput model
class UserInput(Model):
    amount: float
    risk: float

# Function to select top 5 stocks based on user input and historical data
def select_top_5_stocks(user_input: UserInput) -> list:
    investment_amount = user_input.amount
    risk_tolerance = user_input.risk

    # Retrieve list of NIFTY 50 tickers
    nifty_50_tickers = [
        "INFY.NS", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "HDFC.NS",
        "ICICIBANK.NS", "KOTAKBANK.NS", "HINDUNILVR.NS", "AXISBANK.NS",
        "ITC.NS", "SBIN.NS", "BAJAJFINSV.NS", "BHARTIARTL.NS",
        "ASIANPAINT.NS", "MARUTI.NS", "LT.NS", "HCLTECH.NS", "POWERGRID.NS",
        "ONGC.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "TECHM.NS",
        "NTPC.NS", "INDUSINDBK.NS", "BAJFINANCE.NS", "SUNPHARMA.NS",
        "COALINDIA.NS", "JSWSTEEL.NS", "M&M.NS", "BRITANNIA.NS",
        "IOC.NS", "TATASTEEL.NS", "UPL.NS", "DIVISLAB.NS", "TITAN.NS",
        "HDFCLIFE.NS", "SHREECEM.NS", "DRREDDY.NS", "CIPLA.NS",
        "SBILIFE.NS", "BAJAJ-AUTO.NS", "WIPRO.NS", "ONGC.NS",
        "NTPC.NS", "HINDALCO.NS", "HEROMOTOCO.NS", "GAIL.NS",
        "BPCL.NS", "ADANIPORTS.NS", "GRASIM.NS"
    ]

    # Initialize a list to store selected stocks
    selected_stocks = []

    # Iterate through each ticker
    for ticker in nifty_50_tickers:
        try:
            # Retrieve historical data for the ticker
            ticker_data = yf.download(ticker, start="2024-04-01", end="2024-04-07")

            # Check if the data is not empty
            if not ticker_data.empty:
                # Calculate metrics
                ticker_data["PriceChange"] = ticker_data["Close"] - ticker_data["Open"]
                ticker_data["PercentChange"] = (ticker_data["Close"] - ticker_data["Open"]) / ticker_data["Open"] * 100
                ticker_data["Volatility"] = np.std(ticker_data["Close"])
                ticker_data["Liquidity"] = np.mean(ticker_data["Volume"])

                # Apply selection criteria
                if (ticker_data["Close"].iloc[-1] <= investment_amount and
                    ticker_data["Volatility"].iloc[-1] > 0 and
                    ticker_data["Liquidity"].iloc[-1] > 0 and
                    ticker_data["PercentChange"].iloc[-1] > 0 and
                    ticker_data["Volume"].iloc[-1] > 100000):
                    selected_stocks.append((ticker, ticker_data["PercentChange"].iloc[-1]))

        except Exception as e:
            analyzer_agent.logger.error(f"Error processing {ticker}: {e}")

    # Sort selected stocks by percent change in descending order and select top 5
    selected_stocks.sort(key=lambda x: x[1], reverse=True)
    top_5_stocks = [stock[0] for stock in selected_stocks[:5]]

    return top_5_stocks

# Function to generate recommendations based on user input and other metrics
def generate_recommendations(ctx: Context, stock: str, user_input: UserInput):
    # Retrieve the price and other data from Yahoo Finance
    ticker_data = yf.Ticker(stock)

    # Get the current price of the stock
    current_price = ticker_data.history(period="1d")["Close"].iloc[-1]

    # Calculate take profit and stop loss
    risk_per = user_input.risk
    take_profit = current_price * (1 + 2 * risk_per)
    stop_loss = current_price * (1 - risk_per)

    # Calculate quantity based on investment amount
    quantity = int(user_input.amount / current_price)

    # Calculate total profit
    total_profit = (take_profit - current_price) * quantity

    # Generate buy/sell recommendation based on risk tolerance
    recommendation = "Buy" if risk_per > 0.02 else "Hold"

    # Log the recommendation
    ctx.logger.info(
        f"Recommendation for {stock}: {recommendation}\n"
        f"Price: {current_price}\n"
        f"Take Profit: {take_profit}\n"
        f"Stop Loss: {stop_loss}\n"
        f"Quantity: {quantity}\n"
        f"Total Profit: {total_profit}\n"
    )

# Define the function to handle user input received from the User Agent
@analyzer_agent.on_message(model=UserInput)
async def analyze_user_input(ctx: Context, sender: str, user_input: UserInput):
    # Select top 5 stocks based on user input
    top_5_stocks = select_top_5_stocks(user_input)

    # Log the selected top 5 stocks
    ctx.logger.info(f"Selected top 5 stocks: {top_5_stocks}")

    # Analyze each selected stock
    for stock in top_5_stocks:
        # Generate buy/sell recommendation based on user input
        generate_recommendations(ctx, stock, user_input)

# Run the Analyzer Agent
analyzer_agent.run()
