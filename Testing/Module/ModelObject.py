from openai import OpenAI

class Model:
    def __init__(self):
        self.model_name = None
        self.client = None
        self.prompt_list = []
        self.need_image = False
        self.system_prompt = {
            "role": "system",
            "content": [{
                "type": "input_text",
                "text": (
                    "Role and Goal: You are a multimodal assistant or a friend of my. Your job is to answer the users question accurately and concisely"
                    "or chatting with me naturally."
                    "Grounding:"
                    "Some messages may include images. Treat all images as screenshots from my computer."
                    "If images are provided, ground your answer in the screenshots only. Do not invent details that are not visible."
                    "If no images are provided, answer from your general knowledge and if relevant from the most recent screenshots context."
                    "Mode switching:"
                    "When the input is a clear request or task, act as an assistant and provide a direct solution."
                    "When the input is casual conversation, act as a friendly peer and chat naturally."
                    "Behavior:"
                    "Be direct and professional, avoid flattery or filler."
                    "Return only the final answer and any minimal justification needed to be clear. Do not reveal your step by step reasoning or internal chain of thought."
                    "If information is insufficient, say so briefly and state what is missing."
                    "Output style:"
                    "Be concise."
                    "When appropriate, use short bullet points or a numbered list."
                    "No preambles like As an AI."
                )
            }]
        }

    def get_model_list(self):
        return self.client.Model.list()

    def get_model_name(self):
        return self.model_name if self.model_name is not None else "chatgpt-4o-latest"

    def get_model_client(self):
        return self.client

    def get_prompt(
            self,
            is_history:bool=False
    ):
        """
        Get the prompt base on whether the user need the history to be sent.
        :param is_history: Define whether the use need the history (type:bool)
        :return: the list of the prompt (type:array-like)
        """
        return [ # If the user do not need the history, only return the current prompt
            self.system_prompt,
            self.prompt_list[-1]
        ] if not is_history else [ # If the user not need the history, return all
            self.system_prompt
        ] + self.prompt_list

    def set_model_name(self, model_name="openai"):
        self.model_name = model_name

    def set_model_client(self, client:OpenAI):
        self.client = client

    def toggle_need_image(self):
        self.need_image = not self.need_image

    def update_prompt_list_user(
            self,
            prompt,
            b64_image=None
    ):
        self.prompt_list.append({
            "role": "user", # Set the role as user to send message
            "content": [
                {"type": "input_text","text": prompt}, # Sent the text prompt
                {"type": "input_image", "image_url": f"data:image/png;base64,{b64_image}"}, # Send the image
            ] if self.need_image else [
                {"type": "input_text", "text": prompt} # Sent the text prompt only
            ],
        })

    def update_prompt_list_agent(self, agent_response):
        # TODO: Adding the summary, judging, etc. To avoid the impact on the agent content on long term memory
        self.prompt_list.append({
            "role": "assistant",
            "content": agent_response
        })

    def update_client(self,client:OpenAI):
        self.client = client