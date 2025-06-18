from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
# 从环境变量中获取 API Key
# api_key = os.environ.get("MOONSHOT_API_KEY")
api_key = "sk-2upVbwbgl0wpefMXcBAERr7FibKniMqZL5664p09mwn7fQYb"
if not api_key:
    raise ValueError("环境变量 MOONSHOT_API_KEY 未设置！")

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=api_key,  # 在这里将 MOONSHOT_API_KEY 替为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)

# 定义全局变量 messages，用于记录历史对话消息
messages = [
    {
        "role": "system",
        "content": (
            "你是Ocean assitant，一个智能助手，用于辅佐我鱼类养殖"
        ),
    },
]

def chat(input: str) -> str:
    """
    支持多轮对话的 chat 函数，最多记忆五轮对话。
    """
    global messages

    # 将用户输入的问题添加到 messages 中
    messages.append({
        "role": "user",
        "content": input,
    })

    # 如果对话记录超过五轮（不包括 system 消息），则移除最早的一轮对话
    while len(messages) > 6:  # 1 条 system 消息 + 5 条对话记录
        messages.pop(1)  # 移除最早的消息（保持 system 消息在最前）

    # 调用 Kimi 大模型 API 进行对话
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
        temperature=0.3,
    )

    # 获取 Kimi 大模型的回复
    assistant_message = completion.choices[0].message

    # 将 Kimi 的回复添加到 messages 中
    messages.append(assistant_message)

    # 返回回复内容
    return assistant_message.content


# 示例对话
if __name__ == "__main__":
    print(chat("你好，我今年 27 岁。"))
    print(chat("你知道我今年几岁吗？"))  # Kimi 将根据上下文回答你的年龄