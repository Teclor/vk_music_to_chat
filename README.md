# VKChatMusic

VKChatMusic — это Serverless Single Page Application (SPA), позволяющее удобно просматривать свою музыку и альбомы из ВКонтакте и массово рассылать треки в выбранные диалоги и беседы с учетом обхода API-лимитов ВКонтакте (Flood Control).

## Особенности
*   **Serverless Архитектура (JSONP):** Приложение работает исключительно в браузере клиента. Все запросы к VK API выполняются напрямую через технологию JSONP, что позволяет полностью обойти ограничения CORS и избежать ошибки `access_token was given to another ip address` (запросы идут с того же IP, на который выдан токен).
*   **Прямая Авторизация:** Использование официального веб-токена `vk.com` (client_id: 6287487) гарантирует стабильный доступ к аудиозаписям.
*   **Умная защита от лимитов (Батчинг):** При массовой отправке браузер сам разбивает треки на пачки по 10 штук и выдерживает случайные плавающие паузы от 5 до 10 секунд для предотвращения банов.
*   **Живой прогресс:** Отслеживание статуса отправки в реальном времени с помощью встроенного UI прогресс-бара.
*   **Отложенная отправка:** Таймер на 5 (одиночная) и 7 секунд (мультивыбор) с возможностью отмены перед физической отправкой в чат.
*   **State Management & Lazy Load:** Состояние авторизации и выбора чатов/альбомов безопасно сохраняется в `sessionStorage`. Треки подгружаются динамически по мере скроллинга (Intersection Observer) для экономии трафика.
*   **Адаптивность:** Идеальное отображение на смартфонах и десктопах.

## Архитектура проекта
*   **Стек:** Vue 3 (Composition API), Vite, Tailwind CSS. 
*   **Взаимодействие с API:** Кастомный JSONP-клиент (`services/api.js`).
*   **Деплой:** Docker, Nginx (для статики и редиректов), Certbot (для SSL). Python-бэкенд **полностью удален** за ненадобностью.

## Структура директорий
```text
/VKChatMusic
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue-компоненты интерфейса (Auth, Chats, Tracks и т.д.)
│   │   ├── services/       # JS-модули (api.js - JSONP клиент для VK API)
│   │   ├── App.vue         # Корневой компонент
│   │   ├── main.js         # Точка входа
│   │   └── style.css       # Глобальные стили и Tailwind
│   ├── index.html
│   ├── nginx.local.conf    # Nginx конфиг для локальной разработки (HTTP)
│   ├── nginx.prod.conf     # Nginx конфиг для продакшена (HTTPS + Certbot)
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── Dockerfile          # Сборка статики через Node.js и упаковка в Nginx
└── docker/
    └── docker-compose.yml  # Оркестрация контейнеров (Только Frontend + Certbot)
```

## Установка и запуск (Docker - Продакшен)

1. Убедитесь, что на сервере установлены **Docker** и **Docker Compose**.
2. В файле `frontend/nginx.prod.conf` замените `yourdomain.com` на ваш реальный домен.
3. Перейдите в директорию `docker`:
   ```bash
   cd docker
   ```
4. Выпустите первичные SSL-сертификаты с помощью Certbot (остановив Nginx, если он работает):
   ```bash
   docker run -it --rm --name certbot \
     -p 80:80 \
     -v "$(pwd)/certbot/conf:/etc/letsencrypt" \
     -v "$(pwd)/certbot/www:/var/www/certbot" \
     certbot/certbot certonly \
     --standalone \
     --email admin@yourdomain.com \
     --agree-tos \
     --no-eff-email \
     -d yourdomain.com -d [www.yourdomain.com](https://www.yourdomain.com)
   ```
5. Запустите сборку и старт контейнеров:
   ```bash
   docker-compose up -d --build
   ```
6. Приложение будет доступно по защищенному HTTPS протоколу. Контейнер `certbot` в `docker-compose` настроен на фоновое авто-продление сертификатов.

## Локальная разработка

Для запуска проекта на локальной машине без Docker:
```bash
cd frontend
npm install
npm run dev
```
Приложение будет доступно по адресу `http://localhost:5173`.