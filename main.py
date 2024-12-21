import os
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api.interface.controllers.controller import router
from containers import Container
from model.llm import LLMManager
from model.db import DB

# AI 서버 설정
app = FastAPI()

# Dependency Injection Container
app.container = Container()

# Include FastAPI Router
app.include_router(router=router)

# Load CORS Origins (프론트엔드 등 AI 서버를 호출할 클라이언트만 허용)
allow_origins = os.getenv("ALLOW_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM Manager
try:
    llm_manager = LLMManager.get_instance()
    llm_manager.load_model()
    print("LLMManager initialized successfully")
except Exception as e:
    print(f"Failed to initialize LLMManager: {str(e)}")

# Initialize DB
try:
    db = DB.get_instance()
    db.load_db()
    print("DB initialized successfully")
except Exception as e:
    print(f"Failed to initialize DB: {str(e)}")

if __name__ == "__main__":
    # AI 서버는 항상 8000번 포트로 실행
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # 모든 네트워크 인터페이스에서 접근 가능
        reload=os.getenv("PYTHON_ENV", "development") == "development",  # 개발 모드에서만 reload 활성화
        timeout_keep_alive=60,
        log_level="debug",
        port=8000  # 포트 고정
    )
