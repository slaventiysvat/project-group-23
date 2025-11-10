#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматичний демонстраційний скрипт
"""

import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from personal_assistant.models import Contact, Note  
from personal_assistant.managers import ContactManager, NoteManager
from personal_assistant.storage import FileStorage
from personal_assistant.utils.command_matcher import CommandMatcher


def print_separator(title="", char="=", length=60):
    if title:
        print(f"\n{char * length}")
        print(f"  {title.upper()}")
        print(f"{char * length}")
    else:
        print(f"{char * length}")


def main():
    print_separator("ПЕРСОНАЛЬНИЙ ПОМІЧНИК - АВТОДЕМО", "=", 70)
    print("🤖 Демонстрація всіх можливостей програми")
    
    # Створюємо тимчасове сховище
    demo_storage = FileStorage("demo_data")
    contact_manager = ContactManager(demo_storage)
    note_manager = NoteManager(demo_storage)
    
    # === КОНТАКТИ ===
    print_separator("Контакти")
    
    # Створюємо контакти
    ivan = Contact("Іван Петров")
    ivan.add_phone("+380501234567")
    ivan.add_email("ivan@example.com")
    ivan.set_birthday("15.03.1990")
    contact_manager.add_contact(ivan)
    
    maria = Contact("Марія Коваленко") 
    maria.add_phone("+380679876543")
    maria.add_email("maria@gmail.com")
    maria.set_birthday("22.07.1985")
    contact_manager.add_contact(maria)
    
    print("✅ Створено 2 тестові контакти")
    
    # Показуємо контакти
    contacts = contact_manager.get_all_contacts()
    for i, contact in enumerate(contacts, 1):
        print(f"\n{i}. {contact}")
    
    # Пошук
    print("\n🔍 Пошук за 'Іван':")
    found = contact_manager.search_contacts("Іван")
    for contact in found:
        print(f"  Знайдено: {contact.name.value}")
    
    # === НОТАТКИ ===
    print_separator("Нотатки")
    
    # Створюємо нотатки
    note1 = note_manager.create_note(
        "Робочий проект",
        "Планування архітектури системи",
        ["робота", "проект", "важливо"]
    )
    
    note2 = note_manager.create_note(
        "Python поради", 
        "Використовуйте list comprehensions та docstrings",
        ["навчання", "python", "важливо"]
    )
    
    print("✅ Створено 2 тестові нотатки")
    
    # Показуємо нотатки
    notes = note_manager.get_all_notes()
    for index, note in notes:
        print(f"\n{index}. {note}")
    
    # Пошук за тегами
    print("\n🏷️ Нотатки з тегом 'важливо':")
    tagged = note_manager.find_notes_by_tags(["важливо"])
    for index, note in tagged:
        print(f"  #{index}: {note.title}")
    
    # === РОЗПІЗНАВАННЯ КОМАНД ===
    print_separator("Розпізнавання команд")
    
    matcher = CommandMatcher()
    test_phrases = [
        "знайти іван",
        "додат контак", 
        "нотатки з тегами",
        "статистика",
        "вихід"
    ]
    
    for phrase in test_phrases:
        command, confidence = matcher.find_best_command(phrase)
        description = matcher.get_command_description(command)
        print(f"'{phrase}' → {description} ({confidence:.0%})")
    
    # === СТАТИСТИКА ===
    print_separator("Статистика")
    
    contact_stats = contact_manager.get_statistics()
    note_stats = note_manager.get_statistics()
    
    print(f"📞 Контактів: {contact_stats['total_contacts']}")
    print(f"📝 Нотаток: {note_stats['total_notes']}")
    print(f"🏷️ Унікальних тегів: {note_stats['total_tags']}")
    print(f"📊 Слів у нотатках: {note_stats['total_words']}")
    
    print_separator("ДЕМО ЗАВЕРШЕНО", "=", 70)
    print("🚀 Запустіть 'python main.py' для повної роботи!")
    
    # Очищуємо демо-дані
    demo_storage.clear_all_data()


if __name__ == "__main__":
    main()