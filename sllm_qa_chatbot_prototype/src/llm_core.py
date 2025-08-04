import os
from typing import List
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

def create_rag_chain(documents: List[Document]):
    """
    주어진 문서들을 기반으로 RAG 체인을 생성합니다.

    Args:
        documents: 검색 및 답변 생성에 사용될 Document 객체 리스트.

    Returns:
        실행 가능한 RAG 체인 (Runnable).
    """
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY 환경 변수를 찾을 수 없습니다. .env 파일을 확인해주세요.")

    # 1. 모델 및 임베딩 초기화 (Ollama)
    model = ChatOllama(model="qwen3:0.6b", temperature=0.7)
    embeddings = OllamaEmbeddings(model="qwen3:0.6b")

    # 2. 벡터 저장소 생성 (FAISS)
    # documents가 비어있으면 에러가 발생하므로 확인
    if not documents:
        raise ValueError("RAG 체인을 생성하기 위한 문서가 비어있습니다.")
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()

    # 3. 프롬프트 템플릿 정의
    template = """
    당신은 주어진 컨텍스트를 바탕으로 질문에 답변하는 AI 어시스턴트입니다.
    컨텍스트에 답변이 없는 경우, "자료에 없는 내용입니다."라고만 답변해주세요.

    Context:
    {context}

    Question:
    {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 4. LCEL을 사용해 RAG 체인 구성
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    return rag_chain
