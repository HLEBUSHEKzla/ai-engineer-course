"""ДЗ 2 - арена температур: один промпт, два запити з різною temperature.

python arena.py                 - промпт за замовчуванням
python arena.py "свій промпт"   - свій промпт

Спостереження (запускав 3 рази з промптом про кав'ярню для програмістів):
- temperature 0.0: всі 3 рази слово в слово та сама відповідь - "Code & Coffee"
  з тим самим слоганом. Модель щоразу бере найімовірніший токен, тому результат
  передбачуваний і повторюваний. Добре для фактів, коду, класифікації, JSON.
- temperature 1.0: щоразу інша назва (Code Brew, CODE & BREW, DEBUG COFFEE),
  інший слоган і структура, більше жартів і емодзі. Для креативу краще,
  але й помилок більше: "кофе" замість "кава", "кава не холодне".
- навіть на 0.0 є дрібні мовні помилки ("не холодне") - температура не робить
  модель розумнішою, вона лише прибирає випадковість.
- у Claude діапазон 0.0-1.0, тому 1.5 зі слайдів тут не спробувати.
- головне: на нових моделях Claude (5.x) temperature більше не налаштовується,
  API на неї повертає 400. Різноманітність там регулюють промптом, а глибину
  міркувань - effort.
"""

import os
import sys

import anthropic
from dotenv import load_dotenv

# ключ лежить в .env в корені репо (він в гітігнорі)
load_dotenv()

# нові моделі (Haiku/Sonnet/Opus 5.x) temperature взагалі не приймають - 400,
# тому для експерименту беру Haiku 4.5, вона ще вміє
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
        # в SDK 2.x поля temperature вже нема, тому шлю його напряму в тіло запиту
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
