import telebot
import yfinance as yf
from datetime import datetime

API_TOKEN = '7705072328:AAElGoUVLaXNnbwsMyBg59tWOCXNdVtHkz4'
bot = telebot.TeleBot(API_TOKEN)

# Function to get stock info from Yahoo Finance (including international stocks)
def get_stock_info(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        stock_info = stock.info

        # Extract required stock info
        stock_price = stock_info.get("regularMarketPrice", "N/A")
        market_cap = stock_info.get("marketCap", "N/A")
        pe_ratio = stock_info.get("trailingPE", "N/A")

        # Return formatted stock info
        return f"{stock_symbol.upper()}:\nPrice: {stock_price} USD\nMarket Cap: {market_cap} USD\nP/E Ratio: {pe_ratio}"
    except Exception as e:
        return f"Sorry, I couldn't fetch data for {stock_symbol.upper()}. Error: {str(e)}"

# Start and Help Command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the stock info bot! Use /chungkhoan <symbol> to get stock information. Example: /chungkhoan AAPL")

# Greeting Command when the user sends 'Hi'
@bot.message_handler(func=lambda message: message.text.lower() == 'hi')
def greet_user(message):
    user_first_name = message.from_user.first_name
    bot.reply_to(message, f"Hello {user_first_name}, how can I assist you today?")

# /chungkhoan Command: Get stock info based on stock symbol
@bot.message_handler(commands=['chungkhoan'])
def chungkhoan_info(message):
    # Extract the stock symbol from the message
    command_text = message.text.strip().lower()

    # Ensure the user provides a stock symbol after the command
    if len(command_text.split()) < 2:
        bot.reply_to(message, "Please provide a stock symbol after the command. Example: /chungkhoan AAPL")
        return

    stock_symbol = command_text.split()[1].upper()  # Extract and convert to uppercase

    # Get the stock info from Yahoo Finance
    stock_info = get_stock_info(stock_symbol)

    # Send the stock info to the user
    bot.reply_to(message, stock_info)

# Run the bot
if __name__ == "__main__":
    print("Bot is running... Press Ctrl+C to stop.")
    bot.polling(none_stop=True, interval=0)
