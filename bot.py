Python 3.12.8 (tags/v3.12.8:2dc476b, Dec  3 2024, 19:07:15) [MSC v.1942 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import time

import os

from bitmart.api_spot import Spot



# Load environment variables

from dotenv import load_dotenv

load_dotenv()



# BitMart API credentials from .env file
API_KEY = os.getenv("971d19e29391401ed532770974c4abbb7b7d9e9e")
API_SECRET = os.getenv("a2ac3c359de5b1ad67b30a715a5d90b9c3c023d71b77f02b9acd81a9b99968f7")



# Initialize the BitMart API client

client = Spot(api_key=971d19e29391401ed532770974c4abbb7b7d9e9e, secret_key=a2ac3c359de5b1ad67b30a715a5d90b9c3c023d71b77f02b9acd81a9b99968f7)



# Trading pairs and price levels

# Enter buy and sell prices only for the trading pair you want to trade.

TRADING_PAIRS = {

    "XRP_USDT": {"buy_price": None, "sell_price": None},

    "DOGE_USDT": {"buy_price": 0.335, "sell_price": .3609},

    "SHIB_USDT": {"buy_price": None, "sell_price": None},

    "PEPE_USDT": {"buy_price": None, "sell_price": None},

    "ADA_USDT": {"buy_price": None, "sell_price": None},

}



# Trading amount (in USDT)

TRADE_AMOUNT = 30  # Adjust as per your preference





def get_balance(client, symbol):

    """Retrieve available balance for a specific symbol."""

    try:

        response = client.get_wallet()

        for asset in response['data']['wallet']:

            if asset['currency'] == symbol:

                return float(asset['available'])

    except Exception as e:

        print(f"Error fetching balance: {e}")

        return 0





def place_order(client, symbol, side, amount):

    """Place an order (buy or sell)."""

    try:

        price = TRADING_PAIRS[symbol]["buy_price"] if side == "buy" else TRADING_PAIRS[symbol]["sell_price"]

        response = client.post_submit_limit_order(

            symbol=symbol,

            side=side,

            size=amount,

            price="{:.8f}".format(price),

        )

        print(f"Order placed: {response}")

    except Exception as e:

        print(f"Error placing order: {e}")





def trade_pair(client, pair, config):

    """Execute trades for a specific trading pair."""

    try:

        if config["buy_price"] is None or config["sell_price"] is None:

            print(f"Skipping {pair}: No buy/sell prices defined.")

            return



        ticker = client.get_ticker(symbol=pair)

        current_price = float(ticker["data"]["tickers"][0]["last_price"])

        print(f"{pair} current price: {current_price}")



        # Check for buy condition

        if current_price <= config["buy_price"]:

            usdt_balance = get_balance(client, "USDT")

            if usdt_balance >= TRADE_AMOUNT:

                amount_to_buy = TRADE_AMOUNT / current_price

                place_order(client, pair, "buy", round(amount_to_buy, 4))

            else:

                print(f"Insufficient USDT balance to buy {pair}")



        # Check for sell condition

        elif current_price >= config["sell_price"]:

            token_symbol = pair.split("_")[0]

            token_balance = get_balance(client, token_symbol)

...             if token_balance > 0:
... 
...                 place_order(client, pair, "sell", round(token_balance, 4))
... 
...             else:
... 
...                 print(f"Insufficient {token_symbol} balance to sell {pair}")
... 
... 
... 
...     except Exception as e:
... 
...         print(f"Error trading {pair}: {e}")
... 
... 
... 
... 
... 
... def main():
... 
...     """Main trading loop."""
... 
...     print("Starting trading bot...")
... 
... 
... 
...     while True:
... 
...         # Process only one trading pair at a time
... 
...         for pair, config in TRADING_PAIRS.items():
... 
...             if config["buy_price"] is not None and config["sell_price"] is not None:
... 
...                 print(f"Trading {pair}...")
... 
...                 trade_pair(client, pair, config)
... 
...                 print("Waiting 30 seconds before the next cycle...")
... 
...                 time.sleep(30)
... 
...                 break  # Stop after processing one trading pair
... 
... 
... 
...         # If no pair has valid buy/sell prices, sleep for a while
... 
...         if all(config["buy_price"] is None or config["sell_price"] is None for config in TRADING_PAIRS.values()):
... 
...             print("No trading pairs configured. Waiting 30 seconds...")
... 
...             time.sleep(30)
... 
... 
... 
... 
... 
... if __name__ == "__main__":
... 
