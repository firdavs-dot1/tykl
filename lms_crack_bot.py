from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORS
from fastapi.responses import FileResponse
import httpx
import os
import uvicorn

# Bot tokeni va chat ID muhit o'zgaruvchilaridan olinadi
TOKEN = os.getenv("7598055697:AAHimQmvY1N0BEUT0T68FJiIct8VkIWuYCc")
CHAT_ID = os.getenv("5728779626")

# FastAPI ilovasini yaratish
app = FastAPI()
app.add_middleware(CORS, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# f1.js faylini berish
@app.get("/f1.js")
async def get_f1_js():
    return FileResponse("f1.js", media_type="application/javascript")

# HTMLni Telegramga yuborish
async def send_html_to_telegram(html_content: str):
    file_path = "page.html"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as f:
                files = {"document": ("page.html", f, "text/html"), "chat_id": (None, CHAT_ID)}
                response = await client.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendDocument", files=files
                )
                response.raise_for_status()
        os.remove(file_path)
        return True
    except Exception as e:
        print(f"HTML yuborishda xatolik: {str(e)}")
        return False

# HTMLni qabul qilish va Telegramga yuborish
@app.post("/upload-html")
async def upload_html(request: Request):
    try:
        data = await request.json()
        html = data.get("html")
        if not html:
            raise HTTPException(status_code=400, detail="Bo‘sh HTML")
        
        success = await send_html_to_telegram(html)
        if success:
            return {"success": True, "message": "Skript yuklandi! HTML yuborildi."}
        else:
            raise HTTPException(status_code=500, detail="HTML yuborishda xatolik")
    except Exception as e:
        print(f"Xatolik: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Serverni ishga tushirish
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))  # Render.com da PORT muhit o'zgaruvchisi ishlatiladi
    uvicorn.run(app, host="0.0.0.0", port=port)
