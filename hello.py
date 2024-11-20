from flask import Flask, request, jsonify
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autoriser CORS pour toutes les routes

@app.route('/calculate', methods=['POST'])
def calculate_partial_factorial():
    try:
        # Récupérer les données JSON
        data = request.get_json()
        start = data.get('start')
        end = data.get('end')

        # Validation des données
        if not (isinstance(start, int) and isinstance(end, int)) or start > end:
            return jsonify({'error': 'Invalid range'}), 400

        # Calcul du factoriel partiel
        partial_factorial = 1
        for i in range(start, end + 1):
            partial_factorial *= i

        return jsonify({'partial_factorial': partial_factorial})

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)