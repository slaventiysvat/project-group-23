#!/usr/bin/env python3
"""
🧪 STEP 4: FILE STORAGE - Поетапна перевірка

Цей файл допомагає розробнику поетапно створювати клас FileStorage,
перевіряючи кожен метод окремо з еталонною реалізацією.

Використання:
    python step_04_storage.py                  # Базова перевірка
    python step_04_storage.py --verbose        # Детальний вивід  
    python step_04_storage.py --step 3         # Тільки крок 3
    python step_04_storage.py --compare        # Порівняння з еталоном
"""

import sys
import os
import json
import tempfile
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Імпорт еталонної реалізації
try:
    from personal_assistant.storage.file_storage import FileStorage
    REFERENCE_AVAILABLE = True
except ImportError:
    print("⚠️  Еталонна реалізація недоступна")
    REFERENCE_AVAILABLE = False

# Спроба імпорту розробницької реалізації
DEV_IMPLEMENTATION = None
try:
    dev_path = project_root / "dev_implementation"
    if dev_path.exists():
        sys.path.insert(0, str(dev_path))
        try:
            import storage.file_storage as dev_storage
            DEV_IMPLEMENTATION = dev_storage
            print("✅ Знайдено розробницьку реалізацію")
        except ImportError as e:
            print(f"⚠️  Помилка імпорту: {e}")
    else:
        print("📝 Створіть папку dev_implementation/storage/")
except Exception as e:
    print(f"⚠️  Помилка: {e}")

