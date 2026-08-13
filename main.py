import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from schemas import MenuAnalysisResponse
from pipeline import analyze_menu_image
import database

app = FastAPI(title="KP ALLERSCAN API")

database.init_db()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. CORS 설정 (에러 발생 시에도 브라우저 차단 방지)
>>>>>>> c5c0c91a70907bbcdfe357bfc95238f53a289969
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProfileUpdate(BaseModel):
    restaurant_id: str
    allergy_profile: str

@app.get("/")
async def read_index():
    """웹 화면 출력 (브라우저 캐시 방지 헤더 적용)"""
    file_path = "index.html"
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    return FileResponse(file_path, headers=headers)

@app.post("/api/v1/profile")
async def update_profile(data: ProfileUpdate):
    """사용자의 자연어 알레르기 프로필 저장"""
    try:
        database.save_user_profile(data.restaurant_id, data.allergy_profile)
        return {"status": "success", "message": "알레르기 프로필이 저장되었습니다."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile Save Error: {str(e)}"
        )

@app.get("/api/v1/profile/{restaurant_id}")
async def get_profile(restaurant_id: str):
    """저장된 알레르기 프로필 조회"""
    profile = database.get_user_profile(restaurant_id)
    return {"restaurant_id": restaurant_id, "allergy_profile": profile or ""}

@app.post("/api/v1/parser/menu-image", response_model=MenuAnalysisResponse)
async def parse_menu_image(
    file: UploadFile = File(...),
    restaurant_id: str = Form(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미지 파일만 업로드할 수 있습니다."
        )
    
    try:
        image_bytes = await file.read()
        
        file_extension = os.path.splitext(file.filename)[1] or ".jpg"
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        
        image_url = f"/uploads/{filename}"

        # 사용자의 자연어 알레르기 프로필 조회
        profile_text = database.get_user_profile(restaurant_id) or "등록된 알레르기 정보가 없습니다."

        # 파이프라인 호출 시 프로필 텍스트 전달
        result = await analyze_menu_image(image_bytes, mime_type=file.content_type, profile_text=profile_text)
        
        result_dict = result.model_dump()
        record_id = database.save_history(restaurant_id, image_url, result_dict)
        
        result.id = record_id
        result.restaurant_id = restaurant_id
        result.image_url = image_url
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis Error: {str(e)}"
        )

@app.get("/api/v1/parser/history/{restaurant_id}")
async def get_history(restaurant_id: str):
    return database.get_history_by_restaurant(restaurant_id)

@app.get("/1088312001.png")
async def get_icon():
    return FileResponse("1088312001.png")
=======
# 2. 이미지 저장용 uploads 폴더 자동 생성 (필수)
os.makedirs("uploads", exist_ok=True)


import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from schemas import MenuAnalysisResponse
from pipeline import analyze_menu_image
import database

app = FastAPI(title="Menu Allergy Parser API")

database.init_db()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    """웹 화면 출력"""
    return FileResponse("index.html")

@app.post("/api/v1/parser/menu-image", response_model=MenuAnalysisResponse)
async def parse_menu_image(
    file: UploadFile = File(...),
    restaurant_id: str = Form(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미지 파일만 업로드할 수 있습니다."
        )
    
    try:
        image_bytes = await file.read()
        
        file_extension = os.path.splitext(file.filename)[1] or ".jpg"
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        
        image_url = f"/uploads/{filename}"

        result = await analyze_menu_image(image_bytes, mime_type=file.content_type)
        
        result_dict = result.model_dump()
        record_id = database.save_history(restaurant_id, image_url, result_dict)
        
        result.id = record_id
        result.restaurant_id = restaurant_id
        result.image_url = image_url
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis Error: {str(e)}"
        )

@app.get("/api/v1/parser/history/{restaurant_id}")
async def get_history(restaurant_id: str):
    return database.get_history_by_restaurant(restaurant_id)
>>>>>>> c5c0c91a70907bbcdfe357bfc95238f53a289969
