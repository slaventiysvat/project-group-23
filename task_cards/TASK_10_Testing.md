# 🧪 TASK CARD #10: ТЕСТУВАННЯ

**Розробник**: QA Engineer або Senior Developer  
**Файл**: `tests/test_main.py` та інші тестові файли  
**Пріоритет**: 🔴 ВИСОКИЙ  
**Час**: 4-5 днів  
**Складність**: ⭐⭐⭐⭐

---

## 📋 ЗАВДАННЯ

Створити повне покриття unit тестами всіх компонентів системи з фокусом на якість, надійність та покриття edge cases.

## 🎯 МЕТА

Забезпечити:
- Мінімум 90% code coverage
- Тестування всіх публічних методів
- Покриття позитивних та негативних сценаріїв
- Тестування edge cases та error handling
- Стабільні тести що можна запускати автоматично
- Performance тести для критичних операцій

## 📦 СТРУКТУРА ТЕСТІВ

### Організація файлів:
```
tests/
├── __init__.py
├── test_main.py                 # Головний тестовий файл (з прикладу)
├── test_fields.py               # Тести Field класів
├── test_contact.py              # Тести Contact моделі
├── test_note.py                 # Тести Note моделі  
├── test_file_storage.py         # Тести FileStorage
├── test_contact_manager.py      # Тести ContactManager
├── test_note_manager.py         # Тести NoteManager
├── test_command_matcher.py      # Тести CommandMatcher
├── test_validators.py           # Тести validators
├── test_cli_integration.py      # Інтеграційні тести CLI
├── fixtures/                    # Тестові дані
│   ├── sample_contacts.json
│   ├── sample_notes.json
│   └── test_data.py
└── utils/                       # Тестові утиліти
    ├── __init__.py
    ├── mock_helpers.py
    └── test_helpers.py
```

## 🧩 ТЕСТОВІ КЛАСИ

### TestField - тестування валідації (12+ тестів):
```python
class TestField:
    """Тестування базових класів Field та їх нащадків."""
    
    def test_field_basic_validation(self):
        """Базова валідація Field класу."""
        
    def test_name_validation_success(self):
        """Успішна валідація імен."""
        
    def test_name_validation_failure(self):
        """Помилки валідації імен."""
        
    def test_phone_normalization(self):
        """Нормалізація телефонних номерів."""
        
    def test_phone_validation_ukrainian_operators(self):
        """Валідація українських операторів."""
        
    def test_email_normalization(self):
        """Нормалізація email адрес."""
        
    def test_birthday_date_parsing(self):
        """Парсинг різних форматів дат."""
        
    def test_birthday_validation_edge_cases(self):
        """Edge cases для днів народження."""
        
    def test_address_validation(self):
        """Валідація адрес."""
        
    def test_field_string_representation(self):
        """Тестування __str__ та __repr__ методів."""
        
    def test_field_equality_and_hashing(self):
        """Тестування порівняння та хешування."""
```

### TestContact - тестування моделі контакту (15+ тестів):
```python
class TestContact:
    """Тестування Contact моделі."""
    
    def test_contact_creation(self):
        """Створення контакту з валідним ім'ям."""
        
    def test_add_phone_success(self):
        """Додавання телефонів."""
        
    def test_add_phone_duplicates(self):
        """Обробка дублікатів телефонів."""
        
    def test_remove_phone(self):
        """Видалення телефонів."""
        
    def test_edit_phone(self):
        """Редагування існуючих телефонів."""
        
    def test_find_phone(self):
        """Пошук телефонів."""
        
    def test_email_management(self):
        """Управління email адресами."""
        
    def test_birthday_operations(self):
        """Операції з днем народження."""
        
    def test_days_to_birthday_calculation(self):
        """Розрахунок днів до ДН в різних сценаріях."""
        
    def test_days_to_birthday_leap_year(self):
        """Обробка високосних років."""
        
    def test_address_operations(self):
        """Операції з адресою."""
        
    def test_contact_serialization(self):
        """Серіалізація в dict."""
        
    def test_contact_deserialization(self):
        """Десеріалізація з dict."""
        
    def test_contact_string_representation(self):
        """Красивий вивід контакту."""
        
    def test_contact_edge_cases(self):
        """Edge cases та error handling."""
```

