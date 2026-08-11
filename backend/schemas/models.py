from pydantic import BaseModel
from typing import List

class SendRequest(BaseModel):
    chat_id: int
    track_ids: List[str]
