<template>
  <div class="min-h-screen max-w-4xl mx-auto p-4 md:p-8">
    <HeaderBar 
      :user="user" :selectedChat="selectedChat" :selectedAlbum="selectedAlbum" 
      @logout="logout" @clear-chat="clearChat" @clear-album="clearAlbum" 
    />
    <AuthStep v-if="!token" @auth-success="login" />
    <ChatSelector v-if="token && !selectedChat" :token="token" @select="selectedChat = $event" />
    <AlbumSelector v-if="selectedChat && !selectedAlbum" :token="token" @select="selectedAlbum = $event" />
    <TrackManager v-if="selectedAlbum" :token="token" :chat="selectedChat" :album="selectedAlbum" />
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import HeaderBar from './components/HeaderBar.vue';
import AuthStep from './components/AuthStep.vue';
import ChatSelector from './components/ChatSelector.vue';
import AlbumSelector from './components/AlbumSelector.vue';
import TrackManager from './components/TrackManager.vue';
import { getMe } from './services/api';

const token = ref(null);
const user = ref(null);
const selectedChat = ref(null);
const selectedAlbum = ref(null);

const loadUser = async () => {
  try {
    user.value = await getMe(token.value);
  } catch (e) {
    // Если ошибка содержит 5 (проблема с токеном/IP), выкидываем пользователя
    if(e.message.includes('[5]')) logout();
  }
};

const login = (t) => {
  token.value = t;
  sessionStorage.setItem('vk_token', t);
  loadUser();
};

const logout = () => {
  sessionStorage.removeItem('vk_token');
  token.value = null; user.value = null;
  selectedChat.value = null; selectedAlbum.value = null;
};

const clearChat = () => { selectedChat.value = null; selectedAlbum.value = null; };
const clearAlbum = () => { selectedAlbum.value = null; };

onMounted(() => {
  const t = sessionStorage.getItem('vk_token');
  if (t) { token.value = t; loadUser(); }
});
</script>