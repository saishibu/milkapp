import os
import json
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# File paths to store purchase data and payment data
purchase_data_file = 'purchase_data.json'
payment_data_file = 'payment_data.json'

# Cost of 1L of milk
milk_cost_per_liter = 60

def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

@app.route('/', methods=['GET', 'POST'])
def milk_purchase():
    if request.method == 'POST':
        date = request.form['date']
        quantity = float(request.form['quantity'])
        total_cost = quantity * milk_cost_per_liter

        # Load existing purchase data, add new purchase, and save it back
        purchases = load_data(purchase_data_file)
        purchases.append({'date': date, 'quantity': quantity, 'total_cost': total_cost})
        save_data(purchases, purchase_data_file)

    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])

        # Load existing payment data, add new payment, and save it back
        payments = load_data(payment_data_file)
        payments.append({'date': date, 'amount': amount})
        save_data(payments, payment_data_file)

    # Load data for display
    purchases = load_data(purchase_data_file)
    payments = load_data(payment_data_file)

    # Calculate total purchases and total cost
    total_quantity = sum(item['quantity'] for item in purchases)
    total_cost = sum(item['total_cost'] for item in purchases)

    # Prepare data for the graph
    purchase_dates = [item['date'] for item in purchases]
    quantities = [item['quantity'] for item in purchases]
    costs = [item['total_cost'] for item in purchases]

    # Generate the graph and get the base64 string
    graph = generate_graph(purchase_dates, quantities, costs)

    # Render the template with the graph and data
    return render_template('milk_purchase.html', purchases=purchases, payments=payments,
                           total_quantity=total_quantity, total_cost=total_cost, graph=graph)

def generate_graph(dates, quantities, costs):
    # ... (previous code, unchanged)

if __name__ == '__main__':
    app.run(debug=True)

    # graph = generate_graph(dates, quantities, costs)

    # # Render the template with the graph
    # return render_template('milk_purchase.html', purchases=purchases, total_quantity=total_quantity, total_cost=total_cost, graph=graph)

@app.route('/clear', methods=['POST'])
def clear_purchase_history():
    # Clear the purchase history by overwriting the data file
    save_data([])
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
