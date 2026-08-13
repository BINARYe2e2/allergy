import os
import io
import re
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import MenuAnalysisResponse

load_dotenv()

def clean_json_string(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()

async def analyze_menu_image(image_bytes: bytes, mime_type: str = "image/jpeg", profile_text: str = "") -> MenuAnalysisResponse:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해 주세요.")

    client = genai.Client(api_key=api_key)
    image = Image.open(io.BytesIO(image_bytes))

    # 사용자의 프로필 조건이 포함된 동적 시스템 프롬프트 구성
    system_prompt = f"""
당신은 다국어 알레르기 유발 물질 및 식재료 분석 전문가입니다.
제공된 메뉴판 또는 원산지 표기판 이미지를 분석하여 알레르기 위험 요소를 추출하세요.

[사용자 맞춤형 알레르기 프로필 및 주의사항]
"{profile_text if profile_text else '등록된 특별한 알레르기 조건이 없습니다.'}"

[분석 및 출력 필수 지시사항]
1. 메뉴판 이미지의 각 메뉴를 분석하여 사용자의 프로필 조건을 바탕으로 안전/주의/위험 여부를 판별하세요.
2. 각 메뉴별로 **구체적인 판정 근거(reasoning)**를 필수로 작성하세요.
3. **매우 중요:** 메뉴판 이미지나 텍스트의 원래 언어가 무엇이든(일본어, 영어 등), **모든 분석 결과, 메뉴 이름, 판정 근거, 설명은 반드시 자연스러운 한국어**로만 출력하세요.

[분석 대상 알레르기 참고 코드]
- ALLERGEN_PERILLA: 들깨, 들기름, 들깨가루, 깻잎 등
- ALLERGEN_SESAME: 참깨, 참기름, 깨소금 등
- ALLERGEN_PEANUT: 땅콩, 땅콩버터 등
"""

    candidate_models = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-3.5-flash"]
    
    last_error = None
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    image,
                    "이 메뉴판/원산지 표기 이미지에서 메뉴와 프로필 맞춤 알레르기 위험 요소를 추출해줘."
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=MenuAnalysisResponse,
                    temperature=0.1,
                ),
            )
            cleaned_text = clean_json_string(response.text)
            return MenuAnalysisResponse.model_validate_json(cleaned_text)
        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(f"Gemini API 호출 실패: {str(last_error)}")
