from Classes.weapon import *
from Classes.monster import *


class Fighter:
    def __init__(self, name:str):
        self.name = name
        self.health = 10
        self.money = 2
        weapon = Weapon('Fists',2,0,0)
        self.weapon = weapon
        self.isAlive = True
        self.kills = 0
        self.hasDoneNothing = 0
        self.hasRested = False
        self.hasShopped = False

    def attack(self, monster:Monster):
        """
        returns -1 if fighter is dead; 0 if no one dies; 1 if monster dies
        :param monster:
        :return:
        """
        monster.health-= self.weapon.damage
#if monster is killed
        if(monster.health<=0):
            self.money += monster.reward
            self.kills+=1;
            print(f"{monster.name} has been slain! {self.name} has gained {monster.reward} 💰.")
            return 1
#else it attacks
        if(self.weapon.defense<monster.damage):
            if monster.damage - self.weapon.damage>0:
                self.health-= monster.damage- self.weapon.defense
            if(self.health<=0):
                self.isAlive = False

                print(f"{self.name} tried to kill {monster.name} and has died in combat. RIP 🪦")
                return -1
        return 0

    def buying(self, weapon:Weapon):
        if weapon.price<= self.money:
            self.money-= weapon.price
            self.weapon = weapon
            return 1

        print("Not enough funds!")
        return 0

    def rest(self):
        self.health+=5
        self.hasRested= True


    def printData(self):
        output =(f"{self.name} has {self.health} ❤️ and {self.money} 💰"
                 f" and wields {self.weapon.name} with {self.weapon.damage} ⚔️ and {self.weapon.defense} 🛡️.\n"
                 f"They have killed {self.kills} 👾 and today has done nothing {self.hasDoneNothing} times.\n")
        if self.hasRested:
            output+=(f"They have already rested today.\n")
        else:
            output+=(f"They havent rested today.\n")
        if self.hasShopped:
            output += (f"They have already shopped today.")
        else:
            output += (f"They havent shopped today.")
        print(output);