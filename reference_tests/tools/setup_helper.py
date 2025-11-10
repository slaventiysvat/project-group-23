#!/usr/bin/env python3
"""
🚀 SETUP HELPER - Налаштування середовища розробки

Цей скрипт допомагає налаштувати правильну структуру папок
та створює базові файли для розробки.

Використання:
    python setup_helper.py                     # Повне налаштування
    python setup_helper.py --component field   # Тільки для Field
    python setup_helper.py --component contact # Тільки для Contact
"""

import argparse
import os
from pathlib import Path

def create_directory(path: Path, description: str):
    """Створює директорію з описом."""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Створено папку: {path} ({description})")
    else:
        print(f"📁 Папка вже існує: {path}")

def create_file(path: Path, content: str, description: str):
    """Створює файл з контентом."""
    if not path.exists():
        path.write_text(content, encoding='utf-8')
        print(f"✅ Створено файл: {path} ({description})")
    else:
        print(f"📄 Файл вже існує: {path}")

def setup_field_component():
    """Налаштування для компонента Field."""
    print("\n🔧 НАЛАШТУВАННЯ КОМПОНЕНТА FIELD")
    print("=" * 50)
    
    # Структура папок
    base_path = Path("dev_implementation")
    models_path = base_path / "models"
    
    create_directory(base_path, "Розробницька реалізація")
    create_directory(models_path, "Моделі даних")
    
    # __init__.py файли
    init_content = '"""Модуль моделей даних."""\n'
    create_file(base_path / "__init__.py", init_content, "Ініціалізація пакету")
    create_file(models_path / "__init__.py", init_content, "Ініціалізація моделей")
    
    # Базовий field.py
    field_template = '''"""
Field Classes - Базові класи для полів контакту.

Завдання:
1. Реалізувати базовий клас Field
2. Реалізувати класи Name, Phone, Email, Birthday, Address
3. Додати валідацію для кожного типу поля
"""

class Field:
    """Базовий клас для полів контакту."""
    
    def __init__(self, value: str):
        """Ініціалізація поля з валідацією."""
        self.value = self.validate(value)
    
    def validate(self, value: str) -> str:
        """Валідація значення поля."""
        # TODO: Реалізувати базову валідацію
        return value.strip()
    
    def __str__(self) -> str:
        """Строкове представлення поля."""
        # TODO: Реалізувати строкове представлення
        return str(self.value)

class Name(Field):
    """Поле для імені контакту."""
    
    def validate(self, value: str) -> str:
        """Валідація імені."""
        # TODO: Реалізувати валідацію імені
        # Підказка: використайте регулярні вирази
        # Приведіть до Title Case
        pass

class Phone(Field):
    """Поле для телефону контакту."""
    
    def validate(self, value: str) -> str:
        """Валідація та нормалізація телефону."""
        # TODO: Реалізувати валідацію українського телефону
        # Підказка: приведіть до формату +380XXXXXXXXX
        pass

class Email(Field):
    """Поле для email контакту."""
    
    def validate(self, value: str) -> str:
        """Валідація email адреси."""
        # TODO: Реалізувати валідацію email
        # Підказка: приведіть до нижнього регістру
        pass

class Birthday(Field):
    """Поле для дня народження."""
    
    def validate(self, value: str) -> str:
        """Валідація дати народження."""
        # TODO: Реалізувати валідацію дати
        # Підказка: підтримайте різні формати дат
        pass
    
    def to_date(self):
        """Конвертація в об'єкт datetime.date."""
        # TODO: Реалізувати конвертацію в date
        pass

class Address(Field):
    """Поле для адреси контакту."""
    
    def validate(self, value: str) -> str:
        """Валідація адреси."""
        # TODO: Реалізувати валідацію адреси
        # Підказка: перевірте мінімальну довжину
        pass
'''
    
    create_file(models_path / "field.py", field_template, "Шаблон Field класів")
    
    print("\n📋 НАСТУПНІ КРОКИ:")
    print("1. Відкрийте dev_implementation/models/field.py")
    print("2. Реалізуйте методи з TODO коментарами")
    print("3. Запустіть: python reference_tests/step_by_step/step_01_field.py")

