# AI Engineer: домашки

Тут мої домашні завдання з курсу AI Engineer (Web Academy). Кожна домашка лежить в окремій папці:

- [`hw01_ask_claude`](hw01_ask_claude): скрипт, який задає питання Claude через API
- [`hw02_temperature_arena`](hw02_temperature_arena): порівнюю відповіді з temperature 0.0 і 1.0

## Як запустити у себе

Потрібен Python 3.10 або новіший. venv, залежності і ключ одні на весь репозиторій, тому налаштовується все один раз у корені.

```bash
git clone https://github.com/HLEBUSHEKzla/ai-engineer-course.git
cd ai-engineer-course
```

Створити і активувати venv. На Windows у PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

На macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

У PyCharm треба ще вибрати цей інтерпретатор: Settings → Project → Python Interpreter → Add Interpreter → Existing, і там `venv/Scripts/python.exe` (на Windows) або `venv/bin/python`.

Поставити залежності:

```bash
pip install -r requirements.txt
```

Ключ: скопіювати `.env.example` в `.env` (у корені) і вставити туди свій `ANTHROPIC_API_KEY`. `.env` є в `.gitignore`, тож на GitHub він не потрапить. Скрипти з будь-якої папки його знаходять самі.

## Для себе: як додавати нову домашку

Нова папка `hwNN_назва`. Якщо треба нова бібліотека, дописую її в кореневий `requirements.txt` і додаю домашку в список вище.
