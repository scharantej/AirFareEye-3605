
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'topsecret'

flights = {
    'Tokyo': {
        'price': 500,
        'departure_date': '2023-03-08',
        'return_date': '2023-03-15',
    },
    'Singapore': {
        'price': 400,
        'departure_date': '2023-03-10',
        'return_date': '2023-03-17',
    },
    'Seoul': {
        'price': 600,
        'departure_date': '2023-03-12',
        'return_date': '2023-03-19',
    },
    'Taipei': {
        'price': 550,
        'departure_date': '2023-03-14',
        'return_date': '2023-03-21',
    },
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        origin = request.form.get('origin')
        destinations = request.form.getlist('destinations')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')

        # Exclude results from "Spring Airlines"
        for destination in destinations:
            flights[destination]['price'] = get_price(origin, destination, departure_date, return_date)

        # Capture the cheapest price for each destination
        cheapest_prices = {destination: flights[destination]['price'] for destination in destinations}

        # Generate an HTML table with the updated flight data
        table = generate_table(cheapest_prices)

        return render_template('index.html', table=table)

    return render_template('index.html')

@app.route('/refresh', methods=['GET'])
def refresh():
    for destination in flights:
        flights[destination]['price'] = get_price('Shanghai', destination, datetime.now().strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'))

    table = generate_table({destination: flights[destination]['price'] for destination in flights})

    return make_response(table)

def get_price(origin, destination, departure_date, return_date):
    # Make a request to an external API to retrieve flight data
    response = requests.get('https://example.com/api/flights', params={
        'origin': origin,
        'destination': destination,
        'departure_date': departure_date,
        'return_date': return_date,
    })

    # Parse the flight data and capture the cheapest price
    data = response.json()
    prices = [flight['price'] for flight in data['flights'] if flight['airline'] != 'Spring Airlines']
    cheapest_price = min(prices) if prices else None

    return cheapest_price

def generate_table(prices):
    table = '<table border="1">'
    table += '<tr><th>Destination</th><th>Price</th></tr>'
    for destination, price in prices.items():
        table += f'<tr><td>{destination}</td><td>{price}</td></tr>'
    table += '</table>'

    return table

if __name__ == '__main__':
    app.run()
