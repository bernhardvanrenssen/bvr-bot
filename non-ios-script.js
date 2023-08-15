var artyomInstance;

document.addEventListener('DOMContentLoaded', function() {
    const startSpeechButton = document.getElementById('startSpeech');
    const speechOutput = document.getElementById('speechOutput');
    const debugOutput = document.getElementById('debug');
    const lastDebugOutput = document.getElementById('lastDebug');
    const testButton = document.getElementById('testSound');
    const testSound = new Audio('https://www.xrai.co.za/webar/test-sound.mp3');
    const enterARButton = document.getElementById('enterAR');
    const modelViewer = document.getElementById('modelViewer');

    let silenceTimer;

    // Artyom initialization function
    function initializeArtyom() {
        var artyom = new Artyom();
        artyom.initialize({
            lang: "en-US",
            continuous: true,
            debug: true,
            listen: true
        }).then(() => {
            console.log("Artyom has been correctly initialized");
        }).catch((err) => {
            console.error("Artyom couldn't be initialized: ", err);
        });
        return artyom;
    }

    // Function to handle Artyom commands
    function startArtyom() {
        var artyom = initializeArtyom();
        artyom.addCommands([
            {
                indexes: ["*"],
                smart: true,
                action: function(i, transcript) {
                    clearTimeout(silenceTimer); // Clear the existing timer
                    speechOutput.innerText += transcript + ' ';
                    updateDebug(transcript);
                    lastDebugOutput.innerText = transcript; // Update the last recognized message

                    // Set a new timer
                    silenceTimer = setTimeout(function() {
                        debugOutput.innerText = 'Event fired';
                    }, 3000);
                }
            }
        ]);

        // Initial 3-second timer setup
        silenceTimer = setTimeout(function() {
            debugOutput.innerText = 'Event fired';
        }, 3000);
    }

    function updateDebug(message) {
        lastDebugOutput.innerText = debugOutput.innerText;
        debugOutput.innerText = message;
    }

    function stopArtyom() {
        console.log("CALLED STOP!!");
        //if (artyomInstance) {
        artyomInstance.fatality();
        console.log("Artyom stopped");
        //}
    }

    window.stopArtyom = stopArtyom;

    // Event listener for the AR button
    if (enterARButton && modelViewer) {
        enterARButton.addEventListener('click', function() {
            modelViewer.activateAR();
            startArtyom();
        });
    }

    startSpeechButton.addEventListener('click', function() {
        startArtyom();
    });

    testButton.addEventListener('click', function() {
        testSound.play();
    });
});
