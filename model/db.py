from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings
from config import DATABASE_HOST, DATABASE_PORT


class DB:
    _instance = None

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
            self.client_settings = Settings(
                chroma_api_impl="rest",
                chroma_server_host=DATABASE_HOST,
                chroma_server_http_port=DATABASE_PORT
            )

            self.chroma_client = chromadb.HttpClient(
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                settings=self.client_settings
            )

            self.embeddings = OpenAIEmbeddings()
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=512,
                chunk_overlap=200,
                length_function=len
            )

            self.no_dup_collection = self.chroma_client.get_or_create_collection("no_dup")
            self.roadmap_collection = self.chroma_client.get_or_create_collection("roadmap")

            # 중복 미션 생성 방지 컬렉션
            self.no_dup_vectorstore = self._initialize_vectorstore(collection_name="no_dup")
            # 선행, 후속 미션 생성을 위한 컬렉션
            self.roadmap_vectorstore = self._initialize_vectorstore(collection_name="roadmap")

    def _initialize_vectorstore(self, collection_name) -> Chroma:
        return Chroma(
            client=self.chroma_client,
            collection_name=collection_name,
            embeddings=self.embeddings
        )

    def add_documents(self, mission_title: str, metadatas=list[dict]) -> None:
        splits = self.text_splitter.create_documents(mission_title, metadatas=metadatas)
        self.vectorstore.add_documents(splits)

