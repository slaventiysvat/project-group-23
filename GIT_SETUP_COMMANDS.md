# 🚀 Git Setup Commands для завантаження на GitHub

## Якщо у вас вже є GitHub репозиторій:
```bash
# Додайте remote origin (замініть YOUR_USERNAME та YOUR_REPO на ваші)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Завантажте на GitHub
git push -u origin master
```

## Якщо потрібно створити новий репозиторій на GitHub:

### Крок 1: Створіть репозиторій на GitHub.com
1. Зайдіть на https://github.com
2. Натисніть "New repository"
3. Назвіть репозиторій: `neoversity-personal-assistant` (або як забажаєте)
4. НЕ створюйте README.md, .gitignore або license (вони вже є)
5. Натисніть "Create repository"

### Крок 2: Підключіть локальний репозиторій
```bash
# Замініть YOUR_USERNAME на ваш GitHub username
git remote add origin https://github.com/YOUR_USERNAME/neoversity-personal-assistant.git
git branch -M main
git push -u origin main
```

## Альтернатива - використання SSH (рекомендовано):
```bash
# Замініть YOUR_USERNAME на ваш GitHub username
git remote add origin git@github.com:YOUR_USERNAME/neoversity-personal-assistant.git
git branch -M main  
git push -u origin main
```

## Перевірка стану:
```bash
# Перевірити remote репозиторії
git remote -v

# Перевірити поточний branch
git branch

# Перевірити статус
git status
```

## Додавання нових файлів в майбутньому:
```bash
# Додати нові файли
git add .

# Зафіксувати зміни
git commit -m "Опис змін"

# Завантажити на GitHub
git push origin main
```

## Робота з гілками (для командної розробки):
```bash
# Створити нову гілку для завдання
git checkout -b feature/task-01-fields

# Працювати над завданням...
git add .
git commit -m "Implement Field classes"

# Завантажити гілку на GitHub
git push origin feature/task-01-fields

# На GitHub створити Pull Request для review та merge
```

## Клонування для нових учасників команди:
```bash
# Клонувати репозиторій
git clone https://github.com/YOUR_USERNAME/neoversity-personal-assistant.git

# Зайти в папку
cd neoversity-personal-assistant

# Встановити віртуальне середовище
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Встановити залежності
pip install -r requirements.txt

# Запустити тести
python -m pytest tests/

# Запустити додаток
python main.py
```