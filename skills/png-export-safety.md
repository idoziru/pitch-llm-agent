# png-export-safety.md

## Назначение

Используй этот skill только для задач, связанных с PNG export, html2canvas, запуском локального сервера или проверкой экспортированных изображений.

Этот skill не задаёт визуальный стиль.

---

## Запуск проекта

Если в проекте есть `scripts/serve.py`, запускай из корня проекта:

```bash
python3 scripts/serve.py
```

Для Windows:

```bash
python scripts/serve.py
```

Не используй хардкод абсолютных путей конкретного пользователя.

---

## Экспорт PNG через браузер

`index.html` должен содержать кнопку:

```text
Export to PNG
```

Кнопка вызывает функцию:

```javascript
exportSlidesToPNG()
```

Экспорт должен создавать PNG-файлы по одному на каждый слайд.

Требования:

- каждый PNG должен быть ровно 1280×720px;
- слайды экспортируются последовательно;
- скачивания не должны запускаться параллельно;
- имена файлов должны сортироваться в правильном порядке.

---

## Именование PNG

Рекомендуемый формат:

```text
a-01.png
b-02.png
c-03.png
```

Для 27+ слайдов:

```text
aa-27.png
ab-28.png
```

---

## html2canvas: что может сломаться

html2canvas работает иначе, чем браузер. Проблемы возникают при:

- Неправильном flexbox (без `min-height: 0;`)
- Footer не отрендерилась → нужен fallback
- Неправильном размере canvas → нужна явная обрезка
- CSS variables в inline-стилях → html2canvas их не понимает

---

## Требования к HTML для export

Чтобы export PNG работал БЕЗ ошибок, HTML должен соответствовать этим требованиям:

### 1. Структура слайда — ОБЯЗАТЕЛЬНА

```html
<div class="slide">
  <div class="slide-header">...</div>
  <div class="slide-body">...</div>
  <div class="slide-footer">...</div>
</div>
```

**Если структура другая, export будет ломаться.**

### 2. CSS базовые правила — ОБЯЗАТЕЛЬНЫ

```css
* { box-sizing: border-box; margin: 0; padding: 0; }

.slide {
  width: 1280px;
  height: 720px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
}

.slide-header {
  flex-shrink: 0;
  height: 44px;
}

.slide-body {
  flex: 1;
  min-height: 0;    /* ← КРИТИЧНО */
  overflow: hidden;
}

.slide-footer {
  flex-shrink: 0;
  height: 40px;
}
```

**Без `min-height: 0;` на `.slide-body` контент выедет за пределы при export.**

### 3. Все вложенные контейнеры — ОБЯЗАТЕЛЬНЫ

```css
.grid, .flex-container, .split-56, .split-60, .grid-3 {
  min-height: 0;    /* ← КРИТИЧНО */
  overflow: hidden;
}

.grid > *, .flex-container > *, .split-56 > *, .split-60 > * {
  min-height: 0;    /* ← КРИТИЧНО */
  overflow: hidden;
}
```

**Это касается ВСЕХ контейнеров внутри slide-body:**
- Grid контейнеры
- Flex контейнеры
- Split контейнеры (56%, 60%, etc)
- Карточки с flex-содержимым

### 4. Цвета — ОБЯЗАТЕЛЬНЫ для печати

```css
.slide, .slide-header, .slide-footer {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
```

Без этого браузер может менять цвета при export.

### 5. Visual slots — ОБЯЗАТЕЛЬНЫ

```css
.visual-slot img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.visual-slot.has-image {
  background: transparent;
}

.visual-slot.has-image .ph-text {
  display: none;
}
```

---

## Чеклист для проверки ДО export

Перед тем, как пользователь экспортирует PNG:

- [ ] Все `.slide` имеют `width: 1280px; height: 720px;`?
- [ ] `.slide-body` имеет `flex: 1; min-height: 0; overflow: hidden;`?
- [ ] ВСЕ flex/grid контейнеры внутри body имеют `min-height: 0;`?
- [ ] Header высота 44px, footer 40px?
- [ ] Нет inline-стилей с CSS variables (html2canvas их не поймёт)?
- [ ] Все изображения используют `object-fit: contain;`?
- [ ] `box-sizing: border-box;` установлен для всех?

**Если хотя бы один пункт не выполнен, export будет ломаться.**

---

## Canvas crop

Даже если в браузере слайд выглядит правильно, после html2canvas обязательно обрезай canvas до целевого размера.

---

## Обязательные правила export-функции

1. Сохраняй оригинальные inline-стили до изменений.
2. Меняй стили только временно.
3. Header/footer/body фиксируй absolute-позиционированием.
4. Body не должен терять исходные `padding`, `justify-content`, `align-items`.
5. `canvas.toBlob` должен быть `await`.
6. После скачивания освобождай `URL.revokeObjectURL`.
7. После экспорта восстанавливай все стили.
8. Не оставляй слайды скрытыми после экспорта.
9. Не запускай скачивания параллельно.

---

## Проверка экспорта

После изменения export workflow проверь:

- кнопка `Export to PNG` видна;
- экспорт запускается;
- скачивается правильное количество PNG;
- каждый PNG 1280×720;
- footer/header видны;
- изображения не искажены;
- слайды сортируются правильно;
- после экспорта браузерный view восстановлен.
