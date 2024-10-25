import threading
import time

from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") #hier noch spezifizieren

def simulate_button_presses():
    while True:
        time.sleep(5)  # Warte 5 Sekunden
        button_name = 'Kobalt'  # Beispiel: Du kannst hier auch 'led2', 'led3', etc. verwenden.
        print(f"Simuliertes Button-Event: {button_name}")
        # Rufe die Funktion für ein simuliertes Button-Event auf
        socketio.emit('physical_button_pressed', button_name)

threading.Thread(target=simulate_button_presses, daemon=True).start()

#Von Website zu Raspberry
@socketio.on('activate_led')
def handle_activate_led(data):
    button_name = data.get('button', '').strip()
    print(f"LED {button_name} activated from web")
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
    #emit('led_status', {'led': led_name, 'status': 'activated'}, broadcast=True)

@socketio.on('physical_button_pressed')
def handle_physical_button(button_name):
    print(f"Physical button {button_name} pressed")
    # Informiere alle Clients über den Druck
    emit('led_status', {'button': button_name, 'status': 'activated'}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
    #with app.app_context():
    #socketio.emit('physical_button_pressed', 'Kobalt')

