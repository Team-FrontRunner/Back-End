from fastapi import FastAPI
from app.routers import users, games, health, products # games, health는 파일을 만든 후 추가

app = FastAPI(title="할매피디아 API", version="1.0.0")

# --- 라우터 등록 (조립) ---
app.include_router(users.router)
app.include_router(products.router)
# app.include_router(games.router)  # 나중에 추가
# app.include_router(health.router) # 나중에 추가

@app.get("/")
def read_root():
    return {"message": "할매피디아 서버가 정상 작동 중입니다! 👵"}

# 파이참에서 실행할 때 필요한 코드 (터미널 실행 시엔 없어도 됨)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)