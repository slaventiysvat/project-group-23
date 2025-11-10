"""
Тести для персонального помічника
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from personal_assistant.models.contact import Contact
from personal_assistant.models.note import Note
from personal_assistant.managers.contact_manager import ContactManager
from personal_assistant.managers.note_manager import NoteManager
from personal_assistant.storage.file_storage import FileStorage


class TestContact(unittest.TestCase):
    """Тести для класу Contact"""
    
    def setUp(self):
        """Підготовка даних для тестів"""
        self.contact = Contact("Іван Петров")
    
    def test_contact_creation(self):
        """Тест створення контакту"""
        self.assertEqual(self.contact.name.value, "Іван Петров")
        self.assertEqual(len(self.contact.phones), 0)
        self.assertEqual(len(self.contact.emails), 0)
        self.assertIsNone(self.contact.birthday)
        self.assertIsNone(self.contact.address)
    
    def test_add_phone(self):
        """Тест додавання телефону"""
        self.contact.add_phone("+380501234567")
        self.assertEqual(len(self.contact.phones), 1)
        self.assertEqual(self.contact.phones[0].value, "+380501234567")
    
    def test_add_duplicate_phone(self):
        """Тест додавання дублікату телефону"""
        self.contact.add_phone("+380501234567")
        with self.assertRaises(ValueError):
            self.contact.add_phone("+380501234567")
    
    def test_add_email(self):
        """Тест додавання email"""
        self.contact.add_email("ivan@example.com")
        self.assertEqual(len(self.contact.emails), 1)
        self.assertEqual(self.contact.emails[0].value, "ivan@example.com")
    
    def test_set_birthday(self):
        """Тест встановлення дня народження"""
        self.contact.set_birthday("15.03.1990")
        self.assertIsNotNone(self.contact.birthday)
        self.assertEqual(self.contact.birthday.value, "15.03.1990")
    
    def test_days_to_birthday(self):
        """Тест підрахунку днів до дня народження"""
        self.contact.set_birthday("15.03.1990")
        days = self.contact.days_to_birthday()
        self.assertIsInstance(days, int)
        self.assertGreaterEqual(days, 0)


class TestNote(unittest.TestCase):
    """Тести для класу Note"""
    
    def test_note_creation(self):
        """Тест створення нотатки"""
        note = Note("Тестова нотатка", "Це тестовий зміст", ["тест", "робота"])
        
        self.assertEqual(note.title, "Тестова нотатка")
        self.assertEqual(note.content, "Це тестовий зміст")
        self.assertEqual(len(note.tags), 2)
        self.assertIn("тест", note.tags)
        self.assertIn("робота", note.tags)
    
    def test_add_tag(self):
        """Тест додавання тегу"""
        note = Note("Тест")
        note.add_tag("важливо")
        
        self.assertIn("важливо", note.tags)
    
    def test_search_in_content(self):
        """Тест пошуку у змісті"""
        note = Note("Заголовок", "Це важлива інформація про роботу")
        
        self.assertTrue(note.search_in_content("важлива"))
        self.assertTrue(note.search_in_content("роботу"))
        self.assertFalse(note.search_in_content("неіснуюче"))


class TestFileStorage(unittest.TestCase):
    """Тести для класу FileStorage"""
    
    def setUp(self):
        """Підготовка тимчасової папки для тестів"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.temp_dir)
    
    def tearDown(self):
        """Очищення тимчасової папки після тестів"""
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_data(self):
        """Тест збереження та завантаження даних"""
        test_data = {"name": "Тест", "value": 42}
        
        # Зберігаємо дані
        self.storage.save_data("test", test_data)
        
        # Завантажуємо дані
        loaded_data = self.storage.load_data("test")
        
        self.assertEqual(loaded_data, test_data)
    
    def test_file_exists(self):
        """Тест перевірки існування файлу"""
        self.assertFalse(self.storage.file_exists("nonexistent"))
        
        self.storage.save_data("test", {"data": "value"})
        self.assertTrue(self.storage.file_exists("test"))


class TestContactManager(unittest.TestCase):
    """Тести для класу ContactManager"""
    
    def setUp(self):
        """Підготовка тимчасового сховища для тестів"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.temp_dir)
        self.manager = ContactManager(self.storage)
    
    def tearDown(self):
        """Очищення тимчасової папки після тестів"""
        shutil.rmtree(self.temp_dir)
    
    def test_add_contact(self):
        """Тест додавання контакту"""
        contact = Contact("Тест Контакт")
        self.manager.add_contact(contact)
        
        self.assertEqual(len(self.manager), 1)
        self.assertIn("тест контакт", self.manager)
    
    def test_find_contact(self):
        """Тест пошуку контакту"""
        contact = Contact("Іван Петров")
        self.manager.add_contact(contact)
        
        found_contact = self.manager.find_contact("Іван Петров")
        self.assertIsNotNone(found_contact)
        self.assertEqual(found_contact.name.value, "Іван Петров")
    
    def test_remove_contact(self):
        """Тест видалення контакту"""
        contact = Contact("Тест Видалення")
        self.manager.add_contact(contact)
        
        self.assertTrue(self.manager.remove_contact("Тест Видалення"))
        self.assertEqual(len(self.manager), 0)


class TestNoteManager(unittest.TestCase):
    """Тести для класу NoteManager"""
    
    def setUp(self):
        """Підготовка тимчасового сховища для тестів"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.temp_dir)
        self.manager = NoteManager(self.storage)
    
    def tearDown(self):
        """Очищення тимчасової папки після тестів"""
        shutil.rmtree(self.temp_dir)
    
    def test_create_note(self):
        """Тест створення нотатки"""
        note = self.manager.create_note("Тест", "Зміст тесту", ["тест"])
        
        self.assertEqual(len(self.manager), 1)
        self.assertEqual(note.title, "Тест")
        self.assertIn("тест", note.tags)
    
    def test_search_notes(self):
        """Тест пошуку нотаток"""
        self.manager.create_note("Перша", "Важлива інформація", ["робота"])
        self.manager.create_note("Друга", "Особиста замітка", ["особисте"])
        
        results = self.manager.search_notes("важлива")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1].title, "Перша")
    
    def test_find_notes_by_tags(self):
        """Тест пошуку нотаток за тегами"""
        self.manager.create_note("Робоча", "Зміст", ["робота", "важливо"])
        self.manager.create_note("Особиста", "Зміст", ["особисте"])
        
        results = self.manager.find_notes_by_tags(["робота"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1].title, "Робоча")


if __name__ == "__main__":
    unittest.main()