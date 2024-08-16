"""
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# File paths for JSON storage
WALLET_FILE = 'wallets.json'
TRANSACTION_FILE = 'transactions.json'

# Helper functions to load and save data
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# API to create a wallet
@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    data = request.json
    user_id = data['user_id']
    pin = data['pin']
    initial_balance = data.get('initial_balance', 0.0)
    
    wallets = load_json(WALLET_FILE)
    if user_id in wallets:
        return jsonify({"message": "Wallet already exists."}), 400
    
    wallets[user_id] = {
        "balance": initial_balance,
        "pin": pin
    }
    save_json(WALLET_FILE, wallets)
    return jsonify({"message": "Wallet created successfully."})

# API to get balance
@app.route('/balance/<user_id>', methods=['GET'])
def get_balance(user_id):
    wallets = load_json(WALLET_FILE)
    if user_id in wallets:
        return jsonify({"balance": wallets[user_id]['balance']})
    return jsonify({"message": "Wallet not found."}), 404

# API to perform a transaction (credit or debit)
@app.route('/transaction', methods=['POST'])
def perform_transaction():
    data = request.json
    user_id = data['user_id']
    amount = data['amount']
    transaction_type = data['type']
    pin = data['pin']
    
    wallets = load_json(WALLET_FILE)
    if user_id not in wallets or wallets[user_id]['pin'] != pin:
        return jsonify({"message": "Invalid wallet or PIN."}), 400
    
    if transaction_type == 'debit' and wallets[user_id]['balance'] < amount:
        return jsonify({"message": "Insufficient balance."}), 400
    
    if transaction_type == 'credit':
        wallets[user_id]['balance'] += amount
    else:
        wallets[user_id]['balance'] -= amount
    
    transactions = load_json(TRANSACTION_FILE)
    if user_id not in transactions:
        transactions[user_id] = []
    
    transactions[user_id].append({
        "amount": amount,
        "type": transaction_type,
        "date": "2024-08-15"  # Placeholder for date
    })
    
    save_json(WALLET_FILE, wallets)
    save_json(TRANSACTION_FILE, transactions)
    
    return jsonify({"message": f"{transaction_type.capitalize()} of ${amount} successful."})

# API to get transaction history
@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    transactions = load_json(TRANSACTION_FILE)
    if user_id in transactions:
        return jsonify({"history": transactions[user_id]})
    return jsonify({"message": "No transactions found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
"""

import json
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# File paths for JSON storage
WALLET_FILE = 'wallets.json'
TRANSACTION_FILE = 'transactions.json'

# Helper functions to load and save data
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Serve the HTML page
@app.route('/')
def serve_ui():
    return send_from_directory('.', 'index.html')

# Serve static files like CSS and JS
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('.', path)

# API to create a wallet
@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    data = request.json
    user_id = data['user_id']
    pin = data['pin']
    initial_balance = data.get('initial_balance', 0.0)
    
    wallets = load_json(WALLET_FILE)
    if user_id in wallets:
        return jsonify({"message": "Wallet already exists."}), 400
    
    wallets[user_id] = {
        "balance": initial_balance,
        "pin": pin
    }
    save_json(WALLET_FILE, wallets)
    return jsonify({"message": "Wallet created successfully."})

# API to get balance
@app.route('/balance/<user_id>', methods=['GET'])
def get_balance(user_id):
    wallets = load_json(WALLET_FILE)
    if user_id in wallets:
        return jsonify({"balance": wallets[user_id]['balance']})
    return jsonify({"message": "Wallet not found."}), 404

# API to perform a transaction (credit or debit)
@app.route('/transaction', methods=['POST'])
def perform_transaction():
    data = request.json
    user_id = data['user_id']
    amount = data['amount']
    transaction_type = data['type']
    pin = data['pin']
    
    wallets = load_json(WALLET_FILE)
    if user_id not in wallets or wallets[user_id]['pin'] != pin:
        return jsonify({"message": "Invalid wallet or PIN."}), 400
    
    if transaction_type == 'debit' and wallets[user_id]['balance'] < amount:
        return jsonify({"message": "Insufficient balance."}), 400
    
    if transaction_type == 'credit':
        wallets[user_id]['balance'] += amount
    else:
        wallets[user_id]['balance'] -= amount
    
    transactions = load_json(TRANSACTION_FILE)
    if user_id not in transactions:
        transactions[user_id] = []
    
    transactions[user_id].append({
        "amount": amount,
        "type": transaction_type,
        "date": "2024-08-15"  # Placeholder for date, you can replace with the current date
    })
    
    save_json(WALLET_FILE, wallets)
    save_json(TRANSACTION_FILE, transactions)
    
    return jsonify({"message": f"{transaction_type.capitalize()} of ${amount} successful."})

# API to get transaction history
@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    transactions = load_json(TRANSACTION_FILE)
    if user_id in transactions:
        return jsonify({"history": transactions[user_id]})
    return jsonify({"message": "No transactions found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
