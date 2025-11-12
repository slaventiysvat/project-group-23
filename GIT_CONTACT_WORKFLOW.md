# 🧑‍🤝‍🧑 Git Workflow для командної розробки Contact класу

## 🎯 Стратегія: Contact Class - 3 Developers

### 👥 Розподіл завдань Contact класу:
- **Developer 1** (Sarah): `Contact.__init__`, основні атрибути, `__str__`/`__repr__`
- **Developer 2** (Alex): Phone/Email методи (`add_phone`, `remove_phone`, `add_email`, `remove_email`)
- **Developer 3** (Emma): Birthday інтеграція + серіалізація (`to_dict`, `from_dict`, `days_to_birthday`)

---

## 📋 Аналіз Contact класу для розподілу

### 🏗️ **Developer 1 - Contact Foundation (Sarah)**
**Відповідальність:**
- `Contact.__init__(name, phone=None, email=None, birthday=None, address=None)`
- Основні атрибути: `self.name`, `self.phones`, `self.emails`
- `__str__()` та `__repr__()` методи
- Базова валідація ініціалізації

**Код що треба реалізувати:**
```python
class Contact:
    def __init__(self, name: str, phone: str = None, email: str = None, 
                 birthday: str = None, address: str = None):
        # Sarah implements this
        pass
    
    def __str__(self) -> str:
        # Sarah implements this
        pass
        
    def __repr__(self) -> str:
        # Sarah implements this  
        pass
```

---

### 📞 **Developer 2 - Phone & Email Management (Alex)**
**Відповідальність:**
- `add_phone(phone)`, `remove_phone(phone)`, `edit_phone(old_phone, new_phone)`
- `add_email(email)`, `remove_email(email)`, `edit_email(old_email, new_email)`
- `find_phone(phone)`, `get_phones()`, `get_emails()`
- Валідація дублікатів телефонів/email

**Код що треба реалізувати:**
```python
def add_phone(self, phone: str) -> None:
    # Alex implements this
    pass

def remove_phone(self, phone: str) -> bool:
    # Alex implements this
    pass
    
def edit_phone(self, old_phone: str, new_phone: str) -> bool:
    # Alex implements this
    pass

def add_email(self, email: str) -> None:
    # Alex implements this
    pass

def remove_email(self, email: str) -> bool:
    # Alex implements this
    pass
```

---

### 🎂 **Developer 3 - Birthday & Serialization (Emma)**
**Відповідальність:**
- `add_birthday(birthday)`, `days_to_birthday()`
- `to_dict()` - серіалізація в словник для JSON
- `from_dict(data)` - десеріалізація з словника  
- `__eq__()` - порівняння контактів
- Інтеграція з Birthday field класом

**Код що треба реалізувати:**
```python
def add_birthday(self, birthday: str) -> None:
    # Emma implements this
    pass

def days_to_birthday(self) -> int:
    # Emma implements this
    pass
    
def to_dict(self) -> dict:
    # Emma implements this
    pass
    
@classmethod 
def from_dict(cls, data: dict) -> 'Contact':
    # Emma implements this
    pass
```

---

## 🚀 Покрокові команди для кожного розробника

### 👩‍💻 **Developer 1 (Sarah) - Contact Foundation:**

