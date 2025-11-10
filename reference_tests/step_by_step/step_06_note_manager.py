#!/usr/bin/env python3
"""
🧪 STEP 6: NOTE MANAGER - Поетапна перевірка

Цей файл допомагає розробнику поетапно створювати клас NoteManager,
перевіряючи кожен метод окремо з еталонною реалізацією.

Використання:
    python step_06_note_manager.py             # Базова перевірка
    python step_06_note_manager.py --verbose   # Детальний вивід  
    python step_06_note_manager.py --step 3    # Тільки крок 3
    python step_06_note_manager.py --compare   # Порівняння з еталоном
"""

import sys
import os
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
    from personal_assistant.managers.note_manager import NoteManager
    from personal_assistant.models.note import Note
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
            import managers.note_manager as dev_manager
            import models.note as dev_note
            import storage.file_storage as dev_storage
            
            DEV_IMPLEMENTATION = dev_manager
            DEV_MODELS = {'Note': getattr(dev_note, 'Note', None)}
            DEV_STORAGE = getattr(dev_storage, 'FileStorage', None)
            print("✅ Знайдено розробницьку реалізацію")
        except ImportError as e:
            print(f"⚠️  Помилка імпорту: {e}")
    else:
        print("📝 Створіть папку dev_implementation/managers/")
except Exception as e:
    print(f"⚠️  Помилка: {e}")

