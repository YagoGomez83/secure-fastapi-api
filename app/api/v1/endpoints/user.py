from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/users")
def get_users():
    return {
        "status": "success",
        "data": [
            {"id": 1, "name": "Yago"},
            {"id": 2, "name": "Admin"}
        ]
    }


@router.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user id")

    return {
        "status": "success",
        "data": {
            "id": user_id,
            "name": f"user_{user_id}"
        }
    }