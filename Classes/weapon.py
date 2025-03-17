class Weapon:
    def __init__(self, name:str, damage:int, defense:int, price:int):
        self.name = name
        self.damage = damage
        self.defense = defense
        self.price = price

    def printData(self):
        return (f"{self.name} deals {self.damage} ⚔️, has {self.defense} 🛡️ and costs {self.price} 💰")