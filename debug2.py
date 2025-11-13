content = 'Контент з розширеними функціями'
max_length = 20

print(f'Content[{max_length}]: "{content[max_length]}"')  # Символ на позиції 20
print(f'Looking for space backwards from position {max_length}...')

cutoff = max_length
while cutoff > 0 and cutoff < len(content) and content[cutoff] != ' ':
    print(f'  Position {cutoff}: "{content[cutoff]}"')
    cutoff -= 1

print(f'Found space at position: {cutoff}')
if cutoff > 0:
    print(f'Character at cutoff: "{content[cutoff]}"')
    print(f'Substring: "{content[:cutoff]}"')