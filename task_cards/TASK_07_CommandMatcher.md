# 🤖 TASK CARD #7: РОЗПІЗНАВАННЯ КОМАНД

**Розробник**: AI/ML Developer або Senior Backend  
**Файл**: `personal_assistant/utils/command_matcher.py`  
**Пріоритет**: 🟡 СЕРЕДНІЙ  
**Час**: 5-6 днів  
**Складність**: ⭐⭐⭐⭐⭐

---

## 📋 ЗАВДАННЯ

Створити інтелектуальний розпізнавач команд що розуміє природну мову та допомагає користувачу вводити команди інтуїтивно.

## 🎯 МЕТА

Дозволити користувачу вводити команди у вільній формі:
- "додай контакт" → `add_contact`
- "знайди нотатки з тегом робота" → `notes_by_tags`
- "покажи дні народження" → `birthdays`
- "хелп" → `help`

## 🧠 АЛГОРИТМИ РОЗПІЗНАВАННЯ

### 1. Точний збіг (100% confidence)
Словник прямих відповідностей:
```python
EXACT_MATCHES = {
    # Українські
    "додай контакт": "add_contact",
    "новий контакт": "add_contact", 
    "створи контакт": "add_contact",
    
    # Англійські
    "add contact": "add_contact",
    "new contact": "add_contact",
    
    # Скорочення
    "add": "add_contact",
    "додай": "add_contact"
}
```

### 2. Pattern Matching (90% confidence)
Регулярні вирази для гнучкого розпізнавання:
```python
PATTERNS = {
    "add_contact": [
        r"(додай|створи|новий)\s+(контакт|людину)",
        r"(add|create|new)\s+contact",
        r"контакт.*додати"
    ],
    "search_contact": [
        r"(знайди|шукай|пошук)\s+контакт",
        r"(find|search)\s+contact",
        r"де\s+контакт"
    ]
}
```

### 3. Keyword Scoring (50-90% confidence)
Пошук ключових слів з підрахунком релевантності:
```python
KEYWORDS = {
    "add_contact": {
        "контакт": 50, "додай": 40, "створи": 40, 
        "новий": 30, "contact": 50, "add": 40
    },
    "birthdays": {
        "день": 40, "народження": 50, "birthday": 60,
        "дн": 30, "др": 30
    }
}
```

### 4. Fuzzy Search (30-80% confidence)
Для обробки друкарських помилок:
```python
from difflib import SequenceMatcher

def fuzzy_match(input_text: str, commands: List[str]) -> List[Tuple[str, float]]:
    """Нечіткий пошук схожих команд."""
    results = []
    for command in commands:
        ratio = SequenceMatcher(None, input_text.lower(), command).ratio()
        if ratio > 0.4:  # Мінімальна схожість
            results.append((command, ratio * 0.8))  # Знижуємо confidence
    return sorted(results, key=lambda x: x[1], reverse=True)
```

## 📦 КЛАС CommandMatcher

```python
class CommandMatcher:
    """Інтелектуальний розпізнавач команд."""
    
    def __init__(self) -> None:
        """Ініціалізація з завантаженням словників."""
        
    def find_best_command(self, user_input: str) -> Tuple[str, float]:
        """Знаходить найкращу команду для введеного тексту."""
        
    def suggest_commands(self, user_input: str, limit: int = 3) -> List[Tuple[str, float]]:
        """Повертає топ N найбільш відповідних команд."""
        
    def get_command_description(self, command: str) -> str:
        """Опис команди українською мовою."""
        
    def get_all_commands(self) -> List[str]:
        """Список всіх доступних команд."""
        
    def add_custom_alias(self, alias: str, command: str) -> None:
        """Додавання користувацьких скорочень."""
```

## 🎭 ПІДТРИМУВАНІ КОМАНДИ

### Контакти (6 команд):
- `add_contact` - додавання нового контакту
- `search_contact` - пошук контактів  
- `show_contacts` - показ всіх контактів
- `edit_contact` - редагування контакту
- `delete_contact` - видалення контакту
- `birthdays` - дні народження

### Нотатки (6 команд):
- `add_note` - створення нотатки
- `search_notes` - пошук у нотатках
- `show_notes` - показ всіх нотаток
- `edit_note` - редагування нотатки
- `delete_note` - видалення нотатки
- `notes_by_tags` - пошук за тегами

### Системні (3 команди):
- `help` - довідка
- `statistics` - статистика
- `exit` - вихід

## 🔧 ДЕТАЛЬНА РЕАЛІЗАЦІЯ

### Метод find_best_command():
```python
def find_best_command(self, user_input: str) -> Tuple[str, float]:
    """
    Алгоритм розпізнавання:
    1. Очистити та нормалізувати ввід
    2. Спробувати точний збіг
    3. Спробувати pattern matching
    4. Підрахувати keyword score
    5. Застосувати fuzzy search
    6. Повернути команду з найвищим confidence
    """
    
    # Нормалізація
    cleaned_input = self._normalize_input(user_input)
    
    # 1. Точний збіг (100%)
    if cleaned_input in self.exact_matches:
        return self.exact_matches[cleaned_input], 1.0
    
    # 2. Pattern matching (90%)
    pattern_match = self._try_patterns(cleaned_input)
    if pattern_match:
        return pattern_match, 0.9
    
    # 3. Keyword scoring (змінний)
    keyword_scores = self._calculate_keyword_scores(cleaned_input)
    if keyword_scores:
        best_keyword = max(keyword_scores, key=keyword_scores.get)
        confidence = min(keyword_scores[best_keyword] / 100.0, 0.85)
        return best_keyword, confidence
    
    # 4. Fuzzy search (низький confidence)
    fuzzy_results = self._fuzzy_search(cleaned_input)
    if fuzzy_results:
        return fuzzy_results[0]  # (command, confidence)
    
    # Нічого не знайдено
    return "help", 0.1
```

