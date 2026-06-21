# html-structure.md

## Назначение

Используй этот skill для технической структуры `index.html`, visual slots и placeholder mechanics.

Этот skill не задаёт визуальный стиль.

Все решения о цветах, шрифтах, визуальном языке, настроении, плотности и композиционном характере должны браться из `visual_refs/` и `style_brief.md`.

---

## Базовые требования

`index.html` должен быть одним файлом:

- HTML, CSS и JS внутри;
- без сборки;
- без Node.js;
- без внешних локальных зависимостей;
- Google Fonts допустимы через CDN, если они соответствуют `style_brief.md`;
- font files в проект не добавлять.

---

## Canvas

Каждый слайд:

```css
.slide {
  width: 1280px;
  height: 720px;
  overflow: hidden;
}
```

Слайды отображаются вертикально в браузере.

---

## CSS variables

Можно использовать CSS custom properties для технической поддержки консистентности.

Не задавай дефолтную палитру или дефолтную типографику из этого skill.

Значения переменных должны быть получены из `style_brief.md`.

Допустимый паттерн:

```css
:root {
  --bg: /* value from style_brief.md */;
  --text: /* value from style_brief.md */;
  --accent: /* value from style_brief.md */;
  --font-display: /* value from style_brief.md */;
  --font-body: /* value from style_brief.md */;
  --header-h: 44px;
  --footer-h: 40px;
}
```

---

## Visual slots

Visual slot должен поддерживать два состояния:

1. placeholder;
2. найденное изображение.

Технический паттерн:

```css
.visual-slot {
  position: relative;
  overflow: hidden;
}

.visual-slot.has-image {
  background: transparent;
}

.visual-slot img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}
```

Цвета, радиусы, фон и оформление placeholder бери из `style_brief.md`.

---

## Placeholder

Placeholder должен быть:

- подробным;
- на русском языке;
- достаточно конкретным для генерации изображения;
- с filename;
- с aspect ratio;
- с target size.

Текст placeholder может быть мелким, чтобы не портить композицию.

Не задавай внешний вид placeholder из этого skill. Используй `style_brief.md`.

---

## Не переписывать HTML/CSS без причины

Если нужно изменить один слайд, не меняй всю структуру.

Перед изменением:

1. Найди существующий класс.
2. Проверь, где он используется.
3. Если класс общий, не ломай другие слайды.
4. Для локального исключения лучше добавить modifier, чем менять базовый класс.
