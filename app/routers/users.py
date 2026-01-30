# app/routers/users.py
from fastapi import APIRouter, HTTPException
from app.db.session import supabase
from app.schemas.users_dto import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """
    특정 유저 조회 (ID로 검색)
    * 인증 없이 ID만 알면 누구나 조회 가능
    """
    # Supabase에서 user_id가 일치하는 데이터 조회
    response = supabase.table("users").select("*").eq("user_id", user_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    return response.data[0]

@router.get("/", summary="모든 유저 조회")
def get_users():
    """
    모든 유저 목록 조회
    """
    response = supabase.table("users").select("*").execute()
    return response.data