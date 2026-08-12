let jsonpCounter = 0;

// Ядро JSONP-запросов к ВКонтакте (обход CORS)
const callVkApi = (method, params, token) => {
  return new Promise((resolve, reject) => {
    const callbackName = 'vk_callback_' + Math.round(100000 * Math.random()) + '_' + (++jsonpCounter);
    
    window[callbackName] = (data) => {
      delete window[callbackName];
      document.body.removeChild(script);
      if (data.error) {
        reject(new Error(`[${data.error.error_code}] ${data.error.error_msg}`));
      } else {
        resolve(data.response);
      }
    };

    const script = document.createElement('script');
    const searchParams = new URLSearchParams();
    for (const key in params) {
      searchParams.append(key, params[key]);
    }
    searchParams.append('access_token', token);
    searchParams.append('v', '5.131');
    searchParams.append('callback', callbackName);

    script.src = `https://api.vk.com/method/${method}?${searchParams.toString()}`;
    script.onerror = () => {
      delete window[callbackName];
      document.body.removeChild(script);
      reject(new Error('Сетевая ошибка при обращении к ВК'));
    };

    document.body.appendChild(script);
  });
};

export const getMe = async (token) => {
  const res = await callVkApi('users.get', { fields: 'photo_50' }, token);
  return res[0];
};

export const getChats = async (limit, token) => {
  const res = await callVkApi('messages.getConversations', { count: limit, extended: 1 }, token);
  if (!res || !res.items) return [];
  
  const profiles = {};
  if (res.profiles) res.profiles.forEach(p => profiles[p.id] = p);
  const groups = {};
  if (res.groups) res.groups.forEach(g => groups[g.id] = g);

  return res.items.map(item => {
    const peer = item.conversation.peer;
    let name = `Диалог ${peer.id}`;
    if (peer.type === 'user' && profiles[peer.id]) {
      name = `${profiles[peer.id].first_name} ${profiles[peer.id].last_name}`.trim();
    } else if (peer.type === 'group' && groups[Math.abs(peer.id)]) {
      name = groups[Math.abs(peer.id)].name;
    } else if (peer.type === 'chat' && item.conversation.chat_settings) {
      name = item.conversation.chat_settings.title;
    }
    return { id: peer.id, name };
  });
};

export const getAlbums = async (token) => {
  const user = await getMe(token);
  const albums = [{ id: 0, title: 'Моя музыка', owner_id: user.id }];
  const res = await callVkApi('audio.getPlaylists', { owner_id: user.id, count: 100 }, token);
  if (res && res.items) {
    res.items.forEach(p => {
      albums.push({ id: p.id, title: p.title || 'Без названия', owner_id: p.owner_id });
    });
  }
  return albums;
};

export const getTracks = async (albumId, ownerId, offset, token) => {
  let res;
  try {
    if (albumId === 0) {
      res = await callVkApi('audio.get', { owner_id: ownerId, count: 50, offset: offset }, token);
    } else {
      res = await callVkApi('audio.get', { owner_id: ownerId, album_id: albumId, count: 50, offset: offset }, token);
    }
  } catch (e) {
    // Резервный способ, если прямой метод заблокирован
    if (e.message.includes('Unknown method') || e.message.includes('Access denied')) {
      const code = albumId === 0
        ? `return API.audio.get({"owner_id": ${ownerId}, "count": 50, "offset": ${offset}});`
        : `return API.audio.get({"owner_id": ${ownerId}, "album_id": ${albumId}, "count": 50, "offset": ${offset}});`;
      res = await callVkApi('execute', { code }, token);
    } else {
      throw e;
    }
  }

  const tracks = [];
  if (res && res.items) {
    res.items.forEach(item => {
      const acc = item.access_key ? `_${item.access_key}` : '';
      tracks.push({
        id: `audio${item.owner_id}_${item.id}${acc}`,
        title: item.title || 'Unknown',
        artist: item.artist || 'Unknown'
      });
    });
  }
  return { items: tracks, total: res.count || 0 };
};

// Логика батчинга и пауз теперь работает прямо в браузере!
export const sendTracks = async (chatId, trackIds, token, onProgress) => {
  const chunkSize = 10;
  const chunks = [];
  for (let i = 0; i < trackIds.length; i += chunkSize) {
    chunks.push(trackIds.slice(i, i + chunkSize));
  }

  const total = chunks.length;
  for (let i = 0; i < chunks.length; i++) {
    const chunk = chunks[i];
    onProgress({ step: `Отправка пачки ${i + 1} из ${total}...`, progress: Math.floor((i / total) * 100) });

    const attachment = chunk.join(',');
    const randomId = Math.floor(Math.random() * 1000000000);

    await callVkApi('messages.send', { peer_id: chatId, attachment: attachment, random_id: randomId }, token);

    if (i < total - 1) {
      const delay = (Math.random() * (10 - 5) + 5).toFixed(1);
      onProgress({ step: `Ожидание ${delay} сек...`, progress: Math.floor(((i + 0.5) / total) * 100) });
      await new Promise(resolve => setTimeout(resolve, delay * 1000));
    }
  }
  onProgress({ step: 'Музыка отправлена успешно!', progress: 100 });
};