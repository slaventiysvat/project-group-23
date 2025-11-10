# 📝 TASK CARD #4: МОДЕЛЬ НОТАТКИ

**Розробник**: Backend Developer  
**Файл**: `personal_assistant/models/note.py`  
**Пріоритет**: 🟡 СЕРЕДНІЙ  
**Час**: 3-4 дні  
**Складність**: ⭐⭐⭐⭐

---

## 📋 ЗАВДАННЯ

Створити повнофункціональну модель нотатки з системою тегів, метаданими та потужними можливостями пошуку.

## 🎯 МЕТА

Забезпечити:
- Зберігання заголовку та змісту нотаток
- Гнучку систему тегів для категоризації
- Автоматичне управління метаданими (дати створення/оновлення)
- Ефективний пошук по тексту та тегах
- Валідацію та нормалізацію даних

## 📦 СТРУКТУРА КЛАСУ

```python
class Note:
    """Модель нотатки з системою тегів та метаданими."""
    
    def __init__(self, title: str, content: str = "", tags: List[str] = None) -> None:
        """Створення нотатки з автоматичними timestamp."""
        self.title = title                              # Заголовок
        self.content = content                          # Зміст  
        self.tags: Set[str] = set()                     # Теги (унікальні)
        self.created_at = datetime.now()                # Створено
        self.updated_at = datetime.now()                # Оновлено
        
        if tags:
            for tag in tags:
                self.add_tag(tag)
```

## 🔧 ОБОВ'ЯЗКОВІ МЕТОДИ

### Управління змістом:
```python
def set_title(self, title: str) -> None:
    """
    Встановлення нового заголовку з валідацією.
    Автоматично оновлює updated_at.
    """
    
def set_content(self, content: str) -> None:
    """
    Встановлення нового змісту.
    Автоматично оновлює updated_at.
    """
```

### Система тегів:
```python
def add_tag(self, tag: str) -> None:
    """
    Додавання тегу з валідацією та нормалізацією.
    Правила валідації:
    - Тільки літери, цифри, дефіс, підкреслення
    - Максимум 30 символів
    - Автоматичне приведення до нижнього регістру
    """
    
def remove_tag(self, tag: str) -> bool:
    """
    Видалення тегу.
    Повертає True якщо тег було знайдено та видалено.
    """
    
def has_tag(self, tag: str) -> bool:
    """Перевірка чи має нотатка певний тег."""
    
def clear_tags(self) -> None:
    """Видалення всіх тегів з нотатки."""
```

### Пошукові методи:
```python
def search_in_content(self, query: str, case_sensitive: bool = False) -> bool:
    """
    Пошук підрядка в заголовку та змісті нотатки.
    Підтримує регістрозалежний та регістронезалежний пошук.
    """
    
def matches_tags(self, tags: List[str]) -> bool:
    """
    Перевіряє чи має нотатка хоча б один з переданих тегів.
    Корисно для фільтрації по тегах.
    """
    
def matches_all_tags(self, tags: List[str]) -> bool:
    """
    Перевіряє чи має нотатка ВСІ передані теги.
    Для точнішої фільтрації (AND логіка).
    """
```

### Аналітичні методи:
```python
def get_word_count(self) -> int:
    """Підрахунок слів у змісті нотатки (без заголовку)."""
    
def get_char_count(self) -> int:
    """Підрахунок символів у змісті (без пробілів)."""
    
def get_reading_time(self) -> int:
    """Приблизний час читання в хвилинах (200 слів/хв)."""
```

## 🔒 ВАЛІДАЦІЯ ТЕГІВ

### Правила валідації:
```python
TAG_PATTERN = r'^[a-zA-Zа-яА-ЯіІїЇєЄ0-9_\-]+$'
MAX_TAG_LENGTH = 30

def _validate_tag(self, tag: str) -> str:
    """
    Валідація та нормалізація тегу:
    1. Видалення пробілів
    2. Приведення до нижнього регістру  
    3. Перевірка довжини (≤ 30 символів)
    4. Перевірка на відповідність регекспу
    5. Перевірка що не порожній
    """
```

