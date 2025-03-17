class Monster:
    def __init__(self, name:str, health:int, damage:int, reward:int):
        self.name = name
        self.health = health
        self.damage = damage
        self.reward = reward

    def printData(self):
        print(f'{self.name} has {self.health} ❤️, deals {self.damage} ⚔️ and gives {self.reward} 💰')