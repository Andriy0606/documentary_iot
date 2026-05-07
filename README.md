## DPZ lab: Employees (FastAPI + Jinja2)

### Запуск

1) Створіть та активуйте venv, встановіть залежності:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2) Створіть файл `.env` (можна скопіювати з `.env.example`) і заповніть:

- `SESSION_SECRET`: будь-який довгий випадковий рядок
- `BASE_URL`: для локального запуску залишайте `http://127.0.0.1:8000`
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`: беруться з Google OAuth credentials (див. нижче)
- `OUTPUT_SINK`: `console` або `kafka` (перемикає Strategy для виводу повідомлень під час імпорту CSV)
- Якщо `OUTPUT_SINK=kafka`, додайте:
  - `KAFKA_BOOTSTRAP_SERVERS` (наприклад `localhost:9092`)
  - `KAFKA_TOPIC` (наприклад `employees_import_log`)

3) Запустіть сервер:

```bash
py .\main.py
```

Відкрийте `http://127.0.0.1:8000/` — без логіну перекине на Google.

---

### Налаштування Google Login (мінімально)

Щоб Google Login працював, вам потрібні **OAuth Client ID** та **Client Secret** (тип **Web application**).

1) Відкрийте **Google Cloud Console**.
2) Створіть проект (або виберіть існуючий).
3) Перейдіть: **APIs & Services → OAuth consent screen**.
   - Оберіть **External** (щоб міг зайти будь-хто).
   - Заповніть мінімальні поля (App name, email) і збережіть.
4) Перейдіть: **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
   - Application type: **Web application**
   - Authorized redirect URIs додайте:
     - `http://127.0.0.1:8000/auth/callback`
5) Скопіюйте значення в `.env`:
   - `GOOGLE_CLIENT_ID=...apps.googleusercontent.com`
   - `GOOGLE_CLIENT_SECRET=...`

Після змін у `.env` обовʼязково **перезапустіть** сервер.