### TestNote - тестування моделі нотатки (12+ тестів):
```python
class TestNote:
    """Тестування Note моделі."""
    
    def test_note_creation(self):
        """Створення нотатки з різними параметрами."""
        
    def test_tag_management(self):
        """Додавання, видалення, валідація тегів."""
        
    def test_tag_validation_rules(self):
        """Правила валідації тегів."""
        
    def test_content_operations(self):
        """Оновлення заголовку та змісту."""
        
    def test_search_in_content(self):
        """Пошук в змісті (case sensitive/insensitive)."""
        
    def test_tag_matching(self):
        """Перевірка співпадіння тегів."""
        
    def test_word_count_calculation(self):
        """Підрахунок слів та символів."""
        
    def test_timestamp_updates(self):
        """Автооновлення updated_at."""
        
    def test_note_serialization(self):
        """Серіалізація з датами."""
        
    def test_note_comparison_and_sorting(self):
        """Порівняння та сортування нотаток."""
        
    def test_note_string_representation(self):
        """Форматований вивід нотатки."""
        
    def test_note_edge_cases(self):
        """Edge cases для нотаток."""
```

### TestFileStorage - тестування збереження (8+ тестів):
```python
class TestFileStorage:
    """Тестування файлового сховища."""
    
    def setUp(self):
        """Створення тимчасової папки для тестів."""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.temp_dir)
    
    def tearDown(self):
        """Очищення тимчасових файлів."""
        shutil.rmtree(self.temp_dir)
        
    def test_save_and_load_data(self):
        """Базове збереження та завантаження."""
        
    def test_backup_creation(self):
        """Створення backup файлів."""
        
    def test_recovery_from_backup(self):
        """Відновлення з backup при пошкодженні."""
        
    def test_json_corruption_handling(self):
        """Обробка пошкоджених JSON файлів."""
        
    def test_utf8_encoding(self):
        """Підтримка української мови."""
        
    def test_large_file_handling(self):
        """Робота з великими файлами."""
        
    def test_storage_info(self):
        """Інформація про стан сховища."""
        
    def test_file_system_errors(self):
        """Обробка помилок файлової системи."""
```

### TestContactManager - тестування бізнес-логіки (15+ тестів):
```python
class TestContactManager:
    """Тестування ContactManager."""
    
    def setUp(self):
        """Підготовка тестового менеджера."""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.temp_dir)
        self.manager = ContactManager(self.storage)
        
    def test_add_contact(self):
        """Додавання нових контактів."""
        
    def test_find_contact_by_name(self):
        """Пошук контактів за ім'ям."""
        
    def test_search_contacts_universal(self):
        """Універсальний пошук по всіх полях."""
        
    def test_update_contact_operations(self):
        """Оновлення існуючих контактів."""
        
    def test_remove_contact(self):
        """Видалення контактів."""
        
    def test_upcoming_birthdays_calculation(self):
        """Розрахунок майбутніх днів народження."""
        
    def test_birthday_calendar(self):
        """Календар днів народження."""
        
    def test_statistics_calculation(self):
        """Розрахунок статистики."""
        
    def test_domain_statistics(self):
        """Статистика email доменів."""
        
    def test_sorting_operations(self):
        """Сортування контактів."""
        
    def test_batch_operations(self):
        """Пакетні операції з контактами."""
        
    def test_persistence_integration(self):
        """Інтеграція зі збереженням."""
        
    def test_search_performance(self):
        """Performance пошуку з великими даними."""
        
    def test_edge_cases_and_errors(self):
        """Edge cases та error handling."""
        
    def test_data_integrity(self):
        """Цілісність даних після операцій."""
```

