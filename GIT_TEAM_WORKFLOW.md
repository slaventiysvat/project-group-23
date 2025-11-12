# 🔧 Git Workflow для командної розробки field.py

## 🎯 Стратегія: Feature Branches + Pull Requests

### 👥 Розподіл завдань:
- **Developer 1** (John): `Field`, `Name`, `Phone` класи
- **Developer 2** (Anna): `Email`, `Birthday` класи  
- **Developer 3** (Mike): `Address` клас + додаткова валідація

---

## 📋 Покрокові команди

### 🚀 Початкове налаштування (Team Lead):

```bash
# 1. Клонування проекту з submodules
git clone --recurse-submodules https://github.com/slaventiysvat/project-group-23.git
cd project-group-23/dev_implementation

# 2. Створення початкової структури field.py
cat > models/field.py << 'EOF'
#!/usr/bin/env python3
"""
Personal Assistant Field Classes
Розробка: Team Neoversity Group 1
"""

from abc import ABC, abstractmethod
from typing import Any
import re
from datetime import datetime, date


class Field(ABC):
    """Базовий клас для всіх полів."""
    
    def __init__(self, value: Any):
        self.value = self.validate(value)
    
    @abstractmethod
    def validate(self, value: Any) -> Any:
        """Валідація значення поля."""
        pass
    
    def __str__(self) -> str:
        return str(self.value)


# TODO: Developer 1 - implement these classes
class Name(Field):
    """Поле для імені контакту."""
    pass

class Phone(Field):
    """Поле для телефонного номера."""
    pass


# TODO: Developer 2 - implement these classes  
class Email(Field):
    """Поле для email адреси."""
    pass

class Birthday(Field):
    """Поле для дати народження."""
    pass


# TODO: Developer 3 - implement these classes
class Address(Field):
    """Поле для адреси."""
    pass
EOF

# 3. Коміт початкової структури
git add models/field.py
git commit -m "🏗️ Початкова структура field.py для командної розробки"
git push origin main
```

---

## 👨‍💻 Команди для Developer 1 (Field, Name, Phone):

```bash
# 1. Клонування та налаштування
git clone --recurse-submodules https://github.com/slaventiysvat/project-group-23.git
cd project-group-23/dev_implementation

# 2. Створення feature гілки
git checkout -b feature/field-name-phone-classes
git push -u origin feature/field-name-phone-classes

# 3. Розробка класів (field.py modifications)
# Реалізувати Field.validate(), Name, Phone класи

# 4. Тестування
cd ..
python reference_tests/step_by_step/step_01_field.py --step 1
python reference_tests/step_by_step/step_01_field.py --step 2  
python reference_tests/step_by_step/step_01_field.py --step 3

# 5. Коміт та push
cd dev_implementation
git add models/field.py
git commit -m "✨ Реалізовано Field, Name, Phone класи

- Додано Field.validate() з обрізанням пробілів
- Реалізовано Name з Title Case та regex валідацією  
- Додано Phone з українською нормалізацією (+380 формат)
- Всі тести step_01, step_02, step_03 проходять"

git push origin feature/field-name-phone-classes

# 6. Створення Pull Request на GitHub
# Перейти на https://github.com/slaventiysvat/assistant_dev_implementation
# Create Pull Request: feature/field-name-phone-classes → main
```

---

## 👩‍💻 Команди для Developer 2 (Email, Birthday):

```bash
# 1. Синхронізація з останніми змінами
git checkout main
git pull origin main

# 2. Створення feature гілки
git checkout -b feature/email-birthday-classes  
git push -u origin feature/email-birthday-classes

# 3. Розробка класів
# Реалізувати Email, Birthday класи

# 4. Тестування
cd ..
python reference_tests/step_by_step/step_01_field.py --step 4
python reference_tests/step_by_step/step_01_field.py --step 5

# 5. Коміт та PR
cd dev_implementation
git add models/field.py
git commit -m "✨ Реалізовано Email та Birthday класи

- Додано Email з regex валідацією та lowercase
- Реалізовано Birthday з підтримкою різних форматів дат
- Додано to_date() метод для Birthday
- Тести step_04, step_05 проходять"

git push origin feature/email-birthday-classes
# Створити PR на GitHub
```

---

## 🛠️ Команди для Developer 3 (Address + Integration):

```bash
# 1. Синхронізація 
git checkout main
git pull origin main

# 2. Feature гілка
git checkout -b feature/address-integration
git push -u origin feature/address-integration

# 3. Розробка + інтеграція
# Реалізувати Address клас
# Протестувати всю систему разом

# 4. Повне тестування
cd ..
python reference_tests/step_by_step/step_01_field.py --verbose
python reference_tests/step_by_step/step_01_field.py --compare

# 5. Final commit
cd dev_implementation
git add models/field.py
git commit -m "✅ Завершено field.py - всі класи готові

- Реалізовано Address клас з валідацією довжини
- Інтеграція всіх Field класів
- Всі step-тesti проходять (6/6)
- Готово до інтеграції з Contact моделлю"

git push origin feature/address-integration
```

---

## 🔄 Rebase та конфлікти:

### Якщо є конфлікти при rebase:
```bash
# Синхронізація з main перед роботою
git checkout main
git pull origin main
git checkout feature/my-branch
git rebase main

# Якщо конфлікти:
# 1. Відкрити field.py в редакторі
# 2. Розв'язати конфлікти (видалити <<<< ==== >>>>)
# 3. Зберегти файл
git add models/field.py
git rebase --continue

# Форс push після rebase
git push --force-with-lease origin feature/my-branch
```

### Merge конфліктів в field.py:
```python
# Приклад конфлікту:
<<<<<<< HEAD
class Email(Field):
    def validate(self, value):
        # Developer 2 version
        return value.lower()
=======
class Email(Field):  
    def validate(self, value):
        # Developer 1 version  
        return value.strip()
>>>>>>> feature/other-branch

# Розв'язання - взяти обидві логіки:
class Email(Field):
    def validate(self, value):
        return value.strip().lower()
```

---

## 📊 Pull Request Review Process:

### Code Review Checklist:
- ✅ Всі step-тести проходять
- ✅ Код відповідає PEP 8
- ✅ Додані docstrings  
- ✅ Type hints використовуються
- ✅ Немає дублювання коду
- ✅ Валідація працює правильно

### Approval Process:
1. **Developer створює PR**
2. **2 інші розробники роблять review**  
3. **Team Lead дає final approval**
4. **Merge до main**
5. **Delete feature branch**

---

## 🎯 Фінальна синхронізація:

```bash
# Після всіх merge в main
cd dev_implementation  
git checkout main
git pull origin main

# Оновити основний проект
cd ..
git add dev_implementation
git commit -m "📈 Оновлено dev_implementation - field.py готовий"
git push origin main
```

**Результат: field.py створений командою з правильною Git історією! 🚀**