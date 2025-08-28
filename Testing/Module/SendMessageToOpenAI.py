from openai import OpenAI

class Model:
    def __init__(self,client):
        self.model_name = None
        self.client = client
        self.prompt_list = None
        self.system_prompt = (
            "The image i send you is a screenshot of my computer."
            "You are suppose to answer the question base on the screenshot."
        )

    def get_model_list(self):
        return self.client.Model.list()

    def get_model_name(self):
        return self.model_name

    def get_current_prompt(self):
        return [self.system_prompt,self.prompt_list[-1]]

    def set_model_name(self, model_name):
        self.model_name = model_name

    def update_prompt_list(self, prompt):
        self.prompt_list.append(prompt)

def send_receive_message(
        client:OpenAI,
        prompt,
        b64_image,
        model_object:Model
):
    """
    Get the image and the prompt and send them through OpenAI API, and get a response
    :param client: client (type:OpenAI)
    :param model_name: The LLM model that it use (type:string-like, default="gpt-4o-mini")
    :param prompt: Prompt (type:string-like object)
    :param b64_image: Encoding image using b64 encoding (type:string-like object)
    :param model_object: The Model object (type:Model)
    :return: Response (type:)
    """

    # Send and getting response
    response = model_object.client.responses.create(
        model=model_object.get_model_name(), # Choosing a model that support image
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