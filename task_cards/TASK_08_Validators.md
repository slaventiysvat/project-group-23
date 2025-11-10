# 🔧 TASK CARD #8: ВАЛІДАТОРИ ТА УТИЛІТИ

**Розробник**: Junior/Middle Developer  
**Файл**: `personal_assistant/utils/validators.py`  
**Пріоритет**: 🟢 НИЗЬКИЙ  
**Час**: 2-3 дні  
**Складність**: ⭐⭐

---

## 📋 ЗАВДАННЯ

Створити набір допоміжних функцій для валідації користувацького вводу, форматування тексту та парсингу команд у CLI інтерфейсі.

## 🎯 МЕТА

Забезпечити:
- Уніфіковані функції валідації для CLI
- Красиве форматування виводу
- Парсинг та обробку користувацьких команд
- Допоміжні утиліти для роботи з текстом
- Зменшення дублювання коду

## 📦 ФУНКЦІЇ ВАЛІДАЦІЇ

### Базова валідація:
```python
def validate_input_not_empty(value: str, field_name: str) -> str:
    """
    Перевірка що ввід не порожній після очищення.
    
    Args:
        value: Введене значення
        field_name: Назва поля для помилки
        
    Returns:
        Очищене значення без зайвих пробілів
        
    Raises:
        ValueError: Якщо значення порожнє
        
    Examples:
        >>> validate_input_not_empty("  Іван  ", "ім'я")
        "Іван"
        >>> validate_input_not_empty("", "телефон")
        ValueError: Поле 'телефон' не може бути порожнім
    """

def validate_positive_integer(value: str, field_name: str, min_value: int = 1, max_value: int = None) -> int:
    """
    Перевірка та перетворення в позитивне ціле число.
    
    Args:
        value: Введене значення
        field_name: Назва поля для помилки  
        min_value: Мінімальне значення (за замовчуванням 1)
        max_value: Максимальне значення (необов'язково)
        
    Returns:
        Перетворене число
        
    Examples:
        >>> validate_positive_integer("5", "кількість днів")
        5
        >>> validate_positive_integer("-1", "індекс")
        ValueError: Поле 'індекс' має бути числом >= 1
    """
```

### Спеціалізована валідація:
```python
def validate_choice_from_list(value: str, choices: List[str], field_name: str = "вибір") -> str:
    """
    Валідація вибору зі списку варіантів (регістронезалежна).
    
    Args:
        value: Введене значення
        choices: Список допустимих варіантів
        field_name: Назва поля для помилки
        
    Returns:
        Нормалізований вибір (в оригінальному регістрі з choices)
        
    Examples:
        >>> validate_choice_from_list("YES", ["yes", "no"], "підтвердження")
        "yes"
    """

def validate_yes_no(value: str) -> bool:
    """
    Перетворення yes/no вводу в boolean.
    
    Підтримувані варіанти:
    True: "y", "yes", "так", "т", "1", "true"
    False: "n", "no", "ні", "н", "0", "false"
    
    Args:
        value: Введене значення
        
    Returns:
        Boolean значення
        
    Examples:
        >>> validate_yes_no("так")
        True
        >>> validate_yes_no("n")
        False
    """

def validate_tags_input(tags_str: str) -> List[str]:
    """
    Парсинг та валідація тегів з рядка.
    
    Args:
        tags_str: Рядок з тегами через кому/пробіл
        
    Returns:
        Список валідних унікальних тегів
        
    Examples:
        >>> validate_tags_input("python, робота,  AI_ML")
        ["python", "робота", "ai_ml"]
        >>> validate_tags_input("тег з пробілами, valid_tag")
        ValueError: Тег 'тег з пробілами' містить неприпустимі символи
    """
```

