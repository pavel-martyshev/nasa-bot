# [NASA Open APIs Telegram Bot](https://t.me/NasaAPIsBot)

![Python](https://img.shields.io/badge/python-3.11-yellow.svg)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)

**NASA Open APIs Telegram Bot** is a Telegram bot that allows users to view NASA's "Astronomy Picture of the Day" with automatic translation of the title and explanation. In the future, the bot may support other NASA Open APIs.

---

## 🚀 Features

- 🔭 Retrieve the Astronomy Picture of the Day (APOD) from NASA
- 📅 Select a specific date
- 🎲 View a random picture
- 🌙  WebApp for displaying long explanations

---

## 🛠 Installation and Running the Bot

1. Clone the repository:

```bash
git clone https://github.com/yourusername/nasa-bot.git
cd nasa-bot
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
```
- for Linux/MacOS
```bash
source venv/bin/activate
```
- for Windows
```bash
venv/Scripts/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file based on .env.example and fill in the variables:
```bash
BOT_TOKEN=your_bot_token
NASA_API_KEY=your_nasa_api_key
...
```
Translation variables should match Yandex Translate API requirements.

5. Run the bot::
```bash
python main.py
```

---

## 🧩 WebApp

To display a long text explanation, Telegram uses WebApp, a mini web application that opens directly in the chat bot.

To make it work:
1. You need to host a web page with HTTPS (e.g. via Vercel, Netlify or your own server with an SSL certificate).
2. The page should accept parameters (title and image description) and display them.
3. The bot must be launched using webhooks.

You may also configure a web server like Nginx to proxy requests to this API if needed.

---

## 📂 Project Structure

- api/ — REST API to serve data to the WebApp
- config/ — configuration and environment management
- database/ — Tortoise ORM with PostgreSQL and Redis
- dialogs/ — aiogram_dialog conversation logic (main bot logic)
- locales/ — localization files
- resources/ — static assets
- states/ — finite state machine definitions
- tests/ — unit tests
- utils/ — helper modules (translation, HTTP client, enums, etc.)

---
## 📜 License

This project is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed).

You may not use the code for commercial purposes or deploy public instances of the bot without the author's permission.

> NASA Open APIs Telegram Bot © 2025 by Pavel Martyshev is licensed under CC BY-NC 4.0
