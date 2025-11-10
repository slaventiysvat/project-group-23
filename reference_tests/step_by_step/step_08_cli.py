#!/usr/bin/env python3
"""
🧪 STEP 8: CLI - Поетапна перевірка

Цей файл допомагає розробнику поетапно створювати клас PersonalAssistantCLI,
перевіряючи кожен компонент окремо з еталонною реалізацією.

Використання:
    python step_08_cli.py          # Базова перевірка
    python step_08_cli.py --verbose # Детальний вивід  
    python step_08_cli.py --step 3  # Тільки крок 3
    python step_08_cli.py --compare # Порівняння з еталоном
"""

import sys
import os
import argparse
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Додаємо шлях до проекту
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Імпорт еталонної реалізації
try:
    from personal_assistant.cli.interface import PersonalAssistantCLI
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
            import cli.interface as dev_cli
            DEV_IMPLEMENTATION = dev_cli
            print("✅ Знайдено розробницьку реалізацію")
        except ImportError as e:
            print(f"⚠️  Помилка імпорту: {e}")
    else:
        print("📝 Створіть папку dev_implementation/cli/")
except Exception as e:
    print(f"⚠️  Помилка: {e}")

class CLITester:
    """Тестер для поетапної перевірки класу PersonalAssistantCLI."""
    
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
    
    def step_1_cli_init(self):
        """Крок 1: Перевірка ініціалізації CLI."""
        self.print_step(1, "Ініціалізація PersonalAssistantCLI")
        
        if not self.dev or not hasattr(self.dev, 'PersonalAssistantCLI'):
            self.print_failure("Клас PersonalAssistantCLI не знайдено")
            return
        
        cli_class = self.dev.PersonalAssistantCLI
        
        # Тест ініціалізації без параметрів
        try:
            cli = cli_class()
            self.print_success("PersonalAssistantCLI створюється без параметрів")
            
            # Перевірка менеджерів
            required_attrs = ['contact_manager', 'note_manager', 'command_matcher']
            for attr in required_attrs:
                if hasattr(cli, attr):
                    if getattr(cli, attr) is not None:
                        self.print_success(f"PersonalAssistantCLI має атрибут {attr}")
                    else:
                        self.print_failure(f"PersonalAssistantCLI.{attr} є None")
                else:
                    self.print_failure(f"PersonalAssistantCLI.{attr} атрибут відсутній")
            
            # Перевірка running флага
            if hasattr(cli, 'running'):
                if isinstance(cli.running, bool):
                    self.print_success("PersonalAssistantCLI.running є boolean")
                else:
                    self.print_failure("PersonalAssistantCLI.running не є boolean")
            else:
                self.print_failure("PersonalAssistantCLI.running атрибут відсутній")
            
            # Перевірка методу run
            if hasattr(cli, 'run'):
                self.print_success("PersonalAssistantCLI має метод run()")
            else:
                self.print_failure("PersonalAssistantCLI.run() метод відсутній")
            
            # Перевірка методу process_command
            if hasattr(cli, 'process_command'):
                self.print_success("PersonalAssistantCLI має метод process_command()")
            else:
                self.print_failure("PersonalAssistantCLI.process_command() метод відсутній")
            
        except Exception as e:
            self.print_failure(f"PersonalAssistantCLI не створюється: {e}")
    
    def step_2_command_processing(self):
        """Крок 2: Обробка команд."""
        self.print_step(2, "Обробка команд")
        
        if not self.dev or not hasattr(self.dev, 'PersonalAssistantCLI'):
            self.print_failure("Клас PersonalAssistantCLI не знайдено")
            return
        
        try:
            cli = self.dev.PersonalAssistantCLI()
            
            if hasattr(cli, 'process_command'):
                # Тест команди виходу
                exit_commands = ['exit', 'quit', 'вихід', 'stop']
                for cmd in exit_commands:
                    try:
                        result = cli.process_command(cmd)
                        # Очікуємо що команда виходу поставить running=False
                        if hasattr(cli, 'running') and not cli.running:
                            self.print_success(f"Команда '{cmd}' правильно обробляється як вихід")
                            cli.running = True  # Відновлюємо для наступних тестів
                            break
                        elif result == "goodbye" or "до побачення" in str(result).lower():
                            self.print_success(f"Команда '{cmd}' повертає повідомлення про вихід")
                        else:
                            self.print_failure(f"Команда '{cmd}' не обробляється як вихід")
                    except Exception as e:
                        self.print_failure(f"Помилка при обробці команди '{cmd}': {e}")
                
                # Тест команди допомоги
                help_commands = ['help', 'допомога', '?']
                for cmd in help_commands:
                    try:
                        result = cli.process_command(cmd)
                        if result and isinstance(result, str) and len(result) > 50:
                            self.print_success(f"Команда '{cmd}' повертає розширену довідку")
                        else:
                            self.print_failure(f"Команда '{cmd}' не повертає детальну довідку")
                    except Exception as e:
                        self.print_failure(f"Помилка при обробці команди допомоги '{cmd}': {e}")
                
                # Тест невідомої команди
                try:
                    unknown_result = cli.process_command("абсолютно невідома команда xyz")
                    if unknown_result and ("не розумію" in unknown_result.lower() or 
                                         "невідома" in unknown_result.lower() or 
                                         "help" in unknown_result.lower()):
                        self.print_success("Невідомі команди обробляються правильно")
                    else:
                        self.print_failure("Невідомі команди обробляються неправильно")
                except Exception as e:
                    self.print_failure(f"Помилка при обробці невідомої команди: {e}")
                
                # Тест порожньої команди
                try:
                    empty_result = cli.process_command("")
                    if not empty_result or len(empty_result.strip()) == 0:
                        self.print_success("Порожні команди обробляються правильно")
                    else:
                        self.print_failure("Порожні команди обробляються неправильно")
                except Exception as e:
                    self.print_failure(f"Помилка при обробці порожньої команди: {e}")
                    
            else:
                self.print_failure("Метод process_command() відсутній")
                
        except Exception as e:
            self.print_failure(f"Помилка в обробці команд: {e}")
    
    def step_3_contact_commands(self):
        """Крок 3: Команди роботи з контактами."""
        self.print_step(3, "Команди роботи з контактами")
        
        if not self.dev or not hasattr(self.dev, 'PersonalAssistantCLI'):
            self.print_failure("Клас PersonalAssistantCLI не знайдено")
            return
        
        try:
            cli = self.dev.PersonalAssistantCLI()
            
            # Тест додавання контакту
            add_contact_commands = [
                "додай контакт",
                "add contact",
                "новий контакт"
            ]
            
            for cmd in add_contact_commands:
                try:
                    # Імітуємо додавання контакту
                    with patch('builtins.input', side_effect=['Іван Петров', '0501234567', '', '']):
                        result = cli.process_command(cmd)
                        
                        if result and ("додано" in result.lower() or "створено" in result.lower() or "success" in result.lower()):
                            self.print_success(f"Команда '{cmd}' додає контакт")
                            break
                        else:
                            self.print_failure(f"Команда '{cmd}' не додає контакт правильно")
                except Exception as e:
                    if self.verbose:
                        print(f"Попередження: {e}")
            
            # Тест пошуку контакту
            search_commands = [
                "знайди контакт Іван",
                "search contact Ivan",
                "пошук контакт"
            ]
            
            for cmd in search_commands:
                try:
                    result = cli.process_command(cmd)
                    # Очікуємо що команда пошуку поверне щось (навіть якщо не знайдено)
                    if result is not None:
                        self.print_success(f"Команда '{cmd}' виконує пошук")
                        break
                    else:
                        self.print_failure(f"Команда '{cmd}' не виконує пошук")
                except Exception as e:
                    if self.verbose:
                        print(f"Попередження: {e}")
            
            # Тест показу всіх контактів
            show_commands = [
                "покажи всі контакти",
                "show all contacts",
                "список контактів"
            ]
            
            for cmd in show_commands:
                try:
                    result = cli.process_command(cmd)
                    if result is not None:
                        self.print_success(f"Команда '{cmd}' показує контакти")
                        break
                    else:
                        self.print_failure(f"Команда '{cmd}' не показує контакти")
                except Exception as e:
                    if self.verbose:
                        print(f"Попередження: {e}")
            
            # Тест редагування контакту
            edit_commands = [
                "редагувати контакт",
                "edit contact",
                "змінити контакт"
            ]
            
            for cmd in edit_commands:
                try:
                    with patch('builtins.input', side_effect=['Іван', '', '', '']):
                        result = cli.process_command(cmd)
                        if result is not None:
                            self.print_success(f"Команда '{cmd}' редагує контакт")
                            break
                        else:
                            self.print_failure(f"Команда '{cmd}' не редагує контакт")
                except Exception as e:
                    if self.verbose:
                        print(f"Попередження: {e}")
                        
        except Exception as e:
            self.print_failure(f"Помилка в командах контактів: {e}")
    
    def step_4_note_commands(self):
        """Крок 4: Команди роботи з нотатками."""
        self.print_step(4, "Команди роботи з нотатками")
        
        if not self.dev or not hasattr(self.dev, 'PersonalAssistantCLI'):
            self.print_failure("Клас PersonalAssistantCLI не знайдено")
            return
        
        try:
            cli = self.dev.PersonalAssistantCLI()
            
            # Тест додавання нотатки
            add_note_commands = [
                "додай нотатку",
                "add note",
                "нова нотатка"
            ]
            
            for cmd in add_note_commands:
                try:
                    with patch('builtins.input', side_effect=['Тест нотатка', 'тест,важливо']):
                        result = cli.process_command(cmd)
                        
                        if result and ("додано" in result.lower() or "створено" in result.lower()):
                            self.print_success(f"Команда '{cmd}' додає нотатку")
                            break
                        else:
                            self.print_failure(f"Команда '{cmd}' не додає нотатку правильно")
                except Exception as e:
                    if self.verbose:
                        print(f"Попередження: {e}")
            
            # Тест пошуку нотаток
            search_note_commands = [
                "знайди нотатки",
                "search notes",
                "пошук нотаток"
            ]
            
            for cmd in search_note_commands:
                try:
                    result = cli.process_command(cmd)
                    if result is not None:
                        self.print_success(f"Команда '{cmd}' шукає нотатки")
                        break
                    else:
                        self.print_failure(f"Команда '{cmd}' не шукає нотатки")
                except Exception as e:
                    if self.verbose:
                        print(f"Попередження: {e}")
            
            # Тест показу нотаток
            show_note_commands = [
                "покажи нотатки",
                "show notes",
                "список нотаток"
            ]
            
            for cmd in show_note_commands:
                try:
                    result = cli.process_command(cmd)
                    if result is not None:
                        self.print_success(f"Команда '{cmd}' показує нотатки")
                        break
                    else:
                        self.print_failure(f"Команда '{cmd}' не показує нотатки")
                except Exception as e:
                    if self.verbose:
                        print(f"Попередження: {e}")
            
            # Тест редагування нотатки
            edit_note_commands = [
                "редагувати нотатку",
                "edit note",
                "змінити нотатку"
            ]
            
            for cmd in edit_note_commands:
                try:
                    with patch('builtins.input', side_effect=['1', 'Оновлена нотатка', '']):
                        result = cli.process_command(cmd)
                        if result is not None:
                            self.print_success(f"Команда '{cmd}' редагує нотатку")
                            break
                        else:
                            self.print_failure(f"Команда '{cmd}' не редагує нотатку")
                except Exception as e:
                    if self.verbose:
                        print(f"Попередження: {e}")
                        
        except Exception as e:
            self.print_failure(f"Помилка в командах нотаток: {e}")
    
    def step_5_cli_interface(self):
        """Крок 5: Інтерфейс CLI."""
        self.print_step(5, "Інтерфейс CLI")
        
        if not self.dev or not hasattr(self.dev, 'PersonalAssistantCLI'):
            self.print_failure("Клас PersonalAssistantCLI не знайдено")
            return
        
        try:
            cli = self.dev.PersonalAssistantCLI()
            
            # Тест методу start/run
            if hasattr(cli, 'run'):
                try:
                    # Симулюємо запуск з негайним виходом
                    with patch('builtins.input', side_effect=['exit']):
                        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                            cli.run()
                            output = mock_stdout.getvalue()
                            
                            if "вітаю" in output.lower() or "welcome" in output.lower() or "assistant" in output.lower():
                                self.print_success("CLI показує вітальне повідомлення")
                            else:
                                self.print_failure("CLI не показує вітальне повідомлення")
                                
                            if "до побачення" in output.lower() or "goodbye" in output.lower():
                                self.print_success("CLI показує прощальне повідомлення")
                            else:
                                self.print_failure("CLI не показує прощальне повідомлення")
                                
                except Exception as e:
                    self.print_failure(f"Помилка в запуску CLI: {e}")
            else:
                self.print_failure("Метод run() відсутній")
            
            # Тест обробки помилок
            if hasattr(cli, 'process_command'):
                try:
                    # Тест з командою що може викликати помилку
                    result = cli.process_command("додай контакт з невалідними даними")
                    # Очікуємо що CLI не крашиться
                    self.print_success("CLI обробляє помилки без краху")
                except Exception as e:
                    self.print_failure(f"CLI не обробляє помилки: {e}")
            
            # Тест форматування виводу
            if hasattr(cli, 'format_output') or hasattr(cli, 'print_colored'):
                self.print_success("CLI має методи форматування виводу")
            else:
                # Не критично, але бажано
                print("⚠️  CLI може мати методи форматування виводу")
            
            # Тест збереження стану
            try:
                # Перевіряємо що менеджери зберігають дані
                if hasattr(cli.contact_manager, 'save_data') and hasattr(cli.note_manager, 'save_data'):
                    self.print_success("CLI має менеджери що зберігають дані")
                else:
                    self.print_failure("CLI не має методів збереження даних")
            except Exception as e:
                self.print_failure(f"Помилка перевірки збереження даних: {e}")
            
            # Тест загальної функціональності
            try:
                # Простий тест цілого циклу: додати контакт і знайти його
                with patch('builtins.input', side_effect=['Тест Користувач', '0501111111', '', '']):
                    add_result = cli.process_command("додай контакт")
                    
                search_result = cli.process_command("знайди контакт Тест")
                
                if add_result and search_result:
                    self.print_success("CLI виконує повний цикл операцій")
                else:
                    self.print_failure("CLI не виконує повний цикл операцій")
            except Exception as e:
                if self.verbose:
                    print(f"Попередження в тесті повного циклу: {e}")
                    
        except Exception as e:
            self.print_failure(f"Помилка в інтерфейсі CLI: {e}")
    
    def run_step(self, step_num: int):
        """Запуск конкретного кроку."""
        steps = {
            1: self.step_1_cli_init,
            2: self.step_2_command_processing,
            3: self.step_3_contact_commands,
            4: self.step_4_note_commands,
            5: self.step_5_cli_interface,
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
            print(f"\n🎉 Всі тести пройдені! Клас PersonalAssistantCLI готовий.")
        else:
            print(f"\n🔧 Є проблеми що потребують вирішення.")
            print(f"💡 Підказка: Подивіться на еталонну реалізацію у personal_assistant/cli/interface.py")

def main():
    parser = argparse.ArgumentParser(description='Поетапна перевірка класу PersonalAssistantCLI')
    parser.add_argument('--step', type=int, help='Запустити тільки певний крок (1-5)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    parser.add_argument('--compare', '-c', action='store_true', help='Порівняння з еталоном')
    
    args = parser.parse_args()
    
    print("🧪 ПОЕТАПНА ПЕРЕВІРКА КЛАСУ PERSONALASSISTANTCLI")
    print("=" * 60)
    
    if not DEV_IMPLEMENTATION:
        print("\n📝 Щоб розпочати:")
        print("1. Створіть папку: dev_implementation/cli/")
        print("2. Створіть файл: dev_implementation/cli/__init__.py")
        print("3. Створіть файл: dev_implementation/cli/interface.py")
        print("4. Імплементуйте клас PersonalAssistantCLI з усіма методами")
        return
    
    tester = CLITester(verbose=args.verbose, compare=args.compare)
    
    if args.step:
        tester.run_step(args.step)
    else:
        tester.run_all_steps()
    
    tester.show_summary()

if __name__ == "__main__":
    main()