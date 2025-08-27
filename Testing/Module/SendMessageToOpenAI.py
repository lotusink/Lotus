from openai import OpenAI

def send_receive_message(
        client:OpenAI,
        prompt,
        b64_image
):
    """
    Get the image and the prompt and send them through OpenAI API, and get a response
    :param client: client (type:OpenAI)
    :param prompt: Prompt (type:string-like)
    :param b64_image: Encoding image using b64 encoding (type:string)
    :return: Response (type:)
    """

    system_prompt = ("The image i send you is a screenshot of my computer."
                     "You are suppose to answer the question base on the screenshot.")

    # Send and getting response
    response = client.responses.create(
        model="gpt-4o-mini", # Choosing a model that support image
        input=[{
            "role": "system",
            "content": [{"type": "input_text","text":system_prompt},]
        },{
            "role": "user", # Set the role as user to send message
            "content": [
                {"type": "input_text","text": prompt}, # Sent the text prompt
                {"type": "input_image", "image_url": f"data:image/png;base64,{b64_image}"}, # Send the image
            ],
        }]
    )

    return response

if __name__ == "__main__":
    pass