### Валідація дат та часу:
```python
def validate_date_input(date_str: str) -> str:
    """
    Валідація та нормалізація дати.
    
    Підтримувані формати: DD.MM.YYYY, DD-MM-YYYY, DD/MM/YYYY
    
    Returns:
        Нормалізована дата у форматі DD.MM.YYYY
        
    Examples:
        >>> validate_date_input("15/03/1990")
        "15.03.1990"
    """

def validate_days_ahead(days_str: str) -> int:
    """
    Валідація кількості днів наперед (для днів народження).
    
    Args:
        days_str: Кількість днів як рядок
        
    Returns:
        Число днів (1-365)
    """
```

## 🎨 ФУНКЦІЇ ФОРМАТУВАННЯ

### Форматування списків:
```python
def format_list_for_display(items: List[Any], max_items: int = None, 
                          item_formatter: Callable = str) -> str:
    """
    Красиве форматування списку для виводу.
    
    Args:
        items: Список елементів
        max_items: Максимум елементів для показу
        item_formatter: Функція форматування окремого елемента
        
    Returns:
        Форматований рядок
        
    Examples:
        >>> format_list_for_display(["apple", "banana", "cherry"], max_items=2)
        "apple, banana та ще 1 елемент"
        >>> format_list_for_display([])
        "(порожній список)"
    """

def format_numbered_list(items: List[Any], start_index: int = 1) -> str:
    """
    Форматування пронумерованого списку.
    
    Examples:
        >>> format_numbered_list(["Перша нотатка", "Друга нотатка"])
        "1. Перша нотатка\n2. Друга нотатка"
    """
```

### Форматування тексту:
```python
def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Обрізання тексту до максимальної довжини.
    
    Args:
        text: Текст для обрізання
        max_length: Максимальна довжина
        suffix: Суфікс для показу обрізання
        
    Returns:
        Обрізаний текст
        
    Examples:
        >>> truncate_text("Дуже довгий текст", 10)
        "Дуже дов..."
    """

def highlight_search_term(text: str, term: str, 
                         highlight_start: str = "**", 
                         highlight_end: str = "**") -> str:
    """
    Підсвічування пошукового терміну в тексті.
    
    Args:
        text: Текст для обробки
        term: Термін для підсвічування
        highlight_start/end: Маркери підсвічування
        
    Returns:
        Текст з підсвіченими термінами
        
    Examples:
        >>> highlight_search_term("Python programming", "python")
        "**Python** programming"
    """

def pluralize_ukrainian(count: int, singular: str, plural_2_4: str, plural_5_plus: str) -> str:
    """
    Українська плюралізація числівників.
    
    Args:
        count: Кількість
        singular: Форма для 1 (день, нотатка, контакт)
        plural_2_4: Форма для 2-4 (дні, нотатки, контакти)
        plural_5_plus: Форма для 5+ (днів, нотаток, контактів)
        
    Returns:
        Правильна форма слова
        
    Examples:
        >>> pluralize_ukrainian(1, "день", "дні", "днів")
        "день"
        >>> pluralize_ukrainian(3, "нотатка", "нотатки", "нотаток")
        "нотатки"
        >>> pluralize_ukrainian(10, "контакт", "контакти", "контактів")
        "контактів"
    """
```

## 🔍 ПАРСИНГ КОМАНД

### Розбір користувацького вводу:
```python
def parse_command_with_args(input_str: str) -> Tuple[str, List[str]]:
    """
    Парсинг команди з аргументами.
    
    Args:
        input_str: Введена користувачем команда
        
    Returns:
        Tuple (команда, список аргументів)
        
    Examples:
        >>> parse_command_with_args("додай контакт Іван Петров")
        ("додай контакт", ["Іван", "Петров"])
        >>> parse_command_with_args('пошук "Іван Петров" за телефоном')
        ("пошук", ["Іван Петров", "за", "телефоном"])
    """

def extract_quoted_strings(text: str) -> List[str]:
    """
    Витягування рядків у лапках з тексту.
    
    Examples:
        >>> extract_quoted_strings('додай "Іван Петров" тег "важливий контакт"')
        ["Іван Петров", "важливий контакт"]
    """

def parse_search_query(query: str) -> Dict[str, Any]:
    """
    Розширений парсинг пошукового запиту.
    
    Args:
        query: Пошуковий запит
        
    Returns:
        Словник з параметрами пошуку
        
    Examples:
        >>> parse_search_query("знайди python tag:робота -tag:застаріле")
        {
            "text": "знайди python",
            "include_tags": ["робота"],
            "exclude_tags": ["застаріле"],
            "case_sensitive": False
        }
    """
```

