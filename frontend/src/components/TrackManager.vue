<template>
  <div class="bg-white p-3 sm:p-6 rounded-2xl shadow-sm border border-gray-100 relative">

    <!-- Панель мультивыбора -->
    <div v-if="selectedTracks.length > 0" class="sticky top-2 sm:top-4 z-10 bg-gray-900 text-white rounded-2xl p-3 sm:p-4 shadow-xl mb-4 sm:mb-6 flex flex-col sm:flex-row justify-between items-center gap-3 sm:gap-4 transition-all">
      <div class="font-medium text-base sm:text-lg">Выбрано: <span class="font-bold text-blue-400">{{ selectedTracks.length }}</span></div>
      <div v-if="multiSendTimer.active" class="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
        <span class="text-yellow-400 font-bold animate-pulse text-sm sm:text-base">Через {{ multiSendTimer.remaining }}s</span>
        <button @click="cancelMultiSend" class="bg-gray-700 hover:bg-gray-600 px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg font-medium text-sm sm:text-base">Отменить</button>
      </div>
      <button v-else-if="!sendProgress.active" @click="startMultiSend" class="w-full sm:w-auto bg-blue-600 hover:bg-blue-500 px-4 py-2 sm:px-6 rounded-xl font-bold shadow-lg text-sm sm:text-base">Отправить ({{ selectedTracks.length }})</button>
    </div>

    <!-- Индикатор отправки -->
    <div v-if="sendProgress.active" class="mb-4 sm:mb-6 p-4 sm:p-6 bg-blue-50 rounded-2xl border border-blue-200 text-center">
      <div v-if="sendProgress.error" class="text-red-600 font-bold mb-2 text-sm sm:text-base">Ошибка: {{ sendProgress.error }}</div>
      <div v-else>
        <div v-if="sendProgress.progress < 100" class="flex flex-col items-center gap-2 sm:gap-3 mb-4">
           <svg class="w-8 h-8 sm:w-10 sm:h-10 animate-spin text-blue-600" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
           <div class="text-blue-800 font-semibold text-base sm:text-lg">Отправка...</div>
        </div>
        <div v-else class="text-green-600 font-bold text-lg sm:text-xl mb-4">Успешно!</div>
        <div class="text-gray-700 font-medium mb-3 text-sm sm:text-base">{{ sendProgress.step }}</div>
        <div class="w-full bg-gray-200 rounded-full h-2 sm:h-3 mb-2 overflow-hidden"><div class="bg-blue-600 h-2 sm:h-3 transition-all duration-500" :style="{ width: sendProgress.progress + '%' }"></div></div>
      </div>
      <button v-if="sendProgress.progress === 100 || sendProgress.error" @click="closeProgress" class="mt-3 sm:mt-4 bg-white border border-gray-300 px-4 py-2 sm:px-6 rounded-lg font-medium hover:bg-gray-50 text-sm sm:text-base">Закрыть</button>
    </div>

    <div class="flex items-center gap-2 sm:gap-4 px-2 sm:px-3 py-2 sm:py-3 mb-2 text-[10px] sm:text-xs font-bold text-gray-400 uppercase tracking-wider border-b border-gray-100">
      <div class="w-24 sm:w-28 text-center flex-shrink-0" title="Мультивыбор">Мультивыбор</div>
      <div class="flex-grow min-w-0">Название и исполнитель</div>
      <div class="w-24 sm:w-28 text-center sm:text-right flex-shrink-0">Отправка</div>
    </div>

    <!-- Список треков -->
    <div class="space-y-1.5 sm:space-y-2 relative" :class="{'opacity-50 pointer-events-none': sendProgress.active || multiSendTimer.active}">
      <div v-for="track in tracks" :key="track.id" class="flex items-center gap-2 sm:gap-4 p-2 sm:p-3 rounded-xl border border-transparent hover:border-gray-200 hover:bg-gray-50 transition" :class="{'bg-gray-50 opacity-60': isSent(track.id)}">

        <!-- Колонка 1: Выровненный по центру чекбокс -->
        <div class="w-24 sm:w-28 flex-shrink-0 flex justify-center">
          <input type="checkbox" :value="track.id" v-model="selectedTracks" :disabled="multiSendTimer.active || sendProgress.active" class="track-checkbox w-8 h-8 sm:w-10 sm:h-10" :title="isSent(track.id) ? 'Уже отправлен' : ''">
        </div>

        <!-- Колонка 2: Название и исполнитель -->
        <div class="flex-grow min-w-0" :title="isSent(track.id) ? 'Уже отправлен' : ''">
          <div class="font-bold text-sm sm:text-base text-gray-900 truncate">{{ track.title }}</div>
          <div class="text-xs sm:text-sm text-gray-500 truncate">{{ track.artist }}</div>
        </div>

        <!-- Колонка 3: Действия (Сохраняет свою ширину даже если пустая) -->
        <div class="w-24 sm:w-28 flex-shrink-0 flex justify-center sm:justify-end items-center">
          <template v-if="selectedTracks.length === 0">
          <div v-if="instantSendTimer.trackId === track.id" class="flex items-center justify-end gap-1 sm:gap-2">
            <span class="text-xs sm:text-sm font-bold text-yellow-500 animate-pulse">{{ instantSendTimer.remaining }}s</span>
            <button @click="cancelInstantSend" class="bg-gray-200 hover:bg-gray-300 text-xs sm:text-sm px-2 py-1 sm:px-3 sm:py-1.5 rounded-lg font-medium">Отмена</button>
          </div>
          <button v-else @click="startInstantSend(track.id)" class="text-gray-400 hover:text-blue-600 p-1.5 sm:p-2 rounded-full hover:bg-blue-50 transition" title="Отправить">
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
          </button>
          </template>
        </div>
      </div>

      <!-- Спиннер загрузки -->
      <div ref="bottomObserver" class="h-10 w-full flex items-center justify-center mt-4">
        <svg v-if="isLoading" class="w-6 h-6 animate-spin text-gray-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getTracks, sendTracks } from '../services/api';

