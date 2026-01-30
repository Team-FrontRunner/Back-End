import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel

# 1. 환경변수 로드 (.env 파일 읽기)
load_dotenv()

# 2. Supabase 클라이언트 설정
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase 환경변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")

supabase: Client = create_client(url, key)

# 3. FastAPI 앱 초기화
app = FastAPI()

# --- 데이터 모델 정의 (Pydantic) ---
# 프론트엔드에서 보낼 데이터 형식을 정의합니다.
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

# --- API 엔드포인트 작성 ---

@app.get("/")
def read_root():
    return {"message": "FastAPI + Supabase 연동 성공! 🚀"}

# 예시 1: 모든 유저 정보 조회 (GET)
@app.get("/users")
def get_users():
    # supabase.table("테이블명").select("*").execute()
    response = supabase.table("users").select("*").execute()
    return response.data

# 예시 2: 회원가입 (Supabase Auth 사용) (POST)
@app.post("/signup")
def sign_up(user: UserCreate):
    try:
        # Supabase Auth 기능을 사용하여 유저 생성
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "name": user.name
                    # 추가 메타데이터(프로필 이미지 등)는 여기에
                }
            }
        })
        return {"message": "회원가입 성공", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

print("githubtest")