import os
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

def initialize_llm_chain():
    """
    sLLM을 초기화하고 Langchain 체인을 설정합니다.
    이 함수는 프롬프트 엔지니어링과 솔루션 개발의 핵심 부분을 담당합니다.

    Returns:
        실행 준비가 된 LLMChain 객체
    """
    load_dotenv()
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_key:
        raise ValueError("Hugging Face API 토큰을 찾을 수 없습니다. HUGGINGFACEHUB_API_TOKEN 환경 변수를 설정해주세요.")

    # Hugging Face Hub에서 특정 소형 모델 사용 예시
    repo_id = "google/flan-t5-small"
    llm = HuggingFaceHub(
        repo_id=repo_id,
        model_kwargs={"temperature": 0.7, "max_length": 128},
        huggingfacehub_api_token=api_key
    )

    # 프롬프트 엔지니어링: 모델의 입력 구조 정의
    template = """
    당신은 AI 어시스턴트입니다. 다음 질문에 대해 답변해주세요.
    질문: {user_question}
    답변:
    """
    prompt = PromptTemplate(template=template, input_variables=["user_question"])

    # 프롬프트와 모델을 연결하는 체인 생성
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain

def generate_response(chain: LLMChain, question: str) -> str:
    """
    LLM 체인을 통해 응답을 생성합니다.

    Args:
        chain: 초기화된 LLMChain 객체
        question: 사용자의 질문

    Returns:
        모델이 생성한 응답
    """
    try:
        response = chain.run(question)
        return response
    except Exception as e:
        return f"응답 생성 중 오류 발생: {e}"
