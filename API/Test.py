import requests

url = "http://localhost:5000/receive-data"  # Die URL der API
data = {
    "Kobalt"
}

try:
    response = requests.post(url, json=data)  # Senden der POST-Anfrage an die API
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())  # Antwort der API anzeigen
except requests.exceptions.RequestException as e:
    print("Fehler bei der Anfrage:", e)

