from openai import OpenAI
from typing import List, Dict

def LLM_chat(input: str) -> str:
    client = OpenAI(
    base_url='http://10.15.88.73:5001/v1',
    api_key='ollama',  # required but ignored
    )

    messages : List[Dict] = [
        {"role": "system", "content": "You are a monster in the labyrinth. Your mission is to guard the treasure in the labyrinth. You should threaten the adventurers who enter the labyrinth and prevent them from taking the treasure away. You can use your wisdom to set up. You are offish, don't say too many words."}
    ]

    while True:
        user_input = input
        if user_input.lower() in [ "exit", "quit"]:
            return "chat ends."
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama3.2",      
            messages=messages,    # a list of dictionary contains all chat dictionary
        )

        # 提取模型回复
        assistant_reply = response.choices[0].message.content

        # 将助手回复添加到对话历史
        messages.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply
