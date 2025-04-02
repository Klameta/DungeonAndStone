from Classes.weapon import *
from Classes.monster import *


class Fighter:
    """
    A class representing the player character in the game.
    
    The Fighter class manages the player's stats, combat abilities, and daily actions.
    It handles health, money, weapon management, and tracks various game state variables.
    
    Attributes:
        name (str): The fighter's name
        health (int): Current health points (❤️)
        money (int): Current gold (💰)
        weapon (Weapon): Currently equipped weapon
        isAlive (bool): Whether the fighter is still alive
        kills (int): Number of monsters defeated
        hasDoneNothing (int): Number of times "do nothing" action was used today
        hasRested (bool): Whether the fighter has rested today
        hasShopped (bool): Whether the fighter has visited the shop today
    """
    
    def __init__(self, name: str):
        """
        Initialize a new Fighter instance.
        
        Args:
            name (str): The fighter's name
        """
        self.name = name
        self.health = 10
        self.money = 2
        weapon = Weapon('Fists', 2, 0, 0)
        self.weapon = weapon
        self.isAlive = True
        self.kills = 0
        self.hasDoneNothing = 0
        self.hasRested = False
        self.hasShopped = False

    def attack(self, monster: Monster) -> int:
        """
        Attack a monster and handle combat resolution.
        
        The attack deals damage equal to the weapon's damage stat.
        If the monster survives, it counter-attacks dealing damage equal to
        its damage stat minus the weapon's defense.
        
        Args:
            monster (Monster): The monster to attack
            
        Returns:
            int: Combat result code
                -1: Fighter died
                0: No one died (combat continues)
                1: Monster died
        """
        monster.health -= self.weapon.damage
        if monster.health <= 0:
            self.money += monster.reward
            self.kills += 1
            print(f"{monster.name} has been slain! {self.name} has gained {monster.reward} 💰.")
            return 1
            
        if self.weapon.defense < monster.damage:
            damage_taken = monster.damage - self.weapon.defense
            if damage_taken > 0:
                self.health -= damage_taken
            if self.health <= 0:
                self.isAlive = False
                print(f"{self.name} tried to kill {monster.name} and has died in combat. RIP 🪦")
                return -1
        return 0

    def buying(self, weapon: Weapon) -> int:
        """
        Attempt to purchase a new weapon.
        
        Args:
            weapon (Weapon): The weapon to purchase
            
        Returns:
            int: Purchase result code
                0: Not enough money
                1: Purchase successful
        """
        if weapon.price <= self.money:
            self.money -= weapon.price
            self.weapon = weapon
            return 1

        print("Not enough funds!")
        return 0

    def rest(self) -> None:
        """
        Rest to recover health.
        
        Heals 5 health points and marks the fighter as having rested for the day.
        """
        self.health += 5
        self.hasRested = True

    def printData(self) -> None:
        """
        Print the fighter's current stats and status.
        
        Displays health, money, weapon stats, kill count, and daily action status.
        """
        output = (f"{self.name} has {self.health} ❤️ and {self.money} 💰"
                 f" and wields {self.weapon.name} with {self.weapon.damage} ⚔️ and {self.weapon.defense} 🛡️.\n"
                 f"They have killed {self.kills} 👾 and today has done nothing {self.hasDoneNothing} times.\n")
        if self.hasRested:
            output += (f"They have already rested today.\n")
        else:
            output += (f"They haven't rested today.\n")
        if self.hasShopped:
            output += (f"They have already shopped today.")
        else:
            output += (f"They haven't shopped today.")
        print(output)