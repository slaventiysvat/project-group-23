#!/usr/bin/env python3
"""
🧪 STEP 5: CONTACT MANAGER - Поетапна перевірка

Цей файл допомагає розробнику поетапно створювати клас ContactManager,
перевіряючи кожен метод окремо з еталонною реалізацією.

Використання:
    python step_05_contact_manager.py          # Базова перевірка
    python step_05_contact_manager.py --verbose # Детальний вивід  
    python step_05_contact_manager.py --step 2  # Тільки крок 2
    python step_05_contact_manager.py --compare # Порівняння з еталоном
"""

import sys
import os
import tempfile
import shutil
import argparse
from pathlib import Path
from datetime import datetime, date

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Імпорт еталонної реалізації
try:
    from personal_assistant.managers.contact_manager import ContactManager
    from personal_assistant.models.contact import Contact
    from personal_assistant.models.field import Name, Phone, Email, Birthday, Address
    from personal_assistant.storage.file_storage import FileStorage
    REFERENCE_AVAILABLE = True
except ImportError:
    print("⚠️  Еталонна реалізація недоступна")
    REFERENCE_AVAILABLE = False

# Спроба імпорту розробницької реалізації
DEV_IMPLEMENTATION = None
DEV_MODELS = None
DEV_STORAGE = None
try:
    dev_path = project_root / "dev_implementation"
    if dev_path.exists():
        sys.path.insert(0, str(dev_path))
        try:
            import managers.contact_manager as dev_manager
            import models.contact as dev_contact
            import models.field as dev_field
            import storage.file_storage as dev_storage
            
            DEV_IMPLEMENTATION = dev_manager
            DEV_MODELS = {
                'Contact': getattr(dev_contact, 'Contact', None),
                'Name': getattr(dev_field, 'Name', None),
                'Phone': getattr(dev_field, 'Phone', None),
                'Email': getattr(dev_field, 'Email', None),
                'Birthday': getattr(dev_field, 'Birthday', None),
                'Address': getattr(dev_field, 'Address', None)
            }
            DEV_STORAGE = getattr(dev_storage, 'FileStorage', None)
            print("✅ Знайдено розробницьку реалізацію")
        except ImportError as e:
            print(f"⚠️  Помилка імпорту: {e}")
    else:
        print("📝 Створіть папку dev_implementation/managers/")
except Exception as e:
    print(f"⚠️  Помилка: {e}")

