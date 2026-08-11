from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from core.dependencies import get_vk, get_token
from schemas.models import SendRequest
from services import vk_service

router = APIRouter()

@router.get("/me")
def me(vk = Depends(get_vk)):
    return vk_service.get_me(vk)

@router.get("/chats")
def chats(limit: int = 10, vk = Depends(get_vk)):
    return vk_service.get_chats(vk, limit)

@router.get("/albums")
def albums(vk = Depends(get_vk)):
    return vk_service.get_albums(vk)

@router.get("/tracks")
def tracks(album_id: int, owner_id: int = 0, offset: int = 0, vk = Depends(get_vk)):
    return vk_service.get_tracks(vk, album_id, owner_id, offset)

@router.post("/send")
async def send_music(req: SendRequest, token: str = Depends(get_token)):
    return StreamingResponse(
        vk_service.send_tracks_generator(token, req.chat_id, req.track_ids),
        media_type="text/event-stream"
    )
