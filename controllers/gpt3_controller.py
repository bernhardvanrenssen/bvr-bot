import openai
import json
from dotenv import load_dotenv
import os
from token_counter import TokenCounter

# Load environment variables from .env file
load_dotenv()

# Fetch the OpenAI API key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)

token_counter = TokenCounter()

def load_keywords_from_json(filename):
    """
    Reads the specified JSON file and extracts the list of keywords.
    """
    with open(filename, 'r') as file:
        data = json.load(file)
        
        keywords = []
        for section_key, section_data in data.items():
            for item_key, item_data in section_data.items():
                try:
                    keywords.extend(item_data['keywords'])
                except KeyError:
                    print(f"Error in data entry for {section_key} - {item_key}: {item_data}")
                
        print("RETURNING KEYWORDS:", keywords)
        return keywords

def gpt3_match_keywords(prompt):
    """
    Uses OpenAI's Davinci model to match the user's prompt against the extracted list of keywords.
    """
    filename = os.path.join(ROOT_DIR, 'data', 'data.json')

    try:
        token_counter.add_sent(len(prompt.split()))
        keyword_list = load_keywords_from_json(filename)
        formatted_keywords = ', '.join(keyword_list[:-1]) + " and " + keyword_list[-1]
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Given the list of keywords [{formatted_keywords}], which keyword(s) best relate to the user's input (maximum 5): \"{prompt}\"?",
            max_tokens=50
        )
        token_counter.add_received(response['usage']['total_tokens'])
        matched_keywords = response.choices[0].text.strip()
        return matched_keywords
    except Exception as e:
        print(f"Error while matching keywords: {e}")
        return None

def get_answer_by_keyword(keyword_string):
    print("INPUT KEYWORDS:", keyword_string)
    """
    Given a keyword string, the function will split it into individual keywords 
    and fetch the relevant answer from the data.json file.
    """

    filename = os.path.join(ROOT_DIR, 'data', 'data.json')

    # Load the data
    with open(filename, 'r') as file:
        data = json.load(file)

    # Ensure data is a dictionary
    if not isinstance(data, dict):
        raise ValueError("Expected a dictionary in data.json")

    # Extract the personal_profile dictionary
    personal_profile = data.get('personal_profile', {})
    #print("PERSONAL PROFILE:", personal_profile)

    # Split the input keyword string into individual keywords
    input_keywords = [k.strip() for k in keyword_string.split(",")]

    # Loop through sections in the personal profile
    for section, content in personal_profile.items():
        # Check if any of the input keywords exist in the keywords list
        if any(k in content['keywords'] for k in input_keywords):
            return content['answer']

    return "Im not sure I understand correctly, can you please rephrase the question"

def get_gpt3_response(prompt):
    '''This function calls the GPT-3 API and fetches a response for the given prompt'''
    token_counter.add_sent(len(prompt.split()))
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=150
    )
    token_counter.add_received(response['usage']['total_tokens'])
    return response.choices[0].text.strip()

def get_extended_answer_for_prompt(user_prompt):
    keyword_match = gpt3_match_keywords(user_prompt)
    raw_answer = get_answer_by_keyword(keyword_match)
    
    # Combine the raw_answer with the user's prompt to form a new prompt for GPT-3
    gpt3_prompt = f"User asked: {user_prompt}. Context: {raw_answer}. How would you respond?"
    
    # Fetch the response from GPT-3 based on the combined prompt
    gpt3_response = get_gpt3_response(gpt3_prompt)

    total_tokens = token_counter.display()

    print(f"Extracted Keyword: {answers['keyword']}")
    print(f"Raw Answer: {answers['raw_answer']}")
    print(f"GPT-3's Answer: {answers['gpt3_answer']}")

    return {
        'keyword': keyword_match,
        'raw_answer': raw_answer,
        'gpt3_answer': gpt3_response,
        'tokens': total_tokens
    }

# TEST ONLY THIS...
if __name__ == '__main__':
    user_prompt = input("Ask me a question: ")
    answers = get_extended_answer_for_prompt(user_prompt)
    print(f"Extracted Keyword: {answers['keyword']}")
    print(f"Raw Answer: {answers['raw_answer']}")
    print(f"GPT-3's Answer: {answers['gpt3_answer']}")
