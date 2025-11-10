# 📄 TASK CARD #11: ДОПОМІЖНІ ФАЙЛИ

**Розробник**: DevOps або Junior Developer  
**Файли**: `main.py`, `setup.py`, `requirements.txt`, `README.md`  
**Пріоритет**: 🟢 НИЗЬКИЙ  
**Час**: 1 день  
**Складність**: ⭐

---

## 📋 ЗАВДАННЯ

Створити допоміжні файли для правильного розгортання, встановлення та використання персонального помічника як повноцінного Python проекту.

## 🎯 МЕТА

Забезпечити:
- Легке встановлення та запуск програми
- Правильне управління залежностями
- Зрозумілу документацію для користувачів
- Можливість створення executable файлу
- Готовність до розповсюдження

## 📦 ФАЙЛИ ДО СТВОРЕННЯ

### 1. main.py - точка входу:
```python
#!/usr/bin/env python3
"""
Персональний помічник від команди Neoversity.

Головний файл для запуску персонального помічника з CLI інтерфейсом.
Підтримує управління контактами та нотатками з розумним розпізнаванням команд.
"""

import sys
import os
from pathlib import Path

# Додавання поточної директорії до Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from personal_assistant.cli import PersonalAssistantCLI
except ImportError as e:
    print(f"❌ Помилка імпорту: {e}")
    print("Переконайтеся що всі файли проекту на місці")
    sys.exit(1)

def main():
    """Головна функція запуску програми."""
    try:
        print("🚀 Запуск персонального помічника...")
        assistant = PersonalAssistantCLI()
        assistant.run()
    except KeyboardInterrupt:
        print("\n👋 До побачення! Програму завершено користувачем.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        print("Зверніться до розробників для вирішення проблеми")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 2. setup.py - конфігурація пакета:
```python
"""
Setup configuration for Personal Assistant project.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Читаємо README для опису пакета
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Читаємо requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split('\n')
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="personal-assistant-neoversity",
    version="1.0.0",
    description="Персональний помічник з управлінням контактами та нотатками",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Інформація про автора
    author="Neoversity Project Group 1",
    author_email="group1@neoversity.com",  # Замініть на реальний email
    
    # URLs
    url="https://github.com/neoversity/personal-assistant",  # Замініть на реальний repo
    project_urls={
        "Documentation": "https://github.com/neoversity/personal-assistant/wiki",
        "Source": "https://github.com/neoversity/personal-assistant",
        "Tracker": "https://github.com/neoversity/personal-assistant/issues",
    },
    
    # Пакети та залежності
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    
    # Додаткові залежності
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0", 
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0"
        ],
        "build": [
            "pyinstaller>=5.0.0",
            "setuptools>=60.0.0",
            "wheel>=0.37.0"
        ]
    },
    
    # Entry points для console commands
    entry_points={
        "console_scripts": [
            "personal-assistant=main:main",
            "pa=main:main",  # Коротка команда
        ],
    },
    
    # Включення додаткових файлів
    include_package_data=True,
    package_data={
        "personal_assistant": [
            "data/*.json",
            "templates/*.txt",
        ],
    },
    
    # Метадані
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10", 
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
        "Environment :: Console",
        "Natural Language :: Ukrainian",
    ],
    
    # Ключові слова
    keywords=[
        "personal assistant", "contacts", "notes", "cli", "ukraine",
        "персональний помічник", "контакти", "нотатки", "консоль"
    ],
    
    # Ліцензія
    license="MIT",
    
    # Zip safety
    zip_safe=False,
)
```

### 3. requirements.txt - залежності:
```txt
# Основні залежності для роботи програми
colorama>=0.4.6

# Опціональні залежності для розширеної функціональності  
# python-dateutil>=2.8.2  # Для покращеної роботи з датами
# fuzzywuzzy>=0.18.0       # Для покращеного fuzzy matching
# python-Levenshtein>=0.20.0  # Для швидших fuzzy операцій

# Залежності для розробки (встановлювати з pip install -e ".[dev]")
# pytest>=7.0.0
# pytest-cov>=4.0.0
# black>=22.0.0
# flake8>=5.0.0
# mypy>=1.0.0

# Залежності для збірки executable (pip install -e ".[build]")  
# pyinstaller>=5.0.0
# setuptools>=60.0.0
# wheel>=0.37.0
```

### 4. README.md - документація:
```markdown
# 🤖 Персональний помічник

Інтелектуальний персональний помічник з управлінням контактами та нотатками, створений командою студентів Neoversity.

## ✨ Особливості

- 📞 **Управління контактами**: Додавання, редагування, пошук контактів
- 📝 **Система нотаток**: Створення, організація та пошук нотаток з тегами  
- 🤖 **Розумне розпізнавання**: AI-powered розпізнавання команд українською та англійською
- 🎨 **Красивий інтерфейс**: Кольоровий CLI з інтуїтивною навігацією
- 💾 **Надійне збереження**: Автоматичне збереження з backup системою
- 🔍 **Потужний пошук**: Full-text пошук по всіх даних
- 📊 **Аналітика**: Детальна статистика та звіти

## 🚀 Швидкий старт

### Встановлення

```bash
# Клонування репозиторію
git clone https://github.com/neoversity/personal-assistant.git
cd personal-assistant

# Встановлення залежностей
pip install -r requirements.txt

# Запуск програми
python main.py
```

### Перші кроки

1. **Додайте контакт**:
   ```
   📱 Введіть команду: додай контакт
   ```

2. **Створіть нотатку**:
   ```
   📱 Введіть команду: нова нотатка
   ```

3. **Подивіться довідку**:
   ```
   📱 Введіть команду: допомога
   ```

## 📋 Команди

### Контакти
- `додай контакт` - Додавання нового контакту
- `знайди контакт [ім'я]` - Пошук контакту
- `всі контакти` - Показати всі контакти  
- `редагуй контакт [ім'я]` - Редагування контакту
- `видали контакт [ім'я]` - Видалення контакту
- `дні народження [дні]` - Майбутні дні народження

### Нотатки
- `додай нотатку` - Створення нової нотатки
- `знайди нотатки [текст]` - Пошук в нотатках
- `всі нотатки` - Показати всі нотатки
- `нотатки з тегом [тег]` - Пошук за тегами
- `редагуй нотатку [номер]` - Редагування нотатки
- `видали нотатку [номер]` - Видалення нотатки

### Системні
- `статистика` - Детальна статистика даних
- `допомога` - Показати довідку
- `вихід` - Завершити програму

## 💡 Приклади використання

### Робота з контактами
```bash
📱 Введіть команду: додай контакт
👤 Ім'я контакту: Іван Петров  
☎️ Телефон: +380501234567
📧 Email (Enter щоб пропустити): ivan@example.com
🎂 День народження (DD.MM.YYYY): 15.03.1990
🏠 Адреса (Enter щоб пропустити): вул. Хрещатик, 1
✅ Контакт "Іван Петров" додано успішно!
```

### Робота з нотатками
```bash
📱 Введіть команду: нова нотатка
📝 Заголовок: Python Tutorial
📄 Зміст: Вивчення основ програмування на Python
🏷️ Теги (через кому): python, навчання, програмування
✅ Нотатку "Python Tutorial" створено!
```

## 🛠️ Розробка

### Встановлення для розробки

```bash
# Клонування та встановлення в development режимі
git clone https://github.com/neoversity/personal-assistant.git
cd personal-assistant
pip install -e ".[dev]"
```

### Запуск тестів

```bash
# Всі тести
pytest tests/

# З coverage звітом
pytest tests/ --cov=personal_assistant --cov-report=html
```

### Форматування коду

```bash
# Автоматичне форматування
black personal_assistant/ tests/

# Перевірка стилю
flake8 personal_assistant/ tests/

# Type checking
mypy personal_assistant/
```

## 📊 Архітектура

```
personal_assistant/
├── models/          # Моделі даних (Contact, Note, Field classes)
├── managers/        # Бізнес-логіка (ContactManager, NoteManager)  
├── storage/         # Збереження даних (FileStorage)
├── utils/           # Утиліти (validators, CommandMatcher)
├── cli.py          # CLI інтерфейс
└── __init__.py

tests/              # Unit та інтеграційні тести
data/               # Файли даних (створюються автоматично)
docs/               # Документація
```

## 🔧 Конфігурація

Програма створює папку `data/` для збереження:
- `contacts.json` - Файл з контактами
- `notes.json` - Файл з нотатками  
- `*.backup` - Backup файли

## 📈 Системні вимоги

- **Python**: 3.9 або новіший
- **ОС**: Windows, macOS, Linux
- **RAM**: Мінімум 256 MB
- **Диск**: 50 MB вільного місця
- **Terminal**: Підтримка Unicode (для кольорів та емодзі)

## 🤝 Команда розробки

Проект створено командою студентів **Neoversity Project Group 1**:

- Backend Developer #1 - Field classes, Contact model
- Backend Developer #2 - FileStorage, ContactManager  
- Backend Developer #3 - Note model, NoteManager
- Senior Developer - CommandMatcher, CLI Interface
- QA Engineer - Testing, Quality Assurance
- Junior Developer - Utilities, Setup

## 📄 Ліцензія

Цей проект ліцензований під MIT License - див. [LICENSE](LICENSE) файл.

## 🐛 Повідомлення про баги

Знайшли баг? [Створіть issue](https://github.com/neoversity/personal-assistant/issues) або напишіть на group1@neoversity.com

## 🙏 Подяки

Дякуємо **Neoversity** за навчання та підтримку в розробці цього проекту!

---

**Зроблено з ❤️ командою Neoversity Project Group 1**
```

### 5. .gitignore - виключення файлів:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
data/
*.json
*.backup
logs/
temp/
```

### 6. LICENSE - ліцензія MIT:
```text
MIT License

Copyright (c) 2024 Neoversity Project Group 1

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🔧 ДОДАТКОВІ СКРИПТИ

### build.py - скрипт для збірки:
```python
"""
Скрипт для створення executable файлу.
"""

import subprocess
import sys
from pathlib import Path

def build_executable():
    """Створення executable за допомогою PyInstaller."""
    
    print("🔨 Створення executable файлу...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console", 
        "--name", "PersonalAssistant",
        "--icon", "icon.ico",  # якщо є іконка
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executable створено в папці dist/")
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка при створенні executable: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
```

### dev_setup.py - налаштування для розробки:
```python
"""
Скрипт для швидкого налаштування development середовища.
"""

import subprocess
import sys
from pathlib import Path

def setup_dev_environment():
    """Налаштування середовища для розробки."""
    
    print("🛠️ Налаштування development середовища...")
    
    # Встановлення в editable режимі з dev залежностями
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])
    
    # Налаштування pre-commit hooks (якщо потрібно)
    # subprocess.run(["pre-commit", "install"])
    
    print("✅ Development середовище готове!")
    print("📋 Доступні команди:")
    print("  pytest tests/          - Запуск тестів")
    print("  black .                - Форматування коду") 
    print("  flake8 .               - Перевірка стилю")
    print("  mypy personal_assistant/ - Type checking")

if __name__ == "__main__":
    setup_dev_environment()
```

## ✅ КРИТЕРІЇ ПРИЙНЯТТЯ

### Функціональні вимоги:
- [ ] `main.py` правильно запускає програму
- [ ] `setup.py` дозволяє встановлювати проект як пакет
- [ ] `requirements.txt` містить всі необхідні залежності
- [ ] `README.md` містить повну документацію користувача
- [ ] Console scripts працюють після встановлення

### Технічні вимоги:
- [ ] Підтримка Python 3.9+
- [ ] Правильна обробка помилок в `main.py`
- [ ] Метадані в `setup.py` заповнені правильно
- [ ] `.gitignore` виключає непотрібні файли
- [ ] Entry points налаштовані для зручного запуску

### Якісні вимоги:
- [ ] Документація зрозуміла для користувачів
- [ ] Встановлення працює на різних ОС
- [ ] Executable можна створити через PyInstaller
- [ ] Code style перевіряється linters

## 🧪 ТЕСТОВІ СЦЕНАРІЇ

### Встановлення та запуск:
```bash
# Тест встановлення
pip install -e .

# Тест console scripts
personal-assistant --help  # або pa --help
python main.py

# Тест залежностей
python -c "import colorama; print('✅ colorama imported')"
```

### Створення executable:
```bash
# Встановлення build залежностей  
pip install -e ".[build]"

# Створення executable
python build.py

# Тест executable
./dist/PersonalAssistant  # Linux/Mac
dist\PersonalAssistant.exe  # Windows
```

### Валідація метаданих:
```bash
# Перевірка setup.py
python setup.py check --strict --metadata

# Створення source distribution
python setup.py sdist

# Створення wheel
python setup.py bdist_wheel
```

## 📁 СТРУКТУРА ПІСЛЯ ЗАВЕРШЕННЯ

```
personal-assistant/
├── main.py                 # ✅ Точка входу
├── setup.py               # ✅ Конфігурація пакета
├── requirements.txt       # ✅ Залежності
├── README.md             # ✅ Документація
├── LICENSE               # ✅ Ліцензія MIT
├── .gitignore           # ✅ Git виключення
├── build.py             # ✅ Скрипт збірки
├── dev_setup.py         # ✅ Development setup
├── personal_assistant/   # 📦 Основний пакет
├── tests/               # 🧪 Тести  
└── docs/                # 📚 Додаткова документація
```

## 🚀 ГОТОВНІСТЬ ДО ЗДАЧІ

### Checklist:
- [ ] Всі обов'язкові файли створені
- [ ] Документація повна та зрозуміла
- [ ] Встановлення працює через pip
- [ ] Console commands функціонують
- [ ] Executable можна створити
- [ ] Метадані правильно заповнені
- [ ] Git repository готовий для публікації

**Фінальний штрих** - робить проект готовим до розповсюдження та використання!