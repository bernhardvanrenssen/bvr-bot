import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the OpenAI API key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

def test_extract_keyword(prompt):
    """
    Uses OpenAI's Ada model to extract the main keyword from the provided prompt.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Extract the main keyword from the following text: \"{prompt}\".",
            max_tokens=10
        )
        keyword = response.choices[0].text.strip()
        return keyword
    except Exception as e:
        print(f"Error while extracting keyword: {e}")
        return None
