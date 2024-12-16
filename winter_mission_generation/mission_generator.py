import os
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import random
import chromadb
from chromadb.utils import embedding_functions
from chromadb.errors import InvalidCollectionException
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain_core.pydantic_v1 import BaseModel, Field
from langsmith import Client
from dotenv import load_dotenv

class LangSmithLogger:
    """LangSmith를 사용하여 미션 생성 과정을 로깅하는 클래스"""
    
    def __init__(self):
        self.api_key = os.getenv("LANGCHAIN_API_KEY")
        self.client = None
        if self.api_key:
            self.client = Client(api_key=self.api_key)
    
    def validate(self) -> bool:
        """API 키 유효성 검증"""
        if not self.api_key:
            print("API 키가 설정되지 않았습니다.")
            return False
        
        try:
            self.client.list_projects()
            print("LangSmith API 키 유효성 검사 성공!")
            return True
        except Exception as e:
            print(f"API 키 유효성 검사 실패: {str(e)}")
            return False
    
    def log_topic(self, language: str, difficulty: str, topic_data: dict) -> None:
        """토픽 정보 로깅"""
        if not self.client:
            return
            
        try:
            self.client.create_run(
                project_name="devita-1",
                name=f"{language}_{difficulty}_topic",
                inputs={
                    "language": language,
                    "difficulty": difficulty
                },
                outputs={
                    "selected_topic": topic_data
                },
                run_type="retriever",
                start_time=datetime.now(),
                end_time=datetime.now()
            )
            print(f"[{difficulty}] 토픽 로깅 성공")
        except Exception as e:
            print(f"토픽 로깅 실패: {str(e)}")

class MissionGeneratorChain(Chain):
    """미션 토픽을 검색하고 선택하는 체인"""
    
    client: Any = Field(exclude=True)
    collection_name: str = Field(description="ChromaDB collection name")
    difficulty_levels: List[str] = ["Advanced", "Intermediate", "Beginner"]
    
    def __init__(self, client: chromadb.Client, collection_name: str, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.collection_name = collection_name
    
    class Config:
        arbitrary_types_allowed = True
    
    @property
    def input_keys(self) -> List[str]:
        return ["language"]
    
    @property
    def output_keys(self) -> List[str]:
        return ["missions"]

    def _retrieve_topics(self, language: str, difficulty: str) -> Dict:
        """특정 언어와 난이도의 토픽을 검색"""
        try:
            results = self.client.get_collection(self.collection_name).get(
                where={
                    "$and": [
                        {"language": {"$eq": language}},
                        {"difficulty_level": {"$eq": difficulty}}
                    ]
                }
            )
            if results["documents"]:
                random_idx = random.randint(0, len(results["documents"]) - 1)
                return {
                    "topic": results["metadatas"][random_idx]["topic"],
                    "description": results["metadatas"][random_idx]["description"],
                    "difficulty": difficulty
                }
        except Exception as e:
            print(f"토픽 검색 중 오류 발생: {e}")
        return None

    def _call(self, inputs: Dict[str, str]) -> Dict[str, List[Dict]]:
        """각 난이도별 토픽 검색 실행"""
        missions = []
        for difficulty in self.difficulty_levels:
            topic_data = self._retrieve_topics(inputs["language"], difficulty)
            if topic_data:
                missions.append({
                    "topic": topic_data["topic"],
                    "description": topic_data["description"],
                    "difficulty": difficulty
                })
        return {"missions": missions}

class MissionGenerator:
    """미션 생성을 총괄하는 메인 클래스"""
    
    def __init__(self, base_dir: str = "data_store"):
        load_dotenv()
        
        self.db_dir = Path(base_dir) / "chromadb"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=str(self.db_dir))
        
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        
        try:
            self.collection = self.client.get_collection(
                name="mission_dataset",
                embedding_function=self.embedding_function
            )
        except InvalidCollectionException:
            self.collection = self.client.create_collection(
                name="mission_dataset",
                embedding_function=self.embedding_function
            )
        
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=1.0
        )
        
        self._setup_chains()

    def _setup_chains(self):
        """체인 설정"""
        self.retriever_chain = MissionGeneratorChain(
            client=self.client,
            collection_name="mission_dataset"
        )
        
        self.mission_prompt = ChatPromptTemplate.from_template("""
        주어진 토픽에 대해 간단한 미션 제목만 생성해주세요.

        토픽: {topic}
        설명: {description}
        난이도: {difficulty}

        실무에서 실제로 마주할 수 있는 현실적인 미션 제목을 한 줄로 작성해주세요.
        예시 형식: "사용자 인증 시스템 구현하기" 또는 "데이터 캐싱 시스템 개발"처럼 간단명료하게 작성해주세요.
        """)
        
        self.generation_chain = LLMChain(
            llm=self.llm,
            prompt=self.mission_prompt
        )

    def generate_missions(self, language: str) -> Dict:
        """미션 생성 실행"""
        try:
            topics_result = self.retriever_chain({"language": language})
            if not topics_result or "missions" not in topics_result:
               raise ValueError("토픽 검색 결과가 없습니다.")

            generated_missions = []
            for mission_data in topics_result["missions"]:
                try:
                    result = self.generation_chain.invoke({
                        "topic": mission_data["topic"],
                        "description": mission_data["description"],
                        "difficulty": mission_data["difficulty"]
                    })
                
                    generated_missions.append({
                        "difficulty": mission_data["difficulty"],
                        "mission": result["text"],
                        "topic": mission_data["topic"]
                    })
                except Exception as e:
                    print(f"개별 미션 생성 중 오류 발생: {e}")
                    continue

            return {"generated_missions": generated_missions}
        
        except Exception as e:
            print(f"미션 생성 중 오류 발생: {e}")
            return None

