from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.telegram_auth import get_telegram_user

app = FastAPI(title="Money App")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")


class TelegramData(BaseModel):
    init_data: str


@app.get("/")
async def root():
    """Отдаем главную страницу"""
    return FileResponse("static/index.html")


@app.post("/api/telegram-user")
async def get_user(data: TelegramData):
    """Получить данные пользователя от Telegram"""
    user = get_telegram_user(data.init_data)
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail="Неверные данные от Telegram")

    return {
        "success": True,
        "user": {
            "id": user.get("id"),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "username": user.get("username"),
            "language_code": user.get("language_code"),
            "is_premium": user.get("is_premium", False)
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)