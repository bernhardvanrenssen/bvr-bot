from dotenv import load_dotenv
import os
import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_url_path='', static_folder='static')

# Replace with your OpenAI API key
load_dotenv()  # This will load the .env file that's in the same directory as the script
api_key = os.environ['OPENAI_API_KEY']
openai_api_key = api_key = os.environ['OPENAI_API_KEY']
openai.api_key = openai_api_key

@app.route('/')
def index():
    return render_template('index.html') # This serves the index.html file

@app.route('/ask-chatgpt', methods=['POST'])
def ask_chatgpt():
    # Get the prompt from the request body
    prompt = request.json['prompt']
    
    # Send the prompt to OpenAI's GPT model
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=20
    )

    # Extract the text from the response
    text = response.choices[0].text

    # Return the text as JSON
    return jsonify({'text': text})

@app.route('/static/<path:path>')  # Add this route
def serve_static(path):
    print("Serving static file:", path)  # Debugging line
    return app.send_static_file(path)

@app.route('/button-pressed', methods=['POST'])
def button_pressed():
    # Log the button press to the console
    print("Initialize Speech button was pressed!")
    return jsonify({'message': 'Button press received'})


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