def setup_contact_component():
    """Налаштування для компонента Contact."""
    print("\n🔧 НАЛАШТУВАННЯ КОМПОНЕНТА CONTACT")
    print("=" * 50)
    
    base_path = Path("dev_implementation/models")
    
    # Contact шаблон
    contact_template = '''"""
Contact Class - Клас для представлення контакту.

Завдання:
1. Реалізувати клас Contact з усіма полями
2. Додати методи для роботи з телефонами
3. Реалізувати серіалізацію/десеріалізацію
4. Додати методи пошуку та порівняння
"""

from .field import Name, Phone, Email, Birthday, Address
from typing import Optional, List, Dict, Any
from datetime import date

class Contact:
    """Клас для представлення контакту."""
    
    def __init__(self, name: Name):
        """Ініціалізація контакту з ім'ям."""
        # TODO: Реалізувати ініціалізацію
        self.name = name
        self.phones: List[Phone] = []
        self.email: Optional[Email] = None
        self.birthday: Optional[Birthday] = None
        self.address: Optional[Address] = None
    
    def add_phone(self, phone: Phone):
        """Додати телефон."""
        # TODO: Реалізувати додавання телефону
        # Підказка: перевірте на дублікати
        pass
    
    def remove_phone(self, phone_str: str):
        """Видалити телефон."""
        # TODO: Реалізувати видалення телефону
        pass
    
    def edit_phone(self, old_phone: str, new_phone: str):
        """Змінити телефон."""
        # TODO: Реалізувати зміну телефону
        pass
    
    def add_birthday(self, birthday: Birthday):
        """Додати день народження."""
        # TODO: Реалізувати додавання дня народження
        pass
    
    def days_to_birthday(self) -> Optional[int]:
        """Розрахувати дні до дня народження."""
        # TODO: Реалізувати розрахунок днів
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Серіалізація в словник."""
        # TODO: Реалізувати серіалізацію
        pass
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contact':
        """Десеріалізація зі словника."""
        # TODO: Реалізувати десеріалізацію
        pass
    
    def matches_search(self, query: str) -> bool:
        """Перевірити чи відповідає контакт пошуковому запиту."""
        # TODO: Реалізувати пошук
        pass
    
    def __str__(self) -> str:
        """Строкове представлення контакту."""
        # TODO: Реалізувати красиве представлення
        pass
    
    def __eq__(self, other) -> bool:
        """Порівняння контактів."""
        # TODO: Реалізувати порівняння
        pass
'''
    
    create_file(base_path / "contact.py", contact_template, "Шаблон Contact класу")
    
    print("\n📋 НАСТУПНІ КРОКИ:")
    print("1. Переконайтеся що Field класи завершені")
    print("2. Відкрийте dev_implementation/models/contact.py") 
    print("3. Реалізуйте методи з TODO коментарями")
    print("4. Запустіть: python reference_tests/step_by_step/step_02_contact.py")

def setup_all():
    """Повне налаштування."""
    print("🚀 ПОВНЕ НАЛАШТУВАННЯ СЕРЕДОВИЩА")
    print("=" * 60)
    
    setup_field_component()
    setup_contact_component()
    
    print("\n🎯 ЗАГАЛЬНІ РЕКОМЕНДАЦІЇ:")
    print("=" * 60)
    print("1. Розробляйте поетапно - спочатку Field, потім Contact")
    print("2. Використовуйте step-by-step тести для перевірки")
    print("3. Порівнюйте з еталоном через validator.py")
    print("4. Звертайтеся до документації у task_cards/")
    
    print("\n📚 КОРИСНІ КОМАНДИ:")
    print("python reference_tests/step_by_step/step_01_field.py --verbose")
    print("python reference_tests/step_by_step/step_02_contact.py --step 1")
    print("python reference_tests/tools/validator.py field")

def main():
    parser = argparse.ArgumentParser(description='Налаштування середовища розробки')
    parser.add_argument('--component', choices=['field', 'contact'], 
                       help='Налаштувати тільки певний компонент')
    
    args = parser.parse_args()
    
    if args.component == 'field':
        setup_field_component()
    elif args.component == 'contact':
        setup_contact_component()
    else:
        setup_all()

if __name__ == "__main__":
    main()