from fastapi import Header, HTTPException
import vk_api
from core.logger import logger


def get_vk(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        logger.error(f"Internal API - Missing or invalid Authorization header. Received: '{authorization}'")
        raise HTTPException(status_code=401, detail="Invalid token format")

    parts = authorization.split(" ")
    if len(parts) < 2 or parts[1] in ("null", "undefined", ""):
        logger.error("Internal API - Token is empty or null after 'Bearer'")
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = parts[1]
    try:
        vk_session = vk_api.VkApi(token=token, api_version='5.131')
        vk_session.http.headers.update({
            'User-Agent': 'VKAndroidApp/8.23-14479 (Android 11; SDK 30; arm64-v8a; samsung SM-G998B; ru; 2960x1440)'
        })
        return vk_session.get_api()
    except Exception as e:
        logger.error(f"Internal API - VK Session init error: {e}")
        raise HTTPException(status_code=401, detail=str(e))


def get_token(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    parts = authorization.split(" ")
    if len(parts) < 2 or parts[1] in ("null", "undefined", ""):
        raise HTTPException(status_code=401, detail="Invalid token")
    return parts[1]