## 📊 УТИЛІТИ ДАНИХ

### Робота з колекціями:
```python
def safe_list_get(lst: List[Any], index: int, default: Any = None) -> Any:
    """
    Безпечне отримання елементу зі списку.
    
    Args:
        lst: Список
        index: Індекс (може бути негативним)
        default: Значення за замовчуванням
        
    Returns:
        Елемент або default значення
    """

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Розбиття списку на частини заданого розміру.
    
    Examples:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """

def deduplicate_preserve_order(items: List[Any]) -> List[Any]:
    """Видалення дублікатів зі збереженням порядку."""
```

### Статистичні утиліти:
```python
def calculate_percentage(part: int, total: int, decimal_places: int = 1) -> float:
    """
    Розрахунок відсотка з обробкою ділення на нуль.
    
    Examples:
        >>> calculate_percentage(30, 100)
        30.0
        >>> calculate_percentage(1, 3, 2)
        33.33
    """

def format_file_size(size_bytes: int) -> str:
    """
    Форматування розміру файлу у зручному вигляді.
    
    Examples:
        >>> format_file_size(1024)
        "1.0 KB"
        >>> format_file_size(1536)
        "1.5 KB"
    """
```

## 🎯 КОНФІГУРАЦІЯ ТА КОНСТАНТИ

### Константи валідації:
```python
# Українські варіанти yes/no
YES_VARIANTS = {"y", "yes", "так", "т", "1", "true", "да"}
NO_VARIANTS = {"n", "no", "ні", "н", "0", "false", "нет"}

# Максимальні довжини полів
MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 10000
MAX_TAG_LENGTH = 30
MAX_NAME_LENGTH = 100

# Формати дат
DATE_FORMATS = [
    "%d.%m.%Y",
    "%d-%m-%Y", 
    "%d/%m/%Y",
    "%d %m %Y"
]

# Регулярні вирази
PHONE_CLEANUP_PATTERN = r'[^\d+]'
EMAIL_DOMAIN_PATTERN = r'@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
TAG_VALIDATION_PATTERN = r'^[a-zA-Zа-яА-ЯіІїЇєЄ0-9_\-]+$'
```

## ✅ КРИТЕРІЇ ПРИЙНЯТТЯ

### Функціональні вимоги:
- [ ] Всі валідатори працюють з різними видами вводу
- [ ] Форматування створює красивий вивід
- [ ] Парсинг команд обробляє лапки та спеціальні символи
- [ ] Українська мова правильно підтримується
- [ ] Error messages зрозумілі та інформативні

### Технічні вимоги:
- [ ] Type hints для всіх функцій
- [ ] Docstrings з прикладами використання
- [ ] Comprehensive error handling
- [ ] Unit тести для кожної функції
- [ ] Consistent naming conventions

### Якісні вимоги:
- [ ] Функції easy to use та intuitive
- [ ] Performance оптимізації де потрібно
- [ ] Реusable components
- [ ] Clean code principles

## 🧪 ТЕСТОВІ СЦЕНАРІЇ

### Валідація вводу:
```python
# Позитивні тести
assert validate_input_not_empty("  Іван  ", "ім'я") == "Іван"
assert validate_positive_integer("5", "число") == 5
assert validate_yes_no("так") == True
assert validate_yes_no("n") == False

# Негативні тести
with pytest.raises(ValueError):
    validate_input_not_empty("", "поле")
    validate_positive_integer("-1", "число")
    validate_yes_no("може")
```

