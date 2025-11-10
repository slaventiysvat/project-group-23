# 🧪 СИСТЕМА ПОЕТАПНОГО ТЕСТУВАННЯ (Reference Tests)

Ця система дозволяє розробникам поетапно створювати код, перевіряючи кожен метод окремо з еталонною реалізацією. 

## 📁 Структура

```
reference_tests/
├── README.md                    # Цей файл
├── step_by_step/               # Поетапні тести
│   ├── step_01_field.py        # ✅ Тести Field класів
│   ├── step_02_contact.py      # ✅ Тести Contact класу
│   ├── step_03_note.py         # ✅ Тести Note класу
│   ├── step_04_storage.py      # ✅ Тести FileStorage
│   ├── step_05_contact_manager.py # ✅ Тести ContactManager
│   ├── step_06_note_manager.py # ✅ Тести NoteManager
│   ├── step_07_command_matcher.py # ✅ Тести CommandMatcher
│   └── step_08_cli.py          # ✅ Тести CLI
├── tools/                      # Допоміжні інструменти
│   ├── validator.py            # Порівняння з еталоном
│   ├── setup_helper.py         # Налаштування середовища
│   ├── diff_tool.py            # Порівняння файлів
│   └── quick_test.py           # Швидкі тести
└── validators/                 # Валідатори компонентів
    └── (буде додано)
```

## � Швидкий старт

### 1. Налаштування середовища
```powershell
# Створити базову структуру
python reference_tests/tools/setup_helper.py

# Налаштувати тільки Field компонент
python reference_tests/tools/setup_helper.py --component field
```

### 2. Розробка Field класів
```powershell
# Поетапна розробка та тестування
python reference_tests/step_by_step/step_01_field.py

# Тестування конкретного кроку
python reference_tests/step_by_step/step_01_field.py --step 2

# Детальний вивід з порівнянням
python reference_tests/step_by_step/step_01_field.py --verbose --compare
```

### 3. Швидке тестування окремих методів
```powershell
# Тест конкретного класу
python reference_tests/tools/quick_test.py Name "іван петров"
python reference_tests/tools/quick_test.py Phone "0501234567"

# Інтерактивний режим
python reference_tests/tools/quick_test.py --interactive

# Множинні тести
python reference_tests/tools/quick_test.py Name --multiple
```

### 4. Порівняння з еталоном
```powershell
# Валідація всіх Field класів
python reference_tests/tools/validator.py field

# Порівняння файлів
python reference_tests/tools/diff_tool.py field.py
python reference_tests/tools/diff_tool.py field.py --side-by-side --analysis

# Запуск всіх кроків до певного моменту
python reference_tests/tools/test_runner.py --up-to step_03
```

## 🔧 Принципи роботи

### 1. Поетапність
Кожен тест перевіряє тільки один аспект:
- ✅ Один метод
- ✅ Одну функцію  
- ✅ Один сценарій

### 2. Еталонне порівняння
```python
# Твій код
result = your_contact.add_phone("+380501234567")

# Еталонний код
reference_result = reference_contact.add_phone("+380501234567")

# Порівняння
assert result == reference_result
```

### 3. Детальний фідбек
```
❌ Тест не пройшов: Contact.add_phone()

🔍 Очікуваний результат:
   contact.phones = [Phone("+380501234567")]
   
📊 Твій результат:  
   contact.phones = [Phone("380501234567")]  # ❌ Без нормалізації +
   
💡 Підказка: Перевір нормалізацію номера в Phone.__init__()
```