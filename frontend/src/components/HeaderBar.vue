<template>
  <div>
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 sm:mb-8 bg-white p-4 rounded-xl shadow-sm border border-gray-100 gap-4">
      <h1 class="text-xl sm:text-2xl font-bold text-blue-600">VKChatMusic</h1>
      <div v-if="user" class="flex flex-wrap items-center gap-4 w-full sm:w-auto justify-between sm:justify-end">
        <div class="flex items-center gap-2">
          <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-xs sm:text-sm font-medium text-gray-600">Подключено</span>
        </div>
        <div class="flex items-center gap-3 bg-gray-50 pl-2 pr-3 sm:pr-4 py-1.5 rounded-full border border-gray-200 max-w-full">
          <img :src="user.photo_50" class="w-6 h-6 sm:w-8 sm:h-8 rounded-full border border-gray-300" />
          <span class="text-xs sm:text-sm font-semibold truncate max-w-[100px] sm:max-w-[150px]">{{ user.first_name }}</span>
          <button @click="$emit('logout')" class="ml-1 sm:ml-2 text-gray-400 hover:text-red-500 transition" title="Выйти">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
      </div>
      <div v-else class="text-sm text-gray-500 italic">Не авторизован</div>
    </div>

    <div v-if="user" class="flex flex-wrap gap-2 sm:gap-4 mb-6">
      <div v-if="selectedChat" class="flex items-center gap-2 bg-blue-50 text-blue-700 px-3 py-2 sm:px-4 rounded-full border border-blue-200 shadow-sm max-w-full">
        <svg class="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
        <span class="font-medium text-sm sm:text-base truncate">{{ selectedChat.name }}</span>
        <button @click="$emit('clear-chat')" class="hover:text-red-500 ml-1 flex-shrink-0"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button>
      </div>
      <div v-if="selectedAlbum" class="flex items-center gap-2 bg-purple-50 text-purple-700 px-3 py-2 sm:px-4 rounded-full border border-purple-200 shadow-sm max-w-full">
        <svg class="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
        <span class="font-medium text-sm sm:text-base truncate">{{ selectedAlbum.title }}</span>
        <button @click="$emit('clear-album')" class="hover:text-red-500 ml-1 flex-shrink-0"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button>
      </div>
    </div>
  </div>
</template>
<script setup>
defineProps(['user', 'selectedChat', 'selectedAlbum']);
defineEmits(['logout', 'clear-chat', 'clear-album']);
</script>q