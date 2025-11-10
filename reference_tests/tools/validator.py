#!/usr/bin/env python3
"""
🧪 VALIDATOR TOOL - Порівняння з еталоном

Цей інструмент порівнює розробницьку реалізацію з еталонною
та показує детальні відмінності в поведінці.

Використання:
    python validator.py field                    # Перевірка Field класів
    python validator.py contact                  # Перевірка Contact класу  
    python validator.py all                      # Перевірка всього
    python validator.py --help                   # Допомога
"""

import sys
import os
import argparse
import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class TestResult:
    """Результат тесту."""
    name: str
    passed: bool
    reference_result: Any = None
    dev_result: Any = None
    error: str = ""

class ComponentValidator:
    """Базовий клас для валідаторів компонентів."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[TestResult] = []
        
    def add_result(self, result: TestResult):
        """Додати результат тесту."""
        self.results.append(result)
        
    def print_results(self):
        """Вивести результати."""
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print(f"\n{'='*70}")
        print(f"📊 РЕЗУЛЬТАТИ ВАЛІДАЦІЇ")
        print(f"{'='*70}")
        print(f"✅ Пройдено: {passed}")
        print(f"❌ Не пройдено: {total - passed}")
        print(f"📈 Прогрес: {passed}/{total} ({passed/total*100:.1f}%)" if total > 0 else "")
        
        # Детальні результати
        for result in self.results:
            if result.passed:
                print(f"✅ {result.name}")
            else:
                print(f"❌ {result.name}")
                if result.error:
                    print(f"   Помилка: {result.error}")
                elif result.reference_result != result.dev_result:
                    print(f"   Еталон: {result.reference_result}")
                    print(f"   Твій код: {result.dev_result}")

class FieldValidator(ComponentValidator):
    """Валідатор для Field класів."""
    
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        
        # Імпорт еталонної реалізації
        try:
            from personal_assistant.models.field import Field, Name, Phone, Email, Birthday, Address
            self.ref_classes = {
                'Field': Field,
                'Name': Name,
                'Phone': Phone,
                'Email': Email,
                'Birthday': Birthday,
                'Address': Address
            }
        except ImportError:
            print("❌ Еталонна реалізація недоступна")
            self.ref_classes = {}
        
        # Імпорт розробницької реалізації
        self.dev_classes = {}
        try:
            dev_path = project_root / "dev_implementation" / "models" / "field.py"
            if dev_path.exists():
                spec = importlib.util.spec_from_file_location("dev_field", dev_path)
                dev_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(dev_module)
                
                for class_name in ['Field', 'Name', 'Phone', 'Email', 'Birthday', 'Address']:
                    if hasattr(dev_module, class_name):
                        self.dev_classes[class_name] = getattr(dev_module, class_name)
            else:
                print("❌ Розробницька реалізація не знайдена")
        except Exception as e:
            print(f"❌ Помилка імпорту розробницької реалізації: {e}")
    
    def validate_name_class(self):
        """Валідація класу Name."""
        if 'Name' not in self.ref_classes or 'Name' not in self.dev_classes:
            self.add_result(TestResult("Name класи", False, error="Класи не знайдені"))
            return
        
        ref_name = self.ref_classes['Name']
        dev_name = self.dev_classes['Name']
        
        test_cases = [
            "іван петров",
            "mary o'connor", 
            "анна-марія",
            "ПЕТРО СИДОРЕНКО"
        ]
        
        for test_case in test_cases:
            try:
                ref_result = ref_name(test_case).value
                dev_result = dev_name(test_case).value
                
                passed = ref_result == dev_result
                self.add_result(TestResult(
                    f"Name('{test_case}')",
                    passed,
                    ref_result,
                    dev_result
                ))
            except Exception as e:
                self.add_result(TestResult(
                    f"Name('{test_case}')",
                    False,
                    error=str(e)
                ))
    
    def validate_phone_class(self):
        """Валідація класу Phone."""
        if 'Phone' not in self.ref_classes or 'Phone' not in self.dev_classes:
            self.add_result(TestResult("Phone класи", False, error="Класи не знайдені"))
            return
        
        ref_phone = self.ref_classes['Phone']
        dev_phone = self.dev_classes['Phone']
        
        test_cases = [
            "+380501234567",
            "380501234567", 
            "0501234567",
            "050 123 45 67"
        ]
        
        for test_case in test_cases:
            try:
                ref_result = ref_phone(test_case).value
                dev_result = dev_phone(test_case).value
                
                passed = ref_result == dev_result
                self.add_result(TestResult(
                    f"Phone('{test_case}')",
                    passed,
                    ref_result,
                    dev_result
                ))
            except Exception as e:
                self.add_result(TestResult(
                    f"Phone('{test_case}')",
                    False,
                    error=str(e)
                ))
    
    def validate_email_class(self):
        """Валідація класу Email."""
        if 'Email' not in self.ref_classes or 'Email' not in self.dev_classes:
            self.add_result(TestResult("Email класи", False, error="Класи не знайдені"))
            return
        
        ref_email = self.ref_classes['Email']
        dev_email = self.dev_classes['Email']
        
        test_cases = [
            "test@example.com",
            "TEST@EXAMPLE.COM",
            "user.name+tag@domain.co.uk"
        ]
        
        for test_case in test_cases:
            try:
                ref_result = ref_email(test_case).value
                dev_result = dev_email(test_case).value
                
                passed = ref_result == dev_result
                self.add_result(TestResult(
                    f"Email('{test_case}')",
                    passed,
                    ref_result,
                    dev_result
                ))
            except Exception as e:
                self.add_result(TestResult(
                    f"Email('{test_case}')",
                    False,
                    error=str(e)
                ))
    
    def validate_birthday_class(self):
        """Валідація класу Birthday."""
        if 'Birthday' not in self.ref_classes or 'Birthday' not in self.dev_classes:
            self.add_result(TestResult("Birthday класи", False, error="Класи не знайдені"))
            return
        
        ref_birthday = self.ref_classes['Birthday']
        dev_birthday = self.dev_classes['Birthday']
        
        test_cases = [
            "15.03.1990",
            "15-03-1990",
            "15/03/1990"
        ]
        
        for test_case in test_cases:
            try:
                ref_obj = ref_birthday(test_case)
                dev_obj = dev_birthday(test_case)
                
                # Порівняння значення
                ref_value = ref_obj.value
                dev_value = dev_obj.value
                
                passed = ref_value == dev_value
                self.add_result(TestResult(
                    f"Birthday('{test_case}').value",
                    passed,
                    ref_value,
                    dev_value
                ))
                
                # Порівняння to_date()
                if hasattr(ref_obj, 'to_date') and hasattr(dev_obj, 'to_date'):
                    ref_date = ref_obj.to_date()
                    dev_date = dev_obj.to_date()
                    
                    passed = ref_date == dev_date
                    self.add_result(TestResult(
                        f"Birthday('{test_case}').to_date()",
                        passed,
                        ref_date,
                        dev_date
                    ))
                    
            except Exception as e:
                self.add_result(TestResult(
                    f"Birthday('{test_case}')",
                    False,
                    error=str(e)
                ))
    
    def validate_address_class(self):
        """Валідація класу Address.""" 
        if 'Address' not in self.ref_classes or 'Address' not in self.dev_classes:
            self.add_result(TestResult("Address класи", False, error="Класи не знайдені"))
            return
        
        ref_address = self.ref_classes['Address']
        dev_address = self.dev_classes['Address']
        
        test_cases = [
            "   вул. Хрещатик, 1   ",
            "проспект Перемоги, 50"
        ]
        
        for test_case in test_cases:
            try:
                ref_result = ref_address(test_case).value
                dev_result = dev_address(test_case).value
                
                passed = ref_result == dev_result
                self.add_result(TestResult(
                    f"Address('{test_case}')",
                    passed,
                    ref_result,
                    dev_result
                ))
            except Exception as e:
                self.add_result(TestResult(
                    f"Address('{test_case}')",
                    False,
                    error=str(e)
                ))
    
    def validate_all(self):
        """Валідація всіх Field класів."""
        print("🔍 ВАЛІДАЦІЯ FIELD КЛАСІВ")
        print("=" * 70)
        
        self.validate_name_class()
        self.validate_phone_class()
        self.validate_email_class()
        self.validate_birthday_class()
        self.validate_address_class()

class ContactValidator(ComponentValidator):
    """Валідатор для класу Contact."""
    
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        
        # Імпорт еталонної реалізації
        try:
            from personal_assistant.models.contact import Contact
            from personal_assistant.models.field import Name, Phone, Email, Birthday, Address
            self.ref_contact = Contact
            self.ref_fields = {
                'Name': Name,
                'Phone': Phone, 
                'Email': Email,
                'Birthday': Birthday,
                'Address': Address
            }
        except ImportError:
            print("❌ Еталонна реалізація недоступна")
            self.ref_contact = None
            self.ref_fields = {}
        
        # Імпорт розробницької реалізації
        self.dev_contact = None
        self.dev_fields = {}
        try:
            # Імпорт Contact
            contact_path = project_root / "dev_implementation" / "models" / "contact.py"
            if contact_path.exists():
                spec = importlib.util.spec_from_file_location("dev_contact", contact_path)
                contact_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(contact_module)
                
                if hasattr(contact_module, 'Contact'):
                    self.dev_contact = contact_module.Contact
            
            # Імпорт Fields
            field_path = project_root / "dev_implementation" / "models" / "field.py"
            if field_path.exists():
                spec = importlib.util.spec_from_file_location("dev_field", field_path)
                field_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(field_module)
                
                for class_name in ['Name', 'Phone', 'Email', 'Birthday', 'Address']:
                    if hasattr(field_module, class_name):
                        self.dev_fields[class_name] = getattr(field_module, class_name)
                        
        except Exception as e:
            print(f"❌ Помилка імпорту: {e}")
    
    def validate_contact_creation(self):
        """Валідація створення контакту."""
        if not self.ref_contact or not self.dev_contact:
            self.add_result(TestResult("Contact створення", False, error="Класи не знайдені"))
            return
        
        try:
            ref_contact = self.ref_contact(self.ref_fields['Name']("Іван Петров"))
            dev_contact = self.dev_contact(self.dev_fields['Name']("Іван Петров"))
            
            # Порівняння структури
            ref_str = str(ref_contact)
            dev_str = str(dev_contact)
            
            # Базова перевірка що і там і там є ім'я
            ref_has_name = "Іван Петров" in ref_str
            dev_has_name = "Іван Петров" in dev_str
            
            passed = ref_has_name and dev_has_name
            self.add_result(TestResult(
                "Contact створення та __str__",
                passed,
                ref_str,
                dev_str
            ))
            
        except Exception as e:
            self.add_result(TestResult(
                "Contact створення",
                False,
                error=str(e)
            ))
    
    def validate_phone_operations(self):
        """Валідація операцій з телефонами."""
        if not self.ref_contact or not self.dev_contact:
            return
        
        try:
            ref_contact = self.ref_contact(self.ref_fields['Name']("Тест"))
            dev_contact = self.dev_contact(self.dev_fields['Name']("Тест"))
            
            # Додавання телефону
            ref_phone = self.ref_fields['Phone']("0501234567")
            dev_phone = self.dev_fields['Phone']("0501234567")
            
            ref_contact.add_phone(ref_phone)
            dev_contact.add_phone(dev_phone)
            
            ref_count = len(ref_contact.phones)
            dev_count = len(dev_contact.phones)
            
            passed = ref_count == dev_count == 1
            self.add_result(TestResult(
                "Contact add_phone",
                passed,
                ref_count,
                dev_count
            ))
            
        except Exception as e:
            self.add_result(TestResult(
                "Contact phone операції",
                False,
                error=str(e)
            ))
    
    def validate_serialization(self):
        """Валідація серіалізації."""
        if not self.ref_contact or not self.dev_contact:
            return
        
        try:
            # Створення повних контактів
            ref_contact = self.ref_contact(self.ref_fields['Name']("Тест"))
            dev_contact = self.dev_contact(self.dev_fields['Name']("Тест"))
            
            ref_contact.add_phone(self.ref_fields['Phone']("0501234567"))
            dev_contact.add_phone(self.dev_fields['Phone']("0501234567"))
            
            # Серіалізація
            if hasattr(ref_contact, 'to_dict') and hasattr(dev_contact, 'to_dict'):
                ref_dict = ref_contact.to_dict()
                dev_dict = dev_contact.to_dict()
                
                # Порівняння ключів
                ref_keys = set(ref_dict.keys())
                dev_keys = set(dev_dict.keys())
                
                passed = ref_keys == dev_keys
                self.add_result(TestResult(
                    "Contact to_dict ключі",
                    passed,
                    sorted(ref_keys),
                    sorted(dev_keys)
                ))
            else:
                self.add_result(TestResult(
                    "Contact to_dict метод",
                    False,
                    error="Метод to_dict відсутній"
                ))
                
        except Exception as e:
            self.add_result(TestResult(
                "Contact серіалізація",
                False,
                error=str(e)
            ))
    
    def validate_all(self):
        """Валідація всього класу Contact."""
        print("🔍 ВАЛІДАЦІЯ КЛАСУ CONTACT") 
        print("=" * 70)
        
        self.validate_contact_creation()
        self.validate_phone_operations()
        self.validate_serialization()

def main():
    parser = argparse.ArgumentParser(description='Валідація коду з еталоном')
    parser.add_argument('component', choices=['field', 'contact', 'all'], 
                       help='Компонент для валідації')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    
    args = parser.parse_args()
    
    print("🔍 ВАЛІДАТОР КОДУ")
    print("=" * 70)
    print(f"Валідація компонента: {args.component}")
    
    if args.component == 'field' or args.component == 'all':
        validator = FieldValidator(verbose=args.verbose)
        validator.validate_all()
        validator.print_results()
    
    if args.component == 'contact' or args.component == 'all':
        validator = ContactValidator(verbose=args.verbose)
        validator.validate_all()
        validator.print_results()

if __name__ == "__main__":
    main()