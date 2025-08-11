import base64
from io import BytesIO
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.docstore.document import Document
from music21 import converter

class MidiService:
    """
    MIDI 생성을 위한 비즈니스 로직을 담당하는 서비스입니다.
    """
    def __init__(self):
        # 샘플 데이터: 실제로는 여러 MIDI 파일에서 로드해야 합니다.
        sample_midi_data_abc = [
            "X:1\nT:Simple C Major Scale\nM:4/4\nL:1/4\nK:C\nC D E F | G A B c |",
            "X:1\nT:Simple G Major Scale\nM:4/4\nL:1/4\nK:G\nG A B c | d e f# g |",
            "X:1\nT:Am Chord Arpeggio\nM:4/4\nL:1/4\nK:Am\nC E A c | E A c e |",
        ]
        documents = [Document(page_content=data) for data in sample_midi_data_abc]

        # 임베딩 모델 설정
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # 벡터 스토어 생성
        vectorstore = FAISS.from_documents(documents, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

        # LLM 설정
        llm = ChatOllama(model="qwen:0.5b")

        # 프롬프트 템플릿 설정
        template = """
        You are a music composer AI. Your goal is to create a short piece of music in ABC notation based on the user's request.
        Use the following pieces of context (existing musical examples) to inform your composition.
        The output MUST be only the ABC notation text, starting with 'X:1'. Do not include any other explanations.

        Context:
        {context}

        User Request: {question}

        Composition (ABC Notation Only):
        """
        prompt_template = ChatPromptTemplate.from_template(template)

        # RAG 체인 구성
        self.rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt_template
            | llm
            | StrOutputParser()
        )

    def generate_midi(self, prompt: str) -> tuple[str, str | None]:
        """RAG 체인을 통해 ABC 표기법을 생성하고 MIDI로 변환합니다."""
        generated_abc = self.rag_chain.invoke(prompt)
        midi_base64_str = self._convert_abc_to_midi_base64(generated_abc)
        return generated_abc, midi_base64_str

    def _convert_abc_to_midi_base64(self, abc_text: str) -> str | None:
        """ABC 표기법 텍스트를 MIDI 파일로 변환하고 Base64로 인코딩합니다."""
        try:
            score = converter.parse(abc_text, format='abc')
            midi_buffer = BytesIO()
            score.write('midi', fp=midi_buffer)
            midi_buffer.seek(0)
            midi_base64 = base64.b64encode(midi_buffer.read()).decode('utf-8')
            return midi_base64
        except Exception as e:
            print(f"Error converting ABC to MIDI: {e}")
            return None

# 애플리케이션 전체에서 단일 인스턴스를 사용하도록 생성
midi_service = MidiService()

