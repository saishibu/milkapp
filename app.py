import os
import json
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# File path to store the purchase data
data_file = 'purchase_data.json'

# Cost of 1L of milk
milk_cost_per_liter = 60

def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file)

def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def generate_graph(dates, quantities, costs):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(dates, quantities, 'g-')
    ax2.plot(dates, costs, 'b-')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Milk Quantity (liters)', color='g')
    ax2.set_ylabel('Total Cost (Rs)', color='b')
    plt.xticks(rotation=45)
    plt.title('Milk Quantity and Cost vs Date')

    # Save the graph to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode the graph as base64 and return the string
    graph_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return graph_base64

@app.route('/', methods=['GET', 'POST'])
def milk_purchase():
    if request.method == 'POST':
        date = request.form['date']
        quantity = float(request.form['quantity'])
        total_cost = quantity * milk_cost_per_liter

        # Load existing data, add new purchase, and save it back
        purchases = load_data()
        purchases.append({'date': date, 'quantity': quantity, 'total_cost': total_cost})
        save_data(purchases)

    # Load data for display
    purchases = load_data()

    # Calculate total purchases and total cost
    total_quantity = sum(item['quantity'] for item in purchases)
    total_cost = sum(item['total_cost'] for item in purchases)

    # Prepare data for the graph
    dates = [item['date'] for item in purchases]
    quantities = [item['quantity'] for item in purchases]
    costs = [item['total_cost'] for item in purchases]

    # Generate the graph and get the base64 string
    graph = generate_graph(dates, quantities, costs)

    # Render the template with the graph
    return render_template('milk_purchase.html', purchases=purchases, total_quantity=total_quantity, total_cost=total_cost, graph=graph)

@app.route('/clear', methods=['POST'])
def clear_purchase_history():
    # Clear the purchase history by overwriting the data file
    save_data([])
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