### TestNoteManager - тестування нотаток (15+ тестів):
```python
class TestNoteManager:
    """Тестування NoteManager."""
    
    # Аналогічна структура як ContactManager
    # Фокус на тестуванні системи тегів, пошуку, індексації
    
    def test_create_and_add_notes(self):
        """Створення та додавання нотаток."""
        
    def test_note_indexing_1_based(self):
        """Правильна 1-based індексація для користувача."""
        
    def test_full_text_search(self):
        """Повнотекстовий пошук."""
        
    def test_tag_based_search_or_logic(self):
        """Пошук за тегами (OR логіка)."""
        
    def test_tag_based_search_and_logic(self):
        """Пошук за тегами (AND логіка)."""
        
    def test_tag_statistics_and_popularity(self):
        """Статистика та популярність тегів."""
        
    def test_tag_management_operations(self):
        """Операції з тегами (перейменування, злиття)."""
        
    def test_sorting_by_different_criteria(self):
        """Сортування за різними критеріями."""
        
    def test_note_filtering_by_date(self):
        """Фільтрація за датами."""
        
    def test_export_import_operations(self):
        """Експорт та імпорт нотаток."""
        
    # ... інші тести
```

### TestCommandMatcher - тестування AI (10+ тестів):
```python
class TestCommandMatcher:
    """Тестування розпізнавання команд."""
    
    def test_exact_command_matching(self):
        """Точне розпізнавання команд."""
        
    def test_ukrainian_commands(self):
        """Підтримка української мови."""
        
    def test_english_commands(self):
        """Підтримка англійської мови."""
        
    def test_fuzzy_matching_typos(self):
        """Обробка друкарських помилок."""
        
    def test_pattern_matching(self):
        """Розпізнавання через patterns."""
        
    def test_keyword_scoring(self):
        """Система підрахунку релевантності."""
        
    def test_confidence_levels(self):
        """Рівні впевненості в розпізнаванні."""
        
    def test_command_suggestions(self):
        """Пропозиції альтернативних команд."""
        
    def test_performance_benchmarks(self):
        """Performance тести швидкості."""
        
    def test_edge_cases_empty_input(self):
        """Edge cases та некоректний ввід."""
```

### TestValidators - тестування утиліт (8+ тестів):
```python
class TestValidators:
    """Тестування допоміжних функцій."""
    
    def test_input_validation_functions(self):
        """Валідація користувацького вводу."""
        
    def test_formatting_functions(self):
        """Функції форматування."""
        
    def test_ukrainian_pluralization(self):
        """Українська плюралізація."""
        
    def test_command_parsing(self):
        """Парсинг команд з лапками."""
        
    def test_text_processing_utilities(self):
        """Утиліти обробки тексту."""
        
    def test_list_and_data_utilities(self):
        """Утиліти роботи з даними."""
        
    def test_error_handling_in_validators(self):
        """Error handling у валідаторах."""
        
    def test_edge_cases_empty_and_special_values(self):
        """Edge cases з порожніми значеннями."""
```

## 🔧 ІНТЕГРАЦІЙНІ ТЕСТИ

### TestCLIIntegration - end-to-end тести:
```python
class TestCLIIntegration:
    """Інтеграційні тести всієї системи."""
    
    def test_complete_contact_workflow(self):
        """Повний workflow роботи з контактами."""
        
    def test_complete_note_workflow(self):
        """Повний workflow роботи з нотатками."""
        
    def test_data_persistence_across_sessions(self):
        """Збереження даних між сесіями."""
        
    def test_command_recognition_integration(self):
        """Інтеграція розпізнавання команд."""
        
    def test_error_recovery_scenarios(self):
        """Сценарії відновлення після помилок."""
        
    def test_performance_with_large_datasets(self):
        """Performance з великими обсягами даних."""
```

## 🛠️ ТЕСТОВІ УТИЛІТИ

### Mock та Helper функції:
```python
# tests/utils/mock_helpers.py

def create_mock_contact(name: str = "Test User", **kwargs) -> Contact:
    """Створення тестового контакту."""
    
def create_mock_note(title: str = "Test Note", **kwargs) -> Note:
    """Створення тестової нотатки."""
    
def generate_test_contacts(count: int) -> List[Contact]:
    """Генерація множинних тестових контактів."""
    
def mock_user_input(inputs: List[str]):
    """Mock для input() функції в CLI тестах."""
    
def assert_contact_equal(contact1: Contact, contact2: Contact):
    """Глибоке порівняння контактів."""
    
def cleanup_test_files(directory: str):
    """Очищення тестових файлів."""
```

