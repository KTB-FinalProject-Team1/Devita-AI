import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from model.db import DB
from config import OPENAI_API_KEY
import logging
logger = logging.getLogger(__name__)


class LLMManager:
    _instance = None
    _client = None
    _db = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_client(self):
        return self._client

    def __init__(self):
        if LLMManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LLMManager._instance = self

    def load_model(self):
        if self._client is None:
            try:
                self._client = ChatOpenAI(
                    model_name="gpt-4o-mini",  # 모델 이름
                    temperature=1.0,          # 생성 텍스트 다양성
                    frequency_penalty=1.0,  # 반복 사용 단어에 페널티
                    presence_penalty=1.0,   # 새 단어 선호
                    openai_api_key=OPENAI_API_KEY
                )

            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise

    def load_db(self):
        if self._db is None:
            try:
                self._db = DB()

            except Exception as e:
                logger.error(f"Error loading database: {str(e)}")
                raise