#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстраційний скрипт для персонального помічника
Показує основні можливості програми
"""

import os
import sys
import time
from pathlib import Path

# Додаємо поточну папку в sys.path
sys.path.append(str(Path(__file__).parent))

from personal_assistant.models import Contact, Note  
from personal_assistant.managers import ContactManager, NoteManager
from personal_assistant.storage import FileStorage


def clear_screen():
    """Очищує екран консолі"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_separator(title="", char="=", length=60):
    """Виводить розділювач з заголовком"""
    if title:
        print(f"\n{char * length}")
        print(f"  {title.upper()}")
        print(f"{char * length}")
    else:
        print(f"{char * length}")


def demo_contacts(contact_manager):
    """Демонструє роботу з контактами"""
    print_separator("Демонстрація роботи з контактами")
    
    print("🔹 Створюємо декілька тестових контактів...")
    
    # Контакт 1: Іван Петров
    ivan = Contact("Іван Петров")
    ivan.add_phone("+380501234567")
    ivan.add_email("ivan.petrov@example.com")
    ivan.set_birthday("15.03.1990")
    ivan.set_address("Київ, вул. Хрещатик, 1")
    contact_manager.add_contact(ivan)
    
    # Контакт 2: Марія Коваленко
    maria = Contact("Марія Коваленко")
    maria.add_phone("+380679876543")
    maria.add_phone("+380441234567")  # Другий телефон
    maria.add_email("maria.kovalenko@gmail.com")
    maria.set_birthday("22.07.1985")
    contact_manager.add_contact(maria)
    
    # Контакт 3: Олександр Шевченко
    alex = Contact("Олександр Шевченко")
    alex.add_phone("0631112233")
    alex.add_email("alex.shevchenko@work.ua")
    alex.set_address("Львів, пл. Ринок, 5")
    contact_manager.add_contact(alex)
    
    print("✅ Контакти створено!")
    time.sleep(1)
    
    print("\n🔹 Показуємо всі контакти:")
    contacts = contact_manager.get_all_contacts()
    for i, contact in enumerate(contacts, 1):
        print(f"\n{i}. {contact}")
        print("-" * 40)
    
    time.sleep(2)
    
    print("\n🔹 Пошук контакту за іменем 'Іван':")
    found_contacts = contact_manager.search_contacts("Іван")
    for contact in found_contacts:
        print(f"Знайдено: {contact}")
    
    time.sleep(1)
    
    print("\n🔹 Пошук за телефоном '+38050':")
    found_contacts = contact_manager.search_contacts("+38050")
    for contact in found_contacts:
        print(f"Знайдено: {contact}")
    
    time.sleep(1)
    
    print("\n🔹 Найближчі дні народження (365 днів):")
    upcoming = contact_manager.get_upcoming_birthdays(365)
    for contact in upcoming:
        days = contact.days_to_birthday()
        print(f"🎂 {contact.name.value} - {contact.birthday.value} (через {days} днів)")


def demo_notes(note_manager):
    """Демонструє роботу з нотатками"""
    print_separator("Демонстрація роботи з нотатками")
    
    print("🔹 Створюємо декілька тестових нотаток...")
    
    # Нотатка 1: Робоча
    note1 = note_manager.create_note(
        title="Планування проекту",
        content="Треба розробити архітектуру нового проекту.\nОсновні компоненти:\n- API сервер\n- База даних\n- Фронтенд",
        tags=["робота", "проект", "планування", "важливо"]
    )
    
    # Нотатка 2: Особиста
    note2 = note_manager.create_note(
        title="Список покупок",
        content="Молоко\nХліб\nЯйця\nМасло\nФрукти",
        tags=["особисте", "покупки"]
    )
    
    # Нотатка 3: Навчання
    note3 = note_manager.create_note(
        title="Python tips",
        content="Корисні поради з Python:\n1. Використовуйте list comprehensions\n2. Не забувайте про docstrings\n3. PEP 8 - ваш друг",
        tags=["навчання", "python", "програмування", "важливо"]
    )
    
    # Нотатка 4: Ідеї
    note4 = note_manager.create_note(
        title="Ідеї для додатка",
        content="- Додати підтримку експорту даних\n- Реалізувати синхронізацію з хмарою\n- Покращити інтерфейс",
        tags=["ідеї", "розробка", "покращення"]
    )
    
    print("✅ Нотатки створено!")
    time.sleep(1)
    
    print("\n🔹 Показуємо всі нотатки:")
    notes = note_manager.get_all_notes()
    for index, note in notes:
        print(f"\n{index}. {note}")
        print("-" * 50)
    
    time.sleep(2)
    
    print("\n🔹 Пошук нотаток за словом 'проект':")
    found_notes = note_manager.search_notes("проект")
    for index, note in found_notes:
        print(f"Знайдено #{index}: {note.title}")
    
    time.sleep(1)
    
    print("\n🔹 Нотатки з тегом 'важливо':")
    tagged_notes = note_manager.find_notes_by_tags(["важливо"])
    for index, note in tagged_notes:
        print(f"#{index}: {note.title} - теги: {', '.join(note.tags)}")
    
    time.sleep(1)
    
    print("\n🔹 Статистика тегів:")
    tag_stats = note_manager.get_tag_statistics()
    for i, (tag, count) in enumerate(list(tag_stats.items())[:5], 1):
        print(f"{i}. {tag}: {count} разів")