### Форматування:
```python
# Списки
items = ["apple", "banana", "cherry"]
result = format_list_for_display(items, max_items=2)
assert "apple, banana та ще 1 елемент" in result

# Обрізання тексту
assert truncate_text("Довгий текст", 5) == "Довг..."

# Підсвічування
result = highlight_search_term("Python code", "python")
assert "**Python**" in result.lower()

# Плюралізація
assert pluralize_ukrainian(1, "день", "дні", "днів") == "день"
assert pluralize_ukrainian(2, "день", "дні", "днів") == "дні"
assert pluralize_ukrainian(5, "день", "дні", "днів") == "днів"
```

### Парсинг команд:
```python
# Основний парсинг
cmd, args = parse_command_with_args("додай контакт Іван")
assert cmd == "додай контакт"
assert args == ["Іван"]

# З лапками
cmd, args = parse_command_with_args('додай "Іван Петров"')
assert "Іван Петров" in args

# Витягування лапок
quotes = extract_quoted_strings('text "quoted1" more "quoted2"')
assert quotes == ["quoted1", "quoted2"]
```

### Edge cases:
```python
# Порожні значення
assert format_list_for_display([]) == "(порожній список)"
assert truncate_text("", 10) == ""
assert safe_list_get([], 0, "default") == "default"

# Великі числа
assert format_file_size(1024**3) == "1.0 GB"

# Спеціальні символи в тегах
with pytest.raises(ValueError):
    validate_tags_input("тег@спецсимвол")
```

## 🔗 ЗАЛЕЖНОСТІ

**Імпорти**:
```python
from typing import List, Dict, Any, Tuple, Callable, Optional
import re
import shlex
from datetime import datetime
```

**Використовується в**:
- CLI Interface (завдання #9) - основний споживач
- Всі інші модулі для валідації

## 📁 СТРУКТУРА КОДУ

```python
# personal_assistant/utils/validators.py

from typing import List, Dict, Any, Tuple, Callable, Optional
import re
import shlex
from datetime import datetime

# Константи
YES_VARIANTS = {...}
NO_VARIANTS = {...}
MAX_LENGTHS = {...}
PATTERNS = {...}

# Валідація
def validate_input_not_empty(value: str, field_name: str) -> str: ...
def validate_positive_integer(value: str, field_name: str, ...) -> int: ...
def validate_choice_from_list(...) -> str: ...
def validate_yes_no(value: str) -> bool: ...
def validate_tags_input(tags_str: str) -> List[str]: ...
def validate_date_input(date_str: str) -> str: ...

# Форматування
def format_list_for_display(...) -> str: ...
def format_numbered_list(...) -> str: ...
def truncate_text(...) -> str: ...
def highlight_search_term(...) -> str: ...
def pluralize_ukrainian(...) -> str: ...

# Парсинг
def parse_command_with_args(input_str: str) -> Tuple[str, List[str]]: ...
def extract_quoted_strings(text: str) -> List[str]: ...
def parse_search_query(query: str) -> Dict[str, Any]: ...

# Утиліти
def safe_list_get(...) -> Any: ...
def chunk_list(...) -> List[List[Any]]: ...
def calculate_percentage(...) -> float: ...
def format_file_size(size_bytes: int) -> str: ...

# Приватні допоміжні функції
def _normalize_tag(tag: str) -> str: ...
def _split_preserve_quotes(text: str) -> List[str]: ...
```

## 📚 РЕСУРСИ

- [Python string methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [Regular expressions guide](https://docs.python.org/3/library/re.html)
- [shlex for command parsing](https://docs.python.org/3/library/shlex.html)
- [Ukrainian pluralization rules](https://uk.wikipedia.org/wiki/Числівник)

## 🚀 ГОТОВНІСТЬ ДО ЗДАЧІ

### Checklist:
- [ ] Всі функції реалізовані з proper typing
- [ ] Docstrings з прикладами для кожної функції
- [ ] Comprehensive test coverage (90%+)
- [ ] Ukrainian language support працює
- [ ] Error messages зрозумілі
- [ ] Performance acceptable для UI usage
- [ ] Code review пройдено

**Використовується в**: CLI Interface (завдання #9), усі інші модулі