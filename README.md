# AI Engineer: домашні завдання

Домашні завдання з курсу AI Engineer (Web Academy). Кожне завдання лежить в окремій папці:

- [`hw01_ask_claude`](hw01_ask_claude): скрипт, що ставить запитання Claude через API
- [`hw02_temperature_arena`](hw02_temperature_arena): порівняння відповідей з temperature 0.0 і 1.0

## Запуск

Потрібен Python 3.10 або новіший. Віртуальне середовище, залежності й API-ключ спільні для всього репозиторію, тому налаштування робиться один раз у корені.

```bash
git clone https://github.com/HLEBUSHEKzla/ai-engineer-course.git
cd ai-engineer-course
```

Створення й активація venv на Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

На macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

У PyCharm цей інтерпретатор обирається так: Settings → Project → Python Interpreter → Add Interpreter → Existing, далі `venv/Scripts/python.exe` (Windows) або `venv/bin/python` (macOS / Linux).

Встановлення залежностей:

```bash
pip install -r requirements.txt
```

API-ключ зберігається у файлі `.env` у корені репозиторію: достатньо скопіювати `.env.example` в `.env` і вписати свій `ANTHROPIC_API_KEY`. Файл `.env` додано в `.gitignore`, тож на GitHub ключ не потрапить. Скрипти з будь-якої папки знаходять його автоматично.

## Додавання нового завдання

Кожне нове завдання отримує окрему папку `hwNN_назва`. Нові бібліотеки дописуються в кореневий `requirements.txt`, а саме завдання додається до списку вище.