```bash
# 1. Синхронізація та створення гілки
cd dev_implementation
git checkout main
git pull origin main
git checkout -b feature/contact-foundation
git push -u origin feature/contact-foundation

# 2. Створення початкової структури
cat > models/contact.py << 'EOF'
#!/usr/bin/env python3
"""
Contact Model for Personal Assistant
Developer: Sarah (Foundation & Structure)
"""

from typing import List, Optional, Dict, Any
from .field import Name, Phone, Email, Birthday, Address


class Contact:
    """Клас для представлення контакту в адресній книзі."""
    
    def __init__(self, name: str, phone: str = None, email: str = None, 
                 birthday: str = None, address: str = None):
        """
        Ініціалізація контакту.
        
        Args:
            name: Ім'я контакту (обов'язкове)
            phone: Телефон (опціонально)
            email: Email (опціонально)  
            birthday: День народження (опціонально)
            address: Адреса (опціонально)
        """
        # Sarah implements initialization logic
        # TODO: Initialize name field
        # TODO: Initialize phones list
        # TODO: Initialize emails list
        # TODO: Initialize birthday field
        # TODO: Initialize address field
        pass
    
    def __str__(self) -> str:
        """Рядкове представлення контакту."""
        # Sarah implements string representation
        # TODO: Format contact info nicely
        pass
        
    def __repr__(self) -> str:
        """Програмне представлення контакту.""" 
        # Sarah implements repr
        pass


# TODO: Developer 2 (Alex) - add phone/email methods here

# TODO: Developer 3 (Emma) - add birthday/serialization methods here
EOF

# 3. Тестування Foundation
cd ..
python reference_tests/step_by_step/step_02_contact.py --step 1

# 4. Реалізація та коміт
cd dev_implementation
# Sarah implements __init__, __str__, __repr__
git add models/contact.py
git commit -m "🏗️ Contact Foundation - init, str, repr

- Додано Contact.__init__ з валідацією
- Реалізовано __str__ для зручного відображення
- Додано __repr__ для debug
- Ініціалізація полів: name, phones[], emails[]
- Step 1 тести проходять"

git push origin feature/contact-foundation
# Create PR: feature/contact-foundation → main
```

---

### 👨‍💻 **Developer 2 (Alex) - Phone & Email Management:**

```bash
# 1. Синхронізація (чекати Sarah's merge або rebase)
git checkout main
git pull origin main
git checkout -b feature/contact-phone-email
git push -u origin feature/contact-phone-email

# 2. Додавання phone/email методів до contact.py
# Alex adds methods after Sarah's foundation

# 3. Реалізація методів
"""
def add_phone(self, phone: str) -> None:
    # Validate and add phone
    
def remove_phone(self, phone: str) -> bool:  
    # Remove phone if exists
    
def edit_phone(self, old_phone: str, new_phone: str) -> bool:
    # Edit existing phone
    
def find_phone(self, phone: str) -> Phone:
    # Find phone in list
    
def add_email(self, email: str) -> None:
    # Add email with validation
    
def remove_email(self, email: str) -> bool:
    # Remove email if exists
"""

# 4. Тестування Phone/Email
cd ..
python reference_tests/step_by_step/step_02_contact.py --step 2
python reference_tests/step_by_step/step_02_contact.py --step 3

# 5. Коміт та PR
cd dev_implementation
git add models/contact.py
git commit -m "📞 Contact Phone/Email Management

- Додано add_phone/remove_phone/edit_phone методи
- Реалізовано add_email/remove_email методи  
- Валідація дублікатів телефонів та email
- Методи find_phone для пошуку
- Step 2-3 тести проходять"

git push origin feature/contact-phone-email
# Create PR після Sarah's merge
```

---

### 👩‍💻 **Developer 3 (Emma) - Birthday & Serialization:**

```bash
# 1. Синхронізація з попередніми змінами
git checkout main  
git pull origin main
git checkout -b feature/contact-birthday-serialization
git push -u origin feature/contact-birthday-serialization

# 2. Додавання birthday та serialization методів
"""
def add_birthday(self, birthday: str) -> None:
    # Add birthday with Birthday field
    
def days_to_birthday(self) -> int:
    # Calculate days until next birthday
    
def to_dict(self) -> Dict[str, Any]:
    # Serialize contact to dictionary
    
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'Contact':
    # Deserialize contact from dictionary
    
def __eq__(self, other) -> bool:
    # Compare contacts for equality
"""

# 3. Тестування Birthday/Serialization  
cd ..
python reference_tests/step_by_step/step_02_contact.py --step 4
python reference_tests/step_by_step/step_02_contact.py --step 5

# 4. Фінальне тестування
python reference_tests/step_by_step/step_02_contact.py --verbose
python reference_tests/step_by_step/step_02_contact.py --compare

# 5. Final commit
cd dev_implementation
git add models/contact.py
git commit -m "🎂 Contact Birthday & Serialization Complete

- Додано add_birthday та days_to_birthday методи
- Реалізовано to_dict/from_dict для JSON серіалізації
- Додано __eq__ для порівняння контактів  
- Інтеграція з Birthday field класом
- Всі step_02 тести проходять (5/5)
- Contact клас готовий до інтеграції"

git push origin feature/contact-birthday-serialization
```

