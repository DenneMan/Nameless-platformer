import json

class Level():
    def __init__(self):
        self.filename = 'save.json'
        with open(self.filename, 'r') as f:
            data = json.load(f)
            self.level = data['level']
            self.exp = data['exp']
            self.money = data['money']
        self.exp_to_level_up = 500 + self.level ** 2 * 25
    def give_exp(self, amount):
        self.exp += amount
        if self.exp > self.exp_to_level_up:
            surplus = self.exp_to_level_up - self.exp
            self.exp = surplus
            self.level += 1
            self.exp_to_level_up = 500 + self.level ** 2 * 25
    def save(self):
        with open('test.json', 'w') as f:
            f.write('{\n' + f'    \"level\":{10},\n' + f'    \"exp\":{100},\n' + f'    \"money\":{1000}\n' + '}')
