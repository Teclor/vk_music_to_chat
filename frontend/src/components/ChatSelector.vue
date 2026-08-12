<template>
  <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-gray-100">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <h2 class="text-lg sm:text-xl font-bold text-gray-800">Выберите чат</h2>
      <select v-model="chatLimit" @change="loadChats" class="w-full sm:w-auto border border-gray-300 rounded-lg px-3 py-2 outline-none focus:border-blue-500 text-sm sm:text-base">
        <option :value="10">Последние 10</option>
        <option :value="20">Последние 20</option>
        <option :value="50">Последние 50</option>
      </select>
    </div>
    <div v-if="loading" class="flex justify-center p-8"><svg class="w-8 h-8 animate-spin text-blue-500" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg></div>
    <div v-else class="grid gap-2 sm:gap-3">
      <div v-for="chat in chats" :key="chat.id" @click="$emit('select', chat)" class="p-3 sm:p-4 rounded-xl border border-gray-100 hover:border-blue-500 hover:bg-blue-50 cursor-pointer transition flex items-center justify-between group">
        <span class="font-medium text-gray-800 text-sm sm:text-base truncate mr-2">{{ chat.name }}</span>
        <button class="sm:opacity-0 group-hover:opacity-100 bg-blue-600 text-white px-3 py-1.5 sm:px-4 rounded-lg text-xs sm:text-sm font-medium transition flex-shrink-0">Выбрать</button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { getChats } from '../services/api';
const props = defineProps(['token']);
const emit = defineEmits(['select']);
const chats = ref([]);
const chatLimit = ref(10);
const loading = ref(false);

const loadChats = async () => {
  loading.value = true;
  try { chats.value = await getChats(chatLimit.value, props.token); }
  catch (e) { console.error(e); }
  loading.value = false;
};
onMounted(loadChats);
</script>