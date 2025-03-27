from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Ziel-URL, an die die Daten weitergeleitet werden sollen
TARGET_URL = "https://marie0202.github.io/Teamprojekt/"  # URL der Website

@app.route('/receive-data', methods=['POST'])
def receive_data():
    # Daten von Raspberry Pi empfangen
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Leite die Daten an die Ziel-Website weiter
    try:
        response = requests.post(TARGET_URL, json=data)
        response.raise_for_status()  # Falls ein HTTP-Fehler auftritt, wird eine Exception ausgelöst
        return jsonify({"status": "success", "forwarded": data}), 200
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Weiterleiten der Daten: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # Auf allen Interfaces des Raspberry Pi laufen lassen
