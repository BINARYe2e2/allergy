<<<<<<< HEAD
from pydantic import BaseModel
from typing import List, Optional

class MenuItem(BaseModel):
    menu_name_ko: str
    menu_name_en: Optional[str] = ""
    raw_ingredients_text: Optional[str] = ""
    detected_allergens: List[str] = []
    is_customizable: Optional[bool] = False
    confidence_score: int
    reasoning: Optional[str] = ""  # [신규 추가] AI 판정 근거 (필수 누락 방지를 위해 Optional 처리)

class MenuAnalysisResponse(BaseModel):
    id: Optional[int] = None
    restaurant_id: Optional[str] = None
    image_url: Optional[str] = None
    restaurant_type_estimated: str
    items: List[MenuItem]
    origin_board_summary: Optional[str] = ""
=======
from pydantic import BaseModel
from typing import List, Optional

class MenuItem(BaseModel):
    menu_name_ko: str
    menu_name_en: str
    raw_ingredients_text: str
    detected_allergens: List[str]
    is_customizable: bool
    confidence_score: int

class MenuAnalysisResponse(BaseModel):
    id: Optional[int] = None
    restaurant_id: Optional[str] = None
    image_url: Optional[str] = None
    restaurant_type_estimated: str
    items: List[MenuItem]
>>>>>>> c5c0c91a70907bbcdfe357bfc95238f53a289969
    origin_board_summary: str