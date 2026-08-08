from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/login")
async def login():
    return {
        "message": "This Account Was Login"
    }
    