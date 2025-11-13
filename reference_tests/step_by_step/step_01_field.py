#!/usr/bin/env python3
"""
🧪 STEP 1: FIELD CLASSES - Поетапна перевірка

Цей файл допомагає розробнику поетапно створювати Field класи,
перевіряючи кожен метод окремо з еталонною реалізацією.

Використання:
    python step_01_field.py                    # Базова перевірка
    python step_01_field.py --verbose          # Детальний вивід  
    python step_01_field.py --step 3           # Тільки крок 3
    python step_01_field.py --compare          # Порівняння з еталоном
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional, Any

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Імпорт еталонної реалізації
try:
    from personal_assistant.models.field import Field, Name, Phone, Email, Birthday, Address
    REFERENCE_AVAILABLE = True
except ImportError:
    print("⚠️  Еталонна реалізація недоступна - запустимо тільки перевірку структури")
    REFERENCE_AVAILABLE = False

# Спроба імпорту розробницької реалізації
DEV_IMPLEMENTATION = None
try:
    # Тут розробник має створити свою реалізацію
    dev_path = project_root / "dev_implementation" / "models" / "field.py"
    if dev_path.exists():
        sys.path.insert(0, str(project_root / "dev_implementation"))
        import models.field as dev_field
        DEV_IMPLEMENTATION = dev_field
        print("✅ Знайдено розробницьку реалізацію")
    else:
        print("📝 Створіть папку dev_implementation/models/ та файл field.py")
except ImportError as e:
    print(f"⚠️  Помилка імпорту розробницької реалізації: {e}")

class FieldTester:
    """Тестер для поетапної перевірки Field класів."""
    
    def __init__(self, verbose: bool = False, compare: bool = False):
        self.verbose = verbose
        self.compare = compare
        self.passed = 0
        self.failed = 0
        self.reference = None
        self.dev = DEV_IMPLEMENTATION
        
        if REFERENCE_AVAILABLE:
            # Створюємо namespace з еталонними класами
            self.reference = type('Reference', (), {
                'Field': Field,
                'Name': Name, 
                'Phone': Phone,
                'Email': Email,
                'Birthday': Birthday,
                'Address': Address
            })
    
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
    
    def compare_behavior(self, test_name: str, dev_func, ref_func, *args, **kwargs):
        """Порівняння поведінки функцій."""
        if not self.compare or not self.reference:
            return True
            
        try:
            dev_result = dev_func(*args, **kwargs)
            ref_result = ref_func(*args, **kwargs)
            
            if dev_result == ref_result:
                if self.verbose:
                    print(f"🔍 {test_name}: Результати співпадають")
                return True
            else:
                print(f"🔍 {test_name}:")
                print(f"   Еталон: {ref_result}")
                print(f"   Твій код: {dev_result}")
                return False
                
        except Exception as e:
            print(f"🔍 {test_name}: Помилка при порівнянні - {e}")
            return False
    
    def step_1_field_base_class(self):
        """Крок 1: Перевірка базового класу Field."""
        self.print_step(1, "Базовий клас Field")
        
        if not self.dev:
            self.print_failure("Розробницька реалізація не знайдена")
            return
        
        # Перевірка наявності класу Field
        if not hasattr(self.dev, 'Field'):
            self.print_failure("Клас Field не знайдено", 
                             "Створіть клас Field у файлі dev_implementation/models/field.py")
            return
        
        field_class = self.dev.Field
        
        # Перевірка методу __init__
        try:
            test_field = field_class("test value")
            self.print_success("Field.__init__() працює")
        except Exception as e:
            self.print_failure(f"Field.__init__() не працює: {e}",
                             "Перевірте що Field.__init__ приймає value та зберігає його")
            return
        
        # Перевірка атрибуту value
        if hasattr(test_field, 'value'):
            self.print_success("Field.value атрибут присутній")
        else:
            self.print_failure("Field.value атрибут відсутній",
                             "Додайте self.value = self.validate(value) у __init__")
        
        # Перевірка методу validate
        if hasattr(field_class, 'validate'):
            self.print_success("Field.validate() метод присутній")
            
            # Тест валідації
            try:
                validated = test_field.validate("  test  ")
                if validated == "test":
                    self.print_success("Field.validate() правильно обрізає пробіли")
                else:
                    self.print_failure(f"Field.validate() не обрізає пробіли: '{validated}'",
                                     "validate() має повертати value.strip()")
            except Exception as e:
                self.print_failure(f"Field.validate() викидає помилку: {e}")
        else:
            self.print_failure("Field.validate() метод відсутній")
        
        # Перевірка __str__ методу
        if hasattr(test_field, '__str__'):
            str_result = str(test_field)
            if str_result:
                self.print_success("Field.__str__() працює")
            else:
                self.print_failure("Field.__str__() повертає порожній рядок")
        else:
            self.print_failure("Field.__str__() метод відсутній")
    
    def step_2_name_class(self):
        """Крок 2: Перевірка класу Name."""
        self.print_step(2, "Клас Name")
        
        if not self.dev or not hasattr(self.dev, 'Name'):
            self.print_failure("Клас Name не знайдено")
            return
        
        name_class = self.dev.Name
        
        # Тест успішного створення
        try:
            name1 = name_class("Іван Петров")
            self.print_success("Name створюється з валідним ім'ям")
            
            # Перевірка Title Case
            if name1.value == "Іван Петров":
                self.print_success("Name зберігає правильний регістр")
            else:
                self.print_failure(f"Name не приводить до Title Case: '{name1.value}'",
                                 "Використайте title() або власну логіку для приведення до Title Case")
        except Exception as e:
            self.print_failure(f"Name не створюється: {e}")
            return
        
        # Тест з lowercase  
        try:
            name2 = name_class("іван петров")
            if name2.value == "Іван Петров":
                self.print_success("Name правильно приводить до Title Case")
            else:
                self.print_failure(f"Name не приводить lowercase до Title Case: '{name2.value}'")
        except Exception as e:
            self.print_failure(f"Name з lowercase викликає помилку: {e}")
        
        # Тест валідації помилкових імен
        invalid_names = ["", "123", "Іван@петров", "  "]
        
        for invalid_name in invalid_names:
            try:
                name_class(invalid_name)
                self.print_failure(f"Name приймає неvalідне ім'я: '{invalid_name}'",
                                 "Додайте валідацію через регекс у методі validate()")
            except ValueError:
                self.print_success(f"Name правильно відкидає неvalідне ім'я: '{invalid_name}'")
            except Exception as e:
                self.print_failure(f"Name з '{invalid_name}' викликає неочікувану помилку: {e}")
        
        # Порівняння з еталоном
        if self.reference:
            test_cases = ["Іван Петров", "mary o'connor", "анна-марія"]
            for test_case in test_cases:
                try:
                    dev_name = name_class(test_case)
                    ref_name = self.reference.Name(test_case)
                    
                    if dev_name.value == ref_name.value:
                        if self.verbose:
                            print(f"🔍 Name('{test_case}'): ✅ Результати співпадають")
                    else:
                        print(f"🔍 Name('{test_case}'):")
                        print(f"   Еталон: '{ref_name.value}'")
                        print(f"   Твій код: '{dev_name.value}'")
                except Exception as e:
                    print(f"🔍 Name('{test_case}'): ❌ Помилка - {e}")
    
    def step_3_phone_class(self):
        """Крок 3: Перевірка класу Phone."""
        self.print_step(3, "Клас Phone") 
        
        if not self.dev or not hasattr(self.dev, 'Phone'):
            self.print_failure("Клас Phone не знайдено")
            return
        
        phone_class = self.dev.Phone
        
        # Тести нормалізації
        test_cases = [
            ("+380501234567", "+380501234567"),  # Вже нормалізований
            ("380501234567", "+380501234567"),   # Без +
            ("0501234567", "+380501234567"),     # Національний формат
        ]
        
        for input_phone, expected in test_cases:
            try:
                phone = phone_class(input_phone)
                if phone.value == expected:
                    self.print_success(f"Phone правильно нормалізує '{input_phone}' → '{expected}'")
                else:
                    self.print_failure(f"Phone неправильно нормалізує '{input_phone}': отримано '{phone.value}', очікувалося '{expected}'",
                                     "Перевірте логіку нормалізації у методі validate()")
            except Exception as e:
                self.print_failure(f"Phone з '{input_phone}' викликає помилку: {e}")
        
        # Тести валідації неправильних номерів
        invalid_phones = ["123", "+1234567890", "абвгде", ""]
        
        for invalid_phone in invalid_phones:
            try:
                phone_class(invalid_phone) 
                self.print_failure(f"Phone приймає неvalідний номер: '{invalid_phone}'",
                                 "Додайте валідацію українських номерів")
            except ValueError:
                self.print_success(f"Phone правильно відкидає неvalідний номер: '{invalid_phone}'")
            except Exception as e:
                self.print_failure(f"Phone з '{invalid_phone}' викликає неочікувану помилку: {e}")
        
        # Порівняння з еталоном
        if self.reference:
            for input_phone, expected in test_cases:
                try:
                    dev_phone = phone_class(input_phone)
                    ref_phone = self.reference.Phone(input_phone)
                    
                    if dev_phone.value == ref_phone.value:
                        if self.verbose:
                            print(f"🔍 Phone('{input_phone}'): ✅ Результати співпадають")
                    else:
                        print(f"🔍 Phone('{input_phone}'):")
                        print(f"   Еталон: '{ref_phone.value}'")
                        print(f"   Твій код: '{dev_phone.value}'")
                except Exception as e:
                    print(f"🔍 Phone('{input_phone}'): ❌ Помилка - {e}")
    
    def step_4_email_class(self):
        """Крок 4: Перевірка класу Email.""" 
        self.print_step(4, "Клас Email")
        
        if not self.dev or not hasattr(self.dev, 'Email'):
            self.print_failure("Клас Email не знайдено")
            return
        
        email_class = self.dev.Email
        
        # Тести валідних email
        valid_emails = [
            ("test@example.com", "test@example.com"),
            ("TEST@EXAMPLE.COM", "test@example.com"),  # Lowercase
            ("user.name+tag@domain.co.uk", "user.name+tag@domain.co.uk"),
        ]
        
        for input_email, expected in valid_emails:
            try:
                email = email_class(input_email)
                if email.value == expected:
                    self.print_success(f"Email правильно обробляє '{input_email}' → '{expected}'")
                else:
                    self.print_failure(f"Email неправильно обробляє '{input_email}': отримано '{email.value}', очікувалося '{expected}'")
            except Exception as e:
                self.print_failure(f"Email з '{input_email}' викликає помилку: {e}")
        
        # Тести неvalідних email
        invalid_emails = ["invalid", "@domain.com", "user@", ""]
        
        for invalid_email in invalid_emails:
            try:
                email_class(invalid_email)
                self.print_failure(f"Email приймає неvalідну адресу: '{invalid_email}'")
            except ValueError:
                self.print_success(f"Email правильно відкидає неvalідну адресу: '{invalid_email}'")
            except Exception as e:
                self.print_failure(f"Email з '{invalid_email}' викликає неочікувану помилку: {e}")
    
    def step_5_birthday_class(self):
        """Крок 5: Перевірка класу Birthday."""
        self.print_step(5, "Клас Birthday")
        
        if not self.dev or not hasattr(self.dev, 'Birthday'):
            self.print_failure("Клас Birthday не знайдено") 
            return
        
        birthday_class = self.dev.Birthday
        
        # Тести різних форматів дат
        valid_dates = [
            "15.03.1990",
            "15-03-1990", 
            "15/03/1990"
        ]
        
        for date_str in valid_dates:
            try:
                birthday = birthday_class(date_str)
                self.print_success(f"Birthday приймає формат: '{date_str}'")
                
                # Перевірка методу to_date()
                if hasattr(birthday, 'to_date'):
                    date_obj = birthday.to_date()
                    if date_obj.year == 1990 and date_obj.month == 3 and date_obj.day == 15:
                        self.print_success(f"Birthday.to_date() правильно парсить '{date_str}'")
                    else:
                        self.print_failure(f"Birthday.to_date() неправильно парсить '{date_str}': {date_obj}")
                else:
                    self.print_failure("Birthday.to_date() метод відсутній")
                    
            except Exception as e:
                self.print_failure(f"Birthday з '{date_str}' викликає помилку: {e}")
        
        # Тести неvalідних дат
        invalid_dates = ["32.13.2000", "15.03.2026", "abc", ""]
        
        for invalid_date in invalid_dates:
            try:
                birthday_class(invalid_date)
                self.print_failure(f"Birthday приймає неvalідну дату: '{invalid_date}'")
            except ValueError:
                self.print_success(f"Birthday правильно відкидає неvalідну дату: '{invalid_date}'") 
            except Exception as e:
                self.print_failure(f"Birthday з '{invalid_date}' викликає неочікувану помилку: {e}")
    
    def step_6_address_class(self):
        """Крок 6: Перевірка класу Address."""
        self.print_step(6, "Клас Address")
        
        if not self.dev or not hasattr(self.dev, 'Address'):
            self.print_failure("Клас Address не знайдено")
            return
        
        address_class = self.dev.Address
        
        # Тести валідних адрес
        valid_addresses = [
            ("   вул. Хрещатик, 1   ", "вул. Хрещатик, 1"),  # Обрізання пробілів
            ("проспект Перемоги, 50", "проспект Перемоги, 50"),
        ]
        
        for input_addr, expected in valid_addresses:
            try:
                address = address_class(input_addr)
                if address.value == expected:
                    self.print_success(f"Address правильно обробляє '{input_addr}' → '{expected}'")
                else:
                    self.print_failure(f"Address неправильно обробляє '{input_addr}': отримано '{address.value}'")
            except Exception as e:
                self.print_failure(f"Address з '{input_addr}' викликає помилку: {e}")
        
        # Тести неvalідних адрес
        invalid_addresses = ["", "abc", "x"]  # Замало символів
        
        for invalid_addr in invalid_addresses:
            try:
                address_class(invalid_addr)
                self.print_failure(f"Address приймає занадто коротку адресу: '{invalid_addr}'")
            except ValueError:
                self.print_success(f"Address правильно відкидає коротку адресу: '{invalid_addr}'")
            except Exception as e:
                self.print_failure(f"Address з '{invalid_addr}' викликає неочікувану помилку: {e}")
    
    def run_step(self, step_num: int):
        """Запуск конкретного кроку."""
        steps = {
            1: self.step_1_field_base_class,
            2: self.step_2_name_class,
            3: self.step_3_phone_class,
            4: self.step_4_email_class, 
            5: self.step_5_birthday_class,
            6: self.step_6_address_class,
        }
        
        if step_num in steps:
            steps[step_num]()
        else:
            print(f"❌ Крок {step_num} не існує. Доступні кроки: 1-6")
    
    def run_all_steps(self):
        """Запуск всіх кроків."""
        for i in range(1, 7):
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
            print(f"\n🎉 Всі тести пройдені! Field класи готові.")
        else:
            print(f"\n🔧 Є проблеми що потребують вирішення.")
            print(f"💡 Підказка: Подивіться на еталонну реалізацію у personal_assistant/models/field.py")

def main():
    parser = argparse.ArgumentParser(description='Поетапна перевірка Field класів')
    parser.add_argument('--step', type=int, help='Запустити тільки певний крок (1-6)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    parser.add_argument('--compare', '-c', action='store_true', help='Порівняння з еталоном')
    
    args = parser.parse_args()
    
    print("🧪 ПОЕТАПНА ПЕРЕВІРКА FIELD КЛАСІВ")
    print("=" * 60)
    
    if not DEV_IMPLEMENTATION:
        print("\n📝 Щоб розпочати:")
        print("1. Створіть папку: dev_implementation/models/")
        print("2. Створіть файл: dev_implementation/models/__init__.py")  
        print("3. Створіть файл: dev_implementation/models/field.py")
        print("4. Почніть з базового класу Field")
        return
    
    tester = FieldTester(verbose=args.verbose, compare=args.compare)
    
    if args.step:
        tester.run_step(args.step)
    else:
        tester.run_all_steps()
    
    tester.show_summary()

if __name__ == "__main__":
    main()