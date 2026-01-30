## 사용자 회원가입, 개인 정보 등을 다루는 모듈입니다.

from fastapi import APIRouter, HTTPException, Depends
from app.db.session import supabase
from app.schemas.users_dto import UserResponse, LoginRequest, TokenResponse
from app.core.deps import get_current_user
from app.core.security import create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/login", response_model=TokenResponse)
def login_with_id(request: LoginRequest):
    """
    [개발용] User ID로 로그인하여 토큰 발급
    * Supabase Auth가 아닌, 백엔드 자체 JWT 토큰을 발급합니다.
    """
    # 1. DB에 해당 user_id가 존재하는지 확인
    response = supabase.table("users").select("*").eq("user_id", request.user_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="존재하지 않는 User ID입니다.")
    
    user = response.data[0]
    
    # 2. 토큰 생성 (sub에 user_id 저장)
    access_token = create_access_token(data={"sub": user["user_id"]})
    
    return {"access_token": access_token, "token_type": "bearer"}