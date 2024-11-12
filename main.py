from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.interface.controllers.controller import router
from containers import Container
from model.llm import LLMManager

app = FastAPI()
app.container = Container()
app.include_router(router=router)

llm_manager = LLMManager.get_instance()
llm_manager.load_model()

# CORS
origins = [
    "https://52.78.141.49:8080",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=True,
        timeout_keep_alive=60,
        log_level="debug"
    )