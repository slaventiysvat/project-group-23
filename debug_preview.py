content = 'Контент з розширеними функціями'
max_length = 20

print(f'Content: "{content}"')
print(f'Length: {len(content)}')

truncated = content[:max_length]
print(f'Truncated: "{truncated}"')

last_space = truncated.rfind(' ')
print(f'Last space at: {last_space}')
print(f'Half max_length: {max_length // 2}')

if last_space > max_length // 2:
    final = truncated[:last_space]
    print(f'Cut at space: "{final}"')
else:
    final = truncated
    print(f'No space cut: "{final}"')

result = final + "..."
print(f'Result: "{result}"')
print(f'Contains target: {"Контент з розширеними" in result}')