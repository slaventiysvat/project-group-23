#!/usr/bin/env python3
"""
🎯 QUICK TEST - Швидкі тести для перевірки функціональності

Цей інструмент дозволяє швидко протестувати окремі методи
або класи без запуску повного набору тестів.

Використання:
    python quick_test.py Name "іван петров"           # Тест класу Name
    python quick_test.py Phone "0501234567"           # Тест класу Phone
    python quick_test.py Email "TEST@EXAMPLE.COM"     # Тест класу Email
    python quick_test.py Birthday "15.03.1990"        # Тест класу Birthday
    python quick_test.py --interactive               # Інтерактивний режим
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Optional

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def import_dev_classes():
    """Імпорт розробницьких класів."""
    try:
        dev_path = project_root / "dev_implementation"
        if not dev_path.exists():
            return None, "Папка dev_implementation не знайдена"
        
        sys.path.insert(0, str(dev_path))
        
        import models.field as dev_field
        classes = {}
        
        for class_name in ['Field', 'Name', 'Phone', 'Email', 'Birthday', 'Address']:
            if hasattr(dev_field, class_name):
                classes[class_name] = getattr(dev_field, class_name)
        
        # Спроба імпорту Contact
        try:
            import models.contact as dev_contact
            if hasattr(dev_contact, 'Contact'):
                classes['Contact'] = dev_contact.Contact
        except ImportError:
            pass
        
        return classes, None
        
    except Exception as e:
        return None, str(e)

def import_reference_classes():
    """Імпорт еталонних класів."""
    try:
        from personal_assistant.models.field import Field, Name, Phone, Email, Birthday, Address
        from personal_assistant.models.contact import Contact
        
        return {
            'Field': Field,
            'Name': Name,
            'Phone': Phone,
            'Email': Email,
            'Birthday': Birthday,
            'Address': Address,
            'Contact': Contact
        }, None
        
    except ImportError as e:
        return None, str(e)

def test_class_method(class_obj: Any, method_name: str, *args, **kwargs) -> tuple[bool, Any, str]:
    """Тестування методу класу."""
    try:
        if method_name == "constructor":
            result = class_obj(*args, **kwargs)
            return True, result, ""
        else:
            instance = class_obj(*args, **kwargs)
            if hasattr(instance, method_name):
                method = getattr(instance, method_name)
                result = method()
                return True, result, ""
            else:
                return False, None, f"Метод {method_name} не знайдено"
    except Exception as e:
        return False, None, str(e)

def quick_test_field(class_name: str, test_value: str):
    """Швидкий тест Field класу."""
    print(f"🧪 ШВИДКИЙ ТЕСТ: {class_name}")
    print("=" * 50)
    
    # Імпорт класів
    dev_classes, dev_error = import_dev_classes()
    ref_classes, ref_error = import_reference_classes()
    
    if dev_error:
        print(f"❌ Розробницька реалізація: {dev_error}")
        return
    
    if ref_error:
        print(f"⚠️  Еталонна реалізація недоступна: {ref_error}")
        ref_classes = {}
    
    # Перевірка наявності класу
    if class_name not in dev_classes:
        print(f"❌ Клас {class_name} не знайдено в розробницькій реалізації")
        available = list(dev_classes.keys())
        print(f"💡 Доступні класи: {', '.join(available)}")
        return
    
    dev_class = dev_classes[class_name]
    ref_class = ref_classes.get(class_name)
    
    print(f"📋 Тестування: {class_name}('{test_value}')")
    
    # Тест розробницького класу
    print("\n🔧 РОЗРОБНИЦЬКА РЕАЛІЗАЦІЯ:")
    dev_success, dev_result, dev_error = test_class_method(dev_class, "constructor", test_value)
    
    if dev_success:
        print(f"✅ Створення: Успішно")
        print(f"📄 Значення: {dev_result.value}")
        print(f"📝 Строка: {str(dev_result)}")
        
        # Додаткові тести для спеціальних класів
        if class_name == "Birthday" and hasattr(dev_result, 'to_date'):
            try:
                date_obj = dev_result.to_date()
                print(f"📅 Дата: {date_obj}")
            except Exception as e:
                print(f"❌ to_date(): {e}")
        
    else:
        print(f"❌ Помилка: {dev_error}")
    
    # Порівняння з еталоном
    if ref_class:
        print("\n🎯 ПОРІВНЯННЯ З ЕТАЛОНОМ:")
        ref_success, ref_result, ref_error = test_class_method(ref_class, "constructor", test_value)
        
        if ref_success and dev_success:
            if dev_result.value == ref_result.value:
                print("✅ Значення співпадають")
            else:
                print("❌ Значення не співпадають:")
                print(f"   Еталон: '{ref_result.value}'")
                print(f"   Розробка: '{dev_result.value}'")
            
            if str(dev_result) == str(ref_result):
                print("✅ Строкові представлення співпадають")
            else:
                print("❌ Строкові представлення різні:")
                print(f"   Еталон: '{str(ref_result)}'")
                print(f"   Розробка: '{str(dev_result)}'")
        
        elif ref_success and not dev_success:
            print(f"❌ Еталон працює, розробка - ні")
            print(f"   Еталон: '{ref_result.value}'")
            
        elif not ref_success and dev_success:
            print(f"⚠️  Розробка працює, еталон - ні")
            
    else:
        print("⚠️  Еталон недоступний для порівняння")

def interactive_mode():
    """Інтерактивний режим тестування."""
    print("🎮 ІНТЕРАКТИВНИЙ РЕЖИМ ТЕСТУВАННЯ")
    print("=" * 60)
    print("Введіть 'exit' для виходу")
    
    # Імпорт класів
    dev_classes, dev_error = import_dev_classes()
    if dev_error:
        print(f"❌ Помилка: {dev_error}")
        return
    
    available_classes = list(dev_classes.keys())
    print(f"📚 Доступні класи: {', '.join(available_classes)}")
    
    while True:
        print("\n" + "-" * 40)
        class_name = input("🔤 Введіть ім'я класу: ").strip()
        
        if class_name.lower() == 'exit':
            break
        
        if class_name not in available_classes:
            print(f"❌ Клас '{class_name}' не знайдено")
            continue
        
        test_value = input(f"📝 Введіть тестове значення для {class_name}: ").strip()
        
        if not test_value:
            continue
        
        quick_test_field(class_name, test_value)

def test_multiple_values(class_name: str, values: list):
    """Тест класу з множинними значеннями."""
    print(f"🎯 МНОЖИННИЙ ТЕСТ: {class_name}")
    print("=" * 50)
    
    dev_classes, dev_error = import_dev_classes()
    if dev_error:
        print(f"❌ {dev_error}")
        return
    
    if class_name not in dev_classes:
        print(f"❌ Клас {class_name} не знайдено")
        return
    
    dev_class = dev_classes[class_name]
    
    for i, value in enumerate(values, 1):
        print(f"\n📋 Тест {i}/{len(values)}: '{value}'")
        
        success, result, error = test_class_method(dev_class, "constructor", value)
        
        if success:
            print(f"✅ Результат: '{result.value}'")
        else:
            print(f"❌ Помилка: {error}")

def main():
    parser = argparse.ArgumentParser(description='Швидкі тести класів')
    parser.add_argument('class_name', nargs='?', help='Ім\'я класу для тестування')
    parser.add_argument('test_value', nargs='?', help='Тестове значення')
    parser.add_argument('--interactive', '-i', action='store_true', help='Інтерактивний режим')
    parser.add_argument('--multiple', '-m', action='store_true', help='Тест з множинними значеннями')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.multiple and args.class_name:
        # Предефінірані тестові значення
        test_sets = {
            'Name': ['іван петров', 'mary o\'connor', 'АННА-МАРІЯ', 'jean-claude'],
            'Phone': ['+380501234567', '380501234567', '0501234567', '050 123 45 67'],
            'Email': ['test@example.com', 'TEST@EXAMPLE.COM', 'user+tag@domain.co.uk'],
            'Birthday': ['15.03.1990', '15-03-1990', '15/03/1990', '01.01.2000'],
            'Address': ['вул. Хрещатик, 1', 'проспект Перемоги, 50', 'Khreshchatyk Street, 1']
        }
        
        values = test_sets.get(args.class_name, [args.test_value or 'test'])
        test_multiple_values(args.class_name, values)
        
    elif args.class_name and args.test_value:
        quick_test_field(args.class_name, args.test_value)
    else:
        parser.print_help()
        print("\n💡 Приклади використання:")
        print("python quick_test.py Name 'іван петров'")
        print("python quick_test.py Phone '0501234567'")
        print("python quick_test.py --interactive")
        print("python quick_test.py Name --multiple")

if __name__ == "__main__":
    main()