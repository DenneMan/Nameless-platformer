import json, random
import universal

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
        if self.exp >= self.exp_to_level_up:
            surplus = self.exp - self.exp_to_level_up
            self.exp = surplus
            self.level += 1
            self.exp_to_level_up = 500 + self.level ** 2 * 25
            universal.scene_manager.scenes[-1].state = 'upgrading'
            pu1 = random.randint(0, 24)
            pu2 = random.randint(0, 24)
            pu3 = random.randint(0, 24)
            while pu2 == pu1:
                pu2 = random.randint(0, 24)
            while pu3 == pu1 and pu3 != pu2:
                pu3 = random.randint(0, 24)
            universal.scene_manager.scenes[-1].upgrade_choices = [pu1, pu2, pu3]
        print(f'{self.level}, {self.exp}/{self.exp_to_level_up}')
    def save(self):
        with open('test.json', 'w') as f:
            f.write('{\n' + f'    \"level\":{10},\n' + f'    \"exp\":{100},\n' + f'    \"money\":{1000}\n' + '}')
