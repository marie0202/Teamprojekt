import time
import logging
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import RPi.GPIO as GPIO
from gpiozero import LED
import sys

# Flask- und SocketIO-Setup
app = Flask(__name__)
CORS(app) #Cors für alle Routen aktivieren
socketio = SocketIO(app, cors_allowed_origins="*")

# Logging-Setup
logging.basicConfig(level=logging.DEBUG)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
button_pins = [26, 19, 13, 6]

leds = {
    'Indonesien': LED(21),
    'Vietnam': LED(20),
    'Russland': LED(16),
    'China': LED(12),
    'Ruanda': LED(7),
    'Kongo': LED(8),
    'Peru': LED(25),
    'Brasilien': LED(9)
}
for pin in button_pins:
    try:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        pin_state = GPIO.input(pin)
        logging.info(f"Pin {pin} Zustand: {pin_state} (korrekt: 1 -> Pin nicht gedrückt")
    except Exception as e:
        logging.exception(f"Fehler in Pin Set-Up für Pin {pin}: {e}")

# WebSocket-Handler für Web-Events
@socketio.on("connect")
def handle_connect():
    logging.info("Client verbunden!")

def read_buttons():
    pressed_buttons = []
    for i, pin in enumerate(button_pins):
        if GPIO.input(pin) == GPIO.LOW:
            pressed_buttons.append(i + 1)
    return pressed_buttons

# WebSocket Event-Handler
@socketio.on('activate_led')
def handle_activate_led(data):
    button_name = data.get('button', '').strip()
    logging.info(f"{button_name} activated from web")
    if button_name == "buttonKobalt":
        active_led('Kobalt')
    elif button_name == "buttonTantal":
        active_led('Tantal')
    elif button_name == "buttonWolfram":
        active_led('Wolfram')
    elif button_name == "buttonZinn":
        active_led('Zinn')
    else:
        print("Ungültiger Button!")


# LED-Logik
def active_led(button_name):
    try:
        logging.info(f"LED {button_name} aktiviert")
        leds_to_activate = {
            'Kobalt': ['Kongo', 'China', 'Russland'],
            'Tantal': ['Ruanda', 'Kongo', 'Brasilien'],
            'Wolfram': ['China', 'Vietnam', 'Russland'],
            'Zinn': ['China', 'Peru', 'Indonesien']
        }

        for led_name in leds_to_activate.get(button_name, []):
            leds[led_name].on()

        time.sleep(2)

        for led_name in leds_to_activate.get(button_name, []):
            leds[led_name].off()

    except Exception as e:
        logging.exception(f"Fehler beim Aktivieren der LED für {button_name}: {e}")

# Überwachung der physischen Buttons & senden an Webseite
def control_buttons():
    while True:
        try:
            button_number = read_buttons()
            if 1 in button_number:
                button_name = 'buttonTantal'
                logging.info(f"{button_name} activated physically")
                active_led(button_name.replace('button', ''))
                socketio.emit("button_pressed", {"buttonID": button_name})
                logging.info(f"WebSocket Event für {button_name} gesendet")
            if 2 in button_number:
                button_name = 'buttonKobalt'
                logging.info(f"{button_name} activated physically")
                active_led(button_name.replace('button', ''))
                socketio.emit("button_pressed", {"buttonID": button_name})
                logging.info(f"WebSocket Event für {button_name} gesendet")
            if 3 in button_number:
                button_name = 'buttonZinn'
                logging.info(f"{button_name} activated physically")
                active_led(button_name.replace('button', ''))
                socketio.emit("button_pressed", {"buttonID": button_name})
                logging.info(f"WebSocket Event für {button_name} gesendet")
            if 4 in button_number:
                button_name = 'buttonWolfram'
                logging.info(f"{button_name} activated physically")
                active_led(button_name.replace('button', ''))
                socketio.emit("button_pressed", {"buttonID": button_name})
                logging.info(f"WebSocket Event für {button_name} gesendet")

            socketio.sleep(0.1)

        except Exception as e:
            logging.exception("Fehler in der Button-Steuerung")

# Hauptprogramm
if __name__ == "__main__":
    try:
        logging.info("Starte WebSocket Server...")
        socketio.start_background_task(control_buttons)
        socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)

    except KeyboardInterrupt:
        logging.info("Programm wird beendet...")
    finally:
        GPIO.cleanup()
        sys.exit()
