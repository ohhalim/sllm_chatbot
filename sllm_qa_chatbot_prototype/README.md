# sLLM 기반 Q&A 챗봇 프로토타입

## 개요
이 프로젝트는 Langchain 프레임워크를 활용하여 소형 대규모 언어 모델(sLLM) 기반의 Q&A 챗봇을 커맨드 라인에서 실행하는 프로토타입입니다. 프롬프트 엔지니어링, AI 애플리케이션을 위한 데이터 처리, 그리고 기본적인 모델 테스트 방법을 실습하는 것을 목표로 합니다.

## 프로젝트 설정 방법

1.  **저장소 복제:**
    ```bash
    git clone https://github.com/your-username/sllm-qa-chatbot.git
    cd sllm-qa-chatbot
    ```

2.  **가상 환경 생성 및 활성화:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate  # Windows
    ```

3.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **환경 변수 설정:**
    프로젝트 루트 디렉터리에 `.env` 파일을 생성하고 Hugging Face API 토큰을 추가합니다.
    ```
    HUGGINGFACEHUB_API_TOKEN="your_api_key_here"
    ```

## 실행 방법

프로젝트 루트 디렉터리에서 다음 명령어를 실행하여 챗봇을 시작합니다.
```bash
python -m src.main
```

## 테스트 방법

프로젝트 루트 디렉터리에서 다음 명령어를 실행하여 테스트를 진행합니다.
```bash
pytest
```
