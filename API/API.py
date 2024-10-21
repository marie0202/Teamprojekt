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
    data = request.get_json(force=True)  # Holt die Daten aus der Anfrage

    #.strip() entfernt Leerzeichen am Anfang / Ende des Strings, sonst funktioniert das IF nicht!
    led_name = data.get("led").strip()
    print(f"Received LED trigger for: {led_name}")

    if led_name == "led 1":
        print("Länder: 1,2,3")
    elif led_name == "led2":
        print("Länder 2,3")
    else:
        print("Länder 3")

    #Rückgabe an den Client
    return jsonify({"message": f"{led_name} triggered"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)
