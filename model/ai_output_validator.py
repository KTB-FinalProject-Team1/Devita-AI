from typing import List, Dict, Union
from model.db import DB


class AIOutputValidator:
    def __init__(self,
                 mission_type: str,
                 similarity_threshold: float = 0.85,
                 ):
        # ChromaDB 설정
        self.vectorstore = DB.get_instance().no_dup_vectorstore
        # self.embedding = DB.get_instance().embeddings
        # self.collection = DB.get_instance().no_dup_collection
        self.similarity_threshold = similarity_threshold
        self.mission_type = mission_type

    def is_duplicate(self, text: str) -> tuple[bool, float, Dict]:
        """
        텍스트가 중복인지 검사
        Returns:
            (is_duplicate, highest_similarity, most_similar_entry)
        """
        # 가장 유사한 결과 검색
        results = self.vectorstore.similarity_search_with_relevance_scores(text, k=5)

        if not results:  # 결과가 없는 경우
            return False, 0.0, {}

        document, similarity = results[0]  # (document, similarity) 튜플

        most_similar_entry = {
            'text': document.page_content,
            'metadata': document.metadata,
            'similarity': similarity
        }

        is_duplicate = similarity > self.similarity_threshold
        return is_duplicate, similarity, most_similar_entry

    def get_similar_outputs(self, text: str, n_results: int = 5, threshold: float = None) -> List[Dict]:
        """주어진 텍스트와 유사한 이전 출력들을 반환"""
        if threshold is None:
            threshold = self.similarity_threshold

        results = self.vectorstore.similarity_search_with_relevance_scores(text, k=n_results)

        similar_outputs = []
        for doc, similarity in results:
            if similarity > threshold:
                similar_outputs.append({
                    'text': doc.page_content,
                    'metadata': doc.metadata,
                    'similarity': similarity
                })

        return similar_outputs

    def get_entries_by_metadata(self, metadata_filter: dict) -> list[dict]:
        """메타데이터 기반으로 엔트리 검색"""
        results = self.vectorstore.get(
            where=metadata_filter,
            include=['documents', 'metadatas']
        )

        return [
            {'text': doc, 'metadata': meta}
            for doc, meta in zip(results['documents'], results['metadatas'])
        ]


# 사용 예시
def generate_with_duplicate_prevention(prompt: str,
                                       generator_func,
                                       validator: AIOutputValidator,
                                       max_attempts: int = 3) -> Union[str, None]:
    """
    중복 검사를 포함한 텍스트 생성
    Args:
        prompt: 생성을 위한 프롬프트
        generator_func: 실제 텍스트를 생성하는 함수
        validator: AIOutputValidator 인스턴스
        max_attempts: 최대 재시도 횟수
    """

    for attempt in range(max_attempts):
        generated_text = generator_func(prompt).content
        is_duplicate, similarity, similar_entry = validator.is_duplicate(generated_text)

        if not is_duplicate:
            return generated_text

        print(f"중복 감지 (유사도: {similarity:.2f}). 재시도 중... ({attempt + 1}/{max_attempts})")

    print("최대 재시도 횟수 도달. 중복되지 않는 출력을 생성하지 못했습니다.")
    return None