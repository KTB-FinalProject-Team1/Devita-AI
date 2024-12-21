from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings
from config import DATABASE_HOST, DATABASE_PORT, OPENAI_API_KEY
import logging

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
        """Initializes the ChromaDB client and collections."""
        if self._chroma_client is None:
            try:
                # Load ChromaDB settings
                self.client_settings = Settings(
                    chroma_api_impl="rest",
                    chroma_server_host=DATABASE_HOST,
                    chroma_server_http_port=int(DATABASE_PORT)  # Ensure port is an integer
                )

                # Initialize ChromaDB client
                self._chroma_client = chromadb.HttpClient(
                    host=DATABASE_HOST,
                    port=8001,
                    settings=self.client_settings
                )

                # Log successful initialization
                logger.info(f"ChromaDB Client connected to {DATABASE_HOST}:{DATABASE_PORT}")

                # Initialize text splitter
                self.text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=512,
                    chunk_overlap=200,
                    length_function=len
                )

                # Initialize embedding function
                ef = OpenAIEmbeddings(
                    openai_api_key=OPENAI_API_KEY,
                    model="text-embedding-3-large",  # Ensure this model is correct
                    dimensions=1536
                )

                # Initialize collections
                self.no_dup_vectorstore = self._initialize_vectorstore(
                    collection_name="no_dup",
                    embedding_function=ef
                )
                self.roadmap_vectorstore = self._initialize_vectorstore(
                    collection_name="roadmap",
                    embedding_function=ef
                )

                logger.info("ChromaDB collections initialized successfully")

            except Exception as e:
                logger.error(f"Error initializing ChromaDB: {str(e)}")
                raise

    def _initialize_vectorstore(self, collection_name, embedding_function) -> Chroma:
        """Initializes a Chroma collection and returns it."""
        try:
            # Create or get the collection from ChromaDB
            return Chroma(
                client=self._chroma_client,
                collection_name=collection_name,
                embedding_function=embedding_function
            )
        except Exception as e:
            logger.error(f"Error initializing collection '{collection_name}': {str(e)}")
            raise
