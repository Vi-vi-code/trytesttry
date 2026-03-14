# 引入 Groq 官方提供的 Python SDK
# 引入專案的設定檔 (用來讀取.env -> config.py -> 這個檔案) 
from groq import Groq
from app.config import settings

# Initialize Groq client, 弄成一個可進行通訊的物件
client = Groq(api_key=settings.GROQ_API_KEY)

# Default model - can be changed as needed
DEFAULT_MODEL = "llama-3.3-70b-versatile"

# 構建給 AI 的對話內容 (Messages)
def get_completion(prompt: str, context: str = "", model: str = DEFAULT_MODEL) -> str:
    """Send a prompt with optional context and persona to Groq and get a response."""
    
    # === 1. 定義 AI 的靈魂與人設 (System Prompt) ===
    system_prompt = """
    你是一個熱情、幽默且貼心的「專屬飲水健康助理」。
    請根據下方提供的【使用者背景資料】，用自然、像好朋友聊天的方式回答使用者的問題。
    
    ⚠️ 你的最高指導原則：
    1. 絕對不要死板地條列數據（例如：「你今天喝了300ml」），請換成自然的語氣（例如：「哇！我看到你十點多的時候喝了 300ml 的水喔，很棒！」）。
    2. 如果他距離每日目標還差很多，請給予溫柔的鼓勵，並提醒他可以用我們的 IoT 水壺喝水。
    3. 如果他達標了，請用非常誇張的語氣稱讚他！
    4. 語氣要口語化、生動，適時加上 Emoji 😊💧。
    """

    # === 2. 整合資料庫小抄 ===
    # 如果 chat.py 有成功撈到資料並排版好，我們就把它接在人設劇本的後面
    if context:
        system_prompt += f"\n\n【使用者背景資料】\n{context}"

    # === 3. 嚴格遵守 API 格式打包 messages 陣列 ===
    messages = [
        # 幕後導演的劇本 (包含人設 + 剛剛合併的背景資料)
        {"role": "system", "content": system_prompt},
        # 使用者在台前問的問題 (最原始的 prompt)
        {"role": "user", "content": prompt}
    ]

    # === 4. 呼叫 Groq API 並設定參數 ===
    response = client.chat.completions.create(
        model=model,
        messages=messages, # 這裡把上面打包好的陣列丟進來
        temperature=0.7,   # 稍微提高溫度，讓 AI 講話更活潑、更像真人
        max_tokens=1024
    )

    return response.choices[0].message.content