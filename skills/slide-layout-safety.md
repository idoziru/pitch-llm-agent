# slide-layout-safety.md

## Назначение

Используй этот skill для задач, связанных с layout, сетками, высотой слайдов, overflow, header/footer и визуальной проверкой.

Этот skill не задаёт визуальный стиль.

Композиционный характер, плотность, размеры типографики и визуальная манера должны браться из `visual_refs/` и `style_brief.md`.

---

## Физика слайда

Слайд:

```text
1280×720px
```

Если есть header/footer:

```text
Header: 44px
Footer: 40px
Body: 636px
```

Перед добавлением большого количества контента оцени, помещается ли он в доступную высоту.

---

## Overflow

Обязательные технические правила:

```css
.slide {
  overflow: hidden;
}

.slide-body {
  overflow: hidden;
  min-height: 0;
}

.split-56,
.split-60 {
  min-height: 0;
}

.split-56 > div,
.split-60 > div {
  min-height: 0;
  overflow: hidden;
}
```

Если контент выходит за footer, сначала уменьши локально:

- количество строк;
- размер visual slot;
- gap;
- padding;
- font-size.

Не меняй всю сетку без необходимости.

---

## Header/footer

Header и footer должны быть технически стабильны на всех слайдах.

Проверяй:

- footer не выталкивается за нижнюю границу;
- номер слайда виден;
- header/footer не перекрывают контент;
- alignment одинаковый на всех слайдах.

Внешний вид header/footer бери из `style_brief.md`.

Если footer съезжает только в PNG export, смотри `skills/png-export-safety.md`.

---

## Требования к структуре слайда (для export)

Каждый слайд должен следовать этой структуре:

```html
<div class="slide">
  <div class="slide-header">
    <!-- header content -->
  </div>
  
  <div class="slide-body">
    <!-- main content: text, grids, cards, etc -->
  </div>
  
  <div class="slide-footer">
    <!-- footer: slide number, etc -->
  </div>
</div>
```

**CSS требования:**

```css
.slide-header {
  flex-shrink: 0;
  height: var(--header-h);  /* 44px */
}

.slide-body {
  flex: 1;
  min-height: 0;     /* ОБЯЗАТЕЛЬНО */
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.slide-footer {
  flex-shrink: 0;
  height: var(--footer-h);  /* 40px */
}
```

Если не будет `min-height: 0` на `.slide-body`, контент выедет за пределы слайда при export.

---

## Вложенные контейнеры (grid, flex внутри slide-body)

Все контейнеры внутри `.slide-body` должны иметь:

```css
.grid-or-flex-container {
  display: grid;  /* или flex */
  flex: 1;        /* если это flex-child */
  min-height: 0;  /* ОБЯЗАТЕЛЬНО */
  overflow: hidden;
}

.grid-or-flex-container > * {
  min-height: 0;  /* для всех детей */
  overflow: hidden;
}
```

**Примеры:**

```css
.split-56 {
  display: grid;
  grid-template-columns: 56% 1fr;
  gap: 52px;
  min-height: 0;        /* ← */
}

.split-56 > div {
  min-height: 0;        /* ← */
  overflow: hidden;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  min-height: 0;        /* ← */
}

.grid-3 > * {
  min-height: 0;        /* ← */
  overflow: hidden;
}
```

---

## Проверка в браузере (ПЕРЕД export)

После существенного изменения `index.html`:

1. **Открой в браузере** на `http://localhost:8000` (через `python3 scripts/serve.py`)
2. **Пролистай все слайды** — визуально проверь:
   - Header не съезжает?
   - Footer не съезжает?
   - Text не выходит за пределы?
   - Изображения не искажены?
3. **Откройте DevTools** (F12) и проверьте:
   - `.slide` имеет высоту 720px (не больше)
   - `.slide-body` не переполнена
   - Grid/flex не схлопываются

Не полагайся только на теоретический анализ CSS — html2canvas работает не так, как браузер.

---

## Сигналы проблем (что искать)

Если при export видишь эти проблемы, ищи `min-height: 0;`:

- Footer съехала вверх или исчезла
- Текст выходит за пределы слайда
- Grid/flex элементы неправильного размера
- Изображения обрезаны или искажены
