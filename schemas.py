from pydantic import BaseModel
from typing import List, Optional

class MenuItem(BaseModel):
    menu_name_ko: str
    menu_name_en: Optional[str] = ""
    raw_ingredients_text: Optional[str] = ""
    detected_allergens: List[str] = []
    is_customizable: Optional[bool] = False
    confidence_score: int
    reasoning: Optional[str] = ""  # AI 판정 근거

class MenuAnalysisResponse(BaseModel):
    id: Optional[int] = None
    restaurant_id: Optional[str] = None
    image_url: Optional[str] = None
    restaurant_type_estimated: str
    items: List[MenuItem]
    origin_board_summary: Optional[str] = ""
