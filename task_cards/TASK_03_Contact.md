# 👤 TASK CARD #3: МОДЕЛЬ КОНТАКТУ

**Розробник**: Backend Developer  
**Файл**: `personal_assistant/models/contact.py`  
**Пріоритет**: 🟡 СЕРЕДНІЙ (залежить від завдання #1)  
**Час**: 3-4 дні  
**Складність**: ⭐⭐⭐⭐

---

## 📋 ЗАВДАННЯ

Створити повнофункціональну модель контакту з управлінням всіма персональними даними та lifecycle операціями.

## 🎯 МЕТА

Забезпечити:
- Зберігання всіх типів контактної інформації
- Валідацію через Field класи
- Гнучке управління множинними телефонами/emails
- Розрахунки з датами народження
- Серіалізацію для збереження

## 📦 СТРУКТУРА КЛАСУ

```python
class Contact:
    """Модель контакту з повним lifecycle управлінням."""
    
    def __init__(self, name: str) -> None:
        """Створення контакту з обов'язковим ім'ям."""
        self.name = Name(name)                    # Обов'язкове
        self.phones: List[Phone] = []             # Список телефонів
        self.emails: List[Email] = []             # Список emails  
        self.birthday: Optional[Birthday] = None  # День народження
        self.address: Optional[Address] = None    # Адреса
```

## 🔧 ОБОВ'ЯЗКОВІ МЕТОДИ

### Управління телефонами:
```python
def add_phone(self, phone: str) -> None:
    """Додавання телефону з валідацією та перевіркою дублікатів."""
    
def remove_phone(self, phone: str) -> bool:
    """Видалення телефону. Повертає True якщо знайдено та видалено."""
    
def edit_phone(self, old_phone: str, new_phone: str) -> None:
    """Заміна існуючого телефону. ValueError якщо старий не знайдено."""
    
def find_phone(self, phone: str) -> Optional[Phone]:
    """Пошук телефону в списку. Повертає Phone об'єкт або None."""
```

### Управління email:
```python
def add_email(self, email: str) -> None:
    """Додавання email з валідацією та перевіркою дублікатів."""
    
def remove_email(self, email: str) -> bool:
    """Видалення email. Повертає True якщо знайдено та видалено."""
```

### Особиста інформація:
```python
def set_birthday(self, birthday: str) -> None:
    """Встановлення дня народження з валідацією."""
    
def remove_birthday(self) -> None:
    """Видалення дня народження."""
    
def set_address(self, address: str) -> None:
    """Встановлення адреси з валідацією."""
    
def remove_address(self) -> None:
    """Видалення адреси."""
```

### Розрахункові методи:
```python
def days_to_birthday(self) -> Optional[int]:
    """
    Розрахунок днів до наступного дня народження.
    Повертає None якщо ДН не встановлено.
    Враховує високосні роки та перехід через новий рік.
    """
```

## 📊 СЕРІАЛІЗАЦІЯ

### Методи збереження/завантаження:
```python
def to_dict(self) -> Dict[str, Any]:
    """
    Серіалізація в словник для JSON збереження.
    Повертає:
    {
        "name": "Іван Петров",
        "phones": ["+380501234567", "+380671234567"],
        "emails": ["ivan@example.com"],
        "birthday": "15.03.1990",  # або None
        "address": "вул. Хрещатик, 1"  # або None
    }
    """

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'Contact':
    """
    Десеріалізація зі словника.
    Створює новий Contact об'єкт з усіма даними.
    """
```

## 🎨 СПЕЦІАЛЬНІ МЕТОДИ

### Представлення:
```python
def __str__(self) -> str:
    """
    Красивий вивід для користувача:
    
    📱 Іван Петров
    ☎️  +380501234567, +380671234567
    📧 ivan@example.com
    🎂 15.03.1990 (до ДН: 125 днів)
    🏠 вул. Хрещатик, 1
    """

def __repr__(self) -> str:
    """Технічне представлення для debug."""
```

### Порівняння та хешування:
```python
def __eq__(self, other) -> bool:
    """Порівняння за ім'ям (регістронезалежне)."""
    
def __hash__(self) -> int:
    """Хеш за ім'ям для використання в set/dict."""
```

## ✅ КРИТЕРІЇ ПРИЙНЯТТЯ

### Функціональні вимоги:
- [ ] Всі методи управління телефонами працюють
- [ ] Всі методи управління emails працюють  
- [ ] Валідація через Field класи
- [ ] Правильний розрахунок днів до ДН
- [ ] Серіалізація/десеріалізація без втрат
- [ ] Запобігання дублюванню телефонів/emails

### Технічні вимоги:
- [ ] Type hints для всіх методів
- [ ] Docstrings з прикладами
- [ ] Proper error handling з ValueError
- [ ] Immutable поведінка Name (не можна змінити після створення)
- [ ] Unit тести покривають всі методи

### Якісні вимоги:
- [ ] Красивий форматований __str__ вивід
- [ ] Ефективна робота з великою кількістю контактів
- [ ] Читабельний та maintainable код
- [ ] Consistent API design

## 🧪 ТЕСТОВІ СЦЕНАРІЇ

### Створення та основні операції:
```python
# Створення контакту
contact = Contact("Іван Петров")
assert contact.name.value == "Іван Петров"
assert len(contact.phones) == 0
assert contact.birthday is None

# Додавання телефонів
contact.add_phone("+380501234567")
contact.add_phone("0671234567")  # Нормалізується до +380671234567
assert len(contact.phones) == 2

# Пошук телефону
phone = contact.find_phone("+380501234567")
assert phone is not None
assert phone.value == "+380501234567"
```

### Управління emails та особистою інформацією:
```python
# Email операції
contact.add_email("ivan@example.com")
contact.add_email("IVAN@WORK.COM")  # Нормалізується до lowercase
assert len(contact.emails) == 2

# День народження
contact.set_birthday("15.03.1990")
days = contact.days_to_birthday()
assert isinstance(days, int)
assert 0 <= days <= 365

# Адреса  
contact.set_address("вул. Хрещатик, 1")
assert contact.address.value == "вул. Хрещатик, 1"
```

### Серіалізація:
```python
# Збереження в словник
data = contact.to_dict()
assert data["name"] == "Іван Петров"
assert "+380501234567" in data["phones"]
assert "ivan@example.com" in data["emails"]

# Відновлення зі словника
restored = Contact.from_dict(data)
assert restored.name.value == contact.name.value
assert len(restored.phones) == len(contact.phones)
assert restored.days_to_birthday() == contact.days_to_birthday()
```

### Edge cases та помилки:
```python
# Дублікати телефонів
contact.add_phone("+380501234567")  # Має ігноруватися
assert len(contact.phones) == 2  # Без змін

# Видалення неіснуючого
result = contact.remove_phone("+380999999999")
assert result == False

# Редагування неіснуючого телефону
with pytest.raises(ValueError):
    contact.edit_phone("+380999999999", "+380501111111")

# Невалідні дані
with pytest.raises(ValueError):
    contact.add_phone("invalid_phone")
    
with pytest.raises(ValueError):
    contact.set_birthday("32.13.2000")
```

### Розрахунок днів до ДН:
```python
from datetime import date, timedelta

# Тестування з різними датами
today = date.today()

# ДН завтра
tomorrow = today + timedelta(days=1)
contact.set_birthday(f"{tomorrow.day:02d}.{tomorrow.month:02d}.1990")
assert contact.days_to_birthday() == 1

# ДН вчора (наступного року)
yesterday = today - timedelta(days=1) 
contact.set_birthday(f"{yesterday.day:02d}.{yesterday.month:02d}.1990")
days = contact.days_to_birthday()
assert days > 360  # Майже рік

# Високосний рік (29 лютого)
contact.set_birthday("29.02.1992")
days = contact.days_to_birthday()
assert days is not None  # Має правильно обробляти
```

## 🔗 ЗАЛЕЖНОСТІ

**Потребує (з завдання #1)**:
- `Name` клас для імені
- `Phone` клас для телефонів
- `Email` клас для emails
- `Birthday` клас для дня народження  
- `Address` клас для адреси

**Імпорти**:
```python
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from .field import Name, Phone, Email, Birthday, Address
```

**Використовується в**:
- ContactManager (завдання #5)
- CLI Interface (завдання #9)

## 📁 СТРУКТУРА КОДУ

```python
# personal_assistant/models/contact.py

from typing import List, Optional, Dict, Any
from datetime import date, datetime
from .field import Name, Phone, Email, Birthday, Address

class Contact:
    """Модель контакту з повним lifecycle управлінням."""
    
    def __init__(self, name: str) -> None:
        """Створення контакту з обов'язковим ім'ям."""
        
    # Телефони
    def add_phone(self, phone: str) -> None: ...
    def remove_phone(self, phone: str) -> bool: ...
    def edit_phone(self, old_phone: str, new_phone: str) -> None: ...
    def find_phone(self, phone: str) -> Optional[Phone]: ...
    
    # Emails
    def add_email(self, email: str) -> None: ...
    def remove_email(self, email: str) -> bool: ...
    
    # Особиста інформація
    def set_birthday(self, birthday: str) -> None: ...
    def remove_birthday(self) -> None: ...
    def set_address(self, address: str) -> None: ...
    def remove_address(self) -> None: ...
    
    # Розрахунки
    def days_to_birthday(self) -> Optional[int]: ...
    
    # Серіалізація
    def to_dict(self) -> Dict[str, Any]: ...
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contact': ...
    
    # Спеціальні методи
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
```

## 📚 РЕСУРСИ

- [Python datetime documentation](https://docs.python.org/3/library/datetime.html)
- [Working with dates in Python](https://realpython.com/python-datetime/)
- [Type hints best practices](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [Class design principles](https://refactoring.guru/design-patterns/python)

## 🚀 ГОТОВНІСТЬ ДО ЗДАЧІ

### Checklist:
- [ ] Всі методи реалізовані та протестовані
- [ ] Валідація працює через Field класи
- [ ] Розрахунок ДН правильний для всіх випадків
- [ ] Серіалізація зберігає всі дані
- [ ] Code review пройдено
- [ ] Готовність до інтеграції з ContactManager

**Розблоковує**: ContactManager (завдання #5), CLI Interface (завдання #9)