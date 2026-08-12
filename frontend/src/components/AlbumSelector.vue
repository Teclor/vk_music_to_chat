<template>
  <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
    <h2 class="text-xl font-bold text-gray-800 mb-6">Выберите откуда брать музыку</h2>
    <div v-if="loading" class="flex justify-center p-8"><svg class="w-8 h-8 animate-spin text-purple-500" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg></div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="album in albums" :key="album.id" @click="$emit('select', album)" class="p-5 rounded-xl border border-gray-200 hover:border-purple-500 hover:bg-purple-50 cursor-pointer transition flex items-center gap-3 bg-gray-50">
        <svg v-if="album.id === 0" class="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
        <svg v-else class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
        <span class="font-semibold text-gray-800">{{ album.title }}</span>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { getAlbums } from '../services/api';
const props = defineProps(['token']);
const emit = defineEmits(['select']);
const albums = ref([]);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  try { albums.value = await getAlbums(props.token); }
  catch (e) { console.error(e); }
  loading.value = false;
});
</script>