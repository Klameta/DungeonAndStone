class Weapon:
    """
    A class representing a weapon in the game.
    
    Weapons are equipment that determine the player's combat capabilities.
    Each weapon has stats that affect damage dealt and damage taken.
    
    Attributes:
        name (str): The weapon's name
        damage (int): Attack power (⚔️)
        defense (int): Damage reduction (🛡️)
        price (int): Cost in gold (💰)
    """
    
    def __init__(self, name: str, damage: int, defense: int, price: int):
        """
        Initialize a new Weapon instance.
        
        Args:
            name (str): The weapon's name
            damage (int): Attack power
            defense (int): Damage reduction
            price (int): Cost in gold
        """
        self.name = name
        self.damage = damage
        self.defense = defense
        self.price = price

    def printData(self) -> str:
        """
        Get a string representation of the weapon's stats.
        
        Returns:
            str: Formatted string containing the weapon's name, damage, defense, and price
        """
        return (f"{self.name} deals {self.damage} ⚔️, has {self.defense} 🛡️ and costs {self.price} 💰")