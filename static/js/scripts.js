document.addEventListener('DOMContentLoaded', (event) => {
    const modelViewer = document.getElementById('modelViewer');

    // Check if the device is iOS
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;

    if (isIOS) {
        // Modify the attributes for iOS
        modelViewer.setAttribute('ar-scale', 'auto');
        modelViewer.setAttribute('ar-modes', 'quick-look webxr scene-viewer');
        modelViewer.setAttribute('src', '/static/models/bvr_avatar_ios.glb');
    }
});

    const enterARButton = document.getElementById('enterAR');
    const initializeSpeech = document.getElementById('initializeSpeech');
    const modelViewer = document.getElementById('modelViewer');
    const startButton = document.getElementById('startButton');
    const output = document.getElementById('output');
    const response = document.getElementById('response');
    const testSound = new Audio('https://www.xrai.co.za/webar/test-sound.mp3');

    // Testing the prompt stuff
    const testKeywordButton = document.getElementById('testKeywordButton');
    const keywordTestInput = document.getElementById('keywordTestInput');
    const keywordResult = document.getElementById('keywordResult');
    const promptAnswer = document.getElementById('promptAnswer');
    const gpt3Answer = document.getElementById('gpt3Answer');
    const totalTokens = document.getElementById('totalTokens');
    
    testKeywordButton.addEventListener('click', function() {
        const prompt = keywordTestInput.value;

        fetch('/test-extract-keyword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt })
        })
        .then(response => {
            if(!response.ok) throw new Error('Network response was not ok' + response.statusText);
            return response.json();
        })
        .then(data => {
            console.log("AM I GETTING RESPONSE?", data);
            keywordResult.innerText = "Extracted keyword: " + data.keyword;
            promptAnswer.innerText = "Raw answer: " + data.raw_answer;
            gpt3Answer.innerText = data.gpt3_answer;
            totalTokens.innerText  = 'Sent: ' + data.tokens_sent + ' Received: ' + data.tokens_received;
    
            // Call the readStoredText function directly here since you have received the data
            readStoredText();
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle errors appropriately, possibly updating the UI to inform the user.
        });
    });

    // End of Test

    let artyomInstance;
    let silenceTimer;

    document.getElementById('initializeSpeech').addEventListener('click', function() {
        const silentUtterance = new SpeechSynthesisUtterance('');
        window.speechSynthesis.speak(silentUtterance);
        // Optionally, enable the Read Text button here, if it's initially disabled
        document.getElementById('readTextButton').disabled = false;
        document.getElementById('enterAR').disabled = false;
        startArtyom();

        fetch('/button-pressed', {
            method: 'POST'
        }).then(response => response.json()).then(data => {
            console.log(data.message);
        }).catch(error => {
            console.error('Error:', error);
        });
    });

    const stopButton = document.getElementById('stopButton');
    stopButton.addEventListener('click', function() {
        stopArtyom();
    });

    function initializeArtyom() {
        artyomInstance = new Artyom();
        artyomInstance.initialize({
            lang: "en-US",
            continuous: true,
            debug: true,
            listen: true
        }).then(() => {
            console.log("Artyom has been correctly initialized");
        }).catch((err) => {
            console.error("Artyom couldn't be initialized: ", err);
        });
        return artyomInstance;
    }

    if (enterARButton && modelViewer) {
        enterARButton.addEventListener('click', function() {
            modelViewer.activateAR();
            //startArtyom();
            initializeSpeech.click();
        });
    }

    function startArtyom() {
        console.log("STARTING ARTYOM");
        var artyom = initializeArtyom();
        artyom.addCommands([
            {
                indexes: ["*"],
                smart: true,
                action: function(i, transcript) {
                    clearTimeout(silenceTimer);
                    silenceTimer = setTimeout(function() {
                        processTranscript(transcript);
                    }, 2000);
                }
            }
        ]);
            // Disable stop button initially
        const stopButton = document.getElementById('stopButton');
        //stopButton.disabled = true;

        // Enable stop button after 2 seconds
        setTimeout(() => {
            stopButton.disabled = false;
        }, 2000);
    }

    function stopArtyom() {
        if (artyomInstance) {
            artyomInstance.fatality();
            setTimeout(() => {
                artyomInstance.initialize({
                    lang: "en-US",
                    continuous: false,
                    debug: true,
                    listen: false
                });
            }, 250);
            console.log("Artyom stopped");
        }
    }

    function processTranscript(transcript) {
        var promptWithAppend = transcript;
        console.log("This is the prompt:", promptWithAppend);
        output.innerText = promptWithAppend;
        //readBack(transcript);
        stopArtyom();
        keywordTestInput.value = promptWithAppend
        testKeywordButton.click();
        //testSound.play();
        //setTimeout(readStoredText, 1000);
        //askChatGPT(promptWithAppend);
    }

    function readStoredText() {
        readBack(gpt3Answer.innerText);
    }

    function readBack(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onend = function() {
            //startArtyom(); // Start listening again once the speech has finished
            console.log("IT SHOULD START HERE AGAIN");
            setTimeout(startArtyom, 1000);
        };
        window.speechSynthesis.speak(utterance);
    }

    readTextButton.addEventListener('click', function() {
        readBack(output.innerText);
    });