def demo_statistics(contact_manager, note_manager, storage):
    """Показує статистику"""
    print_separator("Статистика системи")
    
    # Статистика контактів
    contact_stats = contact_manager.get_statistics()
    print("📞 КОНТАКТИ:")
    print(f"   Усього: {contact_stats['total_contacts']}")
    print(f"   З телефонами: {contact_stats['with_phones']}")
    print(f"   З email: {contact_stats['with_emails']}")
    print(f"   З днями народження: {contact_stats['with_birthdays']}")
    print(f"   З адресами: {contact_stats['with_addresses']}")
    
    # Статистика нотаток
    note_stats = note_manager.get_statistics()
    print("\n📝 НОТАТКИ:")
    print(f"   Усього: {note_stats['total_notes']}")
    print(f"   Унікальних тегів: {note_stats['total_tags']}")
    print(f"   Усього слів: {note_stats['total_words']}")
    print(f"   Середньо слів на нотатку: {note_stats['avg_words_per_note']}")
    
    # Інформація про сховище
    storage_info = storage.get_storage_info()
    print(f"\n💾 СХОВИЩЕ:")
    print(f"   Папка: {storage_info['data_directory']}")
    print(f"   Файлів: {storage_info['total_files']}")
    print(f"   Розмір: {storage_info['total_size_kb']} KB")


def demo_command_matching():
    """Демонструє розпізнавання команд"""
    print_separator("Демонстрація розпізнавання команд")
    
    from personal_assistant.utils.command_matcher import CommandMatcher
    
    matcher = CommandMatcher()
    
    test_phrases = [
        "знайти іван",
        "додат контак",
        "показати всі контакти", 
        "нотатки з тегом робота",
        "дні народження",
        "стат",
        "допомог",
        "вихід"
    ]
    
    print("🔹 Тестуємо розпізнавання природної мови:")
    
    for phrase in test_phrases:
        command, confidence = matcher.find_best_command(phrase)
        description = matcher.get_command_description(command) if command else "Невідома команда"
        
        print(f"\n'{phrase}'")
        print(f"  → {command} (впевненість: {confidence:.0%})")
        print(f"  → {description}")


def main():
    """Головна демонстраційна функція"""
    clear_screen()
    
    print_separator("ПЕРСОНАЛЬНИЙ ПОМІЧНИК - ДЕМОНСТРАЦІЯ", "=", 70)
    print("🤖 Автоматична демонстрація всіх можливостей програми")
    print("📋 Створено для курсу Python Programming від Neoversity")
    
    input("\n🔹 Натисніть Enter для початку демонстрації...")
    
    # Створюємо тимчасове сховище для демо
    demo_storage = FileStorage("demo_data")
    contact_manager = ContactManager(demo_storage)
    note_manager = NoteManager(demo_storage)
    
    try:
        # Демо контактів
        demo_contacts(contact_manager)
        
        input("\n🔹 Натисніть Enter для демонстрації нотаток...")
        
        # Демо нотаток  
        demo_notes(note_manager)
        
        input("\n🔹 Натисніть Enter для показу статистики...")
        
        # Статистика
        demo_statistics(contact_manager, note_manager, demo_storage)
        
        input("\n🔹 Натисніть Enter для демо розпізнавання команд...")
        
        # Демо команд
        demo_command_matching()
        
        print_separator("ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА", "=", 70)
        print("✅ Всі функції персонального помічника продемонстровано!")
        print("🚀 Для повноцінної роботи запустіть: python main.py")
        
        # Очищуємо демо-дані
        demo_storage.clear_all_data()
        
    except KeyboardInterrupt:
        print("\n\n👋 Демонстрацію перервано користувачем")
        demo_storage.clear_all_data()
    except Exception as e:
        print(f"\n❌ Помилка під час демонстрації: {e}")
        demo_storage.clear_all_data()


if __name__ == "__main__":
    main()