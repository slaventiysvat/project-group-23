#!/usr/bin/env python3
"""
🧪 STEP 7: COMMAND MATCHER - Поетапна перевірка

Цей файл допомагає розробнику поетапно створювати клас CommandMatcher,
перевіряючи кожен метод окремо з еталонною реалізацією.

Використання:
    python step_07_command_matcher.py          # Базова перевірка
    python step_07_command_matcher.py --verbose # Детальний вивід  
    python step_07_command_matcher.py --step 2  # Тільки крок 2
    python step_07_command_matcher.py --compare # Порівняння з еталоном
"""

import sys
import os
import argparse
from pathlib import Path

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Імпорт еталонної реалізації
try:
    from personal_assistant.utils.command_matcher import CommandMatcher
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
            import utils.command_matcher as dev_matcher
            DEV_IMPLEMENTATION = dev_matcher
            print("✅ Знайдено розробницьку реалізацію")
        except ImportError as e:
            print(f"⚠️  Помилка імпорту: {e}")
    else:
        print("📝 Створіть папку dev_implementation/utils/")
except Exception as e:
    print(f"⚠️  Помилка: {e}")

class CommandMatcherTester:
    """Тестер для поетапної перевірки класу CommandMatcher."""
    
    def __init__(self, verbose: bool = False, compare: bool = False):
        self.verbose = verbose
        self.compare = compare
        self.passed = 0
        self.failed = 0
        self.dev = DEV_IMPLEMENTATION
    
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
    
    def step_1_matcher_init(self):
        """Крок 1: Перевірка ініціалізації CommandMatcher."""
        self.print_step(1, "Ініціалізація CommandMatcher")
        
        if not self.dev or not hasattr(self.dev, 'CommandMatcher'):
            self.print_failure("Клас CommandMatcher не знайдено")
            return
        
        matcher_class = self.dev.CommandMatcher
        
        # Тест базової ініціалізації
        try:
            matcher = matcher_class()
            self.print_success("CommandMatcher створюється без параметрів")
            
            # Перевірка атрибутів команд
            if hasattr(matcher, 'commands'):
                if isinstance(matcher.commands, dict):
                    self.print_success("CommandMatcher.commands є словником")
                    
                    # Перевірка базових команд
                    expected_commands = ['add_contact', 'search_contact', 'add_note', 'show_contacts', 'help']
                    found_commands = [cmd for cmd in expected_commands if cmd in matcher.commands]
                    
                    if len(found_commands) >= 3:
                        self.print_success(f"CommandMatcher містить базові команди ({len(found_commands)} знайдено)")
                    else:
                        self.print_failure(f"CommandMatcher містить недостатньо команд ({len(found_commands)} з {len(expected_commands)})")
                else:
                    self.print_failure("CommandMatcher.commands не є словником")
            else:
                self.print_failure("CommandMatcher.commands атрибут відсутній")
            
            # Перевірка структури команд
            if hasattr(matcher, 'commands') and matcher.commands:
                sample_command = next(iter(matcher.commands.values()))
                required_keys = ['patterns', 'description', 'examples']
                
                for key in required_keys:
                    if key in sample_command:
                        self.print_success(f"Команди містять ключ '{key}'")
                    else:
                        self.print_failure(f"Команди не містять ключ '{key}'")
                    
        except Exception as e:
            self.print_failure(f"CommandMatcher не створюється: {e}")
    
    def step_2_pattern_matching(self):
        """Крок 2: Розпізнавання паттернів команд."""
        self.print_step(2, "Розпізнавання паттернів команд")
        
        if not self.dev or not hasattr(self.dev, 'CommandMatcher'):
            self.print_failure("Клас CommandMatcher не знайдено")
            return
        
        try:
            matcher = self.dev.CommandMatcher()
            
            # Тест find_best_command
            if hasattr(matcher, 'find_best_command'):
                # Тестові фрази для розпізнавання
                test_cases = [
                    ("додай контакт", "add_contact", 0.7),
                    ("знайди контакт", "search_contact", 0.7),
                    ("додай нотатку", "add_note", 0.7),
                    ("покажи всі контакти", "show_contacts", 0.7),
                    ("допомога", "help", 0.8),
                ]
                
                for phrase, expected_command, min_confidence in test_cases:
                    command, confidence = matcher.find_best_command(phrase)
                    
                    if command == expected_command:
                        self.print_success(f"find_best_command() розпізнає '{phrase}' як '{expected_command}'")
                        
                        if confidence >= min_confidence:
                            self.print_success(f"Впевненість {confidence:.2f} достатня для '{phrase}'")
                        else:
                            self.print_failure(f"Впевненість {confidence:.2f} занадто низька для '{phrase}'")
                    else:
                        self.print_failure(f"find_best_command() не розпізнає '{phrase}' (отримано: '{command}')")
                
                # Тест з невідомою командою
                unknown_command, unknown_confidence = matcher.find_best_command("абсолютно невідома команда xyz")
                if unknown_confidence < 0.5:
                    self.print_success("find_best_command() правильно обробляє невідомі команди")
                else:
                    self.print_failure("find_best_command() занадто впевнено розпізнає невідомі команди")
                    
            else:
                self.print_failure("Метод find_best_command() відсутній")
            
            # Тест match_pattern
            if hasattr(matcher, 'match_pattern'):
                # Тест прямого співпадіння
                direct_match = matcher.match_pattern("додай контакт", "додай контакт")
                if direct_match >= 0.9:
                    self.print_success("match_pattern() дає високу оцінку прямому співпадінню")
                else:
                    self.print_failure("match_pattern() дає низьку оцінку прямому співпадінню")
                
                # Тест часткового співпадіння
                partial_match = matcher.match_pattern("додати", "додай контакт")
                if 0.3 <= partial_match <= 0.8:
                    self.print_success("match_pattern() правильно оцінює часткове співпадіння")
                else:
                    self.print_failure(f"match_pattern() неправильно оцінює часткове співпадіння: {partial_match}")
                
                # Тест відсутності співпадіння
                no_match = matcher.match_pattern("xyz", "додай контакт")
                if no_match < 0.3:
                    self.print_success("match_pattern() дає низьку оцінку відсутності співпадіння")
                else:
                    self.print_failure("match_pattern() дає високу оцінку відсутності співпадіння")
            else:
                self.print_failure("Метод match_pattern() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в розпізнаванні паттернів: {e}")
    
    def step_3_command_info(self):
        """Крок 3: Інформація про команди."""
        self.print_step(3, "Інформація про команди")
        
        if not self.dev or not hasattr(self.dev, 'CommandMatcher'):
            self.print_failure("Клас CommandMatcher не знайдено")
            return
        
        try:
            matcher = self.dev.CommandMatcher()
            
            # Тест get_command_description
            if hasattr(matcher, 'get_command_description'):
                description = matcher.get_command_description('add_contact')
                
                if description:
                    self.print_success("get_command_description() повертає опис команди")
                    
                    if isinstance(description, str) and len(description) > 0:
                        self.print_success("get_command_description() повертає непорожній рядок")
                    else:
                        self.print_failure("get_command_description() повертає порожній або неправильний опис")
                else:
                    self.print_failure("get_command_description() не повертає опис")
                
                # Тест з неіснуючою командою
                no_description = matcher.get_command_description('nonexistent_command')
                if not no_description:
                    self.print_success("get_command_description() обробляє неіснуючі команди")
                else:
                    self.print_failure("get_command_description() повертає опис для неіснуючої команди")
            else:
                self.print_failure("Метод get_command_description() відсутній")
            
            # Тест get_command_examples
            if hasattr(matcher, 'get_command_examples'):
                examples = matcher.get_command_examples('add_contact')
                
                if examples:
                    self.print_success("get_command_examples() повертає приклади")
                    
                    if isinstance(examples, list) and len(examples) > 0:
                        self.print_success("get_command_examples() повертає непорожній список")
                        
                        # Перевіряємо що приклади є рядками
                        if all(isinstance(ex, str) for ex in examples):
                            self.print_success("get_command_examples() повертає рядкові приклади")
                        else:
                            self.print_failure("get_command_examples() повертає не-рядкові приклади")
                    else:
                        self.print_failure("get_command_examples() повертає порожній або неправильний список")
                else:
                    self.print_failure("get_command_examples() не повертає приклади")
                
                # Тест з неіснуючою командою
                no_examples = matcher.get_command_examples('nonexistent_command')
                if not no_examples:
                    self.print_success("get_command_examples() обробляє неіснуючі команди")
                else:
                    self.print_failure("get_command_examples() повертає приклади для неіснуючої команди")
            else:
                self.print_failure("Метод get_command_examples() відсутній")
            
            # Тест get_all_commands
            if hasattr(matcher, 'get_all_commands'):
                all_commands = matcher.get_all_commands()
                
                if isinstance(all_commands, list):
                    self.print_success("get_all_commands() повертає список")
                    
                    if len(all_commands) >= 5:
                        self.print_success(f"get_all_commands() повертає достатню кількість команд ({len(all_commands)})")
                    else:
                        self.print_failure(f"get_all_commands() повертає недостатньо команд ({len(all_commands)})")
                else:
                    self.print_failure("get_all_commands() не повертає список")
            else:
                self.print_failure("Метод get_all_commands() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в інформації про команди: {e}")
    
    def step_4_advanced_matching(self):
        """Крок 4: Розширене розпізнавання."""
        self.print_step(4, "Розширене розпізнавання")
        
        if not self.dev or not hasattr(self.dev, 'CommandMatcher'):
            self.print_failure("Клас CommandMatcher не знайдено")
            return
        
        try:
            matcher = self.dev.CommandMatcher()
            
            # Тест багатослівних фраз
            multi_word_tests = [
                ("мені потрібно додати новий контакт до списку", "add_contact"),
                ("хочу знайти контакт в адресній книзі", "search_contact"),
                ("покажи мені всі мої контакти", "show_contacts"),
                ("створи нову нотатку", "add_note"),
            ]
            
            for phrase, expected in multi_word_tests:
                command, confidence = matcher.find_best_command(phrase)
                if command == expected and confidence > 0.5:
                    self.print_success(f"Розпізнає складну фразу: '{phrase[:30]}...'")
                else:
                    self.print_failure(f"Не розпізнає складну фразу: '{phrase[:30]}...' (отримано: {command})")
            
            # Тест з помилками в словах
            if hasattr(matcher, 'find_best_command'):
                typo_tests = [
                    ("дадай контакт", "add_contact"),  # помилка в "додай"
                    ("знайті контакт", "search_contact"),  # помилка в "знайди"
                    ("нотатка додать", "add_note"),  # інший порядок слів + помилка
                ]
                
                typo_successes = 0
                for phrase, expected in typo_tests:
                    command, confidence = matcher.find_best_command(phrase)
                    if command == expected and confidence > 0.4:
                        typo_successes += 1
                
                if typo_successes >= len(typo_tests) // 2:
                    self.print_success(f"Обробляє помилки в словах ({typo_successes}/{len(typo_tests)})")
                else:
                    self.print_failure(f"Погано обробляє помилки в словах ({typo_successes}/{len(typo_tests)})")
            
            # Тест різних регістрів
            case_tests = [
                ("ДОДАЙ КОНТАКТ", "add_contact"),
                ("Знайди Контакт", "search_contact"),
                ("дОдАй НоТаТкУ", "add_note"),
            ]
            
            case_successes = 0
            for phrase, expected in case_tests:
                command, confidence = matcher.find_best_command(phrase)
                if command == expected and confidence > 0.6:
                    case_successes += 1
            
            if case_successes == len(case_tests):
                self.print_success("Правильно обробляє різні регістри")
            else:
                self.print_failure(f"Проблеми з різними регістрами ({case_successes}/{len(case_tests)})")
                
        except Exception as e:
            self.print_failure(f"Помилка в розширеному розпізнаванні: {e}")
    
    def step_5_performance_edge_cases(self):
        """Крок 5: Продуктивність та крайні випадки."""
        self.print_step(5, "Продуктивність та крайні випадки")
        
        if not self.dev or not hasattr(self.dev, 'CommandMatcher'):
            self.print_failure("Клас CommandMatcher не знайдено")
            return
        
        try:
            matcher = self.dev.CommandMatcher()
            
            # Тест з порожнім вводом
            if hasattr(matcher, 'find_best_command'):
                empty_command, empty_confidence = matcher.find_best_command("")
                if empty_confidence == 0.0:
                    self.print_success("Правильно обробляє порожній ввід")
                else:
                    self.print_failure("Неправильно обробляє порожній ввід")
                
                # Тест з дуже довгим вводом
                long_input = "це дуже довгий рядок " * 20 + "додай контакт"
                long_command, long_confidence = matcher.find_best_command(long_input)
                if long_command == "add_contact" and long_confidence > 0.3:
                    self.print_success("Обробляє довгий ввід")
                else:
                    self.print_failure("Не обробляє довгий ввід")
                
                # Тест зі спеціальними символами
                special_input = "!!!додай@@контакт###"
                special_command, special_confidence = matcher.find_best_command(special_input)
                if special_command == "add_contact" and special_confidence > 0.3:
                    self.print_success("Обробляє спеціальні символи")
                else:
                    self.print_failure("Не обробляє спеціальні символи")
                
                # Тест тільки з числами
                number_command, number_confidence = matcher.find_best_command("12345")
                if number_confidence < 0.3:
                    self.print_success("Правильно обробляє тільки числа")
                else:
                    self.print_failure("Неправильно обробляє тільки числа")
            
            # Тест продуктивності (простий)
            import time
            start_time = time.time()
            
            for i in range(100):
                matcher.find_best_command(f"додай контакт {i}")
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if processing_time < 1.0:  # Менше 1 секунди на 100 запитів
                self.print_success(f"Продуктивність достатня ({processing_time:.3f}с на 100 запитів)")
            else:
                self.print_failure(f"Продуктивність низька ({processing_time:.3f}с на 100 запитів)")
            
            # Тест консистентності
            consistent_results = []
            test_phrase = "додай контакт іван"
            
            for i in range(5):
                command, confidence = matcher.find_best_command(test_phrase)
                consistent_results.append((command, confidence))
            
            # Всі результати мають бути однаковими
            if all(result == consistent_results[0] for result in consistent_results):
                self.print_success("Результати консистентні")
            else:
                self.print_failure("Результати неконсистентні")
                
        except Exception as e:
            self.print_failure(f"Помилка в продуктивності/крайніх випадках: {e}")
    
    def run_step(self, step_num: int):
        """Запуск конкретного кроку."""
        steps = {
            1: self.step_1_matcher_init,
            2: self.step_2_pattern_matching,
            3: self.step_3_command_info,
            4: self.step_4_advanced_matching,
            5: self.step_5_performance_edge_cases,
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
            print(f"\n🎉 Всі тести пройдені! Клас CommandMatcher готовий.")
        else:
            print(f"\n🔧 Є проблеми що потребують вирішення.")
            print(f"💡 Підказка: Подивіться на еталонну реалізацію у personal_assistant/utils/command_matcher.py")

def main():
    parser = argparse.ArgumentParser(description='Поетапна перевірка класу CommandMatcher')
    parser.add_argument('--step', type=int, help='Запустити тільки певний крок (1-5)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    parser.add_argument('--compare', '-c', action='store_true', help='Порівняння з еталоном')
    
    args = parser.parse_args()
    
    print("🧪 ПОЕТАПНА ПЕРЕВІРКА КЛАСУ COMMANDMATCHER")
    print("=" * 60)
    
    if not DEV_IMPLEMENTATION:
        print("\n📝 Щоб розпочати:")
        print("1. Створіть папку: dev_implementation/utils/")
        print("2. Створіть файл: dev_implementation/utils/__init__.py")
        print("3. Створіть файл: dev_implementation/utils/command_matcher.py")
        print("4. Імплементуйте клас CommandMatcher з усіма методами")
        return
    
    tester = CommandMatcherTester(verbose=args.verbose, compare=args.compare)
    
    if args.step:
        tester.run_step(args.step)
    else:
        tester.run_all_steps()
    
    tester.show_summary()

if __name__ == "__main__":
    main()