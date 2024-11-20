from flask import Flask, render_template, request, jsonify
<<<<<<< HEAD
import requests  # Assurez-vous d'importer 'requests' et non 'request'
=======
import requests  
>>>>>>> a975af4e2af12457d2982f055058a38f569ffc64
import math
import time
import numpy as np
import decimal

app = Flask(__name__)

# Liste des nœuds disponibles
nodes = ['http://192.168.1.107:5001', 'http://192.168.1.119:5001']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/factorial', methods=['POST'])
def factorial():
    data = request.get_json()
    n = data['n']

    # Diviser la plage pour chaque nœud
    sub_ranges = np.array_split(range(1, n + 1), len(nodes))
    ranges = [(int(sub_range[0]), int(sub_range[-1])) for sub_range in sub_ranges]

    results = []

    # Envoyer la tâche de calcul à chaque nœud
    for i, (start, end) in enumerate(ranges):
        try:
            # Utiliser la bibliothèque 'requests' et non 'request'
            response = requests.post(
                f"{nodes[i]}/calculate",
                json={"start": start, "end": end},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                results.append(response.json())
                print(f"Réponse du nœud {nodes[i]}: {response.json()}")
            else:
                print(f"Erreur de réponse du nœud {nodes[i]}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la communication avec le nœud {nodes[i]}: {e}")

    # Calcul de la factorielle totale (en utilisant des chaînes pour de grands nombres)
    total_result = math.prod([int(result['partial_factorial']) for result in results])

    # Formater la factorielle pour éviter la notation scientifique
    total_result_str = str(total_result)  # Directement convertir en chaîne de caractères

    # Renvoi de la réponse sous forme JSON avec le temps de calcul
    return jsonify({"factorial": total_result_str, "calculation_time": 0.5})  # Exemple de calcul du temps de calcul

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
