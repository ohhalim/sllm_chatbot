import pandas as pd
from typing import List
from langchain_core.documents import Document

def load_qa_data_as_docs(filepath: str) -> List[Document]:
    """
    CSV 파일에서 Q&A 데이터를 불러와 LangChain의 Document 객체 리스트로 변환합니다.
    페이지 내용은 질문과 답변을 합친 텍스트이고, 메타데이터에는 원본 질문을 저장합니다.

    Args:
        filepath: CSV 파일 경로

    Returns:
        Document 객체 리스트
    """
    try:
        df = pd.read_csv(filepath)
        if 'question' not in df.columns or 'answer' not in df.columns:
            raise ValueError("CSV 파일에 'question'과 'answer' 컬럼이 필요합니다.")
        
        documents = []
        for _, row in df.iterrows():
            # 질문과 답변을 합쳐서 Document의 page_content로 사용
            content = f"질문: {row['question']}\n답변: {row['answer']}"
            # 원본 질문을 메타데이터로 저장
            metadata = {"source": row['question']}
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
            
        return documents
    except FileNotFoundError:
        print(f"Error: {filepath}에서 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"데이터 로딩 중 오류 발생: {e}")
        return []

