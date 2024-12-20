from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings
from config import DATABASE_HOST, DATABASE_PORT, OPENAI_API_KEY
import logging
import chromadb.utils.embedding_functions as embedding_functions


logger = logging.getLogger(__name__)


class DB:
    _instance = None
    _chroma_client = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if DB._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DB._instance = self

    def load_db(self):
        if self._chroma_client is None:
            try:
                self.client_settings = Settings(
                    chroma_api_impl="rest",
                    chroma_server_host=DATABASE_HOST,
                    chroma_server_http_port=int(DATABASE_PORT)
                )

                self._chroma_client = chromadb.HttpClient(
                    host=DATABASE_HOST,
                    port=int(DATABASE_PORT),
                    settings=self.client_settings
                )

                self.text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=512,
                    chunk_overlap=200,
                    length_function=len
                )

                ef = OpenAIEmbeddings(
                    openai_api_key=OPENAI_API_KEY,
                    model="text-embedding-3-large",
                    dimensions=1536
                )

                # 중복 미션 생성 방지 컬렉션
                self.no_dup_vectorstore = self._initialize_vectorstore(collection_name="no_dup", embedding_function=ef)
                # 선행, 후속 미션 생성을 위한 컬렉션
                self.roadmap_vectorstore = self._initialize_vectorstore(collection_name="roadmap", embedding_function=ef)

            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise

    def _initialize_vectorstore(self, collection_name, embedding_function) -> Chroma:
        return Chroma(
            client=self._chroma_client,
            collection_name=collection_name,
            embedding_function=embedding_function
        )



