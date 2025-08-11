from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from . import midi_service

# --- API 모델 정의 ---
class MidiRequest(BaseModel):
    prompt: str

# --- 의존성 주입 ---
def get_midi_service() -> midi_service.MidiService:
    return midi_service.midi_service

# --- API 라우터 ---
router = APIRouter(
    prefix="/midi",
    tags=["MIDI Generation"],
)

@router.post("/generate")
async def generate_midi_endpoint(request: MidiRequest, svc: midi_service.MidiService = Depends(get_midi_service)):
    """
    사용자의 프롬프트를 받아 RAG 체인을 통해 ABC 표기법을 생성하고,
    이를 MIDI 파일(Base64 인코딩)로 변환하여 반환합니다.
    """
    try:
        generated_abc, midi_base64_str = svc.generate_midi(request.prompt)

        if not midi_base64_str:
            raise HTTPException(
                status_code=500,
                detail="Failed to convert generated ABC to MIDI. The LLM might have produced invalid notation."
            )

        return {
            "prompt": request.prompt,
            "generated_abc": generated_abc,
            "midi_base64": midi_base64_str,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
