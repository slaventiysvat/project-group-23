content = 'Контент з розширеними функціями'
print(f'Content length: {len(content)}')

preview = content[:20].strip() + '...'
print(f'Preview: "{preview}"')
print(f'Preview length: {len(preview)}')
print('Contains test:', 'Контент з розширеними' in preview)

# Перевіримо реальну поведінку
from dev_implementation.models.note import Note
note = Note("Розширена нотатка", "Контент з розширеними функціями")
preview = note.get_preview(20)
print(f'Real preview: "{preview}"')
print('Real contains test:', 'Контент з розширеними' in preview)