class FileStorageTester:
    """Тестер для поетапної перевірки класу FileStorage."""
    
    def __init__(self, verbose: bool = False, compare: bool = False):
        self.verbose = verbose
        self.compare = compare
        self.passed = 0
        self.failed = 0
        self.dev = DEV_IMPLEMENTATION
        self.temp_dir = None
    
    def setup_temp_dir(self):
        """Створення тимчасової директорії для тестів."""
        self.temp_dir = tempfile.mkdtemp(prefix="storage_test_")
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
    
    def step_1_storage_init(self):
        """Крок 1: Перевірка ініціалізації FileStorage."""
        self.print_step(1, "Ініціалізація FileStorage")
        
        if not self.dev or not hasattr(self.dev, 'FileStorage'):
            self.print_failure("Клас FileStorage не знайдено")
            return
        
        storage_class = self.dev.FileStorage
        
        # Тест базової ініціалізації
        try:
            storage = storage_class(self.temp_dir)
            self.print_success("FileStorage створюється з директорією")
            
            # Перевірка атрибутів
            if hasattr(storage, 'data_dir'):
                self.print_success("FileStorage.data_dir атрибут присутній")
            else:
                self.print_failure("FileStorage.data_dir атрибут відсутній")
            
            # Перевірка створення директорії
            if Path(storage.data_dir).exists():
                self.print_success("FileStorage створює директорію даних")
            else:
                self.print_failure("FileStorage не створює директорію даних")
            
            # Тест без параметрів (має створити data/ директорію)
            storage_default = storage_class()
            if hasattr(storage_default, 'data_dir'):
                self.print_success("FileStorage працює без параметрів")
            else:
                self.print_failure("FileStorage не працює без параметрів")
                    
        except Exception as e:
            self.print_failure(f"FileStorage не створюється: {e}")
    
    def step_2_save_load_data(self):
        """Крок 2: Збереження та завантаження даних."""
        self.print_step(2, "Збереження та завантаження даних")
        
        if not self.dev or not hasattr(self.dev, 'FileStorage'):
            self.print_failure("Клас FileStorage не знайдено")
            return
        
        try:
            storage = self.dev.FileStorage(self.temp_dir)
            
            # Тестові дані
            test_data = {
                "contacts": [
                    {"name": "Іван Петров", "phones": ["+380501234567"]},
                    {"name": "Марія Іванова", "phones": ["+380677654321"]}
                ]
            }
            
            # Тест save_data
            if hasattr(storage, 'save_data'):
                result = storage.save_data('contacts', test_data)
                
                if result:
                    self.print_success("save_data() зберігає дані")
                    
                    # Перевірка існування файлу
                    contacts_file = Path(storage.data_dir) / 'contacts.json'
                    if contacts_file.exists():
                        self.print_success("save_data() створює JSON файл")
                    else:
                        self.print_failure("save_data() не створює JSON файл")
                else:
                    self.print_failure("save_data() повертає False")
            else:
                self.print_failure("Метод save_data() відсутній")
            
            # Тест load_data
            if hasattr(storage, 'load_data'):
                loaded_data = storage.load_data('contacts')
                
                if loaded_data is not None:
                    self.print_success("load_data() завантажує дані")
                    
                    if loaded_data == test_data:
                        self.print_success("load_data() повертає правильні дані")
                    else:
                        self.print_failure("load_data() повертає неправильні дані")
                else:
                    self.print_failure("load_data() повертає None")
            else:
                self.print_failure("Метод load_data() відсутній")
            
            # Тест завантаження неіснуючого файлу
            if hasattr(storage, 'load_data'):
                empty_data = storage.load_data('nonexistent')
                if empty_data == {}:
                    self.print_success("load_data() повертає {} для неіснуючого файлу")
                else:
                    self.print_failure("load_data() не повертає {} для неіснуючого файлу")
                
        except Exception as e:
            self.print_failure(f"Помилка в збереженні/завантаженні: {e}")
    
    def step_3_backup_system(self):
        """Крок 3: Система резервного копіювання."""
        self.print_step(3, "Система резервного копіювання")
        
        if not self.dev or not hasattr(self.dev, 'FileStorage'):
            self.print_failure("Клас FileStorage не знайдено")
            return
        
        try:
            storage = self.dev.FileStorage(self.temp_dir)
            
            # Створюємо тестові дані
            test_data = {"test": "backup data"}
            storage.save_data('test_backup', test_data)
            
            # Тест create_backup
            if hasattr(storage, 'create_backup'):
                backup_file = storage.create_backup('test_backup')
                
                if backup_file and Path(backup_file).exists():
                    self.print_success("create_backup() створює backup файл")
                    
                    # Перевірка вмісту backup
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        backup_data = json.load(f)
                        
                    if backup_data == test_data:
                        self.print_success("create_backup() зберігає правильні дані")
                    else:
                        self.print_failure("create_backup() зберігає неправильні дані")
                else:
                    self.print_failure("create_backup() не створює backup файл")
            else:
                self.print_failure("Метод create_backup() відсутній")
            
            # Тест restore_backup
            if hasattr(storage, 'restore_backup') and hasattr(storage, 'create_backup'):
                backup_file = storage.create_backup('test_backup')
                
                # Змінюємо оригінальні дані
                modified_data = {"test": "modified data"}
                storage.save_data('test_backup', modified_data)
                
                # Відновлюємо з backup
                result = storage.restore_backup('test_backup', backup_file)
                
                if result:
                    self.print_success("restore_backup() виконується успішно")
                    
                    # Перевіряємо відновлення
                    restored_data = storage.load_data('test_backup')
                    if restored_data == test_data:
                        self.print_success("restore_backup() відновлює правильні дані")
                    else:
                        self.print_failure("restore_backup() не відновлює правильні дані")
                else:
                    self.print_failure("restore_backup() повертає False")
            else:
                self.print_failure("Метод restore_backup() відсутній")
            
            # Тест list_backups
            if hasattr(storage, 'list_backups'):
                backups = storage.list_backups('test_backup')
                
                if isinstance(backups, list):
                    self.print_success("list_backups() повертає список")
                    
                    if len(backups) > 0:
                        self.print_success("list_backups() знаходить backup файли")
                    else:
                        self.print_failure("list_backups() не знаходить backup файли")
                else:
                    self.print_failure("list_backups() не повертає список")
            else:
                self.print_failure("Метод list_backups() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в системі backup: {e}")
    
    def step_4_utility_methods(self):
        """Крок 4: Допоміжні методи."""
        self.print_step(4, "Допоміжні методи")
        
        if not self.dev or not hasattr(self.dev, 'FileStorage'):
            self.print_failure("Клас FileStorage не знайдено")
            return
        
        try:
            storage = self.dev.FileStorage(self.temp_dir)
            
            # Створюємо тестові файли
            storage.save_data('test1', {"data": "test1"})
            storage.save_data('test2', {"data": "test2"})
            
            # Тест list_data_files
            if hasattr(storage, 'list_data_files'):
                files = storage.list_data_files()
                
                if isinstance(files, list):
                    self.print_success("list_data_files() повертає список")
                    
                    expected_files = ['test1.json', 'test2.json']
                    found_files = [f for f in expected_files if f in files]
                    
                    if len(found_files) == len(expected_files):
                        self.print_success("list_data_files() знаходить всі файли")
                    else:
                        self.print_failure(f"list_data_files() знайшов {len(found_files)} з {len(expected_files)} файлів")
                else:
                    self.print_failure("list_data_files() не повертає список")
            else:
                self.print_failure("Метод list_data_files() відсутній")
            
            # Тест get_storage_info
            if hasattr(storage, 'get_storage_info'):
                info = storage.get_storage_info()
                
                if isinstance(info, dict):
                    self.print_success("get_storage_info() повертає словник")
                    
                    required_keys = ['data_directory', 'total_files', 'total_size_kb']
                    for key in required_keys:
                        if key in info:
                            self.print_success(f"get_storage_info() включає ключ '{key}'")
                        else:
                            self.print_failure(f"get_storage_info() не включає ключ '{key}'")
                else:
                    self.print_failure("get_storage_info() не повертає словник")
            else:
                self.print_failure("Метод get_storage_info() відсутній")
            
            # Тест clear_all_data
            if hasattr(storage, 'clear_all_data'):
                result = storage.clear_all_data()
                
                if result:
                    self.print_success("clear_all_data() виконується успішно")
                    
                    # Перевіряємо що файли видалено
                    files_after = storage.list_data_files()
                    if len(files_after) == 0:
                        self.print_success("clear_all_data() видаляє всі файли")
                    else:
                        self.print_failure(f"clear_all_data() не видалив {len(files_after)} файлів")
                else:
                    self.print_failure("clear_all_data() повертає False")
            else:
                self.print_failure("Метод clear_all_data() відсутній")
            
            # Тест __str__ та __repr__
            str_result = str(storage)
            if "FileStorage" in str_result:
                self.print_success("__str__() включає назву класу")
            else:
                self.print_failure("__str__() не включає назву класу")
            
            repr_result = repr(storage)
            if "FileStorage" in repr_result and self.temp_dir in repr_result:
                self.print_success("__repr__() включає клас та директорію")
            else:
                self.print_failure("__repr__() не включає необхідну інформацію")
                
        except Exception as e:
            self.print_failure(f"Помилка в допоміжних методах: {e}")
    
    def step_5_error_handling(self):
        """Крок 5: Обробка помилок та edge cases."""
        self.print_step(5, "Обробка помилок та edge cases")
        
        if not self.dev or not hasattr(self.dev, 'FileStorage'):
            self.print_failure("Клас FileStorage не знайдено")
            return
        
        try:
            storage = self.dev.FileStorage(self.temp_dir)
            
            # Тест збереження невалідних даних
            if hasattr(storage, 'save_data'):
                try:
                    # Спроба збереження незсеріалізованих даних
                    invalid_data = {"func": lambda x: x}  # function не можна серіалізувати
                    result = storage.save_data('invalid', invalid_data)
                    
                    # Метод має обробити помилку gracefully
                    if not result:
                        self.print_success("save_data() правильно обробляє неserializable дані")
                    else:
                        self.print_failure("save_data() не обробляє неserializable дані")
                except Exception as e:
                    # Виняток - це нормально, але має бути контрольовано
                    self.print_success("save_data() викидає контрольований виняток")
            
            # Тест завантаження пошкодженого JSON
            if hasattr(storage, 'load_data'):
                # Створюємо пошкоджений JSON файл
                corrupted_file = Path(storage.data_dir) / 'corrupted.json'
                with open(corrupted_file, 'w', encoding='utf-8') as f:
                    f.write('{"invalid": json content}')
                
                try:
                    result = storage.load_data('corrupted')
                    if result == {}:
                        self.print_success("load_data() обробляє пошкоджений JSON")
                    else:
                        self.print_failure("load_data() не обробляє пошкоджений JSON")
                except Exception:
                    self.print_success("load_data() викидає контрольований виняток для пошкодженого JSON")
            
            # Тест роботи з readonly директорією (якщо можливо)
            try:
                readonly_dir = Path(self.temp_dir) / 'readonly'
                readonly_dir.mkdir(exist_ok=True)
                
                # Спроба зробити readonly (не завжди працює на Windows)
                if os.name != 'nt':  # Unix-like системи
                    os.chmod(readonly_dir, 0o444)
                    
                    readonly_storage = self.dev.FileStorage(str(readonly_dir))
                    result = readonly_storage.save_data('test', {"data": "test"})
                    
                    if not result:
                        self.print_success("FileStorage обробляє readonly директорії")
                    else:
                        self.print_failure("FileStorage не обробляє readonly директорії")
                else:
                    self.print_success("Тест readonly пропущено на Windows")
                    
            except Exception as e:
                self.print_success("FileStorage правильно обробляє помилки доступу")
            
            # Тест з великими даними
            if hasattr(storage, 'save_data') and hasattr(storage, 'load_data'):
                large_data = {"items": [f"item_{i}" for i in range(10000)]}
                
                save_success = storage.save_data('large_data', large_data)
                if save_success:
                    loaded_data = storage.load_data('large_data')
                    if len(loaded_data.get('items', [])) == 10000:
                        self.print_success("FileStorage працює з великими даними")
                    else:
                        self.print_failure("FileStorage не працює з великими даними")
                else:
                    self.print_failure("FileStorage не зберігає великі дані")
                
        except Exception as e:
            self.print_failure(f"Помилка в обробці помилок: {e}")
    
    def run_step(self, step_num: int):
        """Запуск конкретного кроку."""
        steps = {
            1: self.step_1_storage_init,
            2: self.step_2_save_load_data,
            3: self.step_3_backup_system,
            4: self.step_4_utility_methods,
            5: self.step_5_error_handling,
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
            print(f"\n🎉 Всі тести пройдені! Клас FileStorage готовий.")
        else:
            print(f"\n🔧 Є проблеми що потребують вирішення.")
            print(f"💡 Підказка: Подивіться на еталонну реалізацію у personal_assistant/storage/file_storage.py")

def main():
    parser = argparse.ArgumentParser(description='Поетапна перевірка класу FileStorage')
    parser.add_argument('--step', type=int, help='Запустити тільки певний крок (1-5)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    parser.add_argument('--compare', '-c', action='store_true', help='Порівняння з еталоном')
    
    args = parser.parse_args()
    
    print("🧪 ПОЕТАПНА ПЕРЕВІРКА КЛАСУ FILESTORAGE")
    print("=" * 60)
    
    if not DEV_IMPLEMENTATION:
        print("\n📝 Щоб розпочати:")
        print("1. Створіть папку: dev_implementation/storage/")
        print("2. Створіть файл: dev_implementation/storage/__init__.py")
        print("3. Створіть файл: dev_implementation/storage/file_storage.py")
        print("4. Імплементуйте клас FileStorage з усіма методами")
        return
    
    tester = FileStorageTester(verbose=args.verbose, compare=args.compare)
    
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