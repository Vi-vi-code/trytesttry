from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import groq_service, supabase_service

router = APIRouter()

# === 1. 定義資料模型: API 的「輸入」與「輸出」格式 ===

class ChatRequest(BaseModel):
    # 【重要修改】：強制前端發送訊息時，必須附上 user_id！
    # 這樣我們才知道要撈誰的喝水紀錄，AI 也不會把 A 的紀錄當成 B 的。
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

# === 2. 定義 API 路由與核心邏輯 ===

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that:
    1. 根據 user_id 向 Supabase 取得專屬的飲水目標與近期紀錄。
    2. 將撈出的資料進行「擺盤」，轉成結構化的 Markdown Context。
    3. 結合使用者的 Prompt 送給 Groq AI 處理。
    4. 回傳 AI 的客製化回答。
    """
    try:
        # --- 步驟 1：向 Supabase 索取原始資料 (呼叫我們剛改好的 supabase.py) ---
        profile_data = supabase_service.fetch_user_water_goal(user_id=request.user_id)
        records_data = supabase_service.fetch_recent_water_records(user_id=request.user_id, limit=3)

        # --- 步驟 2：資料擺盤 (打包成乾淨的 Markdown 格式給 AI 看) ---
        
        # 安全地讀取資料 (使用 .get)，如果找不到資料就給予預設值，避免程式當機
        daily_goal = profile_data.get("daily_goal_ml", "尚未設定") if profile_data else "尚未設定"
        nickname = profile_data.get("nickname", "使用者") if profile_data else "使用者"

        # 動態組裝 Context 字串
        context_str = f"## 使用者基本資料\n"
        context_str += f"- 稱呼：{nickname}\n"
        context_str += f"- 每日飲水目標：{daily_goal} ml\n\n"
        
        context_str += f"## 最近 3 次 IoT 水壺飲水紀錄\n"
        
        # 如果有喝水紀錄，就逐筆條列出來；如果沒有，也必須明確告訴 AI
        if records_data:
            for record in records_data:
                # 這裡的 key 請對應你 supabase.py 裡面 select 出來的欄位名稱
                time = record.get("record_time", "未知時間")
                amount = record.get("amount_ml", 0)
                context_str += f"- 時間：{time} | 飲水量：{amount} ml\n"
        else:
            context_str += "- 尚無近期的飲水紀錄。\n"

        # (開發小技巧) 把它印在終端機，讓你開發時清楚看到 AI 到底拿到了什麼小抄
        print(f"\n[Debug] 送給 AI 的 Context:\n{context_str}\n")

        # --- 步驟 3：將 Prompt 與排版好的 Context 送給 Groq ---
        response = groq_service.get_completion(
            prompt=request.message,
            context=context_str
        )

        # --- 步驟 4：回傳結果給前端 ---
        return ChatResponse(response=response)

    except Exception as e:
        # 如果發生錯誤 (例如資料庫連線失敗)，妥善地回報給前端
        raise HTTPException(status_code=500, detail=str(e))







