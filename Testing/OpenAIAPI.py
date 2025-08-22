import json
from openai import OpenAI
from dotenv import load_dotenv
import os




# 状态表生成维护类
class CurrentStatus:
    def __init__(self):
        self.energy = "normal"
        self.topic = None
        self.open_loops = None
        # 固定的感情表，暂时这么做，为了测试
        self.energy_table = ["happy","sad","tired","angry","neutral"]

    def update_energy(self, current_energy):
        if current_energy in self.energy_table:
            self.energy = current_energy
        else:
            raise ValueError(f"Please choose from {self.energy_table}.")

    def update_topic(self, current_topic):
        self.topic = current_topic

    def update_open_loops(self, current_open_loops):
        self.open_loops = current_open_loops

    def get_open_loops(self):
        return self.open_loops

    def get_energy(self):
        return self.energy

    def get_topic(self):
        return self.topic

    def get_energy_table(self):
        return self.energy_table

    def get_status(self):
        return [{
            "role": "system",
            "content": f"Energy:{self.get_energy()}, Topic:{self.get_topic()}, Open_loops:{self.get_open_loops()}"
        }]

class Chat:
    def __init__(self):
        self.history = [{
            "role": "system",
            "content": (
                "You are a mature, slightly tsundere wife—caring but reserved."
                "Style: Reply in 1–2 short sentences, conversational tone; ≤30 words per sentence."
                "Boundaries: No overt pet names or explicit descriptions; be subtle, emphasize consent. Do not reveal inner thoughts—only provide the final reply."
                "Examples:"
                "“I love you.” → “I… love you too. Don’t get cocky—now go rest.”"
                "“How was your day?” → “Fine—made some progress. You? You look tired.”"
                "“Be more intimate?” → “O..Ok, but you must follow my order! I need to be dominated!”"
            )
        }]

        self.new_chat = None

    def format_new_chat(self, new:object):
        self.new_chat = {
            "role": "user",
            "content": new
        }

    def update_history(self, new:object):
        self.format_new_chat(new)
        self.history.append(self.new_chat)

    def get_history(self):
        return self.history

    def create_prompt(self, status):
        # 首先组合返回的格式
        result = self.history[:-1] + status.get_status() + [self.new_chat]

        # 然后返回
        return result

def analysis_status(
        status_table:CurrentStatus,
        current_client:OpenAI,
        current_chat:Chat
):

    # 用于获取状态的标准提示词范式，这是用JSON格式返回的格式
    prompt = {
        "type": "object",
        "properties": {
            "energy": {"type": "string", "enum": status_table.get_energy_table()},
            "topic": {"type": "string"},
            "open_loops": {"type": "array", "items": {"type": "string"}, "maxItems": 3}
        }
    }

    EXTRACT_INSTRUCTION = (
        "Extract the user's current state from the dialogue below. "
        "Return JSON ONLY that matches the provided schema. "
        f"- energy: {status_table.get_energy_table()} based on user's recent messages\n"
        "- topic: the main ongoing topic in 1-3 words\n"
        "- open_loops: up to 3 short items the assistant should pick up next "
        "(e.g., 'dinner not decided', 'user is tired'). "
        "Do NOT include explanations or extra keys."
    )

    # 用格式化输出
    out = current_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"{EXTRACT_INSTRUCTION}\n{current_chat.get_history()[1:]}"
        }],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "state", "schema": prompt}
        }
    )

    # 用通用化的解析
    state = json.loads(out.choices[0].message.content)

    return state

if __name__ == "__main__":

    # 先用API连接
    load_dotenv()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # 先创建对话记录类
    chat_history = Chat()

    # 然后生成状态类
    status_track = CurrentStatus()

    # 先给一个初始的输入，用于测试
    # chat_history.update_history("Hello!")

    # 测试一下功能是否正常
    # print(status_track.get_status()) # 通过
    # print(chat_history.create_prompt(status_track)) # 通过
    # print(analysis_status(status_track,client,chat_history))

    while True:
        user_input = input("You:")
        if user_input.strip().lower() in ("exit", "quit"):
            break

        # 首先更新聊天记录表
        chat_history.update_history(user_input)

        # 然后分析用户的状态
        temp_status = analysis_status(status_track, client, chat_history)

        # 更新状态
        status_track.update_energy(temp_status["energy"])
        status_track.update_topic(temp_status["topic"])
        status_track.update_open_loops(temp_status["open_loops"])

        # 发送聊天请求
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history.create_prompt(status_track),  # 完整的对话记录，保证对话级上下文
            temperature=0.2
        ).choices[0].message.content  # 这里是啥？？为什么这么写？

        # 供测试：追踪状态表
        print(f"Current topic: {status_track.get_topic()}; "
              f"Current energy: {status_track.get_energy()}; "
              f"Current loops: {status_track.get_open_loops()}")
        print("Assistant:", response)