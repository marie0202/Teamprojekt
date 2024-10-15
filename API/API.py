from flask import Flask, request, jsonify

app = Flask(__name__)

# Beispiel-Endpunkt für GET-Anfragen
#Um Daten abzurufen z.B. Zustand der LEDs (kommt aber als Info aktuell nicht von der Website
@app.route('/status', methods=['GET'])
def get_status():
    status = {"led1": "off", "led2": "on", "led3": "off"}
    return jsonify(status)

# Beispiel-Endpunkt für POST-Anfragen
#Um Daten an den Server zu senden & darauf änderungen vorzunehmen
@app.route('/trigger-led', methods=['POST'])
def trigger_led():
    data = request.get_json()  # Holt die Daten aus der Anfrage
    led_name = data.get("led")

    return jsonify({"message": f"{led_name} triggered"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
