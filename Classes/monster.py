class Monster:
    """
    A class representing a monster in the game.
    
    Monsters are the primary enemies that the player must defeat.
    Each monster has stats that determine its combat capabilities and rewards.
    
    Attributes:
        name (str): The monster's name
        health (int): Current health points (❤️)
        damage (int): Attack power (⚔️)
        reward (int): Gold (💰) given when defeated
    """
    
    def __init__(self, name: str, health: int, damage: int, reward: int):
        """
        Initialize a new Monster instance.
        
        Args:
            name (str): The monster's name
            health (int): Starting health points
            damage (int): Attack power
            reward (int): Gold reward when defeated
        """
        self.name = name
        self.health = health
        self.damage = damage
        self.reward = reward

    def printData(self) -> None:
        """
        Print the monster's current stats.
        
        Displays the monster's name, health, damage, and reward values.
        """
        print(f'{self.name} has {self.health} ❤️, deals {self.damage} ⚔️ and gives {self.reward} 💰')