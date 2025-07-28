import pandas as pd
from typing import List, Dict

def load_qa_data(filepath: str) -> List[Dict[str, str]]:
    """
    CSV 파일에서 질문과 답변(Q&A) 데이터를 불러옵니다.

    Args:
        filepath: CSV 파일 경로

    Returns:
        질문과 답변을 담은 딕셔너리 리스트
    """
    try:
        df = pd.read_csv(filepath)
        # 필수 컬럼 확인
        if 'question' not in df.columns or 'answer' not in df.columns:
            raise ValueError("CSV 파일에 'question'과 'answer' 컬럼이 필요합니다.")
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Error: {filepath}에서 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"데이터 로딩 중 오류 발생: {e}")
        return []
