function askChatGPT(prompt) {
  fetch('/ask-chatgpt', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt: prompt }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Assuming the response from the server contains the GPT-3 response in a property named 'text'
      const chatGptResponse = data.text;
      // Update the 'response' div with the ChatGPT response
      document.getElementById('response').innerText = chatGptResponse;
      // You may call a function here to read the response aloud
      readStoredText(); // Assuming this function reads the content of 'response' div
    })
    .catch((error) => {
      // Handle any errors here
      console.error('An error occurred:', error);
    });
}

// document.addEventListener('DOMContentLoaded', function() {
//   console.log('DOM is loaded'); // Check if this event is triggered
//   var outputText = document.getElementById('output').innerText;
//   console.log('Sending the following prompt to ChatGPT:', outputText); // Log the outputText
  //askChatGPT(outputText);
//});

