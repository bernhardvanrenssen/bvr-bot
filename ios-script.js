document.addEventListener('DOMContentLoaded', function() {
  const startSpeechButton = document.getElementById('startSpeech');
  const speechOutput = document.getElementById('speechOutput');
  const debugOutput = document.getElementById('debug');
  const lastDebugOutput = document.getElementById('lastDebug');
  const testButton = document.getElementById('testSound');
  const testSound = new Audio('https://www.xrai.co.za/webar/test-sound.mp3');
  const enterARButton = document.getElementById('enterAR');
  const modelViewer = document.getElementById('modelViewer');

  let recognition;
  let silenceTimer;
  let interimTranscript = '';


    // Event listener for the AR button
  if (enterARButton && modelViewer) {
      enterARButton.addEventListener('click', function() {
      // Manually trigger AR mode
      modelViewer.activateAR();
  
      // Start speech recognition when the AR button is clicked
      if (recognition) {
          recognition.stop();
      }
      startRecognition();
      });
  }

  function startRecognition() {
      recognition = new webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onstart = function() {
          speechOutput.innerText = 'Listening...';
          startSpeechButton.disabled = true;
      };

      recognition.onend = function() {
          startSpeechButton.disabled = false; // Enable the button when listening ends
      };

      recognition.onresult = handleResult;

      recognition.start();
  }

  function updateDebug(message) {
      lastDebugOutput.innerText = debugOutput.innerText; // Store the previous debug message
      debugOutput.innerText = message; // Update with the current debug message
  }

  function handleResult(event) {
      interimTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
              speechOutput.innerText += transcript + ' ';
              updateDebug(transcript);
          } else {
              interimTranscript = transcript;
              updateDebug(interimTranscript);
          }
      }

      // clearTimeout(silenceTimer);
      // silenceTimer = setTimeout(function() {
      //     speechOutput.innerText += interimTranscript + ' ';
      //     const debugMessage = 'Event fired'; // Updated message
      //     updateDebug(debugMessage);
      //     //playTestSound(); // Call the function to play the test sound
      //     recognition.stop(); // Stops the current recognition
      // }, 3000);
  }

  if ('webkitSpeechRecognition' in window) {
      //startRecognition();

      startSpeechButton.addEventListener('click', function() {
          if (recognition) {
              recognition.stop(); // Stops the current recognition when the button is clicked
          }
          startRecognition(); // Starts recognition again
      });

      testButton.addEventListener('click', function() {
          testSound.play();
      });
  } else {
      speechOutput.innerText = 'Your browser does not support the Web Speech API.';
  }

  if (modelViewer) {
      modelViewer.addEventListener('ar-status', function(event) {
        if (event.detail.status === 'session-started') {
          // Start speech recognition when entering AR mode
          startRecognition();
        }
      });
    }
  
    // Ensure the Start Speech Recognition button is not pressed by default
    if (recognition) {
      recognition.stop();
      startSpeechButton.disabled = false;
  }
});
