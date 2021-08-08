from typing import Optional, Any

from pydantic import BaseModel
from datetime import datetime

class Authentication(BaseModel):
    object: str
    id: str
    payload: Any
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None