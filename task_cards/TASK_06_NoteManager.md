# 📚 TASK CARD #6: МЕНЕДЖЕР НОТАТОК

**Розробник**: Backend Developer  
**Файл**: `personal_assistant/managers/note_manager.py`  
**Пріоритет**: 🟡 СЕРЕДНІЙ (залежить від #2, #4)  
**Час**: 4-5 днів  
**Складність**: ⭐⭐⭐⭐

---

## 📋 ЗАВДАННЯ

Створити потужний менеджер для управління колекцією нотаток з розумною системою тегів, full-text пошуком та аналітикою використання.

## 🎯 МЕТА

Забезпечити:
- Повний CRUD для нотаток
- Потужний пошук по тексту та тегах
- Статистику використання тегів
- Гнучке сортування та фільтрацію
- Автоматичне збереження
- Експорт та імпорт нотаток

## 📦 АРХІТЕКТУРА КЛАСУ

```python
class NoteManager:
    """Менеджер для управління колекцією нотаток."""
    
    def __init__(self, storage: FileStorage) -> None:
        """Ініціалізація з автоматичним завантаженням даних."""
        self.storage = storage
        self.notes: List[Note] = []  # Список нотаток
        self.filename = "notes.json"
        self.load_notes()
```

## 🔧 CRUD ОПЕРАЦІЇ

### Створення:
```python
def create_note(self, title: str, content: str = "", tags: List[str] = None) -> Note:
    """
    Створення нової нотатки.
    - Створює Note об'єкт
    - Додає до колекції
    - Автоматично зберігає
    - Повертає створену нотатку
    """

def add_note(self, note: Note) -> int:
    """
    Додавання готової нотатки до колекції.
    Повертає індекс (позицію) нотатки в списку.
    """
```

### Читання та доступ:
```python
def get_note(self, index: int) -> Optional[Note]:
    """
    Отримання нотатки за індексом (1-based для користувача).
    Повертає Note або None якщо індекс неправильний.
    """

def get_all_notes(self, sort_by: str = "created") -> List[Tuple[int, Note]]:
    """
    Отримання всіх нотаток з сортуванням.
    sort_by: "created", "updated", "title", "tags_count"
    Повертає: [(1, note1), (2, note2), ...]
    """

def get_notes_count(self) -> int:
    """Загальна кількість нотаток."""
```

### Оновлення:
```python
def update_note(self, index: int, **kwargs) -> Optional[Note]:
    """
    Оновлення існуючої нотатки.
    kwargs: title, content, tags (замінює всі теги)
    Автоматично оновлює updated_at та зберігає.
    """

def add_tag_to_note(self, index: int, tag: str) -> bool:
    """Додавання тегу до існуючої нотатки."""

def remove_tag_from_note(self, index: int, tag: str) -> bool:
    """Видалення тегу з нотатки."""
```

### Видалення:
```python
def remove_note(self, index: int) -> bool:
    """
    Видалення нотатки за індексом.
    Повертає True якщо нотатка знайдена та видалена.
    Автоматично зберігає зміни.
    """

def clear_all_notes(self) -> int:
    """
    Видалення всіх нотаток.
    Повертає кількість видалених нотаток.
    """
```

## 🔍 ПОШУК ТА ФІЛЬТРАЦІЯ

### Full-text пошук:
```python
def search_notes(self, query: str, case_sensitive: bool = False) -> List[Tuple[int, Note]]:
    """
    Повнотекстовий пошук в заголовках та змісті.
    Повертає список (індекс, нотатка) відсортований за релевантністю.
    """

def search_in_titles(self, query: str) -> List[Tuple[int, Note]]:
    """Пошук тільки в заголовках нотаток."""

def search_in_content(self, query: str) -> List[Tuple[int, Note]]:
    """Пошук тільки в змісті нотаток."""
```

### Пошук за тегами:
```python
def find_notes_by_tags(self, tags: List[str], match_all: bool = False) -> List[Tuple[int, Note]]:
    """
    Пошук нотаток за тегами.
    match_all=False: OR логіка (хоча б один тег співпадає)
    match_all=True: AND логіка (всі теги мають співпадати)
    """

def find_notes_by_single_tag(self, tag: str) -> List[Tuple[int, Note]]:
    """Пошук нотаток з конкретним тегом."""

def get_notes_without_tags(self) -> List[Tuple[int, Note]]:
    """Нотатки без жодного тегу (для cleanup)."""
```

### Фільтрація за датами:
```python
def get_notes_created_after(self, date: datetime) -> List[Tuple[int, Note]]:
    """Нотатки створені після певної дати."""

def get_notes_updated_in_range(self, start_date: datetime, end_date: datetime) -> List[Tuple[int, Note]]:
    """Нотатки оновлені в певному періоді."""

def get_recent_notes(self, days: int = 7) -> List[Tuple[int, Note]]:
    """Нотатки створені/оновлені за останні N днів."""
```

## 🏷️ УПРАВЛІННЯ ТЕГАМИ

### Статистика тегів:
```python
def get_all_tags(self) -> Set[str]:
    """Унікальний набір всіх тегів у колекції."""

def get_tag_statistics(self) -> Dict[str, int]:
    """
    Статистика використання тегів.
    Повертає: {"python": 15, "робота": 8, "ідеї": 5}
    """

def get_most_popular_tags(self, limit: int = 10) -> List[Tuple[str, int]]:
    """
    Найпопулярніші теги з кількістю використань.
    Повертає: [("python", 15), ("робота", 8)]
    """

def get_unused_tags(self) -> Set[str]:
    """Теги які були але зараз не використовуються."""
```

### Управління тегами:
```python
def rename_tag(self, old_tag: str, new_tag: str) -> int:
    """
    Перейменування тегу у всіх нотатках.
    Повертає кількість оновлених нотаток.
    """

def merge_tags(self, tags_to_merge: List[str], new_tag: str) -> int:
    """
    Об'єднання кількох тегів в один.
    Замінює всі tags_to_merge на new_tag.
    """

def cleanup_unused_tags(self) -> int:
    """Видалення тегів які не використовуються."""
```

## 📊 СТАТИСТИКА ТА АНАЛІТИКА

### Основна статистика:
```python
def get_statistics(self) -> Dict[str, Any]:
    """
    Детальна статистика нотаток:
    {
        "total_notes": 245,
        "total_tags": 67,
        "average_tags_per_note": 2.3,
        "total_words": 15420,
        "average_words_per_note": 62.9,
        "most_popular_tag": "python",
        "longest_note": {"index": 15, "title": "...", "words": 450},
        "shortest_note": {"index": 3, "title": "...", "words": 5},
        "notes_without_tags": 12,
        "creation_trend": {  # нотатки за останні місяці
            "2024-01": 15,
            "2024-02": 23,
            "2024-03": 18
        },
        "last_updated": "2024-01-15T10:30:00"
    }
    """

def get_word_count_statistics(self) -> Dict[str, int]:
    """Статистика кількості слів: min, max, average, total."""

def get_creation_timeline(self, period: str = "month") -> Dict[str, int]:
    """
    Часова лінія створення нотаток.
    period: "day", "week", "month", "year"
    """
```

## 📋 СОРТУВАННЯ

### Сортування методи:
```python
def sort_notes_by_date(self, reverse: bool = True) -> List[Tuple[int, Note]]:
    """Сортування за датою створення."""

def sort_notes_by_title(self) -> List[Tuple[int, Note]]:
    """Сортування за заголовком (алфавітне)."""

def sort_notes_by_update_date(self, reverse: bool = True) -> List[Tuple[int, Note]]:
    """Сортування за датою останнього оновлення."""

def sort_notes_by_tags_count(self, reverse: bool = True) -> List[Tuple[int, Note]]:
    """Сортування за кількістю тегів."""

def sort_notes_by_word_count(self, reverse: bool = True) -> List[Tuple[int, Note]]:
    """Сортування за кількістю слів."""
```

## 💾 ЗБЕРЕЖЕННЯ ТА ЕКСПОРТ

### Persistence методи:
```python
def save_notes(self) -> None:
    """
    Збереження всіх нотаток у JSON файл.
    Використовує Note.to_dict() для серіалізації.
    """

def load_notes(self) -> None:
    """
    Завантаження нотаток з JSON файлу.
    Створює Note об'єкти через Note.from_dict().
    """
```

### Експорт та імпорт:
```python
def export_notes(self, format: str = "json", tags: List[str] = None) -> str:
    """
    Експорт нотаток у різних форматах.
    format: "json", "txt", "markdown", "csv"
    tags: експорт тільки нотаток з певними тегами
    Повертає шлях до створеного файлу.
    """

def export_to_markdown(self, filepath: str, tags: List[str] = None) -> None:
    """Експорт в Markdown формат з красивим форматуванням."""

def import_notes(self, filepath: str, format: str = "auto") -> int:
    """
    Імпорт нотаток з файлу.
    Повертає кількість успішно імпортованих нотаток.
    """
```

## 🚀 ADVANCED ФУНКЦІЇ

### Пакетні операції:
```python
def add_notes_batch(self, notes: List[Note]) -> List[int]:
    """Додавання множинних нотаток за одну операцію."""

def update_notes_batch(self, updates: Dict[int, Dict[str, Any]]) -> int:
    """Пакетне оновлення нотаток."""

def apply_tags_to_multiple(self, indices: List[int], tags: List[str]) -> int:
    """Додавання тегів до кількох нотаток одночасно."""
```

### Аналітичні функції:
```python
def find_similar_notes(self, note_index: int, limit: int = 5) -> List[Tuple[int, Note, float]]:
    """
    Пошук схожих нотаток за тегами та змістом.
    Повертає: [(індекс, нотатка, схожість_0_до_1)]
    """

def get_tag_co_occurrence(self) -> Dict[str, Dict[str, int]]:
    """
    Аналіз які теги часто використовуються разом.
    Повертає: {"python": {"код": 10, "навчання": 7}}
    """
```

## ✅ КРИТЕРІЇ ПРИЙНЯТТЯ

### Функціональні вимоги:
- [ ] Всі CRUD операції працюють з правильною індексацією
- [ ] Full-text пошук швидкий та точний
- [ ] Система тегів з AND/OR логікою
- [ ] Статистика відображає реальні дані
- [ ] Сортування працює за всіма критеріями
- [ ] Експорт/імпорт зберігає всі дані

### Технічні вимоги:
- [ ] Індекси для користувача починаються з 1
- [ ] Type hints для всіх методів
- [ ] Efficient пошукові алгоритми
- [ ] Proper error handling
- [ ] Unit тести покривають всі сценарії

### Якісні вимоги:
- [ ] Швидка робота з великою кількістю нотаток
- [ ] Intuitive API design
- [ ] Memory efficient операції
- [ ] Robust handling edge cases

## 🧪 ТЕСТОВІ СЦЕНАРІЇ

### Основні CRUD операції:
```python
manager = NoteManager(storage)

# Створення нотатки
note = manager.create_note("Перша нотатка", "Зміст нотатки", ["тест", "важливо"])
assert note.title == "Перша нотатка"
assert len(manager.notes) == 1

# Отримання за індексом (1-based)
retrieved = manager.get_note(1)
assert retrieved is not None
assert retrieved.title == "Перша нотатка"

# Оновлення
updated = manager.update_note(1, title="Оновлена нотатка")
assert updated.title == "Оновлена нотатка"
assert updated.updated_at > updated.created_at

# Видалення  
result = manager.remove_note(1)
assert result == True
assert len(manager.notes) == 0
```

### Пошук та фільтрація:
```python
# Додаємо тестові дані
notes_data = [
    ("Python Tutorial", "Learning Python programming", ["python", "навчання"]),
    ("Shopping List", "Buy milk, bread, eggs", ["побут"]),
    ("Work Notes", "Meeting with Python team", ["робота", "python"])
]

for title, content, tags in notes_data:
    manager.create_note(title, content, tags)

# Full-text пошук
results = manager.search_notes("python")
assert len(results) == 2  # Tutorial та Work Notes

# Пошук за тегами
python_notes = manager.find_notes_by_tags(["python"])
assert len(python_notes) == 2

# AND логіка
work_python = manager.find_notes_by_tags(["робота", "python"], match_all=True)
assert len(work_python) == 1
assert work_python[0][1].title == "Work Notes"
```

### Система тегів:
```python
# Статистика тегів
tag_stats = manager.get_tag_statistics()
assert tag_stats["python"] == 2
assert tag_stats["навчання"] == 1

# Найпопулярніші теги
popular = manager.get_most_popular_tags(3)
assert popular[0][0] == "python"  # Найпопулярніший
assert popular[0][1] == 2  # 2 використання

# Перейменування тегу
renamed_count = manager.rename_tag("python", "пітон")
assert renamed_count == 2
assert "пітон" in manager.get_all_tags()
assert "python" not in manager.get_all_tags()
```

### Сортування:
```python
import time

# Створюємо нотатки з різними датами
note1 = manager.create_note("A Note", "Content")
time.sleep(0.01)
note2 = manager.create_note("Z Note", "Content") 
time.sleep(0.01)
note3 = manager.create_note("B Note", "Much longer content with many words")

# Сортування за заголовком
sorted_by_title = manager.sort_notes_by_title()
titles = [note.title for idx, note in sorted_by_title]
assert titles == ["A Note", "B Note", "Z Note"]

# Сортування за кількістю слів
sorted_by_words = manager.sort_notes_by_word_count()
assert sorted_by_words[0][1].title == "B Note"  # Найдовша
```

### Збереження та завантаження:
```python
# Збереження стану
original_count = len(manager.notes)
manager.save_notes()

# Новий менеджер
new_manager = NoteManager(storage)
assert len(new_manager.notes) == original_count

# Перевірка цілісності
for i in range(len(manager.notes)):
    original = manager.notes[i]
    loaded = new_manager.notes[i]
    assert original.title == loaded.title
    assert original.content == loaded.content
    assert original.tags == loaded.tags
```

### Performance тести:
```python
import time

# Тест з великою кількістю нотаток
start_time = time.time()
for i in range(500):
    manager.create_note(f"Note {i}", f"Content of note {i}", [f"tag{i%10}"])

# Пошук має бути швидким
search_start = time.time()
results = manager.search_notes("Note")
search_time = time.time() - search_start
assert search_time < 1.0  # < 1 секунди для 500 нотаток

# Статистика теж швидка
stats_start = time.time()
stats = manager.get_statistics()
stats_time = time.time() - stats_start
assert stats_time < 0.5
```

## 🔗 ЗАЛЕЖНОСТІ

**Потребує**:
- FileStorage (завдання #2)  
- Note model (завдання #4)

**Імпорти**:
```python
from typing import List, Dict, Set, Optional, Any, Tuple
from datetime import datetime, timedelta
import re
from collections import Counter
from ..storage.file_storage import FileStorage
from ..models.note import Note
```

**Використовується в**:
- CLI Interface (завдання #9)

## 📁 СТРУКТУРА КОДУ

```python
# personal_assistant/managers/note_manager.py

from typing import List, Dict, Set, Optional, Any, Tuple
from datetime import datetime, timedelta
import re
from collections import Counter
from ..storage.file_storage import FileStorage
from ..models.note import Note

class NoteManager:
    """Менеджер для управління колекцією нотаток."""
    
    def __init__(self, storage: FileStorage) -> None:
        """Ініціалізація з автоматичним завантаженням."""
        
    # CRUD операції
    def create_note(self, title: str, content: str = "", tags: List[str] = None) -> Note: ...
    def add_note(self, note: Note) -> int: ...
    def get_note(self, index: int) -> Optional[Note]: ...
    def get_all_notes(self, sort_by: str = "created") -> List[Tuple[int, Note]]: ...
    def update_note(self, index: int, **kwargs) -> Optional[Note]: ...
    def remove_note(self, index: int) -> bool: ...
    
    # Пошук
    def search_notes(self, query: str, case_sensitive: bool = False) -> List[Tuple[int, Note]]: ...
    def find_notes_by_tags(self, tags: List[str], match_all: bool = False) -> List[Tuple[int, Note]]: ...
    def search_in_titles(self, query: str) -> List[Tuple[int, Note]]: ...
    
    # Теги
    def get_all_tags(self) -> Set[str]: ...
    def get_tag_statistics(self) -> Dict[str, int]: ...
    def rename_tag(self, old_tag: str, new_tag: str) -> int: ...
    def add_tag_to_note(self, index: int, tag: str) -> bool: ...
    
    # Статистика
    def get_statistics(self) -> Dict[str, Any]: ...
    def get_creation_timeline(self, period: str = "month") -> Dict[str, int]: ...
    
    # Сортування
    def sort_notes_by_date(self, reverse: bool = True) -> List[Tuple[int, Note]]: ...
    def sort_notes_by_title(self) -> List[Tuple[int, Note]]: ...
    
    # Persistence
    def save_notes(self) -> None: ...
    def load_notes(self) -> None: ...
    def export_notes(self, format: str = "json", tags: List[str] = None) -> str: ...
    
    # Утиліти
    def _auto_save(self) -> None: ...
    def _calculate_similarity(self, note1: Note, note2: Note) -> float: ...
    def _user_index_to_internal(self, user_index: int) -> Optional[int]: ...
```

## 📚 РЕСУРСИ

- [Python collections.Counter](https://docs.python.org/3/library/collections.html#collections.Counter)
- [Text processing in Python](https://docs.python.org/3/library/string.html)
- [Regular expressions](https://docs.python.org/3/library/re.html)
- [Similarity algorithms](https://en.wikipedia.org/wiki/Jaccard_index)

## 🚀 ГОТОВНІСТЬ ДО ЗДАЧІ

### Checklist:
- [ ] Всі CRUD операції з правильною індексацією
- [ ] Потужний пошук та фільтрація
- [ ] Система тегів з аналітикою
- [ ] Статистика та сортування
- [ ] Експорт/імпорт функціонал
- [ ] Performance оптимізації
- [ ] Integration з FileStorage
- [ ] Code review пройдено

**Використовується в**: CLI Interface (завдання #9)