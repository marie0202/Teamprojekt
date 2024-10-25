from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") #hier noch spezifizieren


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
    emit('led_status', {'led': button_name, 'status': 'activated'}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
