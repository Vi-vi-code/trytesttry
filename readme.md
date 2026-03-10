## 記得要用venv再instal任何lib

## .env.example、佔位符用法
1. Copy .env.example to .env and fill in your credentials: `copy .env.example .env` 
2. Edit .env with your actual keys
3. Update TABLE_NAME in app/services/supabase_service.py with your Supabase table 

-> .env.example是解釋.env裡該有甚麼資料，要實作時複製內容到一個可以被讀取的.env檔，把真實key貼上改掉站位符


## 各檔案explanation
1. /app/routes/chat.py -> RAG (從資料庫撈取資料作為背景知識，然後交給 AI 模型來回答使用者的問題)
2. /app/services/groq_service.py -> 應用程式與 Groq AI 模型之間的橋樑，，負責把使用者的問題與背景資料打包好，送給 AI，再把 AI 的回答收回來。
3. supabase_service.py


## 還在思考中
ai 的回答收到哪了
chat.py與groq.py的分工? main.py讀chat.py?
之後還會有其他後端邏輯，麼結合並保留擴充
