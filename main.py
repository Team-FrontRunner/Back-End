# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, games, health, products,orders

app = FastAPI(title="할매피디아 API (No-Auth)", version="1.0.0")

# --- CORS 설정 (프론트엔드 연동 필수) ---
origins = [
    "http://localhost:3000",    # React/Next.js 기본 포트
    "http://localhost:5173",    # Vite 기본 포트
    "http://127.0.0.1:3000",
    "*"                         # (주의) 개발 중엔 모든 곳 허용, 배포 시엔 특정 도메인만 허용할 것
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE 등 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# --- 라우터 등록 (조립) ---
app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(games.router, prefix="/api")
# app.include_router(health.router, prefix="/api") # 나중에 추가

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # allow_origins가 *일 때 True면 일부 브라우저 경고가 있을 수 있으나, 개발용으론 무방합니다.
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 라우터 등록 ---
# 모든 API 주소 앞에 /api가 붙습니다.
app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(games.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(orders.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "할매피디아 서버(인증 없음)가 정상 작동 중입니다! 👵"}

if __name__ == "__main__":
    import uvicorn
    # ngrok 등 외부 접속을 위해 0.0.0.0 바인딩
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)