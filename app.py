from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

portfolio = []  # Temporary in-memory storage

@app.route('/stocks', methods=['POST'])
def add_stock():
    data = request.json
    symbol = data.get('symbol')
    quantity = data.get('quantity', 0)

    if not symbol or not quantity:
        return jsonify({'error': 'Stock symbol and quantity are required'}), 400
    
    # Fetch stock price using yfinance
    try:
        stock_data = yf.Ticker(symbol)
        stock_info = stock_data.history(period='1d').iloc[0]
        price = stock_info['Close']  # Use closing price for the stock
        if not price:
            return jsonify({'error': 'Unable to fetch stock price'}), 400
    except Exception as e:
        return jsonify({'error': f'Error fetching stock data: {str(e)}'}), 400
    
    # Debugging: Print price and quantity
    print(f"Adding stock: {symbol.upper()} - Price: {price}, Quantity: {quantity}")
    
    portfolio.append({'symbol': symbol.upper(), 'quantity': quantity, 'price': price})
    return jsonify({'message': 'Stock added successfully', 'portfolio': portfolio})

@app.route('/stocks', methods=['GET'])
def get_stocks():
    updated_portfolio = []
    for stock in portfolio:
        symbol = stock['symbol']
        quantity = stock['quantity']
        
        # Fetch stock data
        stock_data = yf.Ticker(symbol)
        price = stock_data.info.get('regularMarketPrice') or stock_data.info.get('previousClose')  # Fallback to previousClose
        value = price * quantity if price else 0  # If price is found, calculate value

        # Append stock info to the updated portfolio list
        updated_portfolio.append({
            'symbol': symbol,
            'quantity': quantity,
            'price': price if price else "N/A",  # Show N/A if no price
            'value': value if price else 0  # Show 0 if no price
        })
    
    return jsonify(updated_portfolio)



@app.route('/stocks/<symbol>', methods=['DELETE'])
def remove_stock(symbol):
    global portfolio
    portfolio = [stock for stock in portfolio if stock['symbol'] != symbol.upper()]
    return jsonify({'message': 'Stock removed successfully', 'portfolio': portfolio})

@app.route('/portfolio', methods=['GET'])
def get_portfolio_value():
    total_value = 0
    for stock in portfolio:
        quantity = stock['quantity']
        price = stock['price']
        total_value += price * quantity if price else 0
    return jsonify({'total_value': total_value})

if __name__ == '__main__':
    app.run(debug=True)
