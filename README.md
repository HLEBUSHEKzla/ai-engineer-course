# AI Engineer — домашні завдання

Репозиторій для домашніх завдань з курсу **AI Engineer** (Web Academy).

## Домашнє завдання 1

- [x] Зробити GitHub-репозиторій
- [x] Клонувати на комп, налаштувати IDE та venv
- [x] Отримати API-ключ
- [x] Зробити Python-скрипт, який відповідає на запитання через API

Скрипт [`ask.py`](ask.py) надсилає запитання в **Claude API** (Anthropic) і друкує відповідь по мірі генерації (streaming).
Він працює у двох режимах:

- **одне запитання**: `python ask.py "Що таке RAG?"`
- **чат**: `python ask.py` — пам'ятає контекст розмови; `/clear` очищує історію, `exit` — вихід.

## Як запустити

Потрібен Python 3.10 або новіший.

### 1. Клонувати репозиторій

```bash
git clone https://github.com/HLEBUSHEKzla/ai-engineer-course.git
cd ai-engineer-course
```

### 2. Створити та активувати віртуальне середовище (venv)

Windows (PowerShell):

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

### 3. Встановити залежності

```bash
pip install -r requirements.txt
```

### 4. Додати API-ключ

Скопіювати `.env.example` у `.env` і вставити свій ключ:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Файл `.env` є в `.gitignore`, тому ключ **не потрапить** на GitHub. API-ключ = гроші, нікому його не показуй.

### 5. Запустити

```bash
python ask.py "Поясни простими словами, що таке LLM"
```

## Налаштування (необов'язково, у `.env`)

| Змінна | За замовчуванням | Що робить |
|---|---|---|
| `CLAUDE_MODEL` | `claude-haiku-5-5` | Модель. Haiku — найдешевша ($0.10 / $0.50 за 1M вхідних / вихідних токенів). Розумніші й дорожчі: `claude-sonnet-5-5`, `claude-opus-5-5` |
| `CLAUDE_EFFORT` | `low` | Наскільки глибоко модель «думає»: `low` / `medium` / `high` / `xhigh` / `max`. Вище = довше й дорожче |

Довжина однієї відповіді обмежена 4096 токенами (`MAX_TOKENS` в `ask.py`).
