import os
from dotenv import load_dotenv
from src.data_handler import load_qa_data_as_docs
from src.llm_core import create_rag_chain

def main():
    """
    RAG 기반의 커맨드 라인 챗봇 인터페이스를 실행하는 메인 함수
    """
    load_dotenv()

    # 데이터 로드
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.join(project_root, 'data', 'qa_data.csv')
    documents = load_qa_data_as_docs(csv_file_path)

    if not documents:
        print("문서 데이터를 로드할 수 없습니다. 프로그램을 종료합니다.")
        return

    print("RAG 챗봇을 초기화하는 중입니다...")

    try:
        # RAG 체인 생성
        rag_chain = create_rag_chain(documents)
        print("챗봇이 준비되었습니다. 종료하려면 'exit'를 입력하세요.")
    except Exception as e:
        print(f"RAG 체인 생성 중 오류 발생: {e}")
        return

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("챗봇을 종료합니다.")
            break

        if not user_input.strip():
            continue

        # RAG 체인을 통해 답변 생성
        try:
            bot_response = rag_chain.invoke(user_input)
            print(f"Bot: {bot_response}")
        except Exception as e:
            print(f"답변 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
