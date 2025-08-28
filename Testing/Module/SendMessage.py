from openai import OpenAI

def send_receive_message(
        model_object:Model
):
    """
    Send the message to the OpenAI API.
    :param model_object: The Model object (type:Model)
    :return: Response (type:string-like)
    """

    # Send and getting response
    response = model_object.client.responses.create(
        model=model_object.get_model_name(), # Choosing a model that support image
        input=model_object.get_prompt()
    )

    return response

if __name__ == "__main__":
    pass