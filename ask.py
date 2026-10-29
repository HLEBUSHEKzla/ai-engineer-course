"""Домашнє завдання 1: скрипт, який відповідає на запитання через Claude API.

Використання:
    python ask.py "Що таке LLM?"   # одне запитання — одна відповідь
    python ask.py                  # інтерактивний чат (пам'ятає контекст розмови)
"""

import os
import sys

import anthropic
from dotenv import load_dotenv

# Ключ та налаштування беремо з файлу .env (він у .gitignore і НЕ потрапляє на GitHub)
load_dotenv()

MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5-5")
EFFORT = os.getenv("CLAUDE_EFFORT", "medium")  # low | medium | high | xhigh | max

SYSTEM_PROMPT = (
    "Ти — корисний асистент. Відповідай мовою, якою поставлене запитання, "
    "чітко і по суті. Якщо чогось не знаєш — так і скажи."
)


def ask(client: anthropic.Anthropic, messages: list) -> list:
    """Відправляє історію розмови в Claude, друкує відповідь по мірі генерації
    і повертає content відповіді, щоб додати його в історію."""
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=messages,
        output_config={"effort": EFFORT},
        # Якщо модель відмовить через фільтри безпеки — API сам повторить запит на іншій моделі
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        response = stream.get_final_message()
    print()

    if response.stop_reason == "refusal":
        print("[Модель відмовилась відповідати на це запитання]")
    elif response.stop_reason == "max_tokens":
        print("[Відповідь обрізана: досягнуто ліміт max_tokens]")

    return response.content


def ask_safely(client: anthropic.Anthropic, messages: list) -> list | None:
    """Те саме, що ask(), але з людськими повідомленнями про помилки.
    Повертає None, якщо запит не вдався."""
    try:
        return ask(client, messages)
    except anthropic.AuthenticationError:
        sys.exit("\nНевірний API-ключ. Перевір ANTHROPIC_API_KEY у файлі .env.")
    except anthropic.RateLimitError:
        print("\nЗабагато запитів або закінчився ліміт. Спробуй пізніше.")
    except anthropic.APIConnectionError:
        print("\nНемає з'єднання з API. Перевір інтернет.")
    except anthropic.APIStatusError as e:
        print(f"\nПомилка API ({e.status_code}): {e.message}")
    return None


def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("Не знайдено ANTHROPIC_API_KEY. Скопіюй .env.example у .env і встав туди свій ключ.")

    client = anthropic.Anthropic()  # сам читає ANTHROPIC_API_KEY із середовища
    messages = []

    # Режим "одне запитання": python ask.py "питання"
    if len(sys.argv) > 1:
        messages.append({"role": "user", "content": " ".join(sys.argv[1:])})
        if ask_safely(client, messages) is None:
            sys.exit(1)
        return

    # Інтерактивний режим
    print(f"Чат з Claude ({MODEL}). Команди: /clear — нова розмова, exit — вихід.\n")
    while True:
        try:
            question = input("Ти: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "вихід"):
            break
        if question == "/clear":
            messages.clear()
            print("Історію очищено.\n")
            continue

        messages.append({"role": "user", "content": question})
        print("Claude: ", end="", flush=True)
        content = ask_safely(client, messages)
        if content is None:
            messages.pop()  # прибираємо запитання, на яке не вдалося відповісти
            continue

        # Зберігаємо повну відповідь, щоб Claude пам'ятав контекст розмови
        messages.append({"role": "assistant", "content": content})
        print()


if __name__ == "__main__":
    main()