const props = defineProps(['token', 'chat', 'album']);
const tracks = ref([]);
const offset = ref(0);
const hasMore = ref(true);
const isLoading = ref(false);
const bottomObserver = ref(null);
let observer = null;

const selectedTracks = ref([]);
const sentTracks = ref(JSON.parse(sessionStorage.getItem(`sent_${props.chat.id}`) || '[]'));

const instantSendTimer = ref({ trackId: null, remaining: 0, timerId: null });
const multiSendTimer = ref({ active: false, remaining: 0, timerId: null });
const sendProgress = ref({ active: false, step: '', progress: 0, error: null });

const isSent = (id) => sentTracks.value.includes(id);

const loadTracks = async () => {
  if (isLoading.value || !hasMore.value) return;
  isLoading.value = true;
  try {
    const data = await getTracks(props.album.id, props.album.owner_id, offset.value, props.token);
    tracks.value.push(...data.items);
    offset.value += data.items.length;
    if (data.items.length < 50) hasMore.value = false;
  } catch (e) { console.error(e); }
  isLoading.value = false;
};

watch(bottomObserver, (el) => {
  if (observer) observer.disconnect();
  if (!el) return;
  observer = new IntersectionObserver(([entry]) => { if (entry.isIntersecting) loadTracks(); });
  observer.observe(el);
});

const executeSend = async (ids) => {
  sendProgress.value = { active: true, step: 'Инициализация...', progress: 0, error: null };
  try {
    await sendTracks(props.chat.id, ids, props.token, (prog) => {
      sendProgress.value.step = prog.step;
      sendProgress.value.progress = prog.progress;
    });
    sentTracks.value = [...new Set([...sentTracks.value, ...ids])];
    sessionStorage.setItem(`sent_${props.chat.id}`, JSON.stringify(sentTracks.value));
    selectedTracks.value = [];
  } catch (e) { sendProgress.value.error = e.message; }
};

const closeProgress = () => { sendProgress.value.active = false; };

const startInstantSend = (id) => {
  cancelInstantSend();
  instantSendTimer.value = { trackId: id, remaining: 5, timerId: setInterval(() => {
    instantSendTimer.value.remaining--;
    if (instantSendTimer.value.remaining <= 0) { cancelInstantSend(); executeSend([id]); }
  }, 1000) };
};
const cancelInstantSend = () => { clearInterval(instantSendTimer.value.timerId); instantSendTimer.value.trackId = null; };

const startMultiSend = () => {
  multiSendTimer.value = { active: true, remaining: 7, timerId: setInterval(() => {
    multiSendTimer.value.remaining--;
    if (multiSendTimer.value.remaining <= 0) {
      const ids = [...selectedTracks.value];
      cancelMultiSend(); executeSend(ids);
    }
  }, 1000) };
};
const cancelMultiSend = () => { clearInterval(multiSendTimer.value.timerId); multiSendTimer.value.active = false; };

onMounted(loadTracks);
</script>