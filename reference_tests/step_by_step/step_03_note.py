#!/usr/bin/env python3
"""
🧪 STEP 3: NOTE CLASS - Поетапна перевірка

Цей файл допомагає розробнику поетапно створювати клас Note,
перевіряючи кожен метод окремо з еталонною реалізацією.

Використання:
    python step_03_note.py                     # Базова перевірка
    python step_03_note.py --verbose           # Детальний вивід  
    python step_03_note.py --step 2            # Тільки крок 2
    python step_03_note.py --compare           # Порівняння з еталоном
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Імпорт еталонної реалізації
try:
    from personal_assistant.models.note import Note
    from personal_assistant.models.field import Name
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
            import models.note as dev_note
            import models.field as dev_field
            DEV_IMPLEMENTATION = dev_note
            DEV_FIELDS = dev_field
            print("✅ Знайдено розробницьку реалізацію")
        except ImportError as e:
            print(f"⚠️  Помилка імпорту: {e}")
    else:
        print("📝 Створіть папку dev_implementation/models/")
except Exception as e:
    print(f"⚠️  Помилка: {e}")

class NoteTester:
    """Тестер для поетапної перевірки класу Note."""
    
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
    
    def step_1_note_init(self):
        """Крок 1: Перевірка ініціалізації Note."""
        self.print_step(1, "Ініціалізація Note")
        
        if not self.dev or not hasattr(self.dev, 'Note'):
            self.print_failure("Клас Note не знайдено")
            return
        
        note_class = self.dev.Note
        
        # Тест базової ініціалізації
        try:
            note = note_class("Тестова нотатка", "Це тестовий контент нотатки")
            self.print_success("Note створюється з заголовком та контентом")
            
            # Перевірка атрибутів
            if hasattr(note, 'title'):
                self.print_success("Note.title атрибут присутній")
            else:
                self.print_failure("Note.title атрибут відсутній")
            
            if hasattr(note, 'content'):
                self.print_success("Note.content атрибут присутній")
            else:
                self.print_failure("Note.content атрибут відсутній")
            
            if hasattr(note, 'tags'):
                if isinstance(note.tags, list):
                    self.print_success("Note.tags є списком")
                else:
                    self.print_failure("Note.tags не є списком")
            else:
                self.print_failure("Note.tags атрибут відсутній")
            
            # Перевірка datetime атрибутів
            datetime_attrs = ['created_at', 'updated_at']
            for attr in datetime_attrs:
                if hasattr(note, attr):
                    attr_value = getattr(note, attr)
                    if isinstance(attr_value, datetime):
                        self.print_success(f"Note.{attr} є datetime об'єктом")
                    else:
                        self.print_failure(f"Note.{attr} не є datetime об'єктом")
                else:
                    self.print_failure(f"Note.{attr} атрибут відсутній")
                    
        except Exception as e:
            self.print_failure(f"Note не створюється: {e}")
    
    def step_2_tags_management(self):
        """Крок 2: Керування тегами."""
        self.print_step(2, "Керування тегами")
        
        if not self.dev or not hasattr(self.dev, 'Note'):
            self.print_failure("Клас Note не знайдено")
            return
        
        try:
            note = self.dev.Note("Тест", "Контент")
            
            # Тест add_tag
            if hasattr(note, 'add_tag'):
                note.add_tag("важливо")
                
                if "важливо" in note.tags:
                    self.print_success("add_tag() додає тег")
                else:
                    self.print_failure("add_tag() не додає тег до списку")
                
                # Тест дублікатів
                note.add_tag("важливо")  # Той самий тег
                if note.tags.count("важливо") == 1:
                    self.print_success("add_tag() запобігає дублікатам")
                else:
                    self.print_failure("add_tag() не запобігає дублікатам")
            else:
                self.print_failure("Метод add_tag() відсутній")
            
            # Тест remove_tag
            if hasattr(note, 'remove_tag'):
                note.remove_tag("важливо")
                if "важливо" not in note.tags:
                    self.print_success("remove_tag() видаляє тег")
                else:
                    self.print_failure("remove_tag() не видаляє тег")
            else:
                self.print_failure("Метод remove_tag() відсутній")
            
            # Тест add_tags (множинні теги)
            if hasattr(note, 'add_tags'):
                test_tags = ["робота", "проект", "терміново"]
                note.add_tags(test_tags)
                
                added_count = sum(1 for tag in test_tags if tag in note.tags)
                if added_count == len(test_tags):
                    self.print_success("add_tags() додає множинні теги")
                else:
                    self.print_failure(f"add_tags() додав тільки {added_count} з {len(test_tags)} тегів")
            else:
                self.print_failure("Метод add_tags() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в тестах тегів: {e}")
    
    def step_3_note_methods(self):
        """Крок 3: Основні методи нотатки."""
        self.print_step(3, "Основні методи нотатки")
        
        if not self.dev or not hasattr(self.dev, 'Note'):
            self.print_failure("Клас Note не знайдено")
            return
        
        try:
            note = self.dev.Note("Тестова нотатка", "Це контент нотатки для тестування")
            
            # Тест __str__
            str_result = str(note)
            if "Тестова нотатка" in str_result:
                self.print_success("__str__() включає заголовок")
            else:
                self.print_failure("__str__() не включає заголовок")
            
            # Тест update_content
            if hasattr(note, 'update_content'):
                old_updated_at = note.updated_at
                import time
                time.sleep(0.01)  # Невелика затримка
                
                note.update_content("Новий контент нотатки")
                
                if note.content == "Новий контент нотатки":
                    self.print_success("update_content() оновлює контент")
                else:
                    self.print_failure("update_content() не оновлює контент")
                
                if note.updated_at > old_updated_at:
                    self.print_success("update_content() оновлює updated_at")
                else:
                    self.print_failure("update_content() не оновлює updated_at")
            else:
                self.print_failure("Метод update_content() відсутній")
            
            # Тест matches_search
            if hasattr(note, 'matches_search'):
                # Пошук у заголовку
                if note.matches_search("Тестова"):
                    self.print_success("matches_search() знаходить у заголовку")
                else:
                    self.print_failure("matches_search() не знаходить у заголовку")
                
                # Пошук у контенті  
                if note.matches_search("контент"):
                    self.print_success("matches_search() знаходить у контенті")
                else:
                    self.print_failure("matches_search() не знаходить у контенті")
                
                # Пошук у тегах
                note.add_tag("тестування")
                if note.matches_search("тестування"):
                    self.print_success("matches_search() знаходить у тегах")
                else:
                    self.print_failure("matches_search() не знаходить у тегах")
                
                # Пошук реєстронезалежний
                if note.matches_search("ТЕСТОВА"):
                    self.print_success("matches_search() реєстронезалежний")
                else:
                    self.print_failure("matches_search() залежить від регістру")
            else:
                self.print_failure("Метод matches_search() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в основних методах: {e}")
    
    def step_4_serialization(self):
        """Крок 4: Серіалізація та десеріалізація."""
        self.print_step(4, "Серіалізація та десеріалізація")
        
        if not self.dev or not hasattr(self.dev, 'Note'):
            self.print_failure("Клас Note не знайдено")
            return
        
        try:
            # Створення повної нотатки
            note = self.dev.Note("Тестова нотатка", "Контент для тестування")
            note.add_tags(["тест", "проект", "важливо"])
            
            # Тест to_dict
            if hasattr(note, 'to_dict'):
                note_dict = note.to_dict()
                
                if isinstance(note_dict, dict):
                    self.print_success("to_dict() повертає словник")
                    
                    # Перевірка ключів
                    required_keys = ['title', 'content', 'tags', 'created_at', 'updated_at']
                    for key in required_keys:
                        if key in note_dict:
                            self.print_success(f"to_dict() включає ключ '{key}'")
                        else:
                            self.print_failure(f"to_dict() не включає ключ '{key}'")
                else:
                    self.print_failure("to_dict() не повертає словник")
            else:
                self.print_failure("Метод to_dict() відсутній")
            
            # Тест from_dict
            if hasattr(self.dev.Note, 'from_dict'):
                try:
                    test_dict = {
                        'title': 'Відновлена нотатка',
                        'content': 'Контент відновленої нотатки',
                        'tags': ['відновлено', 'тест'],
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    }
                    
                    restored_note = self.dev.Note.from_dict(test_dict)
                    
                    if restored_note.title == "Відновлена нотатка":
                        self.print_success("from_dict() відновлює заголовок")
                    else:
                        self.print_failure("from_dict() не відновлює заголовок правильно")
                    
                    if restored_note.content == "Контент відновленої нотатки":
                        self.print_success("from_dict() відновлює контент")
                    else:
                        self.print_failure("from_dict() не відновлює контент")
                    
                    if len(restored_note.tags) == 2 and "відновлено" in restored_note.tags:
                        self.print_success("from_dict() відновлює теги")
                    else:
                        self.print_failure("from_dict() не відновлює теги")
                        
                except Exception as e:
                    self.print_failure(f"from_dict() викликає помилку: {e}")
            else:
                self.print_failure("Метод from_dict() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в серіалізації: {e}")
    
    def step_5_advanced_features(self):
        """Крок 5: Розширені функції."""
        self.print_step(5, "Розширені функції")
        
        if not self.dev or not hasattr(self.dev, 'Note'):
            self.print_failure("Клас Note не знайдено")
            return
        
        try:
            note = self.dev.Note("Розширена нотатка", "Контент з розширеними функціями")
            
            # Тест get_preview
            if hasattr(note, 'get_preview'):
                preview = note.get_preview(20)
                if len(preview) <= 23:  # 20 + "..."
                    self.print_success("get_preview() обмежує довжину")
                else:
                    self.print_failure("get_preview() не обмежує довжину правильно")
                
                if "Контент з розширеними" in preview:
                    self.print_success("get_preview() включає початок контенту")
                else:
                    self.print_failure("get_preview() не включає початок контенту")
            else:
                self.print_failure("Метод get_preview() відсутній")
            
            # Тест has_tag
            if hasattr(note, 'has_tag'):
                note.add_tag("розширений")
                
                if note.has_tag("розширений"):
                    self.print_success("has_tag() знаходить існуючий тег")
                else:
                    self.print_failure("has_tag() не знаходить існуючий тег")
                
                if not note.has_tag("неіснуючий"):
                    self.print_success("has_tag() не знаходить неіснуючий тег")
                else:
                    self.print_failure("has_tag() знаходить неіснуючий тег")
            else:
                self.print_failure("Метод has_tag() відсутній")
            
            # Тест get_age_days
            if hasattr(note, 'get_age_days'):
                age = note.get_age_days()
                if isinstance(age, int) and age >= 0:
                    self.print_success("get_age_days() повертає коректний вік")
                else:
                    self.print_failure("get_age_days() повертає некоректний вік")
            else:
                self.print_failure("Метод get_age_days() відсутній")
            
            # Тест __eq__
            note2 = self.dev.Note("Розширена нотатка", "Інший контент")
            note3 = self.dev.Note("Інша нотатка", "Контент з розширеними функціями")
            
            if note == note2:
                self.print_success("__eq__() порівнює за заголовком")
            else:
                self.print_failure("__eq__() не порівнює за заголовком")
            
            if not (note == note3):
                self.print_success("__eq__() розрізняє різні заголовки")
            else:
                self.print_failure("__eq__() не розрізняє різні заголовки")
                
        except Exception as e:
            self.print_failure(f"Помилка в розширених функціях: {e}")
    
    def run_step(self, step_num: int):
        """Запуск конкретного кроку."""
        steps = {
            1: self.step_1_note_init,
            2: self.step_2_tags_management,
            3: self.step_3_note_methods,
            4: self.step_4_serialization,
            5: self.step_5_advanced_features,
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
            print(f"\n🎉 Всі тести пройдені! Клас Note готовий.")
        else:
            print(f"\n🔧 Є проблеми що потребують вирішення.")
            print(f"💡 Підказка: Подивіться на еталонну реалізацію у personal_assistant/models/note.py")

def main():
    parser = argparse.ArgumentParser(description='Поетапна перевірка класу Note')
    parser.add_argument('--step', type=int, help='Запустити тільки певний крок (1-5)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    parser.add_argument('--compare', '-c', action='store_true', help='Порівняння з еталоном')
    
    args = parser.parse_args()
    
    print("🧪 ПОЕТАПНА ПЕРЕВІРКА КЛАСУ NOTE")
    print("=" * 60)
    
    if not DEV_IMPLEMENTATION:
        print("\n📝 Щоб розпочати:")
        print("1. Завершіть реалізацію Field класів (step_01_field.py)")
        print("2. Створіть файл: dev_implementation/models/note.py")
        print("3. Імплементуйте клас Note з усіма методами")
        return
    
    tester = NoteTester(verbose=args.verbose, compare=args.compare)
    
    if args.step:
        tester.run_step(args.step)
    else:
        tester.run_all_steps()
    
    tester.show_summary()

if __name__ == "__main__":
    main()