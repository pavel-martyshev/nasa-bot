# [NASA Open APIs Telegram Bot](https://t.me/NasaAPIsBot)

![Python](https://img.shields.io/badge/python-3.11-yellow.svg)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)

**NASA Open APIs Telegram Bot** — Telegram-бот, позволяющий просматривать "Astronomy Picture of the Day" от NASA с переводом описания и возможностью выбрать дату или случайное изображение. В дальнейшем планируется возможность работы и другими NASA Open APIs.

---

## 🚀 Возможности

- 🔭 Получение картинки дня от NASA (APOD).
- 📅 Выбор конкретной даты.
- 🎲 Случайная картинка.
- 🌙 WebApp для отображения длинных описаний.

---

## 🛠 Установка и запуск бота

1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/nasa-bot.git
cd nasa-bot
```

2. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv venv
```
- для Linux/MacOS
```bash
source venv/bin/activate
```
- для Windows
```bash
venv/Scripts/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте .env на основе .env.example и заполните переменные:
```bash
BOT_TOKEN=your_bot_token
NASA_API_KEY=your_nasa_api_key
...
```
Переменные для перевода соответствуют требованиям Yandex Translate API.

5. Запустите бота:
```bash
python main.py
```

---

## 🧩 WebApp

Для отображения длинного текста описания в Telegram используется WebApp — мини-веб-приложение, которое открывается прямо в чате бота.

Чтобы это работало:
1. Необходимо разместить веб-страницу с HTTPS (например, через Vercel, Netlify или собственный сервер с SSL-сертификатом).
2. Страница должна принимать параметры (заголовок и описание картинки) и отображать их.
3. Бот должен быть запущен с помощью вебхуков.

Если нужно, можно настроить Nginx или другой веб-сервер для проксирования запросов к API.

---

## 📂 Структура

- api/ - API для отправки данных из БД в WebApp
- config/ - конфигурационные настройки приложения
- database/ — Tortoise ORM + PostgreSQL, Redis
- dialogs/ — диалоги aiogram_dialog (основная логика приложения)
- locales/ - локали для хранения локализации текстов приложения
- resources/ - дополнительные ресурсы приложения
- states/ - объекты машины состояний
- tests/ - юнит-тесты
- utils/ — вспомогательные модули (перевод, HTTP, enum)

---
## 📜 Лицензия

Этот проект лицензирован по [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed).

Нельзя использовать код в коммерческих целях или запускать публичные копии бота без разрешения автора.

> NASA Open APIs Telegram Bot © 2025 by Pavel Martyshev is licensed under CC BY-NC 4.0