class NoteManagerTester:
    """Тестер для поетапної перевірки класу NoteManager."""
    
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
        self.temp_dir = tempfile.mkdtemp(prefix="note_manager_test_")
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
    
    def create_test_note(self, title: str = "Тестова нотатка", content: str = "Контент тестової нотатки"):
        """Створення тестової нотатки."""
        if not self.dev_models or not self.dev_models['Note']:
            return None
        
        try:
            note = self.dev_models['Note'](title, content)
            note.add_tags(["тест", "проект"])
            return note
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Не вдалося створити тестову нотатку: {e}")
            return None
    
    def step_1_manager_init(self):
        """Крок 1: Перевірка ініціалізації NoteManager."""
        self.print_step(1, "Ініціалізація NoteManager")
        
        if not self.dev or not hasattr(self.dev, 'NoteManager'):
            self.print_failure("Клас NoteManager не знайдено")
            return
        
        if not self.dev_storage:
            self.print_failure("FileStorage не знайдено", 
                             "Спочатку реалізуйте FileStorage клас")
            return
        
        manager_class = self.dev.NoteManager
        
        # Тест базової ініціалізації
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = manager_class(storage)
            self.print_success("NoteManager створюється з FileStorage")
            
            # Перевірка атрибутів
            if hasattr(manager, 'storage'):
                self.print_success("NoteManager.storage атрибут присутній")
            else:
                self.print_failure("NoteManager.storage атрибут відсутній")
            
            if hasattr(manager, '_notes'):
                if isinstance(manager._notes, list):
                    self.print_success("NoteManager._notes є списком")
                else:
                    self.print_failure("NoteManager._notes не є списком")
            else:
                self.print_failure("NoteManager._notes атрибут відсутній")
            
            # Перевірка автозавантаження
            if hasattr(manager, 'load_notes'):
                self.print_success("NoteManager має метод load_notes")
            else:
                self.print_failure("NoteManager.load_notes метод відсутній")
                    
        except Exception as e:
            self.print_failure(f"NoteManager не створюється: {e}")
    
    def step_2_add_get_notes(self):
        """Крок 2: Додавання та отримання нотаток."""
        self.print_step(2, "Додавання та отримання нотаток")
        
        if not self.dev or not self.dev_storage:
            self.print_failure("Класи не знайдені")
            return
        
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = self.dev.NoteManager(storage)
            
            test_note = self.create_test_note()
            if not test_note:
                self.print_failure("Не вдалося створити тестову нотатку")
                return
            
            # Тест add_note
            if hasattr(manager, 'add_note'):
                result = manager.add_note(test_note)
                
                if result:
                    self.print_success("add_note() додає нотатку")
                    
                    if len(manager._notes) == 1:
                        self.print_success("add_note() додає до списку _notes")
                    else:
                        self.print_failure("add_note() не додає до списку _notes")
                else:
                    self.print_failure("add_note() повертає False")
                
                # Тест дублікатів (нотатки з однаковим заголовком)
                duplicate_note = self.create_test_note("Тестова нотатка", "Інший контент")
                result2 = manager.add_note(duplicate_note)
                if not result2:
                    self.print_success("add_note() запобігає дублікатам за заголовком")
                else:
                    self.print_failure("add_note() не запобігає дублікатам за заголовком")
            else:
                self.print_failure("Метод add_note() відсутній")
            
            # Тест get_all_notes
            if hasattr(manager, 'get_all_notes'):
                all_notes = manager.get_all_notes()
                
                if isinstance(all_notes, list):
                    self.print_success("get_all_notes() повертає список")
                    
                    # Має повертати список кортежів (index, note)
                    if len(all_notes) > 0 and isinstance(all_notes[0], tuple):
                        index, note = all_notes[0]
                        if isinstance(index, int) and hasattr(note, 'title'):
                            self.print_success("get_all_notes() повертає кортежі (index, note)")
                        else:
                            self.print_failure("get_all_notes() повертає неправильний формат")
                    else:
                        self.print_success("get_all_notes() працює з порожнім списком")
                else:
                    self.print_failure("get_all_notes() не повертає список")
                
                # Тест сортування
                sorted_notes = manager.get_all_notes(sort_by='title')
                if isinstance(sorted_notes, list):
                    self.print_success("get_all_notes() підтримує сортування")
                else:
                    self.print_failure("get_all_notes() не підтримує сортування")
            else:
                self.print_failure("Метод get_all_notes() відсутній")
            
            # Тест get_note_by_index
            if hasattr(manager, 'get_note_by_index'):
                note = manager.get_note_by_index(1)  # Перша нотатка має індекс 1
                
                if note:
                    self.print_success("get_note_by_index() знаходить нотатку за індексом")
                    
                    if note.title == "Тестова нотатка":
                        self.print_success("get_note_by_index() повертає правильну нотатку")
                    else:
                        self.print_failure("get_note_by_index() повертає неправильну нотатку")
                else:
                    self.print_failure("get_note_by_index() не знаходить нотатку")
                
                # Неіснуючий індекс
                not_found = manager.get_note_by_index(999)
                if not not_found:
                    self.print_success("get_note_by_index() повертає None для неіснуючого індексу")
                else:
                    self.print_failure("get_note_by_index() знаходить неіснуючий індекс")
            else:
                self.print_failure("Метод get_note_by_index() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в додаванні/отриманні нотаток: {e}")
    
    def step_3_search_operations(self):
        """Крок 3: Операції пошуку."""
        self.print_step(3, "Операції пошуку")
        
        if not self.dev or not self.dev_storage:
            self.print_failure("Класи не знайдені")
            return
        
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = self.dev.NoteManager(storage)
            
            # Створюємо різні нотатки для тестування пошуку
            note1 = self.create_test_note("Проект Python", "Розробка програми на Python")
            note1.add_tag("програмування")
            
            note2 = self.create_test_note("Список покупок", "Молоко, хліб, масло")
            note2.add_tag("побут")
            
            note3 = self.create_test_note("Ідеї Python", "Ідеї для нових проектів")
            note3.add_tag("програмування")
            
            manager.add_note(note1)
            manager.add_note(note2)
            manager.add_note(note3)
            
            # Тест search_notes
            if hasattr(manager, 'search_notes'):
                # Пошук за заголовком
                python_results = manager.search_notes("Python")
                
                if isinstance(python_results, list):
                    self.print_success("search_notes() повертає список")
                    
                    # Має знайти 2 нотатки з "Python" у заголовку
                    if len(python_results) == 2:
                        self.print_success("search_notes() знаходить нотатки за заголовком")
                    else:
                        self.print_failure(f"search_notes() знайшов {len(python_results)} нотаток замість 2")
                else:
                    self.print_failure("search_notes() не повертає список")
                
                # Пошук за контентом
                milk_results = manager.search_notes("молоко")
                if len(milk_results) >= 1:
                    self.print_success("search_notes() знаходить нотатки за контентом")
                else:
                    self.print_failure("search_notes() не знаходить нотатки за контентом")
                
                # Пошук за тегами
                prog_results = manager.search_notes("програмування")
                if len(prog_results) >= 2:
                    self.print_success("search_notes() знаходить нотатки за тегами")
                else:
                    self.print_failure("search_notes() не знаходить нотатки за тегами")
            else:
                self.print_failure("Метод search_notes() відсутній")
            
            # Тест get_notes_by_tags
            if hasattr(manager, 'get_notes_by_tags'):
                tag_results = manager.get_notes_by_tags(["програмування"])
                
                if isinstance(tag_results, list):
                    self.print_success("get_notes_by_tags() повертає список")
                    
                    if len(tag_results) == 2:
                        self.print_success("get_notes_by_tags() знаходить нотатки за тегами")
                    else:
                        self.print_failure(f"get_notes_by_tags() знайшов {len(tag_results)} нотаток замість 2")
                else:
                    self.print_failure("get_notes_by_tags() не повертає список")
                
                # Пошук за множинними тегами
                multi_tag_results = manager.get_notes_by_tags(["програмування", "побут"])
                if len(multi_tag_results) >= 2:
                    self.print_success("get_notes_by_tags() працює з множинними тегами")
                else:
                    self.print_failure("get_notes_by_tags() не працює з множинними тегами")
            else:
                self.print_failure("Метод get_notes_by_tags() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в операціях пошуку: {e}")
    
    def step_4_note_operations(self):
        """Крок 4: Операції з нотатками."""
        self.print_step(4, "Операції з нотатками")
        
        if not self.dev or not self.dev_storage:
            self.print_failure("Класи не знайдені")
            return
        
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = self.dev.NoteManager(storage)
            
            # Додаємо тестові нотатки
            note1 = self.create_test_note("Нотатка для редагування", "Оригінальний контент")
            note2 = self.create_test_note("Нотатка для видалення", "Контент для видалення")
            
            manager.add_note(note1)
            manager.add_note(note2)
            
            # Тест edit_note
            if hasattr(manager, 'edit_note'):
                result = manager.edit_note(1, content="Оновлений контент", tags=["оновлено"])
                
                if result:
                    self.print_success("edit_note() оновлює нотатку")
                    
                    # Перевіряємо що контент змінився
                    updated_note = manager.get_note_by_index(1)
                    if updated_note and "Оновлений контент" in updated_note.content:
                        self.print_success("edit_note() оновлює контент")
                    else:
                        self.print_failure("edit_note() не оновлює контент")
                    
                    # Перевіряємо що теги оновилися
                    if updated_note and "оновлено" in updated_note.tags:
                        self.print_success("edit_note() оновлює теги")
                    else:
                        self.print_failure("edit_note() не оновлює теги")
                else:
                    self.print_failure("edit_note() повертає False")
                
                # Тест редагування неіснуючої нотатки
                result2 = manager.edit_note(999, content="Не має працювати")
                if not result2:
                    self.print_success("edit_note() обробляє неіснуючий індекс")
                else:
                    self.print_failure("edit_note() не обробляє неіснуючий індекс")
            else:
                self.print_failure("Метод edit_note() відсутній")
            
            # Тест remove_note
            if hasattr(manager, 'remove_note'):
                initial_count = len(manager._notes)
                result = manager.remove_note(2)  # Друга нотатка
                
                if result:
                    self.print_success("remove_note() видаляє нотатку")
                    
                    if len(manager._notes) == initial_count - 1:
                        self.print_success("remove_note() видаляє зі списку")
                    else:
                        self.print_failure("remove_note() не видаляє зі списку")
                else:
                    self.print_failure("remove_note() повертає False")
                
                # Тест видалення неіснуючої нотатки
                result2 = manager.remove_note(999)
                if not result2:
                    self.print_success("remove_note() обробляє неіснуючий індекс")
                else:
                    self.print_failure("remove_note() не обробляє неіснуючий індекс")
            else:
                self.print_failure("Метод remove_note() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в операціях з нотатками: {e}")
    
    def step_5_data_persistence(self):
        """Крок 5: Збереження та завантаження даних."""
        self.print_step(5, "Збереження та завантаження даних")
        
        if not self.dev or not self.dev_storage:
            self.print_failure("Класи не знайдені")
            return
        
        try:
            storage = self.dev_storage(self.temp_dir)
            manager = self.dev.NoteManager(storage)
            
            # Додаємо тестову нотатку
            note = self.create_test_note("Нотатка для збереження", "Контент для збереження")
            manager.add_note(note)
            
            # Тест save_notes
            if hasattr(manager, 'save_notes'):
                result = manager.save_notes()
                
                if result:
                    self.print_success("save_notes() зберігає дані")
                else:
                    self.print_failure("save_notes() повертає False")
            else:
                self.print_failure("Метод save_notes() відсутній")
            
            # Тест load_notes
            if hasattr(manager, 'load_notes'):
                # Створюємо новий менеджер для тестування завантаження
                new_manager = self.dev.NoteManager(storage)
                
                if len(new_manager._notes) >= 1:
                    self.print_success("load_notes() завантажує дані при ініціалізації")
                    
                    loaded_note = new_manager.get_note_by_index(1)
                    if loaded_note and loaded_note.title == "Нотатка для збереження":
                        self.print_success("load_notes() правильно відновлює нотатки")
                    else:
                        self.print_failure("load_notes() не відновлює нотатки правільно")
                else:
                    self.print_failure("load_notes() не завантажує дані")
            else:
                self.print_failure("Метод load_notes() відсутній")
            
            # Тест get_statistics
            if hasattr(manager, 'get_statistics'):
                stats = manager.get_statistics()
                
                if isinstance(stats, dict):
                    self.print_success("get_statistics() повертає словник")
                    
                    expected_keys = ['total_notes', 'total_tags', 'average_tags_per_note']
                    for key in expected_keys:
                        if key in stats:
                            self.print_success(f"get_statistics() включає ключ '{key}'")
                        else:
                            self.print_failure(f"get_statistics() не включає ключ '{key}'")
                else:
                    self.print_failure("get_statistics() не повертає словник")
            else:
                self.print_failure("Метод get_statistics() відсутній")
            
            # Тест get_all_tags
            if hasattr(manager, 'get_all_tags'):
                tags = manager.get_all_tags()
                
                if isinstance(tags, (list, set)):
                    self.print_success("get_all_tags() повертає колекцію тегів")
                    
                    if "тест" in tags:
                        self.print_success("get_all_tags() включає наявні теги")
                    else:
                        self.print_failure("get_all_tags() не включає наявні теги")
                else:
                    self.print_failure("get_all_tags() не повертає колекцію")
            else:
                self.print_failure("Метод get_all_tags() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в збереженні/завантаженні: {e}")
    
    def run_step(self, step_num: int):
        """Запуск конкретного кроку."""
        steps = {
            1: self.step_1_manager_init,
            2: self.step_2_add_get_notes,
            3: self.step_3_search_operations,
            4: self.step_4_note_operations,
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
            print(f"\n🎉 Всі тести пройдені! Клас NoteManager готовий.")
        else:
            print(f"\n🔧 Є проблеми що потребують вирішення.")
            print(f"💡 Підказка: Подивіться на еталонну реалізацію у personal_assistant/managers/note_manager.py")

def main():
    parser = argparse.ArgumentParser(description='Поетапна перевірка класу NoteManager')
    parser.add_argument('--step', type=int, help='Запустити тільки певний крок (1-5)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    parser.add_argument('--compare', '-c', action='store_true', help='Порівняння з еталоном')
    
    args = parser.parse_args()
    
    print("🧪 ПОЕТАПНА ПЕРЕВІРКА КЛАСУ NOTEMANAGER")
    print("=" * 60)
    
    if not DEV_IMPLEMENTATION:
        print("\n📝 Щоб розпочати:")
        print("1. Завершіть реалізацію Note та FileStorage класів")
        print("2. Створіть папку: dev_implementation/managers/")
        print("3. Створіть файл: dev_implementation/managers/__init__.py")
        print("4. Створіть файл: dev_implementation/managers/note_manager.py")
        print("5. Імплементуйте клас NoteManager з усіма методами")
        return
    
    tester = NoteManagerTester(verbose=args.verbose, compare=args.compare)
    
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