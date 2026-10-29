"""ДЗ 1 - питаю Claude через API.

python ask.py "питання"   - одне питання
python ask.py             - чат
"""

import os
import sys

import anthropic
from dotenv import load_dotenv

# ключ лежить в .env в корені репо (він в гітігнорі)
load_dotenv()

# haiku найдешевша, для домашки вистачить
MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-5-5")
EFFORT = os.getenv("CLAUDE_EFFORT", "low")
MAX_TOKENS = 4096  # щоб не спалити купу токенів на одну відповідь

SYSTEM_PROMPT = (
    "Ти — корисний асистент. Відповідай мовою, якою поставлене запитання, "
    "чітко і по суті. Якщо чогось не знаєш — так і скажи."
)


def ask(client: anthropic.Anthropic, messages: list) -> list:
    # stream - щоб текст з'являвся одразу, а не чекати всю відповідь
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=messages,
        output_config={"effort": EFFORT},
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
    # None якщо щось пішло не так
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

    client = anthropic.Anthropic()  # ключ сам підтягне з env
    messages = []

    # одне питання з аргументів
    if len(sys.argv) > 1:
        messages.append({"role": "user", "content": " ".join(sys.argv[1:])})
        if ask_safely(client, messages) is None:
            sys.exit(1)
        return

    # чат
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
            messages.pop()  # питання без відповіді викидаю з історії
            continue

        # API нічого не пам'ятає, тому шлю всю історію кожен раз
        messages.append({"role": "assistant", "content": content})
        print()


if __name__ == "__main__":
    main()
