from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, games, health, products

app = FastAPI(title="할매피디아 API", version="1.0.0")

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


@app.get("/")
def read_root():
    return {"message": "할매피디아 서버가 정상 작동 중입니다! 👵"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)