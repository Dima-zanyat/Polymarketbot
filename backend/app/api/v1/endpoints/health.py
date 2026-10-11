from fastapi import APIRouter, status

router = APIRouter(tags=["health"])


@router.get(
    "/health", status_code=status.HTTP_200_OK, summary="Проверка живости приложения."
)
async def health():
    return {"status": "ok"}



