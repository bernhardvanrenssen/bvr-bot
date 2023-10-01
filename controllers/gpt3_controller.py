import openai
import json
from dotenv import load_dotenv
import os
from token_count import TokenCounter

# Load environment variables from .env file
load_dotenv()

# Fetch the OpenAI API key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)

def load_keywords_from_json(filename, query):
    """
    Reads the specified JSON file and extracts the list of keywords.
    First determine which category it belongs to
    """
    with open(filename, 'r') as file:
        data = json.load(file)

        #categories = list(data.keys())
        categories = []
        for section_key, section_data in data.items():
            categories.extend(section_data.keys())
        prompt = f"I have the following categories: {', '.join(categories)}. Based on the question '{query}', which category does it best match? Please respond with ONLY the category name."
        print("MY CATEGORIES ", categories)
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=20)
        category = response.choices[0].text.strip()
        print("THIS CATEGORY MATCHES THE QUESTION:", category)
        
        keywords = []
        for section_key, section_data in data.items():
            for item_key, item_data in section_data.items():
                try:
                    keywords.extend(item_data['keywords'])
                except KeyError:
                    print(f"Error in data entry for {section_key} - {item_key}: {item_data}")
                
        return keywords
    
def load_category_from_json(filename, query):
    """
    Reads the specified JSON file and extracts the list of keywords.
    First determine which category it belongs to
    """
    with open(filename, 'r') as file:
        data = json.load(file)

        #categories = list(data.keys())
        categories = []
        for section_key, section_data in data.items():
            categories.extend(section_data.keys())
        prompt = f"I have the following categories: {', '.join(categories)}. Based on the question '{query}', which category does it best match? Please respond with ONLY the category name."
        print("MY CATEGORIES ", categories)
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=20)
        category = response.choices[0].text.strip()
        print("THIS CATEGORY MATCHES THE QUESTION:", category)
        return category
        #keywords = []
        for section_key, section_data in data.items():
            for item_key, item_data in section_data.items():
                try:
                    keywords.extend(item_data['keywords'])
                except KeyError:
                    print(f"Error in data entry for {section_key} - {item_key}: {item_data}")
                
        return keywords

def gpt3_match_category(prompt, token_counter):
    """
    Uses OpenAI's Davinci model to match the user's prompt against the extracted list of keywords.
    """
    filename = os.path.join(ROOT_DIR, 'data', 'data.json')

    try:
        token_counter.add_sent(len(prompt.split()))
        category = load_category_from_json(filename, prompt)
        # formatted_keywords = ', '.join(keyword_list[:-1]) + " and " + keyword_list[-1]
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     #model="gpt-3.5-turbo",
        #     prompt=f"Given the category [{formatted_keywords}], which keyword(s) best relate to the user's input (maximum 5): \"{prompt}\"?",
        #     max_tokens=50
        # )
        # token_counter.add_received(response['usage']['total_tokens'])
        #matched_keywords = response.choices[0].text.strip()
        return category, token_counter
    except Exception as e:
        print(f"Error while matching keywords: {e}")
        return None

def get_answer_by_keyword(keyword_string):
    keyword_string = keyword_string.lower()
    print("INPUT KEYWORD:", keyword_string)
    
    filename = os.path.join('data', 'data.json')

    # Load the data
    with open(filename, 'r') as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Expected a dictionary in data.json")

    # Traverse through the data to find the corresponding answer for the input keyword_string
    for main_section_key, main_section_data in data.items():
        for section_key, section_data in main_section_data.items():
            if section_key == keyword_string:
                return section_data['answer']

    print("RETURNING FALSE")
    return False


def get_gpt3_response(prompt, token_counter):
    '''This function calls the GPT-3 API and fetches a response for the given prompt'''
    token_counter.add_sent(len(prompt.split()))
    response = openai.Completion.create(
      engine="text-davinci-003",
      #model="gpt-3.5-turbo",
      prompt=prompt,
      max_tokens=150
    )
    token_counter.add_received(response['usage']['total_tokens'])
    return response.choices[0].text.strip(), token_counter

def get_extended_answer_for_prompt(user_prompt, token_counter):
    keyword_match, token_counter = gpt3_match_category(user_prompt, token_counter)

    raw_answer = get_answer_by_keyword(keyword_match)
    
    # Combine the raw_answer with the user's prompt to form a new prompt for GPT-3
    gpt3_prompt = f"User asked: {user_prompt}. Context: {raw_answer}. How would you respond? Keep the answer short."
    
    # Fetch the response from GPT-3 based on the combined prompt
    gpt3_response = get_gpt3_response(gpt3_prompt)

    total_tokens = token_counter.display()
    print("TOTAL TOKENS:", total_tokens)

    return {
        'keyword': keyword_match,
        'raw_answer': raw_answer,
        'gpt3_answer': gpt3_response,
        'tokens': total_tokens
    }

# TEST ONLY THIS...
if __name__ == '__main__':
    token_counter = TokenCounter()
    user_prompt = input("Ask me a question: ")
    answers = get_extended_answer_for_prompt(user_prompt, token_counter)
    print(f"Extracted Keyword: {answers['keyword']}")
    print(f"Raw Answer: {answers['raw_answer']}")
    print(f"GPT-3's Answer: {answers['gpt3_answer']}")