### Приклади валідних/невалідних тегів:
```python
# ✅ Валідні теги:
"робота" → "робота"
"Python-Programming" → "python-programming"  
"важливе_123" → "важливе_123"
"AI_ML" → "ai_ml"

# ❌ Неvalidні теги:
""                    # Порожній
"дуже довгий тег що перевищує ліміт"  # > 30 символів
"тег з пробілами"     # Пробіли заборонені
"тег@#$%"            # Спеціальні символи
"123"                # Тільки цифри (дискусійно, можна дозволити)
```

## 📊 СЕРІАЛІЗАЦІЯ

### Методи збереження/завантаження:
```python
def to_dict(self) -> Dict[str, Any]:
    """
    Серіалізація в словник для JSON збереження.
    Повертає:
    {
        "title": "Заголовок нотатки",
        "content": "Зміст нотатки...",
        "tags": ["робота", "важливо", "python"],
        "created_at": "2024-01-15T10:30:00.123456",
        "updated_at": "2024-01-16T15:45:00.789012"
    }
    """

@classmethod  
def from_dict(cls, data: Dict[str, Any]) -> 'Note':
    """
    Десеріалізація зі словника.
    Відновлює всі поля включно з timestamp.
    """
```

## 🎨 СПЕЦІАЛЬНІ МЕТОДИ

### Представлення:
```python
def __str__(self) -> str:
    """
    Красивий вивід для користувача:
    
    📝 Заголовок нотатки
    📅 Створено: 15.01.2024 10:30
    📅 Оновлено: 16.01.2024 15:45
    🏷️ Теги: робота, важливо, python
    📊 Слів: 156 | Час читання: ~1 хв
    
    Зміст нотатки тут...
    (обрізано якщо довгий)
    """

def __repr__(self) -> str:
    """Технічне представлення для debug."""
```

### Порівняння:
```python
def __eq__(self, other) -> bool:
    """Порівняння за заголовком та змістом."""
    
def __lt__(self, other) -> bool:
    """Сортування за датою створення (для sorted())."""
    
def __hash__(self) -> int:
    """Хеш за заголовком для використання в set."""
```

## ✅ КРИТЕРІЇ ПРИЙНЯТТЯ

### Функціональні вимоги:
- [ ] Створення нотатки з валідацією заголовку
- [ ] Автоматичне оновлення updated_at при змінах
- [ ] Система тегів з валідацією працює
- [ ] Пошук по тексту (case-sensitive/insensitive)
- [ ] Пошук по тегах (AND/OR логіка)
- [ ] Підрахунок статистики (слова, символи, час читання)

### Технічні вимоги:
- [ ] Type hints для всіх методів
- [ ] Docstrings з прикладами
- [ ] Proper handling неvalідних тегів
- [ ] Efficient пошукові алгоритми
- [ ] Серіалізація з datetime у ISO format

### Якісні вимоги:
- [ ] Читабельний __str__ output з емодзі
- [ ] Consistent API design
- [ ] Memory efficient (Set для тегів)
- [ ] Fast операції пошуку

## 🧪 ТЕСТОВІ СЦЕНАРІЇ

### Створення та основні операції:
```python
# Створення нотатки
note = Note("Моя перша нотатка", "Це зміст нотатки")
assert note.title == "Моя перша нотатка" 
assert note.content == "Це зміст нотатки"
assert len(note.tags) == 0
assert note.created_at <= datetime.now()

# З тегами при створенні
note = Note("Робочі завдання", "Список справ", ["робота", "важливо"])
assert "робота" in note.tags
assert "важливо" in note.tags
assert len(note.tags) == 2
```

### Управління тегами:
```python
# Додавання тегів
note.add_tag("Python")
note.add_tag("PROGRAMMING")  # Нормалізується до "programming"
assert "python" in note.tags
assert "programming" in note.tags

# Валідація тегів
with pytest.raises(ValueError):
    note.add_tag("")  # Порожній
    note.add_tag("тег з пробілами")  # Пробіли
    note.add_tag("a" * 31)  # Занадто довгий

# Видалення тегів
result = note.remove_tag("python")
assert result == True
assert "python" not in note.tags

result = note.remove_tag("неіснуючий")  
assert result == False
```

