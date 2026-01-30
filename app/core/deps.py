from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.session import supabase
from app.core.security import decode_access_token

# Bearer Token (Header: "Authorization: Bearer <token>") 추출기
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    HTTP Header로 전달된 자체 Access Token을 검증하고, 유효한 경우 DB에서 사용자 정보를 조회합니다.
    """
    token = credentials.credentials
    
    # 1. JWT 디코딩
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰에 사용자 정보가 없습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. DB에서 실제 유저 확인 (옵션: 성능을 위해 생략 가능하나, 보안상 권장)
    try:
        response = supabase.table("users").select("*").eq("user_id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        
        # 딕셔너리 형태로 반환 (FastAPI 라우터에서 사용하기 위함)
        return response.data[0]

    except Exception as e:
        print(f"Auth Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 처리 중 오류가 발생했습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
