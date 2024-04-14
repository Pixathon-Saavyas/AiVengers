# Intraday Stocks Predictor

## Description of the project

Intraday Stocks Predictor is a project designed to provide recommendations for intraday trading opportunities based on historical stock data. The system analyzes key indicators such as volume trend, price trend, volatility, and relative strength index (RSI) for a selection of stocks over a recent 7-day period. Based on the analysis, the project suggests buy or sell recommendations tailored to the user's investment amount and risk tolerance.

## Agents

The project uses two agents for its operations:

- *u.py*: This agent acts as a user interface, receiving input from the user such as investment amount and risk tolerance. It forwards this information to the analyzer agent for further processing and provides the user with trading recommendations.

- *analyzer_agent.py*: This agent analyzes historical data for nifty 50 stocks to provide buy or sell recommendations based on volume trend, price trend, volatility, and RSI. It considers the user's investment amount and risk tolerance when generating recommendations and provides detailed output including take profit, stop loss, and quantity of stocks to buy or sell.

## Getting Started 🚀

To use these agents and start trading, follow the steps below:

### Step 1: Obtain API Keys 🔑

Before running the project, obtain the necessary API keys from the following sources:

- *Yahoo Finance API*: The project uses data from the Yahoo Finance API to retrieve historical stock data. You can obtain an API key from [Yahoo Finance](https://finance.yahoo.com/).

- *Google Finance API*: The project uses the nifty 50 stock's status and performance at National Stock Exchange (NSE).You can obtain an API key from [Google Finance](https://www.google.com/finance/?hl=en).

### Step 2: Set API Key and Agent Addresses

- Fill in the API key in the scripts as necessary.
- Ensure the agent addresses are correctly configured in the scripts.

### Step 3: Run the Project

- Navigate to the project's directory.




1. **Navigate to the Project Directory**

   Open your terminal or command prompt and navigate to the project's directory using the `cd` command:

   ```bash
   cd /Intraday Stocks Predictor
   ```

2. **Change Directory to Agents**

   Once inside the project directory, navigate to the `src/agents` directory:

   ```bash
   cd src/agents
   ```

3. **Run the Analyzer Agent**

   To start the analyzer agent, run the following command:

   ```bash
   python analyzer_agent.py
   ```

   The analyzer agent will start running and perform its designated tasks.

4. **Run the User Interface**

   In a separate terminal or command prompt window, navigate to the same `src/agents` directory as in Step 2, and run the user interface:

   ```bash
   python u.py
   ```

   This will allow the user to give the input I) Amount he wants to inveest II) Risk he can take



Now, the Intraday Stocks Predictor is up and running, ready to analyze stock data and provide trading recommendations based on the user's input. Happy trading! 🎉


