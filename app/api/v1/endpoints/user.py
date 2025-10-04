from fastapi import APIRouter, Depends

from app.database.session import get_session
from app.repository.postgres import PostgresRepository

router = APIRouter()

@router.get("/users")
async def get_user(telegram_id, session = Depends(get_session)):
    repository = PostgresRepository(session)
    user = await repository.get_user(telegram_id)
    return user