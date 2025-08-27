from dotenv import load_dotenv
from openai import OpenAI
import os

def connect_openai_api():
    """
    Using load_dotenv to get the api from .env file and connect openai api.
    :return: Client (type:OpenAI)
    """
    # Loading the .env file
    load_dotenv()

    # Getting the api and connect
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if __name__ == "__main__":
    client = connect_openai_api()