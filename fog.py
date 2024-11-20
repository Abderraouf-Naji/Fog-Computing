from flask import Flask, request, jsonify
import requests
import numpy as np
import math

app = Flask(__name__)

# List of nodes (replace with the actual IP addresses of your nodes)
nodes = ['http://10.26.14.209:5001']

@app.route('/factorial', methods=['POST'])
def factorial():
    data = request.get_json()
    n = data['n']

    # Divide the factorial range equally among all nodes
    # For example, if n = 6 and there are 2 nodes, the ranges would be [1, 3] and [4, 6]
    sub_ranges = np.array_split(range(1, n + 1), len(nodes))
    ranges = [(sub_ranges[i][0], sub_ranges[i][-1]) for i in range(len(nodes))]

    results = []

    # Send the factorial task to each node
    for i, (start, end) in enumerate(ranges):
        try:
            response = requests.post(
                f"{nodes[i]}/calculate",
                json={"start": start, "end": end},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                results.append(response.json())
                print(f"Response from {nodes[i]}: {response.json()}")
            else:
                print(f"Failed to get a response from {nodes[i]}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with {nodes[i]}: {e}")

    # Multiply the results from each node to get the final factorial result
    total_result = math.prod([result['partial_factorial'] for result in results])

    return jsonify({"factorial": total_result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
