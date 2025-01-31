//SocketIo Verbindung
const socket = io("http://192.168.2.140:5000");
var activeButton = null; // Speichert den aktuell aktiven Button
var timeoutID = null;    // Speichert das Timeout, um es später zu löschen

//Event-Listener für Verbindungsstatus
socket.on("connect", () => {
    console.log("Verbindung mit dem Server hergestellt");
});
socket.on("disconnect", () => {
    console.log("Verbindung zum Server getrennt");
});

// Empfangen von Button-Events vom Server (Knopf gedrückt) + verarbeiten
socket.on('button_pressed', function(data) {
    const buttonID = data.buttonID;
    console.log(`${buttonID} wurde auf dem Pi gedrückt`);
    console.log('button_pressed received:', data.buttonID);
    inhalteButtonAnzeigen(buttonID); //ruft Methode auf, um Länder auf Webseite anzuzeigen
});


//Event-Listener für Buttons auf der Webseite -> senden an funktion zum reagieren auf Server Seite
document.getElementById("buttonKobalt").addEventListener("click", function() {
    inhalteButtonAnzeigen('buttonKobalt', true); // true = Button wurde auf der Webseite gedrückt
});
document.getElementById("buttonTantal").addEventListener("click", function() {
    inhalteButtonAnzeigen('buttonTantal', true);
});
document.getElementById("buttonWolfram").addEventListener("click", function() {
    inhalteButtonAnzeigen('buttonWolfram', true);
});
document.getElementById("buttonZinn").addEventListener("click", function() {
    inhalteButtonAnzeigen('buttonZinn', true);
});

//neue funktion - kombiniert die InhalteButtonAnzeige zur Anzeige auf Webseite + ggf. senden der active_Led
// Allgemeine Funktion zur Anzeige der Inhalte
function inhalteButtonAnzeigen(buttonID, fromWebsite) {
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

    // Wenn der Button auf der Webseite gedrückt wurde, sende ein Event an den Server
    if (fromWebsite) {
        socket.emit('activate_led', { button: buttonID });
    }

    // Setze das Timeout, um den Button zurückzusetzen
    timeoutID = setTimeout(function() {
        resetButton(buttonID);
    }, 10000);
}
//Reset Funktion
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