class ContactManagerTester:
    """Тестер для поетапної перевірки класу ContactManager."""
    
    def __init__(self, verbose: bool = False, compare: bool = False):
        self.verbose = verbose
        self.compare = compare
        self.passed = 0
        self.failed = 0
        self.dev = DEV_IMPLEMENTATION
        self.dev_models = DEV_MODELS
        self.dev_storage = DEV_STORAGE
        self.temp_dir = None
    
    def setup_temp_dir(self):
        """Створення тимчасової директорії для тестів."""
        self.temp_dir = tempfile.mkdtemp(prefix="manager_test_")
        if self.verbose:
            print(f"📁 Тимчасова папка: {self.temp_dir}")
    
    def cleanup_temp_dir(self):
        """Очищення тимчасової директорії."""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            if self.verbose:
                print(f"🗑️  Очищено тимчасову папку")
    
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
    
    def create_test_contact(self):
        """Створення тестового контакту."""
        if not self.dev_models or not all(self.dev_models.values()):
            return None
        
        try:
            name = self.dev_models['Name']("Іван Петров")
            contact = self.dev_models['Contact'](name)
            contact.add_phone(self.dev_models['Phone']("0501234567"))
            contact.email = self.dev_models['Email']("ivan@test.com")
            contact.add_birthday(self.dev_models['Birthday']("15.03.1990"))
            return contact
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Не вдалося створити тестовий контакт: {e}")
            return None
    
    def step_1_manager_init(self):
        """Крок 1: Перевірка ініціалізації ContactManager."""
        self.print_step(1, "Ініціалізація ContactManager")
        
        if not self.dev or not hasattr(self.dev, 'ContactManager'):
            self.print_failure("Клас ContactManager не знайдено")
            return
        
        if not self.dev_storage:
            self.print_failure("FileStorage не знайдено", 
                             "Спочатку реалізуйте FileStorage клас")
            return
        
        manager_class = self.dev.ContactManager
        
        # Тест базової ініціалізації
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = manager_class(storage)
            self.print_success("ContactManager створюється з FileStorage")
            
            # Перевірка атрибутів
            if hasattr(manager, 'storage'):
                self.print_success("ContactManager.storage атрибут присутній")
            else:
                self.print_failure("ContactManager.storage атрибут відсутній")
            
            if hasattr(manager, '_contacts'):
                if isinstance(manager._contacts, list):
                    self.print_success("ContactManager._contacts є списком")
                else:
                    self.print_failure("ContactManager._contacts не є списком")
            else:
                self.print_failure("ContactManager._contacts атрибут відсутній")
            
            # Перевірка автозавантаження
            if hasattr(manager, 'load_contacts'):
                self.print_success("ContactManager має метод load_contacts")
            else:
                self.print_failure("ContactManager.load_contacts метод відсутній")
                    
        except Exception as e:
            self.print_failure(f"ContactManager не створюється: {e}")
    
    def step_2_add_find_contacts(self):
        """Крок 2: Додавання та пошук контактів."""
        self.print_step(2, "Додавання та пошук контактів")
        
        if not self.dev or not self.dev_storage:
            self.print_failure("Класи не знайдені")
            return
        
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = self.dev.ContactManager(storage)
            
            test_contact = self.create_test_contact()
            if not test_contact:
                self.print_failure("Не вдалося створити тестовий контакт")
                return
            
            # Тест add_contact
            if hasattr(manager, 'add_contact'):
                result = manager.add_contact(test_contact)
                
                if result:
                    self.print_success("add_contact() додає контакт")
                    
                    if len(manager._contacts) == 1:
                        self.print_success("add_contact() додає до списку _contacts")
                    else:
                        self.print_failure("add_contact() не додає до списку _contacts")
                else:
                    self.print_failure("add_contact() повертає False")
                
                # Тест дублікатів
                result2 = manager.add_contact(test_contact)
                if not result2:
                    self.print_success("add_contact() запобігає дублікатам")
                else:
                    self.print_failure("add_contact() не запобігає дублікатам")
            else:
                self.print_failure("Метод add_contact() відсутній")
            
            # Тест find_contact
            if hasattr(manager, 'find_contact'):
                found_contact = manager.find_contact("Іван Петров")
                
                if found_contact:
                    self.print_success("find_contact() знаходить контакт за ім'ям")
                    
                    if found_contact.name.value == "Іван Петров":
                        self.print_success("find_contact() повертає правильний контакт")
                    else:
                        self.print_failure("find_contact() повертає неправильний контакт")
                else:
                    self.print_failure("find_contact() не знаходить існуючий контакт")
                
                # Пошук неіснуючого контакту
                not_found = manager.find_contact("Неіснуючий")
                if not not_found:
                    self.print_success("find_contact() повертає None для неіснуючого контакту")
                else:
                    self.print_failure("find_contact() знаходить неіснуючий контакт")
            else:
                self.print_failure("Метод find_contact() відсутній")
            
            # Тест get_all_contacts
            if hasattr(manager, 'get_all_contacts'):
                all_contacts = manager.get_all_contacts()
                
                if isinstance(all_contacts, list):
                    self.print_success("get_all_contacts() повертає список")
                    
                    if len(all_contacts) == 1:
                        self.print_success("get_all_contacts() повертає правильну кількість")
                    else:
                        self.print_failure(f"get_all_contacts() повертає {len(all_contacts)} контактів замість 1")
                else:
                    self.print_failure("get_all_contacts() не повертає список")
            else:
                self.print_failure("Метод get_all_contacts() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в додаванні/пошуку контактів: {e}")
    
    def step_3_contact_operations(self):
        """Крок 3: Операції з контактами."""
        self.print_step(3, "Операції з контактами")
        
        if not self.dev or not self.dev_storage:
            self.print_failure("Класи не знайдені")
            return
        
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = self.dev.ContactManager(storage)
            
            # Додаємо тестові контакти
            contact1 = self.create_test_contact()
            contact2_name = self.dev_models['Name']("Марія Іванова")
            contact2 = self.dev_models['Contact'](contact2_name)
            contact2.add_phone(self.dev_models['Phone']("0677654321"))
            
            manager.add_contact(contact1)
            manager.add_contact(contact2)
            
            # Тест remove_contact
            if hasattr(manager, 'remove_contact'):
                result = manager.remove_contact("Марія Іванова")
                
                if result:
                    self.print_success("remove_contact() видаляє контакт")
                    
                    if len(manager._contacts) == 1:
                        self.print_success("remove_contact() видаляє зі списку")
                    else:
                        self.print_failure("remove_contact() не видаляє зі списку")
                else:
                    self.print_failure("remove_contact() повертає False")
                
                # Спроба видалення неіснуючого
                result2 = manager.remove_contact("Неіснуючий")
                if not result2:
                    self.print_success("remove_contact() обробляє неіснуючий контакт")
                else:
                    self.print_failure("remove_contact() неправильно обробляє неіснуючий контакт")
            else:
                self.print_failure("Метод remove_contact() відсутній")
            
            # Тест search_contacts
            if hasattr(manager, 'search_contacts'):
                results = manager.search_contacts("Іван")
                
                if isinstance(results, list):
                    self.print_success("search_contacts() повертає список")
                    
                    if len(results) == 1:
                        self.print_success("search_contacts() знаходить контакти за ім'ям")
                    else:
                        self.print_failure(f"search_contacts() знайшов {len(results)} контактів замість 1")
                else:
                    self.print_failure("search_contacts() не повертає список")
                
                # Пошук за телефоном
                phone_results = manager.search_contacts("0501234567")
                if len(phone_results) >= 1:
                    self.print_success("search_contacts() знаходить контакти за телефоном")
                else:
                    self.print_failure("search_contacts() не знаходить контакти за телефоном")
                
                # Пошук за email
                email_results = manager.search_contacts("ivan@test.com")
                if len(email_results) >= 1:
                    self.print_success("search_contacts() знаходить контакти за email")
                else:
                    self.print_failure("search_contacts() не знаходить контакти за email")
            else:
                self.print_failure("Метод search_contacts() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в операціях з контактами: {e}")
    
    def step_4_birthday_features(self):
        """Крок 4: Функції днів народження."""
        self.print_step(4, "Функції днів народження")
        
        if not self.dev or not self.dev_storage:
            self.print_failure("Класи не знайдені")
            return
        
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = self.dev.ContactManager(storage)
            
            # Створюємо контакт з днем народження
            contact = self.create_test_contact()
            manager.add_contact(contact)
            
            # Створюємо контакт з близьким днем народження
            today = date.today()
            tomorrow = today.replace(day=today.day + 1) if today.day < 28 else today.replace(month=today.month + 1, day=1)
            
            close_birthday_contact = self.dev_models['Contact'](self.dev_models['Name']("Близький ДН"))
            close_birthday_contact.add_birthday(self.dev_models['Birthday'](f"{tomorrow.day:02d}.{tomorrow.month:02d}.1990"))
            manager.add_contact(close_birthday_contact)
            
            # Тест get_upcoming_birthdays
            if hasattr(manager, 'get_upcoming_birthdays'):
                upcoming = manager.get_upcoming_birthdays(7)  # 7 днів
                
                if isinstance(upcoming, list):
                    self.print_success("get_upcoming_birthdays() повертає список")
                    
                    # Має знайти контакт з близьким днем народження
                    found_close = any(contact.name.value == "Близький ДН" for contact in upcoming)
                    if found_close:
                        self.print_success("get_upcoming_birthdays() знаходить близькі дні народження")
                    else:
                        self.print_failure("get_upcoming_birthdays() не знаходить близькі дні народження")
                else:
                    self.print_failure("get_upcoming_birthdays() не повертає список")
            else:
                self.print_failure("Метод get_upcoming_birthdays() відсутній")
            
            # Тест get_contacts_by_birthday
            if hasattr(manager, 'get_contacts_by_birthday'):
                birthday_contacts = manager.get_contacts_by_birthday(f"{tomorrow.day:02d}.{tomorrow.month:02d}")
                
                if isinstance(birthday_contacts, list):
                    self.print_success("get_contacts_by_birthday() повертає список")
                    
                    if len(birthday_contacts) >= 1:
                        self.print_success("get_contacts_by_birthday() знаходить контакти за датою")
                    else:
                        self.print_failure("get_contacts_by_birthday() не знаходить контакти за датою")
                else:
                    self.print_failure("get_contacts_by_birthday() не повертає список")
            else:
                self.print_failure("Метод get_contacts_by_birthday() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в функціях днів народження: {e}")
    
    def step_5_data_persistence(self):
        """Крок 5: Збереження та завантаження даних."""
        self.print_step(5, "Збереження та завантаження даних")
        
        if not self.dev or not self.dev_storage:
            self.print_failure("Класи не знайдені")
            return
        
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = self.dev.ContactManager(storage)
            
            # Додаємо тестовий контакт
            contact = self.create_test_contact()
            manager.add_contact(contact)
            
            # Тест save_contacts
            if hasattr(manager, 'save_contacts'):
                result = manager.save_contacts()
                
                if result:
                    self.print_success("save_contacts() зберігає дані")
                else:
                    self.print_failure("save_contacts() повертає False")
            else:
                self.print_failure("Метод save_contacts() відсутній")
            
            # Тест load_contacts
            if hasattr(manager, 'load_contacts'):
                # Створюємо новий менеджер для тестування завантаження
                new_manager = self.dev.ContactManager(storage)
                
                if len(new_manager._contacts) >= 1:
                    self.print_success("load_contacts() завантажує дані при ініціалізації")
                    
                    loaded_contact = new_manager.find_contact("Іван Петров")
                    if loaded_contact:
                        self.print_success("load_contacts() правильно відновлює контакти")
                    else:
                        self.print_failure("load_contacts() не відновлює контакти правильно")
                else:
                    self.print_failure("load_contacts() не завантажує дані")
            else:
                self.print_failure("Метод load_contacts() відсутній")
            
            # Тест get_statistics
            if hasattr(manager, 'get_statistics'):
                stats = manager.get_statistics()
                
                if isinstance(stats, dict):
                    self.print_success("get_statistics() повертає словник")
                    
                    expected_keys = ['total_contacts', 'with_phones', 'with_emails', 'with_birthdays', 'with_addresses']
                    for key in expected_keys:
                        if key in stats:
                            self.print_success(f"get_statistics() включає ключ '{key}'")
                        else:
                            self.print_failure(f"get_statistics() не включає ключ '{key}'")
                else:
                    self.print_failure("get_statistics() не повертає словник")
            else:
                self.print_failure("Метод get_statistics() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в збереженні/завантаженні: {e}")
    
    def run_step(self, step_num: int):
        """Запуск конкретного кроку."""
        steps = {
            1: self.step_1_manager_init,
            2: self.step_2_add_find_contacts,
            3: self.step_3_contact_operations,
            4: self.step_4_birthday_features,
            5: self.step_5_data_persistence,
        }
        
        if step_num in steps:
            steps[step_num]()
        else:
            print(f"❌ Крок {step_num} не існує. Доступні кроки: 1-5")
    
    def run_all_steps(self):
        """Запуск всіх кроків."""
        self.setup_temp_dir()
        try:
            for i in range(1, 6):
                self.run_step(i)
        finally:
            self.cleanup_temp_dir()
    
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
            print(f"\n🎉 Всі тести пройдені! Клас ContactManager готовий.")
        else:
            print(f"\n🔧 Є проблеми що потребують вирішення.")
            print(f"💡 Підказка: Подивіться на еталонну реалізацію у personal_assistant/managers/contact_manager.py")

def main():
    parser = argparse.ArgumentParser(description='Поетапна перевірка класу ContactManager')
    parser.add_argument('--step', type=int, help='Запустити тільки певний крок (1-5)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    parser.add_argument('--compare', '-c', action='store_true', help='Порівняння з еталоном')
    
    args = parser.parse_args()
    
    print("🧪 ПОЕТАПНА ПЕРЕВІРКА КЛАСУ CONTACTMANAGER")
    print("=" * 60)
    
    if not DEV_IMPLEMENTATION:
        print("\n📝 Щоб розпочати:")
        print("1. Завершіть реалізацію Contact та FileStorage класів")
        print("2. Створіть папку: dev_implementation/managers/")
        print("3. Створіть файл: dev_implementation/managers/__init__.py")
        print("4. Створіть файл: dev_implementation/managers/contact_manager.py")
        print("5. Імплементуйте клас ContactManager з усіма методами")
        return
    
    tester = ContactManagerTester(verbose=args.verbose, compare=args.compare)
    
    if args.step:
        tester.setup_temp_dir()
        try:
            tester.run_step(args.step)
        finally:
            tester.cleanup_temp_dir()
    else:
        tester.run_all_steps()
    
    tester.show_summary()

if __name__ == "__main__":
    main()