"""ДЗ 2 - арена температур: один промпт, два запити з різною temperature.

python arena.py                 - промпт за замовчуванням
python arena.py "свій промпт"   - свій промпт

Результати тестів і спостереження - в коментарі в кінці файлу.
"""

import os
import sys

import anthropic
from dotenv import load_dotenv

# ключ лежить в .env в корені репо (він в гітігнорі)
load_dotenv()

# нові моделі (Haiku/Sonnet/Opus 5.x) temperature взагалі не приймають - 400,
# тому для експерименту взято Haiku 4.5, яка ще підтримує цей параметр
MODEL = "claude-haiku-4-5"

# SDK 2.x шле версію API 2026-10-21, а в ній temperature прибрали на всіх моделях.
# на старій версії 2023-06-01 параметр ще працює
API_VERSION = "2023-06-01"

# у Claude temperature від 0.0 до 1.0 (2.0 як у OpenAI тут не можна)
TEMPERATURES = (0.0, 1.0)
MAX_TOKENS = 300

DEFAULT_PROMPT = (
    "Придумай назву і короткий слоган для кав'ярні, куди ходять програмісти. "
    "Дай один варіант, 2-3 речення."
)


def ask(client: anthropic.Anthropic, prompt: str, temperature: float) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
        # в SDK 2.x поля temperature вже нема, тому воно передається напряму в тіло запиту
        extra_body={"temperature": temperature},
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    if response.stop_reason == "max_tokens":
        text += "\n[Відповідь обрізана: досягнуто ліміт max_tokens]"
    return text


def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("Не знайдено ANTHROPIC_API_KEY. Скопіюй .env.example у .env і встав туди свій ключ.")

    # в консолі Windows інакше може впасти на емодзі у відповіді
    sys.stdout.reconfigure(encoding="utf-8")

    prompt = " ".join(sys.argv[1:]) or DEFAULT_PROMPT
    client = anthropic.Anthropic(default_headers={"anthropic-version": API_VERSION})

    print(f"Модель: {MODEL}\nПромпт: {prompt}\n")
    for temperature in TEMPERATURES:
        print(f"=== temperature = {temperature} ===")
        try:
            print(ask(client, prompt, temperature))
        except anthropic.AuthenticationError:
            sys.exit("Невірний API-ключ. Перевір ANTHROPIC_API_KEY у файлі .env.")
        except anthropic.RateLimitError:
            sys.exit("Забагато запитів або закінчився ліміт. Спробуй пізніше.")
        except anthropic.APIConnectionError:
            sys.exit("Немає з'єднання з API. Перевір інтернет.")
        except anthropic.APIStatusError as e:
            sys.exit(f"Помилка API ({e.status_code}): {e.message}")
        print()


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Що вийшло (29.10.2026, claude-haiku-4-5)
#
# Тест 1 - креатив, промпт за замовчуванням (назва + слоган для кав'ярні).
# 5 запусків.
#
#   temperature 0.0 - всі 5 разів одне й те саме, буква в букву:
#     "Code & Coffee. Де код пишеться швидше, ніж варить кава..."
#
#   temperature 1.0 - щоразу щось нове:
#     Code Brew / CODE & BREW / DEBUG COFFEE / Ctrl+Brew / "Кеш"
#     міняються не тільки назви, а й структура відповіді: десь окремий
#     "Слоган:", десь емодзі, десь жарт про розетки і Stack Overflow.
#     але й помилок більше: "кофе", "напиток", "на мові кода", "варится",
#     "кавʼяк", англійське "precision" посеред українського тексту.
#
# Тест 2 - факт: "Поясни одним реченням, що таке токен у LLM." 2 запуски.
#
#   temperature 0.0 - обидва рази однакове речення.
#   temperature 1.0 - майже те саме, відрізняється одне-два слова
#     ("генерації" замість "генерування", додалось "смислова").
#
# Висновки:
# - 0.0 = повторюваність. Одне питання - одна відповідь. Для коду, фактів,
#   JSON, класифікації саме те.
# - 1.0 = різноманітність. Для ідей і брейншторму добре, але українська
#   помітно псується, з'являються русизми і вставки англійською.
# - найцікавіше: на фактичному питанні температура майже нічого не змінює.
#   коли модель і так "впевнена" в наступному токені, підвищення температури
#   майже не впливає на результат. різницю видно тільки там, де багато нормальних
#   варіантів відповіді (креатив).
# - навіть на 0.0 є помилка ("кава не холодне"). температура не робить модель
#   розумнішою, вона тільки прибирає або додає випадковість.
# - 1.5 зі слайдів спробувати не вийшло: у Claude максимум 1.0.
# - на нових моделях Claude (5.x) temperature взагалі не можна змінити,
#   API повертає 400. там різноманітність регулюється промптом ("дай 5 різних
#   варіантів"), а глибину відповіді - через effort.
# ---------------------------------------------------------------------------
