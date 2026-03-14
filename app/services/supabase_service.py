# 引入 Groq 官方提供的 Python SDK
# 引入專案的設定檔 (用來讀取.env -> config.py -> 這個檔案) 
from supabase import create_client, Client
from app.config import settings

# Initialize Supabase client，建立與 Supabase 資料庫的專屬連線。
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# === 資料表名稱設定 (請替換成你 Supabase 裡實際的 Table Name) ===
USER_PROFILE_TABLE = "users"  
WATER_RECORD_TABLE = "drinking_logs"  # 例如: 'water_logs' 或 'iot_records'
GOAL_TABLE= "goals"

#去指定的資料表（TABLE_NAME），撈取前 limit 筆資料
# 以下範例片段，可自行按要抓資料包裝的欄位增減

def fetch_recent_water_records(user_id: str, limit: int = 3) -> list:
    """
    從動態紀錄表中，撈取該使用者最近幾筆的「時間」與「數值」。
    """
    response = (
        supabase.table(WATER_RECORD_TABLE)
        # [修改重點 1] 限定欄位：請替換成實際欄位，例如: "amount_ml, record_time"
        .select("d_volume, record_at")
        # [修改重點 2] 限定對象：確保只撈出該位使用者
        .eq("user_id", user_id)          
        # [修改重點 4] 排序：讓最新的紀錄排在前面，這樣 AI 才不會拿舊資料回答
        .order("record_at", desc=True) 
        .limit(limit)                    
        .execute()
    )
    return response.data

def fetch_username(user_id: str) -> dict:
    """
    從使用者資料表中，只撈取該使用者的「使用者名稱」等 AI 需要知道的基本資訊。
    """
    response = (
        supabase.table(USER_PROFILE_TABLE)
        # [修改重點 1] 限定欄位：請替換成實際欄位，例如: "daily_goal_ml, nickname"
        .select("username")
        # [修改重點 2] 限定對象：確保只撈出該位使用者
        .eq("user_id", user_id)  
        # [修改重點 3] 因為每個 user_id 只會有一筆設定，用 .single() 直接回傳單一字典，不用 list
        .single()                
        .execute()
    )
    return response.data

def fetch_user_water_goal(user_id: str) -> dict:
    """
    從使用者資料表中，只撈取該使用者的「目標飲水量」等 AI 需要知道的基本資訊。
    """
    response = (
        supabase.table(GOAL_TABLE)
        # [修改重點 1] 限定欄位：請替換成實際欄位，例如: "nickname"
        .select("daily_target")
        # [修改重點 2] 限定對象：確保只撈出該位使用者
        .eq("user_id", user_id)  
        # [修改重點 3] 因為每個 user_id 只會有一筆設定，用 .single() 直接回傳單一字典，不用 list
        .single()                
        .execute()
    )
    return response.data





