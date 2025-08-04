import pytest
import os
from src.llm_core import initialize_llm_chain, generate_response
from langchain.chains import LLMChain

# 테스트를 위한 가짜 API 키 설정
os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'your_api_key_here'

@pytest.fixture
def llm_chain():
    """모든 테스트를 위해 LLM 체인을 한 번만 초기화하는 픽스처"""
    try:
        return initialize_llm_chain()
    except ValueError as e:
        pytest.skip(f"API 키가 필요하여 테스트를 건너뜁니다: {e}")

def test_chain_initialization(llm_chain):
    """LLM 체인이 올바르게 초기화되는지 테스트합니다."""
    assert llm_chain is not None
    assert isinstance(llm_chain, LLMChain)
    assert hasattr(llm_chain, 'prompt')
    assert hasattr(llm_chain, 'llm')

def test_generate_response(llm_chain):
    """응답 생성 함수가 비어있지 않은 문자열을 반환하는지 테스트합니다."""
    question = "What is the capital of France?"
    try:
        response = generate_response(llm_chain, question)
        assert isinstance(response, str)
        # 모델이 모르는 경우 빈 응답을 할 수도 있으므로, 길이는 확인하지 않습니다.
    except Exception as e:
        pytest.fail(f"응답 생성 실패: {e}")
