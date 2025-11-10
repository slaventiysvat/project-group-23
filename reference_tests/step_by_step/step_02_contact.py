#!/usr/bin/env python3
"""
🧪 STEP 2: CONTACT CLASS - Поетапна перевірка

Цей файл допомагає розробнику поетапно створювати клас Contact,
перевіряючи кожен метод окремо з еталонною реалізацією.

Використання:
    python step_02_contact.py                  # Базова перевірка
    python step_02_contact.py --verbose        # Детальний вивід  
    python step_02_contact.py --step 2         # Тільки крок 2
    python step_02_contact.py --compare        # Порівняння з еталоном
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, date

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Імпорт еталонної реалізації
try:
    from personal_assistant.models.contact import Contact
    from personal_assistant.models.field import Name, Phone, Email, Birthday, Address
    REFERENCE_AVAILABLE = True
except ImportError:
    print("⚠️  Еталонна реалізація недоступна")
    REFERENCE_AVAILABLE = False

# Спроба імпорту розробницької реалізації
DEV_IMPLEMENTATION = None
DEV_FIELDS = None
try:
    dev_path = project_root / "dev_implementation"
    if dev_path.exists():
        sys.path.insert(0, str(dev_path))
        try:
            import models.contact as dev_contact
            import models.field as dev_field
            DEV_IMPLEMENTATION = dev_contact
            DEV_FIELDS = dev_field
            print("✅ Знайдено розробницьку реалізацію")
        except ImportError as e:
            print(f"⚠️  Помилка імпорту: {e}")
    else:
        print("📝 Створіть папку dev_implementation/models/")
except Exception as e:
    print(f"⚠️  Помилка: {e}")

class ContactTester:
    """Тестер для поетапної перевірки класу Contact."""
    
    def __init__(self, verbose: bool = False, compare: bool = False):
        self.verbose = verbose
        self.compare = compare
        self.passed = 0
        self.failed = 0
        self.dev = DEV_IMPLEMENTATION
        self.dev_fields = DEV_FIELDS
    
    def print_step(self, step_num: int, description: str):
        """Друк заголовку кроку."""
        print(f"\n{'='*60}")
        print(f"📋 КРОК {step_num}: {description}")
        print(f"{'='*60}")
    
    def print_success(self, message: str):
        """Друк повідомлення про успіх."""
        print(f"✅ {message}")
        self.passed += 1
    
    def print_failure(self, message: str, hint: str = ""):
        """Друк повідомлення про помилку."""
        print(f"❌ {message}")
        if hint:
            print(f"💡 Підказка: {hint}")
        self.failed += 1
    
    def step_1_contact_init(self):
        """Крок 1: Перевірка ініціалізації Contact."""
        self.print_step(1, "Ініціалізація Contact")
        
        if not self.dev or not hasattr(self.dev, 'Contact'):
            self.print_failure("Клас Contact не знайдено")
            return
        
        if not self.dev_fields or not hasattr(self.dev_fields, 'Name'):
            self.print_failure("Field класи не знайдені", 
                             "Спочатку реалізуйте Field класи")
            return
        
        contact_class = self.dev.Contact
        name_class = self.dev_fields.Name
        
        # Тест базової ініціалізації
        try:
            contact = contact_class(name_class("Іван Петров"))
            self.print_success("Contact створюється з Name")
            
            # Перевірка атрибутів
            if hasattr(contact, 'name'):
                self.print_success("Contact.name атрибут присутній")
            else:
                self.print_failure("Contact.name атрибут відсутній")
            
            if hasattr(contact, 'phones'):
                if isinstance(contact.phones, list):
                    self.print_success("Contact.phones є списком")
                else:
                    self.print_failure("Contact.phones не є списком")
            else:
                self.print_failure("Contact.phones атрибут відсутній")
            
            # Перевірка інших атрибутів
            optional_attrs = ['email', 'birthday', 'address']
            for attr in optional_attrs:
                if hasattr(contact, attr):
                    self.print_success(f"Contact.{attr} атрибут присутній")
                else:
                    self.print_failure(f"Contact.{attr} атрибут відсутній")
                    
        except Exception as e:
            self.print_failure(f"Contact не створюється: {e}")
    
    def step_2_phone_management(self):
        """Крок 2: Керування телефонами."""
        self.print_step(2, "Керування телефонами")
        
        if not self.dev or not self.dev_fields:
            self.print_failure("Реалізація не знайдена")
            return
        
        try:
            contact = self.dev.Contact(self.dev_fields.Name("Тест"))
            phone_class = self.dev_fields.Phone
            
            # Тест add_phone
            if hasattr(contact, 'add_phone'):
                phone1 = phone_class("0501234567")
                contact.add_phone(phone1)
                
                if len(contact.phones) == 1:
                    self.print_success("add_phone() додає телефон")
                else:
                    self.print_failure("add_phone() не додає телефон до списку")
                
                # Тест дублікатів
                contact.add_phone(phone1)  # Той самий телефон
                if len(contact.phones) == 1:
                    self.print_success("add_phone() запобігає дублікатам")
                else:
                    self.print_failure("add_phone() не запобігає дублікатам")
            else:
                self.print_failure("Метод add_phone() відсутній")
            
            # Тест remove_phone
            if hasattr(contact, 'remove_phone'):
                contact.remove_phone("0501234567")
                if len(contact.phones) == 0:
                    self.print_success("remove_phone() видаляє телефон")
                else:
                    self.print_failure("remove_phone() не видаляє телефон")
            else:
                self.print_failure("Метод remove_phone() відсутній")
            
            # Тест edit_phone
            if hasattr(contact, 'edit_phone'):
                contact.add_phone(phone_class("0501234567"))
                old_phone = "0501234567"
                new_phone = "0677654321"
                
                try:
                    contact.edit_phone(old_phone, new_phone)
                    if any(p.value == "+380677654321" for p in contact.phones):
                        self.print_success("edit_phone() змінює телефон")
                    else:
                        self.print_failure("edit_phone() не змінює телефон правильно")
                except Exception as e:
                    self.print_failure(f"edit_phone() викликає помилку: {e}")
            else:
                self.print_failure("Метод edit_phone() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в тестах телефонів: {e}")
    
    def step_3_contact_methods(self):
        """Крок 3: Основні методи контакту."""
        self.print_step(3, "Основні методи контакту")
        
        if not self.dev or not self.dev_fields:
            self.print_failure("Реалізація не знайдена")
            return
        
        try:
            contact = self.dev.Contact(self.dev_fields.Name("Іван Петров"))
            
            # Тест __str__
            str_result = str(contact)
            if "Іван Петров" in str_result:
                self.print_success("__str__() включає ім'я")
            else:
                self.print_failure("__str__() не включає ім'я")
            
            # Тест add_birthday
            if hasattr(contact, 'add_birthday'):
                birthday = self.dev_fields.Birthday("15.03.1990")
                contact.add_birthday(birthday)
                
                if contact.birthday is not None:
                    self.print_success("add_birthday() встановлює день народження")
                else:
                    self.print_failure("add_birthday() не встановлює день народження")
            else:
                self.print_failure("Метод add_birthday() відсутній")
            
            # Тест days_to_birthday
            if hasattr(contact, 'days_to_birthday'):
                try:
                    days = contact.days_to_birthday()
                    if isinstance(days, int) and days >= 0:
                        self.print_success("days_to_birthday() повертає коректне число днів")
                    else:
                        self.print_failure(f"days_to_birthday() повертає некоректне значення: {days}")
                except Exception as e:
                    self.print_failure(f"days_to_birthday() викликає помилку: {e}")
            else:
                self.print_failure("Метод days_to_birthday() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в основних методах: {e}")
    
    def step_4_serialization(self):
        """Крок 4: Серіалізація та десеріалізація."""
        self.print_step(4, "Серіалізація та десеріалізація")
        
        if not self.dev or not self.dev_fields:
            self.print_failure("Реалізація не знайдена")
            return
        
        try:
            # Створення повного контакту
            contact = self.dev.Contact(self.dev_fields.Name("Іван Петров"))
            contact.add_phone(self.dev_fields.Phone("0501234567"))
            contact.email = self.dev_fields.Email("ivan@test.com")
            contact.add_birthday(self.dev_fields.Birthday("15.03.1990"))
            contact.address = self.dev_fields.Address("вул. Тестова, 1")
            
            # Тест to_dict
            if hasattr(contact, 'to_dict'):
                contact_dict = contact.to_dict()
                
                if isinstance(contact_dict, dict):
                    self.print_success("to_dict() повертає словник")
                    
                    # Перевірка ключів
                    required_keys = ['name', 'phones', 'email', 'birthday', 'address']
                    for key in required_keys:
                        if key in contact_dict:
                            self.print_success(f"to_dict() включає ключ '{key}'")
                        else:
                            self.print_failure(f"to_dict() не включає ключ '{key}'")
                else:
                    self.print_failure("to_dict() не повертає словник")
            else:
                self.print_failure("Метод to_dict() відсутній")
            
            # Тест from_dict
            if hasattr(self.dev.Contact, 'from_dict'):
                try:
                    test_dict = {
                        'name': 'Марія Іванова',
                        'phones': ['+380501234567'],
                        'email': 'maria@test.com',
                        'birthday': '20.05.1985',
                        'address': 'вул. Нова, 5'
                    }
                    
                    restored_contact = self.dev.Contact.from_dict(test_dict)
                    
                    if restored_contact.name.value == "Марія Іванова":
                        self.print_success("from_dict() відновлює ім'я")
                    else:
                        self.print_failure("from_dict() не відновлює ім'я правильно")
                    
                    if len(restored_contact.phones) > 0:
                        self.print_success("from_dict() відновлює телефони")
                    else:
                        self.print_failure("from_dict() не відновлює телефони")
                        
                except Exception as e:
                    self.print_failure(f"from_dict() викликає помилку: {e}")
            else:
                self.print_failure("Метод from_dict() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в серіалізації: {e}")
    
    def step_5_comparison_and_search(self):
        """Крок 5: Порівняння та пошук."""
        self.print_step(5, "Порівняння та пошук")
        
        if not self.dev or not self.dev_fields:
            self.print_failure("Реалізація не знайдена")
            return
        
        try:
            contact1 = self.dev.Contact(self.dev_fields.Name("Іван Петров"))
            contact2 = self.dev.Contact(self.dev_fields.Name("Марія Іванова"))
            contact3 = self.dev.Contact(self.dev_fields.Name("Іван Петров"))  # Дублікат
            
            # Тест __eq__
            if contact1 == contact3:
                self.print_success("__eq__() правильно порівнює однакові контакти")
            else:
                self.print_failure("__eq__() не розпізнає однакові контакти")
            
            if not (contact1 == contact2):
                self.print_success("__eq__() правильно розрізняє різні контакти")
            else:
                self.print_failure("__eq__() не розрізняє різні контакти")
            
            # Тест пошуку
            if hasattr(contact1, 'matches_search'):
                # Пошук за ім'ям
                if contact1.matches_search("Іван"):
                    self.print_success("matches_search() знаходить за ім'ям")
                else:
                    self.print_failure("matches_search() не знаходить за ім'ям")
                
                # Пошук за телефоном
                contact1.add_phone(self.dev_fields.Phone("0501234567"))
                if contact1.matches_search("0501234567"):
                    self.print_success("matches_search() знаходить за телефоном")
                else:
                    self.print_failure("matches_search() не знаходить за телефоном")
                
                # Пошук за email
                contact1.email = self.dev_fields.Email("ivan@test.com")
                if contact1.matches_search("ivan@test.com"):
                    self.print_success("matches_search() знаходить за email")
                else:
                    self.print_failure("matches_search() не знаходить за email")
            else:
                self.print_failure("Метод matches_search() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в порівнянні: {e}")
    
    def run_step(self, step_num: int):
        """Запуск конкретного кроку."""
        steps = {
            1: self.step_1_contact_init,
            2: self.step_2_phone_management,
            3: self.step_3_contact_methods,
            4: self.step_4_serialization,
            5: self.step_5_comparison_and_search,
        }
        
        if step_num in steps:
            steps[step_num]()
        else:
            print(f"❌ Крок {step_num} не існує. Доступні кроки: 1-5")
    
    def run_all_steps(self):
        """Запуск всіх кроків."""
        for i in range(1, 6):
            self.run_step(i)
    
    def show_summary(self):
        """Показ підсумку."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"📊 ПІДСУМОК")
        print(f"{'='*60}")
        print(f"✅ Пройдено: {self.passed}")
        print(f"❌ Не пройдено: {self.failed}")
        print(f"📈 Прогрес: {self.passed}/{total} ({self.passed/total*100:.1f}%)" if total > 0 else "")
        
        if self.failed == 0:
            print(f"\n🎉 Всі тести пройдені! Клас Contact готовий.")
        else:
            print(f"\n🔧 Є проблеми що потребують вирішення.")
            print(f"💡 Підказка: Подивіться на еталонну реалізацію у personal_assistant/models/contact.py")

def main():
    parser = argparse.ArgumentParser(description='Поетапна перевірка класу Contact')
    parser.add_argument('--step', type=int, help='Запустити тільки певний крок (1-5)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    parser.add_argument('--compare', '-c', action='store_true', help='Порівняння з еталоном')
    
    args = parser.parse_args()
    
    print("🧪 ПОЕТАПНА ПЕРЕВІРКА КЛАСУ CONTACT")
    print("=" * 60)
    
    if not DEV_IMPLEMENTATION:
        print("\n📝 Щоб розпочати:")
        print("1. Завершіть реалізацію Field класів (step_01_field.py)")
        print("2. Створіть файл: dev_implementation/models/contact.py")
        print("3. Імплементуйте клас Contact з усіма методами")
        return
    
    tester = ContactTester(verbose=args.verbose, compare=args.compare)
    
    if args.step:
        tester.run_step(args.step)
    else:
        tester.run_all_steps()
    
    tester.show_summary()

if __name__ == "__main__":
    main()