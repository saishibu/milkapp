import os
import json
from flask import Flask, render_template, request
import plotly.graph_objects as go

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

@app.route('/purchase', methods=['POST'])
def milk_purchase():
    if request.method == 'POST':
        date = request.form['date']
        quantity = float(request.form['quantity'])
        total_cost = quantity * milk_cost_per_liter

        # Load existing purchase data, add new purchase, and save it back
        purchases = load_data(purchase_data_file)
        purchases.append({'date': date, 'quantity': quantity, 'total_cost': total_cost})
        save_data(purchases, purchase_data_file)

    return '', 204

@app.route('/payment', methods=['POST'])
def add_payment():
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])

        # Load existing payment data, add new payment, and save it back
        payments = load_data(payment_data_file)
        payments.append({'date': date, 'amount': amount})
        save_data(payments, payment_data_file)

    return '', 204

@app.route('/')
def display_data():
    # Load data for display
    purchases = load_data(purchase_data_file)
    payments = load_data(payment_data_file)

    # Calculate total purchases and total cost
    total_quantity = sum(item['quantity'] for item in purchases)
    total_cost = sum(item['total_cost'] for item in purchases)

    # Prepare data for the graphs
    purchase_dates = [item['date'] for item in purchases]
    quantities = [item['quantity'] for item in purchases]
    costs = [item['total_cost'] for item in purchases]

    # Generate the graphs
    quantity_graph = generate_quantity_graph(purchase_dates, quantities)
    cost_graph = generate_cost_graph(purchase_dates, costs)

    # Render the template with the graphs and data
    return render_template('milk_purchase.html', purchases=purchases, payments=payments,
                           total_quantity=total_quantity, total_cost=total_cost,
                           quantity_graph=quantity_graph, cost_graph=cost_graph)

@app.route('/clear_purchase', methods=['POST'])
def clear_purchase_history():
    # Clear purchase history by saving an empty list to the file
    save_data([], purchase_data_file)
    return '', 204

@app.route('/clear_payment', methods=['POST'])
def clear_payment_history():
    # Clear payment history by saving an empty list to the file
    save_data([], payment_data_file)
    return '', 204

def generate_quantity_graph(dates, quantities):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=quantities, mode='lines+markers', name='Milk Quantity (liters)'))
    fig.update_layout(title='Milk Quantity vs Date', xaxis_title='Date', yaxis_title='Milk Quantity (liters)')
    return fig.to_html()

def generate_cost_graph(dates, costs):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=costs, mode='lines+markers', name='Total Cost (Rs)', line=dict(color='red')))
    fig.update_layout(title='Total Cost vs Date', xaxis_title='Date', yaxis_title='Total Cost (Rs)')
    return fig.to_html()


if __name__ == '__main__':
    app.run(debug=True)
