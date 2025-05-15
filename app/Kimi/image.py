import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import io

# 加载 .env 文件
load_dotenv()
api_key=os.environ.get("MOONSHOT_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)
 
# 在这里，你需要将 kimi.png 文件替换为你想让 Kimi 识别的图片的地址
image_path = "./app/upload/gui.jpg"
 
with open(image_path, "rb") as f:
    image_data = f.read()
 
# 我们使用标准库 base64.b64encode 函数将图片编码成 base64 格式的 image_url
image_url = f"data:image/{os.path.splitext(image_path)[1]};base64,{base64.b64encode(image_data).decode('utf-8')}"
 
question = "图片里面是什么。"

completion = client.chat.completions.create(
    model="moonshot-v1-8k-vision-preview",
    messages=[
        {"role": "system", "content": "你是 Kimi。"},
        {
            "role": "user",
            # 注意这里，content 由原来的 str 类型变更为一个 list，这个 list 中包含多个部分的内容，图片（image_url）是一个部分（part），
            # 文字（text）是一个部分（part）
            "content": [
                {
                    "type": "image_url", # <-- 使用 image_url 类型来上传图片，内容为使用 base64 编码过的图片内容
                    "image_url": {
                        "url": image_url,
                    },
                },
                {
                    "type": "text",
                    "text": question, # <-- 使用 text 类型来提供文字指令，例如“描述图片内容”
                },
            ],
        },
    ],
)


def process_image_with_question(image_path, question):
    """
    将图片路径和问题整合，调用模型接口处理图片和问题。

    参数:
        image_path (str): 图片的文件路径。
        question (str): 提问内容。

    返回:
        str: 模型的回答。
    """
    try:
        # 读取图片文件
        with open(image_path, "rb") as f:
            image_data = f.read()

        # 获取图片格式并编码为 Base64
        image_format = os.path.splitext(image_path)[1][1:]  # 获取文件扩展名（去掉点号）
        image_url = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"

        # 调用模型接口
        completion = client.chat.completions.create(
            model="moonshot-v1-8k-vision-preview",
            messages=[
                {"role": "system", "content": "你是 Kimi。"},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                        {
                            "type": "text",
                            "text": question,
                        },
                    ],
                },
            ],
        )

        # 返回模型的回答
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Error processing image and question: {e}")
        return "处理图片和问题时发生错误，请稍后重试。"

    except Exception as e:
        print(f"Error processing image and question: {e}")
        return "处理图片和问题时发生错误，请稍后重试。"

if __name__ == "__main__":
    # 测试函数
    image_path = "./app/upload/gui.jpg"
    question = "图片里面是什么。"

    response = process_image_with_question(image_path, question)
    print(response)
    # 打印模型的回答
