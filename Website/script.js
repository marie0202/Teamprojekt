var activeButton = null; // Speichert den aktuell aktiven Button
    var timeoutID = null;    // Speichert das Timeout, um es später zu löschen

    document.getElementById("buttonKobalt").addEventListener("click", function() {
        inhalteButtonAnzeigen('buttonKobalt', 'timerElementKobalt1', 'timerElementKobalt2', 'timerElementKobalt3', 'timerTextKobalt');
    });
    document.getElementById("buttonTantal").addEventListener("click", function() {
        inhalteButtonAnzeigen('buttonTantal', 'timerElementTantal1', 'timerElementTantal2', 'timerElementTantal3', 'timerTextTantal');
    });
    document.getElementById("buttonWolfram").addEventListener("click", function() {
        inhalteButtonAnzeigen('buttonWolfram', 'timerElementWolfram1', 'timerElementWolfram2', 'timerElementWolfram3', 'timerTextWolfram');
    });
    document.getElementById("buttonZinn").addEventListener("click", function() {
        inhalteButtonAnzeigen('buttonZinn', 'timerElementZinn1', 'timerElementZinn2', 'timerElementZinn3', 'timerTextZinn');
    });
    function inhalteButtonAnzeigen(buttonID, elementRohstoff1, elementRohstoff2, elementRohstoff3, textRohstoff){
        // Setze den vorherigen Button zurück, falls einer aktiv ist
        if (activeButton) {
            resetButton(activeButton);
        }
        // Setze den neuen aktiven Button
        activeButton = buttonID;

        var button = document.getElementById(buttonID);
        button.style.backgroundColor = "darkgrey"; // Farbe ändern

        document.getElementById(elementRohstoff1).style.display = 'block';
        document.getElementById(elementRohstoff2).style.display = 'block';
        document.getElementById(elementRohstoff3).style.display = 'block';
        document.getElementById(textRohstoff).style.display = 'block';

        //Information an den Server senden (API)
        fetch("http://127.0.0.1:5000/trigger-led", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ button: buttonID })
                })
            .then(response => response.json())
            .then(data => {console.log("Response:", data);})
            .catch(error => {console.error("Error:", error); });

        timeoutID = setTimeout(function() {
            resetButton(buttonID);
        }, 10000);
    }
    function resetButton(buttonID) {
        // Setze die Farbe zurück
        var button = document.getElementById(buttonID);
        button.style.backgroundColor = "lightgray";

        // Alle zugehörigen Inhalte ausblenden
        document.querySelectorAll("[id^='timerElement" + buttonID.replace('button', '') + "']").forEach(function(el) {
            el.style.display = 'none';
        });
        document.getElementById("timerText" + buttonID.replace('button', '')).style.display = 'none';

        // Setze die aktiven Variablen zurück
        activeButton = null;
        clearTimeout(timeoutID);
    }