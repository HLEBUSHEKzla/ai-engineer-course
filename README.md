# AI Engineer — домашні завдання

Домашки з курсу **AI Engineer** (Web Academy). Кожне ДЗ — в окремій папці.

| # | Тема | Папка |
|---|---|---|
| 1 | Запитання до Claude API | [`hw01_ask_claude`](hw01_ask_claude) |

## Налаштування (один раз на весь репозиторій)

Потрібен Python 3.10+. Віртуальне середовище, залежності й ключ спільні для всіх домашок і лежать у корені.

```bash
git clone https://github.com/HLEBUSHEKzla/ai-engineer-course.git
cd ai-engineer-course
```

Віртуальне середовище — Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

> У PyCharm: *Settings → Project → Python Interpreter → Add Interpreter → Existing* і вибрати `venv/Scripts/python.exe` (Windows) або `venv/bin/python` (macOS/Linux).

Залежності:

```bash
pip install -r requirements.txt
```

API-ключ: скопіювати `.env.example` у `.env` (у корені репозиторію) і вписати ключ:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

`.env` є в `.gitignore`, тому ключ не потрапить на GitHub. Скрипти з будь-якої папки знаходять його самі.

## Нове ДЗ

1. Створити папку `hwNN_назва` (наприклад, `hw02_...`).
2. Нові бібліотеки дописати в кореневий `requirements.txt`.
3. Додати рядок у таблицю вище.
