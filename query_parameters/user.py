from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users(name: str):
    return {"Name":name}

@router.get("/product")
def get_product(limit: int = 10):
    return {"limit":limit}

@router.get("/search")
def get_search(name: str, category: str, price: int):
    return {
        "name": name,
        "category": category,
        "price": price
    }

    