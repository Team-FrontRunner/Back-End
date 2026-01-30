## 사용자 회원가입, 개인 정보 등을 다루는 모듈입니다.

from fastapi import APIRouter, HTTPException
from app.db.session import supabase
from app.schemas.user_dto import UserCreate

# prefix="/users" -> 이 파일의 모든 API 주소 앞에 /users가 자동으로 붙음
# tags=["users"] -> Swagger UI에서 'users' 그룹으로 묶임
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    """모든 유저 조회"""
    response = supabase.table("users").select("*").execute()
    return response.data

@router.post("/signup")
def sign_up(user: UserCreate):
    """회원가입"""
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {"name": user.name}
            }
        })
        return {"message": "회원가입 성공", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))