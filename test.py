import json

with open('test.json', 'w') as f:
    f.write('{\n' + f'    \"level\":{10},\n' + f'    \"exp\":{100},\n' + f'    \"money\":{1000}\n' + '}')