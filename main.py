import os

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api.interface.controllers.controller import router
from containers import Container
from model.llm import LLMManager
from config import BACKEND_HOST, BACKEND_PORT
from model.db import DB


app = FastAPI()
app.container = Container()
app.include_router(router=router)


origins = [
    f'http://{BACKEND_HOST}:{BACKEND_PORT}'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_manager = LLMManager.get_instance()
llm_manager.load_model()

db = DB.get_instance()
db.load_db()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=BACKEND_HOST,
        reload=True,
        timeout_keep_alive=60,
        log_level="debug",
        port=8000
    )