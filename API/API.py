from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    button_name = data.get("button").strip()
    print(f"Received LED trigger for: {button_name}")

    if button_name == "buttonKobalt":
        print("Kobalt")
    elif button_name == "buttonTantal":
        print("Tantal")
    elif button_name == "buttonWolfram":
        print("Wolfram")
    elif button_name == "buttonZinn":
        print("Zinn")
    else:
        print("Ungültiger Button!")

    #Rückgabe an den Client
    return jsonify({"message": f"{button_name} triggered"}), 200

if __name__ == '__main__':
    #To-Do: host="0.0.0.0", wenn Anfragen auch von anderen PCs kommen!
    app.run(host='127.0.0.1', port=5000,debug=True)
