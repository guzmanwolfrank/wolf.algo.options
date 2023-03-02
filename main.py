import requests

# Define your Tastytrade API endpoint and credentials
endpoint = "https://api.tastytrade.com"
email = "your_email@example.com"
password = "your_password"

# Authenticate with the Tastytrade API
auth_resp = requests.post(f"{endpoint}/sessions", json={"email": email, "password": password})
auth_resp.raise_for_status()
auth_token = auth_resp.json()["data"]["authentication_token"]

# Define the stock symbol you want to trade options on
symbol = "AAPL"

# Define the number of option contracts to sell
quantity = 1

# Define the expiration date for the options (e.g. the 3rd Friday of the month)
expiration_date = "2023-03-17"

# Define the strike price for the options
strike_price = 135

# Define the type of option to sell (e.g. a call option)
option_type = "CALL"

# Define the credit limit for the option (e.g. $1.00)
credit_limit = 1.0

# Define the moving average period to use (e.g. 100 days)
moving_average_period = 100

# Fetch the historical stock prices for the specified symbol
historical_prices_resp = requests.get(f"{endpoint}/symbols/{symbol}/historicals", params={"range": "5y"})
historical_prices_resp.raise_for_status()
historical_prices = historical_prices_resp.json()["data"]

# Calculate the moving average for the specified period
moving_average_prices = []
for i in range(moving_average_period, len(historical_prices)):
    moving_average = sum(float(p["close_price"]) for p in historical_prices[i-moving_average_period:i]) / moving_average_period
    moving_average_prices.append(moving_average)

# Fetch the current stock price
current_price_resp = requests.get(f"{endpoint}/symbols/{symbol}")
current_price_resp.raise_for_status()
current_price = float(current_price_resp.json()["data"]["last_price"])

# Check if the current price is above the moving average
if current_price > moving_average_prices[-1]:
    # If the current price is above the moving average, sell the option credit
    order_resp = requests.post(f"{endpoint}/orders", headers={"X-Authentication-Token": auth_token}, json={
        "symbol": symbol,
        "order_type": "CREDIT",
        "limit_price": credit_limit,
        "quantity": quantity,
        "expiration_date": expiration_date,
        "strike_price": strike_price,
        "option_type": option_type
    })
    order_resp.raise_for_status()
    print("Option credit sold!")
else:
    print("Stock price is below moving average, no action taken.")

