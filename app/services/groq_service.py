# 引入 Groq 官方提供的 Python SDK
# 引入專案的設定檔 (用來讀取.env -> config.py -> 這個檔案) 
from groq import Groq
from app.config import settings

# Initialize Groq client, 弄成一個可進行通訊的物件
client = Groq(api_key=settings.GROQ_API_KEY)

# Default model - can be changed as needed
DEFAULT_MODEL = "llama-3.3-70b-versatile"

#構建給 AI 的對話內容 (Messages)
def get_completion(prompt: str, context: str = "", model: str = DEFAULT_MODEL) -> str:
    """Send a prompt with optional context to Groq and get a response."""
    messages = []

    if context:
        messages.append({
            "role": "system",
            "content": f"Use the following context to help answer the user's question:\n\n{context}"
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    # 呼叫 Groq API 並設定參數
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1024
    )

    return response.choices[0].message.content
