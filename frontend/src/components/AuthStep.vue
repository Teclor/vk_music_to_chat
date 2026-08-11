<template>
  <div class="bg-white p-6 sm:p-8 rounded-2xl shadow-lg border border-gray-100 text-center space-y-6">
    <h2 class="text-xl sm:text-2xl font-bold">Инструкция по авторизации</h2>
    <p class="text-sm sm:text-base text-gray-600 text-left max-w-2xl mx-auto leading-relaxed">
      Для работы приложения требуется токен доступа с правами на музыку и сообщения.<br>
      <small><i>Токен доступа не хранится на сервере или в куках, авторизация сбросится сразу после закрытия вкладки</i></small><br><br>
      1. Нажмите кнопку <b>"Получить доступ"</b> (откроется новая вкладка).<br>
      2. Разрешите доступ к вашему аккаунту.<br>
      3. На странице с предупреждением "Пожалуйста, не копируйте данные..." <b>скопируйте всю ссылку из адресной строки</b> браузера.<br>
      4. Вставьте ссылку в поле ниже и нажмите "Продолжить".
    </p>

    <a href="https://id.vk.ru/auth?return_auth_hash=450dd2001b6ddee51a&redirect_uri=https%3A%2F%2Foauth.vk.ru%2Fblank.html&redirect_uri_hash=5a12d0ebefa139be56&force_hash=1&app_id=6287487&response_type=token&code_challenge=&code_challenge_method=&scope=408861919&state=" target="_blank" class="inline-block bg-blue-600 text-white font-semibold py-3 px-6 sm:px-8 rounded-full hover:bg-blue-700 transition shadow-md w-full sm:w-auto">
      Получить доступ
    </a>

    <div class="max-w-xl mx-auto mt-6">
      <input v-model="authUrl" type="text" placeholder="Вставьте ссылку сюда..." class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 outline-none transition text-sm sm:text-base" />
      <button @click="parseToken" class="mt-4 w-full bg-gray-800 text-white font-semibold py-3 rounded-xl hover:bg-gray-900 transition">Продолжить</button>
    </div>
    <p v-if="authError" class="text-red-500 font-medium text-sm sm:text-base">{{ authError }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const emit = defineEmits(['auth-success']);
const authUrl = ref('');
const authError = ref('');

const parseToken = () => {
  authError.value = '';
  const match = authUrl.value.match(/access_token=([^&]+)/);
  if (match) {
    emit('auth-success', match[1]);
  } else {
    authError.value = 'Не удалось найти токен в ссылке. Скопируйте ссылку целиком из адресной строки.';
  }
};
</script>