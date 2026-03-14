# Groq + Supabase FastAPI Backend

FastAPI 後端，結合 Groq LLM 與 Supabase 資料庫，提供 AI 飲水建議對話，以及飲水記錄的 CRUD API。

---

## 專案結構

```
Pj_try/
├── main.py                          # 應用程式入口，註冊所有 router
├── .env                             # 環境變數（不進版控）
├── requirements.txt
└── app/
    ├── config.py                    # 讀取 .env，統一管理設定值
    ├── routes/                      # HTTP 層：定義端點、處理請求與回應
    │   ├── chat.py                  # POST /chat
    │   └── drinking_logs.py         # POST/GET/DELETE /logs
    ├── schemas/                     # 資料格式層：欄位定義與驗證規則
    │   └── drinking_log.py          # DrinkingLogCreate, DrinkingLogResponse
    └── services/                    # 資料庫層：實際對 Supabase 下指令
        ├── supabase_service.py      # 查詢使用者、目標、飲水紀錄
        ├── groq_service.py          # 呼叫 Groq LLM
        └── drinking_log_service.py  # 飲水記錄 CRUD
```

---

## 三層架構說明

| 層 | 資料夾 | 負責的事 |
|---|---|---|
| **HTTP 層** | `routes/` | 接收請求、呼叫 service、決定 HTTP status code 與回傳格式 |
| **格式層** | `schemas/` | 用 Pydantic 定義欄位型別與驗證規則，FastAPI 自動產生文件 |
| **資料庫層** | `services/` | 對 Supabase 執行查詢、新增、更新，不知道 HTTP 的存在 |

這樣切的好處：想換資料庫只改 services；想改 API 格式只改 routes；層與層之間不互相依賴。

---

## 環境變數

建立 `.env` 檔，填入以下三個值：

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

> 測試飲水記錄 CRUD 時，`SUPABASE_KEY` 請使用 **service_role_key**。

---

## 啟動方式

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI：`http://localhost:8000/docs`

---

## API 端點

### AI 對話

| 方法 | 路徑 | 說明 |
|---|---|---|
| POST | `/chat` | 傳入 user_id 與訊息，回傳 AI 根據飲水紀錄給出的建議 |

**Request body**
```json
{
  "user_id": "1",
  "message": "我今天喝夠水了嗎？"
}
```

---

### 飲水記錄

| 方法 | 路徑 | 說明 |
|---|---|---|
| POST | `/logs` | 新增一筆飲水記錄，回傳 201 + 新紀錄 |
| GET | `/logs?user_id=&date=` | 查詢記錄，`date` 格式 `YYYY-MM-DD`（可省略） |
| DELETE | `/logs/{log_id}` | 軟刪除（寫入 `deleted_at`），回傳 200 或 404 |

**POST /logs request body**
```json
{
  "user_id": 1,
  "type_id": 1,
  "d_volume": 250,
  "record_at": "2026-03-14T10:00:00+08:00",
  "is_auto": false
}
```

> `record_at` 可省略，預設為當下 UTC 時間。`d_volume` 單位為 ml，範圍 1～5000。

---

## Supabase 資料表

| 資料表 | 用途 |
|---|---|
| `users` | 使用者基本資料（username 等） |
| `goals` | 每日飲水目標（daily_target） |
| `drinking_logs` | 飲水記錄（含 soft delete 欄位 `deleted_at`） |

---

## 未來規劃

- [ ] 加入 `client_event_id`（UUID）防止硬體重送重複寫入
- [ ] JWT 驗證，改用 anon key + RLS
- [ ] 前端串接
