# Presentation Bootstrap

[Скачать архив текущей ветки main (.zip)](https://github.com/idoziru/pitch-llm-agent/archive/refs/heads/main.zip)

Минимальный bootstrap-проект для создания бизнес-презентаций через LLM/coding agent.

## Что это

Шаблон помогает собрать презентацию из готового текста и визуальных референсов.

Визуальный стиль берётся из `visual_refs/`.

Агент создаёт:

- `style_brief.md`
- `image_manifest.json`
- `index.html`

## Структура

```text
project/
├── AGENTS.md
├── README.md
├── .gitignore
├── wording/
├── visual_refs/
├── imgs/
└── skills/
```

## Как пользоваться

1. Положи готовый текст презентации в `wording/`.
2. Положи визуальные референсы в `visual_refs/`.
3. Если есть дополнительные инструкции для агента, положи их в `skills/`.
4. Запусти LLM/coding agent в корне проекта.
5. Агент должен:
   - прочитать `AGENTS.md`;
   - проверить релевантные skills;
   - изучить `wording/`;
   - изучить `visual_refs/`;
   - создать или обновить `style_brief.md` на основе `visual_refs/`;
   - создать или обновить `image_manifest.json`;
   - создать или обновить `index.html`.
6. Сгенерируй изображения по `image_manifest.json`.
7. Положи готовые изображения в `imgs/`.
8. Открой `index.html` в браузере.
9. Запусти экспорт PNG через кнопку в браузере.

## Папки

### wording/

Готовый текст презентации.

Текст, цифры и факты считаются уже проверенными. Агент не должен менять их без явного разрешения.

### visual_refs/

Визуальные референсы:

- презентации;
- PDF;
- изображения;
- скриншоты;
- брендбуки;
- moodboards;
- понравившиеся примеры дизайна.

### imgs/

Готовые изображения, которые агент подставляет в презентацию, если они есть.

### skills/

Технические инструкции для агента.

Базовые skills уже лежат в папке:

- `html-structure.md`
- `png-export-safety.md`
- `slide-layout-safety.md`
- `image-manifest-prompts.md`

Можно добавлять свои `.md`-файлы.

## Важно

Не коммить рабочие материалы конкретной презентации:

- тексты в `wording/`;
- визуальные референсы в `visual_refs/`;
- изображения в `imgs/`;
- сгенерированные `index.html`, `style_brief.md`, `image_manifest.json`.

Это контролируется через `.gitignore`.
