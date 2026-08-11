from core.logger import logger
from fastapi import HTTPException
import vk_api
import random
import asyncio
import json


def call_vk(method_name, func, *args, **kwargs):
    try:
        res = func(*args, **kwargs)
        logger.info(f"VK API [{method_name}] - УСПЕХ")
        return res
    except Exception as e:
        logger.error(f"VK API [{method_name}] - ОШИБКА: {e}")
        raise HTTPException(status_code=400, detail=str(e))


def get_me(vk):
    res = call_vk("users.get", vk.users.get, fields="photo_50")
    if res and isinstance(res, list):
        return res[0]
    return {}


def get_chats(vk, limit: int):
    res = call_vk("messages.getConversations", vk.messages.getConversations, count=limit, extended=1)

    # Защита от пустого или нестандартного ответа
    if not isinstance(res, dict):
        return []

    profiles = {p.get('id'): p for p in res.get('profiles', []) if 'id' in p}
    groups = {g.get('id'): g for g in res.get('groups', []) if 'id' in g}

    chats = []
    for item in res.get('items', []):
        conv = item.get('conversation', {})
        peer = conv.get('peer', {})
        peer_id = peer.get('id')

        if not peer_id:
            continue

        chat_type = peer.get('type')
        name = ""

        if chat_type == "user":
            p = profiles.get(peer_id, {})
            name = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip()
        elif chat_type == "group":
            g = groups.get(abs(peer_id), {})
            name = g.get('name', '')
        elif chat_type == "chat":
            # Безопасное получение настроек чата
            settings = conv.get('chat_settings', {})
            name = settings.get('title', "")

        # Фоллбэк на случай пустых названий (например, из-за кика из беседы)
        if not name:
            name = f"Диалог {peer_id}"

        chats.append({"id": peer_id, "name": name})
    return chats


def get_albums(vk):
    user_res = call_vk("users.get", vk.users.get)
    user_id = user_res[0].get('id') if user_res else 0

    albums = [{"id": 0, "title": "Моя музыка", "owner_id": user_id}]
    playlists = call_vk("audio.getPlaylists", vk.audio.getPlaylists, owner_id=user_id, count=100)

    if isinstance(playlists, dict):
        for p in playlists.get('items', []):
            albums.append({"id": p.get('id'), "title": p.get('title', 'Без названия'), "owner_id": p.get('owner_id')})
    return albums


def get_tracks(vk, album_id: int, owner_id: int, offset: int):
    try:
        if album_id == 0:
            res = call_vk("audio.get(my)", vk.audio.get, owner_id=owner_id, count=50, offset=offset)
        else:
            res = call_vk("audio.get(album)", vk.audio.get, owner_id=owner_id, album_id=album_id, count=50,
                          offset=offset)
    except HTTPException as e:
        if "Unknown method passed" in str(e.detail) or "Access denied" in str(e.detail):
            logger.warning("Прямой метод audio.get недоступен. Пробуем через execute...")
            if album_id == 0:
                code = f'return API.audio.get({{"owner_id": {owner_id}, "count": 50, "offset": {offset}}});'
            else:
                code = f'return API.audio.get({{"owner_id": {owner_id}, "album_id": {album_id}, "count": 50, "offset": {offset}}});'
            res = call_vk("execute(audio.get)", vk.execute, code=code)
        else:
            raise

    tracks = []
    if isinstance(res, dict):
        for item in res.get('items', []):
            owner_id_track = item.get('owner_id')
            track_id = item.get('id')
            if not owner_id_track or not track_id:
                continue

            acc = f"_{item['access_key']}" if 'access_key' in item else ""
            tracks.append({
                "id": f"audio{owner_id_track}_{track_id}{acc}",
                "title": item.get('title', 'Unknown'),
                "artist": item.get('artist', 'Unknown')
            })

    count = res.get('count', 0) if isinstance(res, dict) else 0
    return {"items": tracks, "total": count}


async def send_tracks_generator(token: str, chat_id: int, track_ids: list):
    try:
        vk_session = vk_api.VkApi(token=token, api_version='5.131')
        vk_session.http.headers.update({
            'User-Agent': 'VKAndroidApp/8.23-14479 (Android 11; SDK 30; arm64-v8a; samsung SM-G998B; ru; 2960x1440)'
        })
        vk = vk_session.get_api()

        chunk_size = 10
        chunks = [track_ids[i:i + chunk_size] for i in range(0, len(track_ids), chunk_size)]

        total = len(chunks)
        for i, chunk in enumerate(chunks):
            yield f"data: {json.dumps({'step': f'Отправка пачки {i + 1} из {total}...', 'progress': int((i / total) * 100)})}\n\n"

            attachment = ",".join(chunk)
            await asyncio.to_thread(
                call_vk, "messages.send", vk.messages.send,
                peer_id=chat_id,
                attachment=attachment,
                random_id=random.randint(1, 1000000000)
            )

            if i < total - 1:
                delay = random.uniform(5.0, 10.0)
                yield f"data: {json.dumps({'step': f'Ожидание {delay:.1f} сек...', 'progress': int(((i + 0.5) / total) * 100)})}\n\n"
                await asyncio.sleep(delay)

        logger.info(f"Музыка успешно отправлена в чат {chat_id}")
        yield f"data: {json.dumps({'step': 'Музыка отправлена успешно!', 'progress': 100})}\n\n"
    except Exception as e:
        logger.error(f"Internal API - Send stream error: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"