---

## 🔄 **Merge Strategy та Rebase:**

### **Послідовність merge:**
1. **Sarah (Foundation)** → merge до `main` першою
2. **Alex (Phone/Email)** → rebase на новий main, потім merge  
3. **Emma (Birthday)** → rebase на фінальний main, потім merge

### **Rebase команди для Alex:**
```bash
# Коли Sarah merge завершений
git checkout main
git pull origin main
git checkout feature/contact-phone-email
git rebase main

# Якщо конфлікти в contact.py:
# Розв'язати конфлікти, зберегти файл
git add models/contact.py  
git rebase --continue
git push --force-with-lease origin feature/contact-phone-email
```

### **Rebase для Emma (після Alex merge):**
```bash
git checkout main
git pull origin main  
git checkout feature/contact-birthday-serialization
git rebase main
# Розв'язати конфлікти якщо є
git push --force-with-lease origin feature/contact-birthday-serialization
```

---

## 🧪 **Testing Strategy:**

### **Паралельне тестування:**
```bash
# Кожен розробник тестує свої частини:
# Sarah:
python reference_tests/step_by_step/step_02_contact.py --step 1

# Alex:  
python reference_tests/step_by_step/step_02_contact.py --step 2
python reference_tests/step_by_step/step_02_contact.py --step 3

# Emma:
python reference_tests/step_by_step/step_02_contact.py --step 4  
python reference_tests/step_by_step/step_02_contact.py --step 5

# Фінальне тестування (Emma):
python reference_tests/step_by_step/step_02_contact.py --verbose --compare
```

---

## 📊 **Code Review Checklist для Contact:**

### **Sarah (Foundation) Review:**
- ✅ `__init__` правильно ініціалізує всі поля
- ✅ `__str__` читабельно форматує контакт
- ✅ `__repr__` корисний для debugging  
- ✅ Валідація name field працює
- ✅ Списки phones/emails ініціалізуються

### **Alex (Phone/Email) Review:**
- ✅ `add_phone` валідує та додає Phone об'єкти
- ✅ `remove_phone` знаходить та видаляє правильний телефон
- ✅ `edit_phone` правильно змінює існуючі номери
- ✅ Немає дублікатів телефонів/email
- ✅ Методи повертають правильні типи (bool/None)

### **Emma (Birthday/Serialization) Review:**
- ✅ `days_to_birthday` правильно рахує дні
- ✅ `to_dict` серіалізує всі поля  
- ✅ `from_dict` відновлює Contact з dict
- ✅ `__eq__` правильно порівнює контакти
- ✅ Інтеграція з Birthday field працює

---

## 🎯 **Фінальна інтеграція:**

```bash
# Після всіх merge в main
cd dev_implementation
git checkout main
git pull origin main

# Тестування повного Contact класу
cd ..
python reference_tests/step_by_step/step_02_contact.py --verbose --compare
python reference_tests/step_by_step/step_01_field.py  # Перевірка що Field ще працює

# Оновлення основного проекту  
git add dev_implementation
git commit -m "📈 Contact клас завершений командною розробкою

✨ Результат командної роботи:
- Sarah: Contact foundation (__init__, __str__, __repr__)  
- Alex: Phone/Email management (add/remove/edit методи)
- Emma: Birthday інтеграція та JSON серіалізація

✅ Всі step_02_contact тести проходять
🔗 Готово до розробки Note класу та ContactManager"

git push origin main
```

**Результат: Contact клас розроблений командою з чітким розподілом та правильним Git workflow! 🚀**