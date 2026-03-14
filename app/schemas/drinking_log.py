from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional

class DrinkingLogCreate(BaseModel): #增加的格式規則
    user_id: int
    type_id: int
    d_volume: int = Field(..., ge=1, le=2000)   # 1~2000 ml，密度=1
    record_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_auto: bool = False

    @field_validator('record_at', mode='before')
    @classmethod
    def ensure_utc(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)

class DrinkingLogResponse(BaseModel): #顯示的格式規則
    log_id: int
    type_id: int
    d_volume: int
    record_at: datetime

class DrinkingLogUpdate(BaseModel): #修改的格式規則
    type_id: Optional[int] = None
    d_volume: Optional[int] = Field(None, ge=1, le=2000)
    # record_at: Optional[datetime] = None #要實作修改時間再加