def print_selected_topic(language: str, difficulty: str, topic_data: dict) -> None:
    """선택된 토픽 정보를 출력"""
    #print(f"\n[{difficulty}] 난이도에 선택된 토픽:")
    #print(f"주제: {topic_data['topic']}")
    #print(f"설명: {topic_data['description']}")
    #print("-" * 50)

def main():
    """메인 실행 함수"""
    try:
        # LangSmith 로거 초기화 및 검증
        logger = LangSmithLogger()
        is_logging_enabled = logger.validate()
        
        mission_gen = MissionGenerator()
        programming_languages = ["Java", "Python", "JavaScript", "React", "Spring", "Docker"]
        
        print("=== 미션 생성기 시작 ===")
        print(f"지원하는 언어: {', '.join(programming_languages)}")
        
        while True:
            language = input("\n프로그래밍 언어를 입력하세요 (종료: q): ").strip()
            if language.lower() == 'q':
                break
                
            if language not in programming_languages:
                print(f"지원하지 않는 언어입니다. 다음 중 선택해주세요: {', '.join(programming_languages)}")
                continue
            
            print(f"\n{language} 미션을 생성하는 중...")
            
            # 토픽 선택 및 로깅
            topics_result = mission_gen.retriever_chain({"language": language})
            
            if topics_result and "missions" in topics_result:
                print("\n=== 선택된 토픽 정보 ===")
                for topic_data in topics_result["missions"]:
                    print_selected_topic(language, topic_data["difficulty"], topic_data)
                    if is_logging_enabled:
                        logger.log_topic(language, topic_data["difficulty"], topic_data)
            
            # 미션 생성
            missions = mission_gen.generate_missions(language)
            if missions and "generated_missions" in missions:
                print("\n=== 생성된 최종 미션 ===")
                for mission_data in missions["generated_missions"]:
                    print(f"\n[{mission_data['difficulty']} 난이도]")
                    print(f"- {mission_data['mission'].strip()}")
                    print("="*50)
        
        print("\n미션 생성기를 종료합니다. 감사합니다!")
            
    except Exception as e:
        print(f"프로그램 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    load_dotenv(override=True)
    main()