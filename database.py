<<<<<<< HEAD
import sqlite3
import json
from datetime import datetime

DB_PATH = "menu_allergy.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. 기존 분석 이력 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parse_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id TEXT,
        image_url TEXT,
        result_json TEXT,
        created_at TEXT
    )
    """)
    
    # 2. [신규 추가] 사용자별 자연어 알레르기 프로필 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        restaurant_id TEXT PRIMARY KEY,
        allergy_profile TEXT,
        updated_at TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def save_history(restaurant_id: str, image_url: str, result_dict: dict) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO parse_history (restaurant_id, image_url, result_json, created_at) VALUES (?, ?, ?, ?)",
        (restaurant_id, image_url, json.dumps(result_dict, ensure_ascii=False), now)
    )
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_history_by_restaurant(restaurant_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, restaurant_id, image_url, result_json, created_at FROM parse_history WHERE restaurant_id = ? ORDER BY id DESC",
        (restaurant_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        data = json.loads(row[3])
        data["id"] = row[0]
        data["restaurant_id"] = row[1]
        data["image_url"] = row[2]
        history.append(data)
    return history

# --- [신규 추가] 프로필 저장 및 조회 함수 ---

def save_user_profile(restaurant_id: str, profile: str):
    """사용자의 자연어 알레르기 프로필을 저장하거나 업데이트합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO user_profiles (restaurant_id, allergy_profile, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(restaurant_id) DO UPDATE SET 
            allergy_profile = excluded.allergy_profile,
            updated_at = excluded.updated_at
    """, (restaurant_id, profile, now))
    conn.commit()
    conn.close()

def get_user_profile(restaurant_id: str) -> str:
    """저장된 사용자 알레르기 프로필을 불러옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT allergy_profile FROM user_profiles WHERE restaurant_id = ?", (restaurant_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""
=======
import sqlite3
import json
from datetime import datetime

DB_PATH = "menu_allergy.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parse_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id TEXT,
        image_url TEXT,
        result_json TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_history(restaurant_id: str, image_url: str, result_dict: dict) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO parse_history (restaurant_id, image_url, result_json, created_at) VALUES (?, ?, ?, ?)",
        (restaurant_id, image_url, json.dumps(result_dict, ensure_ascii=False), now)
    )
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_history_by_restaurant(restaurant_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, restaurant_id, image_url, result_json, created_at FROM parse_history WHERE restaurant_id = ? ORDER BY id DESC",
        (restaurant_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        data = json.loads(row[3])
        data["id"] = row[0]
        data["restaurant_id"] = row[1]
        data["image_url"] = row[2]
        history.append(data)
    return history
>>>>>>> c5c0c91a70907bbcdfe357bfc95238f53a289969