### Нормалізація вводу:
```python
def _normalize_input(self, text: str) -> str:
    """Підготовка тексту до аналізу."""
    # Приведення до нижнього регістру
    text = text.lower().strip()
    
    # Видалення зайвих пробілів
    text = re.sub(r'\s+', ' ', text)
    
    # Видалення пунктуації
    text = re.sub(r'[^\w\s\-]', '', text)
    
    return text
```

## 📊 СИСТЕМА КОНФІДЕНЦІЇ

### Рівні confidence:
- **0.9-1.0**: Впевнений збіг (виконати відразу)
- **0.7-0.9**: Вірогідний збіг (запитати підтвердження)
- **0.4-0.7**: Можливий збіг (показати варіанти)
- **0.0-0.4**: Невизначено (показати help)

### Логіка прийняття рішення:
```python
def should_execute_directly(self, confidence: float) -> bool:
    """Чи виконувати команду відразу без підтвердження."""
    return confidence >= 0.85

def should_suggest_alternatives(self, confidence: float) -> bool:
    """Чи показувати альтернативні варіанти."""
    return 0.4 <= confidence < 0.85
```

## 🌐 МУЛЬТИМОВНА ПІДТРИМКА

### Словники для двох мов:
```python
COMMAND_DESCRIPTIONS = {
    "add_contact": {
        "uk": "Додавання нового контакту до адресної книги",
        "en": "Add new contact to address book"
    },
    "search_contact": {
        "uk": "Пошук контактів за ім'ям або телефоном",
        "en": "Search contacts by name or phone"
    }
}

LANGUAGE_PATTERNS = {
    "uk": {
        "add_words": ["додай", "створи", "новий", "додати"],
        "search_words": ["знайди", "шукай", "пошук", "де"],
        "delete_words": ["видали", "стерти", "прибрати"]
    },
    "en": {
        "add_words": ["add", "create", "new", "make"],
        "search_words": ["find", "search", "look", "where"],
        "delete_words": ["delete", "remove", "erase"]
    }
}
```

## ✅ КРИТЕРІЇ ПРИЙНЯТТЯ

### Функціональні вимоги:
- [ ] Розпізнає всі 15 команд з високою точністю
- [ ] Підтримує українську та англійську мови
- [ ] Обробляє друкарські помилки
- [ ] Повертає альтернативні варіанти при невпевненості
- [ ] Працює з природною мовою ("знайди контакт Іван")

### Технічні вимоги:
- [ ] Швидка робота (< 50ms на команду)
- [ ] Type hints та docstrings
- [ ] Configurable thresholds
- [ ] Логування для аналізу використання
- [ ] Unit тести з різними сценаріями

### Якісні вимоги:
- [ ] Точність розпізнавання > 90% для типових команд
- [ ] Graceful degradation при незрозумілому вводі
- [ ] Зрозумілі пропозиції альтернатив
- [ ] Навчання на помилках користувача

## 🧪 ТЕСТОВІ СЦЕНАРІЇ

### Точне розпізнавання:
```python
matcher = CommandMatcher()

# Українські команди
assert matcher.find_best_command("додай контакт")[0] == "add_contact"
assert matcher.find_best_command("знайди нотатки")[0] == "search_notes"
assert matcher.find_best_command("дні народження")[0] == "birthdays"

# Англійські команди
assert matcher.find_best_command("add contact")[0] == "add_contact"
assert matcher.find_best_command("show notes")[0] == "show_notes"
```

### Обробка помилок:
```python
# Друкарські помилки
assert matcher.find_best_command("додай контат")[0] == "add_contact"  # "контат"
assert matcher.find_best_command("seach contact")[0] == "search_contact"  # "seach"

# Часткові збіги
command, confidence = matcher.find_best_command("контакт")
assert command in ["add_contact", "search_contact", "show_contacts"]
assert confidence > 0.5
```

### Природна мова:
```python
# Складні фрази
assert matcher.find_best_command("я хочу додати новий контакт")[0] == "add_contact"
assert matcher.find_best_command("покажи мені всі нотатки з тегом робота")[0] == "notes_by_tags"
assert matcher.find_best_command("коли у кого день народження")[0] == "birthdays"
```

### Performance тести:
```python
import time

# Тест швидкодії
start = time.time()
for _ in range(1000):
    matcher.find_best_command("додай контакт")
elapsed = time.time() - start
assert elapsed < 1.0  # < 1ms per command
```

## 🔗 ЗАЛЕЖНОСТІ

**Імпорти**:
- `re` для регулярних виразів
- `difflib` для fuzzy matching
- `typing` для type hints
- `logging` для аналітики

**Використовується в**:
- CLI interface (завдання #9) - основний споживач

## 📚 АЛГОРИТМІЧНІ РЕСУРСИ

- [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance)
- [Fuzzy String Matching](https://github.com/seatgeek/thefuzz)
- [Natural Language Processing](https://www.nltk.org/)
- [Regular Expressions in Python](https://docs.python.org/3/library/re.html)

## 🚀 ГОТОВНІСТЬ ДО ЗДАЧІ

### Checklist:
- [ ] Всі алгоритми розпізнавання реалізовані
- [ ] Мультимовна підтримка працює
- [ ] Performance вимоги виконані
- [ ] Comprehensive test coverage
- [ ] Документація з прикладами
- [ ] Integration з CLI перевірена

**Використовується в**: CLI Interface (завдання #9)