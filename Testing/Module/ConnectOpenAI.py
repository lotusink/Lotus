from dotenv import load_dotenv
from openai import OpenAI
from Testing.Module import ModelObject
import os

def connect_openai_api(
        model_object:ModelObject.Model
):
    """
    Using load_dotenv to get the api from .env file and connect openai api and update Model object
    :return: The model object (type:Model)
    """
    # Loading the .env file
    load_dotenv()

    # Getting the api and connect
    return model_object.update_client(
        OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    )

if __name__ == "__main__":
    pass