### Пошук:
```python
note = Note("Python Tutorial", "Learning Python programming language")
note.add_tag("python")
note.add_tag("tutorial")

# Пошук в тексті
assert note.search_in_content("python") == True  # case-insensitive
assert note.search_in_content("PYTHON", case_sensitive=True) == False
assert note.search_in_content("Java") == False

# Пошук за тегами
assert note.matches_tags(["python"]) == True
assert note.matches_tags(["java", "python"]) == True  # OR логіка
assert note.matches_tags(["java", "c++"]) == False

assert note.matches_all_tags(["python", "tutorial"]) == True  # AND
assert note.matches_all_tags(["python", "advanced"]) == False
```

### Оновлення та timestamp:
```python
import time

note = Note("Test", "Content")
created_time = note.created_at
updated_time = note.updated_at

# Чекаємо щоб час змінився
time.sleep(0.01)

# Оновлення змісту
note.set_content("New content")
assert note.updated_at > updated_time
assert note.created_at == created_time  # Не змінюється

# Оновлення заголовку
note.set_title("New Title")
assert note.updated_at > note.created_at
```

### Статистика:
```python
note = Note("Test", "Hello world! This is a test note with multiple words.")
note.add_tag("test")

assert note.get_word_count() == 10  # "Hello world This is a test note with multiple words"
assert note.get_char_count() > 0
assert note.get_reading_time() == 1  # < 200 слів = 1 хвилина
```

### Серіалізація:
```python
# Збереження
note = Note("Test Note", "Content here", ["tag1", "tag2"])
data = note.to_dict()
assert data["title"] == "Test Note"
assert "tag1" in data["tags"]
assert "created_at" in data

# Відновлення
restored = Note.from_dict(data)
assert restored.title == note.title
assert restored.content == note.content
assert restored.tags == note.tags
assert restored.created_at == note.created_at
```

## 🔗 ЗАЛЕЖНОСТІ

**Імпорти**:
```python
from typing import List, Set, Dict, Any, Optional
from datetime import datetime
import re
```

**Використовується в**:
- NoteManager (завдання #6)
- CLI Interface (завдання #9)

## 📁 СТРУКТУРА КОДУ

```python
# personal_assistant/models/note.py

from typing import List, Set, Dict, Any, Optional
from datetime import datetime
import re

class Note:
    """Модель нотатки з системою тегів та метаданими."""
    
    # Константи валідації
    TAG_PATTERN = r'^[a-zA-Zа-яА-ЯіІїЇєЄ0-9_\-]+$'
    MAX_TAG_LENGTH = 30
    WORDS_PER_MINUTE = 200  # Для розрахунку часу читання
    
    def __init__(self, title: str, content: str = "", tags: List[str] = None):
        """Створення нотатки з автоматичними timestamp."""
        
    # Управління змістом
    def set_title(self, title: str) -> None: ...
    def set_content(self, content: str) -> None: ...
    
    # Система тегів  
    def add_tag(self, tag: str) -> None: ...
    def remove_tag(self, tag: str) -> bool: ...
    def has_tag(self, tag: str) -> bool: ...
    def clear_tags(self) -> None: ...
    
    # Пошук
    def search_in_content(self, query: str, case_sensitive: bool = False) -> bool: ...
    def matches_tags(self, tags: List[str]) -> bool: ...
    def matches_all_tags(self, tags: List[str]) -> bool: ...
    
    # Аналітика
    def get_word_count(self) -> int: ...
    def get_char_count(self) -> int: ...
    def get_reading_time(self) -> int: ...
    
    # Утиліти
    def _validate_tag(self, tag: str) -> str: ...
    def _update_timestamp(self) -> None: ...
    
    # Серіалізація
    def to_dict(self) -> Dict[str, Any]: ...
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Note': ...
    
    # Спеціальні методи
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other) -> bool: ...
    def __lt__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
```

## 📚 РЕСУРСИ

- [Python Set operations](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [Regular expressions in Python](https://docs.python.org/3/library/re.html)
- [Working with datetime](https://docs.python.org/3/library/datetime.html)
- [String methods in Python](https://docs.python.org/3/library/stdtypes.html#string-methods)

## 🚀 ГОТОВНІСТЬ ДО ЗДАЧІ

### Checklist:
- [ ] Всі методи реалізовані та протестовані
- [ ] Система тегів з валідацією працює
- [ ] Пошук efficient та точний
- [ ] Автоматичні timestamp працюють
- [ ] Серіалізація зберігає всі дані
- [ ] Code review пройдено

**Розблоковує**: NoteManager (завдання #6), CLI Interface (завдання #9)