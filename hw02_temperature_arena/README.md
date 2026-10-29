# ДЗ 2 — арена температур

- [x] Зробити новий файл `arena.py`
- [x] Обрати API та промпт (Claude API, промпт про кав'ярню для програмістів)
- [x] Скрипт робить 2 запити з різним рівнем temperature (0.0 і 1.0)
- [x] Коментом написати спостереження (на початку [`arena.py`](arena.py))
- [ ] Закинути код на GitHub

[`arena.py`](arena.py) надсилає один і той самий промпт двічі, з temperature 0.0 і 1.0, і друкує обидві відповіді.

```bash
python hw02_temperature_arena/arena.py                 # промпт за замовчуванням
python hw02_temperature_arena/arena.py "свій промпт"   # свій промпт
```

## Чому тут Haiku 4.5, а не Haiku 5.5

На нових моделях Claude (Haiku / Sonnet / Opus 5.x) temperature більше не налаштовується, тому API на неї повертає 400. До того ж SDK `anthropic` 2.x шле версію API `2026-10-21`, у якій `temperature` прибрали для всіх моделей. Тому скрипт:

- бере модель `claude-haiku-4-5`, яка ще приймає temperature ($1 / $5 за 1M вхідних / вихідних токенів, один запуск коштує менше цента);
- шле заголовок `anthropic-version: 2023-06-01`;
- передає `temperature` через `extra_body`, бо в SDK 2.x такого аргументу вже немає.

У Claude temperature від 0.0 до 1.0 (в OpenAI від 0.0 до 2.0).
