const socket = io("http://192.168.2.116:5000");
var activeButton = null; // Speichert den aktuell aktiven Button
var timeoutID = null;    // Speichert das Timeout, um es später zu löschen

socket.on("connect", () => {
    console.log("Verbunden mit dem Server");
});

socket.on("server_message", (data) => {
    console.log("Nachricht erhalten:", data);
    document.getElementById("output").innerText = data.data;
});

socket.on("disconnect", () => {
    console.log("Verbindung getrennt");
});


    document.getElementById("buttonKobalt").addEventListener("click", function() {
        inhalteButtonAnzeigenVonWebsite('buttonKobalt');
    });
    document.getElementById("buttonTantal").addEventListener("click", function() {
        inhalteButtonAnzeigenVonWebsite('buttonTantal');
    });
    document.getElementById("buttonWolfram").addEventListener("click", function() {
        inhalteButtonAnzeigenVonWebsite('buttonWolfram');
    });
    document.getElementById("buttonZinn").addEventListener("click", function() {
        inhalteButtonAnzeigenVonWebsite('buttonZinn');
    });

    function inhalteButtonAnzeigenVonWebsite(buttonID){

        // Setze den vorherigen Button zurück, falls einer aktiv ist
        if (activeButton) {
            resetButton(activeButton);
        }
        // Setze den neuen aktiven Button
        activeButton = buttonID;

        var button = document.getElementById(buttonID);
        var elementRohstoff1 = 'element' + buttonID.substring(6) + '1';
        var elementRohstoff2 = 'element' + buttonID.substring(6) + '2';
        var elementRohstoff3 = 'element' + buttonID.substring(6) + '3';
        var textRohstoff = 'text' + buttonID.substring(6);

        button.style.backgroundColor = "darkgrey"; // Farbe ändern

        document.getElementById(elementRohstoff1).style.display = 'block';
        document.getElementById(elementRohstoff2).style.display = 'block';
        document.getElementById(elementRohstoff3).style.display = 'block';
        document.getElementById(textRohstoff).style.display = 'block';

        //Information an den Server senden (API)
        socket.emit('activate_led', { button: buttonID })
        /*fetch("http://127.0.0.1:5000/trigger-led", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ button: buttonID })
                })
            .then(response => response.json())
            .then(data => {console.log("Response:", data);})
            .catch(error => {console.error("Error:", error); });*/

        timeoutID = setTimeout(function() {
            resetButton(buttonID);
        }, 10000);
    }
function inhalteButtonAnzeigenVonPi(buttonID){
    // Setze den vorherigen Button zurück, falls einer aktiv ist
    if (activeButton) {
        resetButton(activeButton);
    }

    //Information vom Pi empfangen

    // Setze den neuen aktiven Button
    activeButton = buttonID;

    var button = document.getElementById(buttonID);
    var elementRohstoff1 = 'element' + buttonID.substring(6) + '1';
    var elementRohstoff2 = 'element' + buttonID.substring(6) + '2';
    var elementRohstoff3 = 'element' + buttonID.substring(6) + '3';
    var textRohstoff = 'text' + buttonID.substring(6);

    button.style.backgroundColor = "darkgrey"; // Farbe ändern

    document.getElementById(elementRohstoff1).style.display = 'block';
    document.getElementById(elementRohstoff2).style.display = 'block';
    document.getElementById(elementRohstoff3).style.display = 'block';
    document.getElementById(textRohstoff).style.display = 'block';

    timeoutID = setTimeout(function() {
        resetButton(buttonID);
    }, 10000);
}
socket.on('led_status', function(data) {
    console.log('LED ${data.button} ist ${data.status}');
    //inhalteButtonAnzeigenVonPi()
});
    function resetButton(buttonID) {
        // Setze die Farbe zurück
        var button = document.getElementById(buttonID);
        button.style.backgroundColor = "lightgray";

        // Alle zugehörigen Inhalte ausblenden
        document.querySelectorAll("[id^='element" + buttonID.replace('button', '') + "']").forEach(function(el) {
            el.style.display = 'none';
        });
        document.getElementById("text" + buttonID.replace('button', '')).style.display = 'none';

        // Setze die aktiven Variablen zurück
        activeButton = null;
        clearTimeout(timeoutID);
    }
// URL der API auf dem Raspberry Pi oder Server
const apiUrl = 'http://localhost:5000/receive-data';
//const apiUrl = 'http://<dein-raspberry-pi-ip>:5000/receive-data';

// Funktion zum Abrufen Daten von der API
/*async function fetchData() {
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ request: 'fetch' })
        });

        if (!response.ok) {
            throw new Error('Netzwerkantwort war nicht ok');
        }

        const data = await response.json();
        const dataString = json.dumps(data);
        inhalteButtonAnzeigen('button'+dataString, 'timerElement'+dataString+'1',
            'timerElement'+dataString+'2', 'timerElement'+dataString+'3',
            'timerText'+dataString);
    } catch (error) {
        console.error('Fehler beim Abrufen der Daten:', error);
        //document.getElementById('data-container').innerText = 'Fehler beim Laden der Daten.';
    }
}

// Beim Laden der Seite Daten abrufen
fetchData();*/