### Fixtures та тестові дані:
```python
# tests/fixtures/test_data.py

SAMPLE_CONTACTS = [
    {
        "name": "Іван Петров",
        "phones": ["+380501234567"],
        "emails": ["ivan@example.com"],
        "birthday": "15.03.1990"
    },
    # ... більше тестових даних
]

SAMPLE_NOTES = [
    {
        "title": "Python Tutorial",
        "content": "Learning Python programming",
        "tags": ["python", "навчання"]
    },
    # ... більше тестових даних
]

def load_sample_contacts() -> List[Contact]:
    """Завантаження тестових контактів."""
    
def load_sample_notes() -> List[Note]:
    """Завантаження тестових нотаток."""
```

## ⚡ PERFORMANCE ТЕСТИ

### Benchmark тести:
```python
def test_search_performance():
    """Тест швидкодії пошуку."""
    # Створити 1000 контактів
    # Виміряти час пошуку
    # Assert < 100ms для звичайного пошуку
    
def test_large_dataset_operations():
    """Операції з великими датасетами."""
    # 5000 контактів, 10000 нотаток
    # Тестування основних операцій
    # Performance benchmarks
    
def test_memory_usage():
    """Тест споживання пам'яті."""
    # Моніторинг memory leaks
    # Efficient використання ресурсів
```

## ✅ КРИТЕРІЇ ПРИЙНЯТТЯ

### Покриття та якість:
- [ ] **90%+ code coverage** для всіх модулів
- [ ] **100% покриття** публічних методів
- [ ] **Позитивні та негативні** тестові сценарії
- [ ] **Edge cases** покриті тестами
- [ ] **Error handling** протестований

### Надійність:
- [ ] Всі тести **стабільно проходять** 
- [ ] **Ізоляція тестів** (кожен тест незалежний)
- [ ] **Cleanup after tests** (tempfile usage)
- [ ] **Repeatable results** (детерміністичні тести)
- [ ] **Fast execution** (< 30 секунд для всіх тестів)

### Документація:
- [ ] **Docstrings** для всіх тестових методів
- [ ] **Clear test names** що описують сценарій
- [ ] **Assertion messages** зрозумілі
- [ ] **Setup/teardown** properly documented

## 🧪 ЗАПУСК ТЕСТІВ

### Команди виконання:
```bash
# Запуск всіх тестів
python -m pytest tests/

# З coverage звітом
python -m pytest tests/ --cov=personal_assistant --cov-report=html

# Конкретний тестовий файл
python -m pytest tests/test_contact.py -v

# Performance тести
python -m pytest tests/ -m "performance"

# Швидкі тести (без performance)
python -m pytest tests/ -m "not performance"
```

### CI/CD інтеграція:
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=personal_assistant --cov-fail-under=90
```

## 📊 COVERAGE ЦІЛІ

### По модулях:
- **Field classes**: 95%+ (критична валідація)
- **Contact/Note models**: 90%+ (бізнес-логіка)
- **Managers**: 85%+ (складна логіка з багатьма методами)
- **FileStorage**: 95%+ (критичне для збереження даних)
- **CommandMatcher**: 80%+ (AI компонент, складно тестувати всі випадки)
- **Validators**: 90%+ (утиліти, багато edge cases)
- **CLI**: 70%+ (UI компонент, частково manual testing)

## 🚀 ГОТОВНІСТЬ ДО ЗДАЧІ

### Checklist:
- [ ] Всі тестові класи створені та реалізовані
- [ ] Coverage reports показують 90%+ покриття
- [ ] Performance тести встановлюють benchmarks
- [ ] Інтеграційні тести покривають main workflows
- [ ] CI/CD pipeline налаштований та працює
- [ ] Документація тестів повна
- [ ] Mock та fixture utilities створені

**Завершальний етап** - забезпечує якість та надійність всієї системи!