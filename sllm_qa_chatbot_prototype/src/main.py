import os
from src.llm_core import initialize_llm_chain, generate_response
from src.data_handler import load_qa_data
from dotenv import load_dotenv

def main():
    """
    커맨드 라인 챗봇 인터페이스를 실행하는 메인 함수
    """
    # .env 파일에서 환경 변수 로드
    load_dotenv()

    # 프로젝트 루트 디렉터리 경로 설정
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.join(project_root, 'data', 'qa_data.csv')

    # Q&A 데이터 로드
    qa_data = load_qa_data(csv_file_path)
    if not qa_data:
        print("Q&A 데이터를 로드할 수 없습니다. 자유로운 대화 모드로 실행합니다.")

    print("sLLM Q&A 챗봇 프로토타입. 종료하려면 'exit'를 입력하세요.")

    try:
        llm_chain = initialize_llm_chain()
    except ValueError as e:
        print(f"초기화 오류: {e}")
        return

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("챗봇을 종료합니다.")
            break

        if not user_input.strip():
            continue

        # 데이터에서 질문 찾아보기
        found_answer = None
        for item in qa_data:
            if user_input.strip().lower() == item['question'].lower():
                found_answer = item['answer']
                break
        
        if found_answer:
            print(f"Bot: {found_answer}")
        else:
            # 데이터에 없는 경우 LLM을 통해 응답 생성
            bot_response = generate_response(llm_chain, user_input)
            print(f"Bot: {bot_response}")

if __name__ == "__main__":
    main()
