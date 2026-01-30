from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.session import supabase

# Bearer Token (Header: "Authorization: Bearer <token>") 추출기
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    HTTP Header로 전달된 Access Token을 검증하고, 유효한 경우 사용자 정보를 반환합니다.
    """
    token = credentials.credentials
    try:
        # Supabase Auth 서버에 토큰 검증 요청
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_response.user

    except Exception as e:
        print(f"Auth Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증에 실패했습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
