content = 'Контент з розширеними функціями'
print(f'Full content: "{content}"')
print(f'Content length: {len(content)}')

target = 'Контент з розширеними'
print(f'Target: "{target}"')
print(f'Target length: {len(target)}')

for i in range(15, 25):
    cut = content[:i]
    print(f'{i:2}: "{cut}" - contains: {target in cut}')