from dotenv import load_dotenv
import os
import openai
from flask import Flask, request, jsonify, render_template
from controllers.gpt3_controller import gpt3_match_category, get_answer_by_keyword, get_gpt3_response
#from keyword_extractor_spacy import extract_keywords
from token_count import TokenCounter

app = Flask(__name__, static_url_path='', static_folder='static')

# Replace with your OpenAI API key
load_dotenv()  # This will load the .env file that's in the same directory as the script
api_key = os.environ['OPENAI_API_KEY']
openai_api_key = api_key = os.environ['OPENAI_API_KEY']
openai.api_key = openai_api_key

token_counter = TokenCounter()

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
      #engine="gpt-3.5-turbo",
      prompt=prompt,
      max_tokens=20
    )

    # Extract the text from the response
    text = response.choices[0].text

    # Return the text as JSON
    return jsonify({'text': text})

@app.route('/test-extract-keyword', methods=['POST'])   # New route for testing
def get_answer_for_prompt():
    '''This is for GPT-3 extraction'''
    prompt = request.json['prompt']

    global token_counter

    # Find the best matching category for the user's prompt
    keyword_match, token_counter = gpt3_match_category(prompt, token_counter)

    # Find the corresponding answer for the matched keyword
    raw_answer = get_answer_by_keyword(keyword_match)

    # Combine the raw_answer with the user's prompt to form a new prompt for GPT-3
    #gpt3_prompt = f"User asked: {prompt}. Context: {raw_answer}. How would you respond?"
    if raw_answer:
        gpt3_prompt = f"Based on this information: {raw_answer}, respond to {prompt} as if you are the individual mentioned. For instance, use 'I' to refer to the person described."
        print("FINAL GPT PROMPT:", gpt3_prompt)
        
        # Now, send this combined prompt to GPT-3 for a response
        gpt3_response, token_counter = get_gpt3_response(gpt3_prompt, token_counter)
        print("GPT3 RESPONSE:", gpt3_response)
    
        sent = token_counter.sent_tokens
        received = token_counter.received_tokens
        print("TOKEN COUNT:", sent, received)
    else:
        print("NOT A GOOD RESPONSE WAS FOUND:")
        return jsonify({
            'keyword': keyword_match,
            'raw_answer': 'No Match',
            'gpt3_answer': 'Im not sure I understand the question, could you please rephrase it?',
            'tokens_sent': 0,
            'tokens_received': 0
        })



    # Return the data
    return jsonify({
        'keyword': keyword_match,
        'raw_answer': raw_answer,
        'gpt3_answer': gpt3_response,
        'tokens_sent': sent,
        'tokens_received': received
    })
    


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
