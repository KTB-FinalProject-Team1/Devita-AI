from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config import DATABASE_PORT, DATABASE_HOST


class RemoteChromaDB:
    def __init__(
            self,
            host: str = DATABASE_HOST,
            port: int = int(DATABASE_PORT),
            collection_name: str = "default_collection"
    ):
        # 원격 서버 설정
        self.client_settings = Settings(
            chroma_api_impl="rest",
            chroma_server_host=host,
            chroma_server_http_port=port
        )

        # 클라이언트 초기화
        self.client = chromadb.HttpClient(
            host=host,
            port=port,
            settings=self.client_settings
        )

        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings()

        # 텍스트 분할기 설정
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    def create_collection(self, metadata: Optional[Dict] = None) -> None:
        """새로운 컬렉션 생성"""
        try:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata=metadata
            )
            print(f"Collection '{self.collection_name}' created successfully")
        except Exception as e:
            print(f"Collection already exists: {e}")
            self.collection = self.client.get_collection(self.collection_name)

    def add_documents(
            self,
            documents: List[str],
            metadatas: Optional[List[Dict]] = None
    ) -> None:
        """문서 추가"""
        # 문서 분할
        splits = self.text_splitter.create_documents(
            documents,
            metadatas=metadatas
        )

        # Langchain 벡터스토어 생성
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            client=self.client,
            collection_name=self.collection_name
        )

        print(f"Added {len(splits)} document chunks to collection")
        return vectorstore

    def add_texts_with_metadata(
            self,
            texts: List[str],
            metadatas: List[Dict],
            ids: Optional[List[str]] = None
    ) -> None:
        """텍스트와 메타데이터 직접 추가"""
        # 임베딩 생성
        embeddings = self.embeddings.embed_documents(texts)

        # 컬렉션에 데이터 추가
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

        print(f"Added {len(texts)} documents to collection")


def main():
    db = RemoteChromaDB()
    # 원격 ChromaDB 초기화
    remote_db = RemoteChromaDB(
        collection_name="no_dup"
    )

    # 컬렉션 생성
    remote_db.create_collection(
        metadata={"description": "중복 미션 생성 방지를 위한 컬렉션"}
    )

    vectorstore = Chroma(
        client=db.client,
        collection_name="no_dup",
        embedding_function=db.embeddings
    )

    # 벡터스토어를 사용한 검색 예시
    results = vectorstore.similarity_search(
        "검색어",
        k=2
    )

    for doc in results:
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")


if __name__ == "__main__":
    main()