from fastapi import APIRouter

router = APIRouter()
    
@router.get("/hello")
async def hello_api():
    return {"message": "Hello Api"}


@router.get("/about")
async def about():
    return {"message": "About Fastapi"}


@router.get("/contact")
async def contact():
    return {"message": "This is My Contact"}


@router.get("/services")
async def services():
    return {"message": "This is My Services"}