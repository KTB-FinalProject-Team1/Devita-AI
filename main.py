from fastapi import FastAPI
import uvicorn
from api.interface.controllers.controller import router
from containers import Container
from model.llm import LLMManager

app = FastAPI()
app.container = Container()
app.include_router(router=router)

llm_manager = LLMManager.get_instance()
llm_manager.load_model()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=True,
        timeout_keep_alive=60,
        log_level="debug"
    )