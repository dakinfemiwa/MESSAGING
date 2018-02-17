import json

with open('config.json') as jsonConfig:
    config = json.load(jsonConfig)
print('INFO: Choose a colour:')
print('1: White')
print('2: Red')
print('3: Blue')
print('4: Green')
print('5: Yellow')
print('6: Purple')
print('7: Orange')
colourInput = input('-> ')
if colourInput == '1':
    config['window']['theme'] = '#FFFFFF'
elif colourInput == '2':
    config['window']['theme'] = '#FF0000'
elif colourInput == '3':
    config['window']['theme'] = '#00BFFF'
elif colourInput == '4':
    config['window']['theme'] = '#7CFC00'
elif colourInput == '5':
    config['window']['theme'] = '#FFFF00'
elif colourInput == '6':
    config['window']['theme'] = '#8A2BE2'
elif colourInput == '7':
    config['window']['theme'] = '#FF8C00'
        
with open('config.json', 'w') as jsonConfig:
    jsonConfig.write(json.dumps(config, indent=8))
