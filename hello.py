from flask import Flask, request, jsonify, render_template
import requests
import os
from flask_cors import CORS
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://allowed-origin.com"}})
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/factorial', methods=['POST'])
def calculate_factorial():
    data = request.get_json()
    n = data['n']
    if n < 0:
        return jsonify({'error': 'n must be a non-negative integer'}), 400

    # Calculate factorial from 1 to n//2
    half = n // 2
    factorial_half = 1
    for i in range(1, half + 1):
        factorial_half *= i
    
    # Send the half result to the worker node
    worker_url = 'http://192.168.1.107:5001/calculate'
    response = requests.post(worker_url, json={'start': half + 1, 'end': n})
    if response.status_code == 200:
        factorial_worker = response.json()['partial_factorial']
        total_factorial = factorial_half * factorial_worker
        return jsonify({'factorial': total_factorial})
    else:
        return jsonify({'error': 'Error from worker node'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
