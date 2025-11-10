# 📞 TASK CARD #5: МЕНЕДЖЕР КОНТАКТІВ

**Розробник**: Backend Developer  
**Файл**: `personal_assistant/managers/contact_manager.py`  
**Пріоритет**: 🟡 СЕРЕДНІЙ (залежить від #2, #3)  
**Час**: 4-5 днів  
**Складність**: ⭐⭐⭐⭐

---

## 📋 ЗАВДАННЯ

Створити повнофункціональний менеджер для управління колекцією контактів з потужними можливостями пошуку, сортування та аналітики.

## 🎯 МЕТА

Забезпечити:
- Повний CRUD для контактів
- Швидкий пошук за всіма полями
- Гнучке сортування
- Розрахунки днів народження
- Детальну статистику
- Автоматичне збереження

## 📦 АРХІТЕКТУРА КЛАСУ

```python
class ContactManager:
    """Менеджер для управління колекцією контактів."""
    
    def __init__(self, storage: FileStorage) -> None:
        """Ініціалізація з автоматичним завантаженням даних."""
        self.storage = storage
        self.contacts: Dict[str, Contact] = {}  # ключ = name.lower()
        self.filename = "contacts.json"
        self.load_contacts()
```

## 🔧 CRUD ОПЕРАЦІЇ

### Створення та додавання:
```python
def add_contact(self, contact: Contact) -> None:
    """
    Додавання нового контакту до колекції.
    - Перевіряє чи не існує контакт з таким ім'ям
    - Зберігає з ключем name.lower() для швидкого пошуку
    - Автоматично зберігає в файл
    """

def create_contact(self, name: str, **kwargs) -> Contact:
    """
    Створення та додавання контакту за одну операцію.
    kwargs може містити: phone, email, birthday, address
    Повертає створений Contact об'єкт.
    """
```

### Читання та пошук:
```python
def find_contact(self, name: str) -> Optional[Contact]:
    """
    Пошук контакту за точним ім'ям (регістронезалежний).
    Повертає Contact або None.
    """

def get_contact(self, name: str) -> Contact:
    """
    Отримання контакту за ім'ям з викиданням винятку якщо не знайдено.
    Використовувати коли впевнені що контакт існує.
    """

def get_all_contacts(self, sort_by: str = "name") -> List[Contact]:
    """
    Отримання всіх контактів з сортуванням.
    sort_by: "name", "created", "birthday", "phone_count"
    """
```

### Оновлення:
```python
def update_contact(self, name: str, **kwargs) -> Optional[Contact]:
    """
    Оновлення існуючого контакту.
    kwargs: нові значення для phone, email, birthday, address
    Повертає оновлений Contact або None якщо не знайдено.
    Автоматично зберігає зміни.
    """
```

### Видалення:
```python
def remove_contact(self, name: str) -> bool:
    """
    Видалення контакту за ім'ям.
    Повертає True якщо контакт знайдено та видалено.
    Автоматично зберігає зміни.
    """

def clear_all_contacts(self) -> int:
    """
    Видалення всіх контактів.
    Повертає кількість видалених контактів.
    """
```

## 🔍 ПОШУК ТА ФІЛЬТРАЦІЯ

### Універсальний пошук:
```python
def search_contacts(self, query: str) -> List[Contact]:
    """
    Пошук контактів за частковим збігом в усіх полях:
    - Ім'я (регістронезалежний)
    - Телефони (часткові збіги)  
    - Emails (регістронезалежний)
    - Адреса (часткові збіги)
    
    Повертає список знайдених контактів, відсортований за релевантністю.
    """

def search_by_phone(self, phone_query: str) -> List[Contact]:
    """Пошук контактів за номером телефону (часткові збіги)."""

def search_by_email(self, email_query: str) -> List[Contact]:
    """Пошук контактів за email адресою."""
```

### Спеціалізовані фільтри:
```python
def get_contacts_with_birthday(self) -> List[Contact]:
    """Отримання контактів у яких встановлено день народження."""

def get_contacts_without_phone(self) -> List[Contact]:
    """Контакти без телефонів (для data cleanup)."""

def get_contacts_by_domain(self, domain: str) -> List[Contact]:
    """Контакти з email адресами певного домену (напр. "gmail.com")."""
```

## 🎂 РОБОТА З ДНЯМИ НАРОДЖЕННЯ

### Розрахунки:
```python
def get_upcoming_birthdays(self, days_ahead: int = 7) -> List[Contact]:
    """
    Контакти з днями народження в наступні N днів.
    Повертає список відсортований за датою ДН.
    Враховує перехід через новий рік.
    """

def get_birthdays_in_range(self, start_date: date, end_date: date) -> List[Contact]:
    """Дні народження в заданому періоді."""

def get_birthday_calendar(self, month: int, year: int) -> Dict[int, List[Contact]]:
    """
    Календар днів народження для місяця.
    Повертає: {день_місяця: [список_контактів]}
    """
```

## 📊 СТАТИСТИКА ТА АНАЛІТИКА

### Основна статистика:
```python
def get_statistics(self) -> Dict[str, Any]:
    """
    Детальна статистика про контакти:
    {
        "total_contacts": 150,
        "contacts_with_phones": 145,
        "contacts_with_emails": 120,  
        "contacts_with_birthday": 80,
        "contacts_with_address": 45,
        "total_phones": 180,
        "total_emails": 135,
        "average_phones_per_contact": 1.2,
        "most_common_domain": "gmail.com",
        "upcoming_birthdays_week": 3,
        "data_completeness": 75.5,  # % полів заповнено
        "last_updated": "2024-01-15T10:30:00"
    }
    """

def get_domain_statistics(self) -> Dict[str, int]:
    """Статистика email доменів: {"gmail.com": 45, "ukr.net": 20}"""

def get_phone_operator_statistics(self) -> Dict[str, int]:
    """Статистика операторів: {"050": 30, "067": 25, "063": 20}"""
```

## 💾 ЗБЕРЕЖЕННЯ ТА ЗАВАНТАЖЕННЯ

### Persistence методи:
```python
def save_contacts(self) -> None:
    """
    Збереження всіх контактів у JSON файл.
    Використовує Contact.to_dict() для серіалізації.
    """

def load_contacts(self) -> None:
    """
    Завантаження контактів з JSON файлу.
    Створює Contact об'єкти через Contact.from_dict().
    При помилці створює порожню колекцію.
    """

def export_contacts(self, format: str = "json") -> str:
    """
    Експорт контактів в різних форматах.
    format: "json", "csv", "txt"
    Повертає шлях до створеного файлу.
    """

def import_contacts(self, filepath: str, format: str = "auto") -> int:
    """
    Імпорт контактів з файлу.
    Повертає кількість успішно імпортованих контактів.
    """
```

## ⚡ ОПТИМІЗАЦІЇ PERFORMANCE

### Індексація та кешування:
```python
def _rebuild_search_index(self) -> None:
    """Перебудова індексів для швидкого пошуку."""

def _get_search_terms(self, contact: Contact) -> Set[str]:
    """Генерація термів для повнотекстового пошуку."""
```

### Пакетні операції:
```python
def add_contacts_batch(self, contacts: List[Contact]) -> int:
    """
    Додавання множинних контактів за одну операцію.
    Оптимізовано для великих обсягів даних.
    Зберігає тільки в кінці.
    """

def update_contacts_batch(self, updates: Dict[str, Dict[str, Any]]) -> int:
    """Пакетне оновлення множинних контактів."""
```

## ✅ КРИТЕРІЇ ПРИЙНЯТТЯ

### Функціональні вимоги:
- [ ] Всі CRUD операції працюють правильно
- [ ] Пошук працює за всіма полями з частковими збігами
- [ ] Сортування працює за різними критеріями
- [ ] Розрахунки днів народження точні
- [ ] Статистика відображає реальний стан даних
- [ ] Автоматичне збереження після кожної зміни

### Технічні вимоги:
- [ ] O(1) пошук за ім'ям (через dict)
- [ ] Efficient пошук за іншими полями
- [ ] Type hints для всіх методів
- [ ] Proper error handling з інформативними повідомленнями
- [ ] Unit тести покривають всі сценарії

### Якісні вимоги:
- [ ] Швидка робота з великою кількістю контактів (1000+)
- [ ] Memory efficient операції
- [ ] Consistent API design
- [ ] Robust обробка edge cases

## 🧪 ТЕСТОВІ СЦЕНАРІЇ

### Основні CRUD операції:
```python
manager = ContactManager(storage)

# Додавання контакту
contact = Contact("Іван Петров")
contact.add_phone("+380501234567")
manager.add_contact(contact)

# Пошук
found = manager.find_contact("Іван Петров")
assert found is not None
assert found.name.value == "Іван Петров"

# Оновлення
updated = manager.update_contact("Іван Петров", email="ivan@example.com")
assert updated is not None
assert "ivan@example.com" in [e.value for e in updated.emails]

# Видалення
result = manager.remove_contact("Іван Петров")
assert result == True
assert manager.find_contact("Іван Петров") is None
```

### Пошук та фільтрація:
```python
# Додаємо тестові дані
contacts = [
    Contact("Іван Петров"),
    Contact("Марія Іванова"), 
    Contact("Петро Сидоров")
]
for contact in contacts:
    contact.add_phone(f"+38050{random.randint(1000000, 9999999)}")
    manager.add_contact(contact)

# Універсальний пошук
results = manager.search_contacts("Іван")
assert len(results) == 2  # Іван Петров, Марія Іванова

# Пошук за телефоном
results = manager.search_by_phone("050")
assert len(results) == 3  # Всі мають 050

# Пошук за email доменом  
manager.update_contact("Іван Петров", email="ivan@gmail.com")
results = manager.get_contacts_by_domain("gmail.com")
assert len(results) == 1
```

### Дні народження:
```python
from datetime import date, timedelta

# Додаємо дні народження
today = date.today()
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(days=5)

manager.update_contact("Іван Петров", 
    birthday=f"{tomorrow.day:02d}.{tomorrow.month:02d}.1990")
manager.update_contact("Марія Іванова",
    birthday=f"{next_week.day:02d}.{next_week.month:02d}.1985")

# Тест майбутніх днів народження
upcoming = manager.get_upcoming_birthdays(7)
assert len(upcoming) == 2
assert upcoming[0].name.value == "Іван Петров"  # Сортовано за датою
```

### Статистика:
```python
stats = manager.get_statistics()
assert stats["total_contacts"] == 3
assert stats["contacts_with_phones"] == 3
assert stats["contacts_with_birthday"] == 2
assert "gmail.com" in stats.get("most_common_domain", "")

domain_stats = manager.get_domain_statistics()
assert domain_stats.get("gmail.com", 0) >= 1
```

### Збереження та завантаження:
```python
# Збереження
original_count = len(manager.contacts)
manager.save_contacts()

# Створення нового менеджера і завантаження
new_manager = ContactManager(storage)
assert len(new_manager.contacts) == original_count

# Перевірка цілісності даних
for name, contact in manager.contacts.items():
    loaded_contact = new_manager.contacts[name]
    assert loaded_contact.name.value == contact.name.value
    assert len(loaded_contact.phones) == len(contact.phones)
```

### Performance тести:
```python
import time

# Тест з великою кількістю контактів
start_time = time.time()
for i in range(1000):
    contact = Contact(f"Test User {i}")
    contact.add_phone(f"+38050{i:07d}")
    manager.add_contact(contact)

# Пошук має бути швидким
search_start = time.time()
results = manager.search_contacts("Test")
search_time = time.time() - search_start
assert search_time < 1.0  # < 1 секунди для 1000 контактів
```

## 🔗 ЗАЛЕЖНОСТІ

**Потребує**:
- FileStorage (завдання #2)
- Contact model (завдання #3)

**Імпорти**:
```python
from typing import Dict, List, Optional, Any, Set
from datetime import date, datetime
import re
from ..storage.file_storage import FileStorage
from ..models.contact import Contact
```

**Використовується в**:
- CLI Interface (завдання #9)

## 📁 СТРУКТУРА КОДУ

```python
# personal_assistant/managers/contact_manager.py

from typing import Dict, List, Optional, Any, Set
from datetime import date, datetime
import re
from ..storage.file_storage import FileStorage
from ..models.contact import Contact

class ContactManager:
    """Менеджер для управління колекцією контактів."""
    
    def __init__(self, storage: FileStorage) -> None:
        """Ініціалізація з автоматичним завантаженням."""
        
    # CRUD операції
    def add_contact(self, contact: Contact) -> None: ...
    def create_contact(self, name: str, **kwargs) -> Contact: ...
    def find_contact(self, name: str) -> Optional[Contact]: ...
    def get_contact(self, name: str) -> Contact: ...
    def get_all_contacts(self, sort_by: str = "name") -> List[Contact]: ...
    def update_contact(self, name: str, **kwargs) -> Optional[Contact]: ...
    def remove_contact(self, name: str) -> bool: ...
    
    # Пошук та фільтрація
    def search_contacts(self, query: str) -> List[Contact]: ...
    def search_by_phone(self, phone_query: str) -> List[Contact]: ...
    def search_by_email(self, email_query: str) -> List[Contact]: ...
    def get_contacts_with_birthday(self) -> List[Contact]: ...
    def get_contacts_by_domain(self, domain: str) -> List[Contact]: ...
    
    # Дні народження
    def get_upcoming_birthdays(self, days_ahead: int = 7) -> List[Contact]: ...
    def get_birthday_calendar(self, month: int, year: int) -> Dict[int, List[Contact]]: ...
    
    # Статистика
    def get_statistics(self) -> Dict[str, Any]: ...
    def get_domain_statistics(self) -> Dict[str, int]: ...
    def get_phone_operator_statistics(self) -> Dict[str, int]: ...
    
    # Persistence
    def save_contacts(self) -> None: ...
    def load_contacts(self) -> None: ...
    def export_contacts(self, format: str = "json") -> str: ...
    
    # Утиліти
    def _auto_save(self) -> None: ...
    def _calculate_relevance_score(self, contact: Contact, query: str) -> float: ...
```

## 📚 РЕСУРСИ

- [Python collections documentation](https://docs.python.org/3/library/collections.html)
- [Efficient searching algorithms](https://realpython.com/binary-search-python/)
- [Working with dates in Python](https://docs.python.org/3/library/datetime.html)
- [Data analysis with Python](https://pandas.pydata.org/docs/)

## 🚀 ГОТОВНІСТЬ ДО ЗДАЧІ

### Checklist:
- [ ] Всі CRUD операції працюють та протестовані
- [ ] Пошук швидкий та точний
- [ ] Статистика відображає реальні дані
- [ ] Дні народження розраховуються правильно
- [ ] Performance прийнятний для великих даних
- [ ] Integration з FileStorage працює
- [ ] Code review пройдено

**Використовується в**: CLI Interface (завдання #9)