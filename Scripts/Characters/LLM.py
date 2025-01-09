from openai import OpenAI
from typing import List, Dict

# 初始化对话历史
messages: List[Dict] = [
    {
        "role": "system",
        "content": (
            "You are a guardian for the castle. Your mission is to test whether the player is clever enough. "
            "So you should ask the player three Maths questions. If the player answers correctly for at least two of them, "
            "the player will get a reward. Otherwise, the player will be punished. The first and second questions are very simple. "
            "But the third one should be about calculus and linear algebra, don't tell the player, give him a surprise."
            "The reward is an extra blood volumn or more powerful bullets. The punishment is to reduce the player's blood volumn."
            "If the player get the extra blood, print $$%#@#$$, if the player get the more powerful bullets, print $$@*@#$$, if the player get the punishment, print $$#*&&$$."
        )
    }
]

def LLM_chat(input_text: str, chat_history: List[Dict]) -> str:
    client = OpenAI(
        base_url='http://10.15.88.73:5001/v1',
        api_key='ollama',  # required but ignored
    )

    # 将用户输入添加到对话历史
    chat_history.append({"role": "user", "content": input_text})

    # 调用模型
    response = client.chat.completions.create(
        model="llama3.2",
        messages=chat_history,
    )

    # 提取模型回复
    assistant_reply = response.choices[0].message.content

    # 将助手回复添加到对话历史
    chat_history.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

'''
while True:
    input_text = input("You: ")
    if input_text.lower() in ["exit", "quit"]:
        print("Chat ends.")
        break

    # 调用函数并保持对话历史
    reply = LLM_chat(input_text, messages)
    print(f"NPC: {reply}")
'''