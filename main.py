"""
Dungeon and Stone - Main Game Module

This module implements a text-based RPG where players battle monsters, collect loot, and try to survive
in a dungeon for 5 days. The game features turn-based combat, weapon management, and resource management.

Game Flow:
1. The game loads monsters and weapons from data files
2. Player creates their character
3. For 5 days, the player can:
   - Fight monsters (4 actions per day)
   - Rest to recover health
   - Shop for better weapons
   - Do nothing (risk ambush)
4. Each day ends with healing and monster difficulty increase
5. Win by surviving all 5 days, lose by dying

File Structure:
- Monsters file format: "monster_name:health damage reward" with "next" indicating new day
- Weapons file format: "weapon_name:damage defense price"
"""

import math
from contextlib import nullcontext
from importlib.resources import read_text
import os
import random
from Classes.fighter import *
from typing import List, Tuple
from Classes.fighter import Fighter
from Classes.monster import Monster
from Classes.weapon import Weapon

# Game Constants
DAYS_TO_SURVIVE = 5
ACTIONS_PER_DAY = 5
DAILY_HEALING = 15
REST_HEALING = 5
SHOP_WEAPONS = 5
AMBUSH_CHANCE_BASE = 6

def monsterSpawner(monstersList: List[List[Monster]]) -> List[List[Monster]]:
    """
    Load and initialize monsters from the Monsters file.
    
    The monsters are organized into daily pools, with each day having its own list of monsters.
    The file format is: "monster_name:health damage reward" with "next" indicating a new day.
    
    Args:
        monstersList (List[List[Monster]]): List to store daily monster pools
        
    Returns:
        List[List[Monster]]: List of daily monster pools
    """
    file_path = os.path.join(os.path.dirname(__file__), "Seeders", "Monsters")
    monsterListPerDay = []
    
    with open(file_path) as file:
        for line in file:
            if 'next' in line:
                monstersList.append(monsterListPerDay.copy())
                monsterListPerDay.clear()
                continue
                
            name, stats = line.split(':')
            health, damage, reward = map(int, stats.split())
            monster = Monster(name, health, damage, reward)
            monsterListPerDay.append(monster)
            
    return monstersList

def weaponSpawner(weaponList: List[Weapon]) -> List[Weapon]:
    """
    Load and initialize weapons from the Weapons file.
    
    The file format is: "weapon_name:damage defense price"
    
    Args:
        weaponList (List[Weapon]): List to store available weapons
        
    Returns:
        List[Weapon]: List of available weapons
    """
    file_path = os.path.join(os.path.dirname(__file__), "Seeders", "Weapons")
    
    with open(file_path) as file:
        for line in file:
            name, stats = line.split(':')
            damage, defense, price = map(int, stats.split())
            weapon = Weapon(name, damage, defense, price)
            weaponList.append(weapon)
            
    return weaponList

def handle_combat(mc: Fighter, monster: Monster) -> Tuple[int, bool]:
    """
    Handle a combat encounter between the fighter and a monster.
    
    Args:
        mc (Fighter): The player character
        monster (Monster): The monster to fight
        
    Returns:
        Tuple[int, bool]: (combat result code, whether monster was defeated)
            result codes: -1=fighter died, 0=continue fighting, 1=monster died, 2=fled
    """
    print(f'{mc.name} is fighting a/an {monster.name}!')
    monster.printData()
    result = mc.attack(monster)
    print('')
    
    while result == 0:
        print(f'{monster.name} is still alive with {monster.health} ❤️! {mc.name} has {mc.health} ❤️. Attack again?\n0-No, 1-Yes')
        try:
            atkChoice = int(input())
            if atkChoice == 0:
                print(f"{mc.name} has run away!")
                return 2, False
            elif atkChoice == 1:
                result = mc.attack(monster)
            else:
                print("Wrong input. Try again.")
        except ValueError:
            print("Please enter a valid number.")
        print('')
        
    return result, result == 1

def handle_shop(mc: Fighter, weaponList: List[Weapon]) -> None:
    """
    Handle the shop interaction where the player can buy weapons.
    
    Args:
        mc (Fighter): The player character
        weaponList (List[Weapon]): List of available weapons
    """
    print("Welcome to the shop! This is our current selection.")
    mc.printData()
    print()
    
    weaponsToday = random.sample(weaponList, k=SHOP_WEAPONS)
    for i, weapon in enumerate(weaponsToday, 1):
        print(f'{i}. {weapon.printData()}')
        
    while True:
        print("Please type 1-5 to buy the desired item.\n"
              "If you wish to exit type 6, but keep in mind that this will count as having shopped, "
              "and you won't be able to come here until tomorrow.")
        try:
            choice = int(input())
            if choice == 6:
                print("You've exited the shop without buying anything.")
                break
            elif 0 < choice < 6:
                weaponChoice = weaponsToday[choice-1]
                if mc.buying(weaponChoice) == 1:
                    weaponList.remove(weaponChoice)
                    break
            else:
                print('Wrong input, try again.')
        except ValueError:
            print("Please enter a valid number.")
        print()

def main():
    """Main game loop and initialization."""
    # Initialize game state
    monsterList = monsterSpawner([])
    weaponList = weaponSpawner([])
    
    # Display game introduction
    greetingText = '''Whether for glory, riches or martial prowess, you've decided to enter the deadly dungeon that is filled with both loot and monsters.

In order to come out alive you'll have to defeat monsters, collect the gold on them and purchase better equipment. You can't continue forever as you only have 5 days to explore the dungeon before you're stuck here forever.
You have 4 actions per day - fight, rest, shop, do nothing.
When you attack, or are getting ambushed, first it's your ⚔️ that gets dealt first, then the monster attacks, dealing their attack. The ❤️ you lose equals their ⚔️ minus your weapon's 🛡️.
You can choose to rest once per day, healing 5 ❤️.
You can only visit the store once per day. Shopping gives you 5 random weapons.
There is no limit to how many times you can do nothing, but with each time the chances to get ambushed increase- it resets on a new day.

Each playthrough the monsters will be the same, but they will get more difficult as time goes on.

Good luck 🍀'''
    print(greetingText)
    
    # Initialize player character
    mcName = input("Enter your character's name: ")
    mc = Fighter(mcName)
    
    # Main game loop
    for day in range(DAYS_TO_SURVIVE):
        print(f"Day {day + 1} out of {DAYS_TO_SURVIVE}")
        monsterListToday = monsterList[day]
        
        # Reset daily actions
        mc.hasDoneNothing = 0
        mc.hasRested = False
        mc.hasShopped = False
        
        # Daily action loop
        for action in range(ACTIONS_PER_DAY):
            print(f"Action {action + 1} out of {ACTIONS_PER_DAY}")
            mc.printData()
            print('')
            
            actName = input("Choose what to do: 1-fight, 2-rest, 3-nothing, 4-shop\n")
            print('')
            
            match actName:
                case '1':  # Fight
                    if monsterListToday:
                        monster = random.choice(monsterListToday)
                        result, monster_defeated = handle_combat(mc, monster)
                        if monster_defeated:
                            monsterListToday.remove(monster)
                    else:
                        print("No more monsters to fight today!")
                        action -= 1
                        
                case '2':  # Rest
                    if not mc.hasRested:
                        mc.rest()
                        print(f"{mc.name} has rested and regained {REST_HEALING} ❤️. They now have {mc.health} ❤️")
                    else:
                        print(f"{mc.name} has already rested!")
                        action -= 1
                        
                case '3':  # Do Nothing
                    encounterChance = random.randrange(mc.hasDoneNothing, AMBUSH_CHANCE_BASE)
                    if encounterChance == AMBUSH_CHANCE_BASE - 1 and monsterListToday:
                        monster = random.choice(monsterListToday)
                        print(f"{mc.name} has been ambushed by a {monster.name}!")
                        result, monster_defeated = handle_combat(mc, monster)
                        if monster_defeated:
                            monsterListToday.remove(monster)
                    else:
                        print(f'{mc.name} has successfully done nothing.')
                    mc.hasDoneNothing += 1
                    
                case '4':  # Shop
                    if not mc.hasShopped:
                        handle_shop(mc, weaponList)
                        mc.hasShopped = True
                    else:
                        print(f"{mc.name} has already shopped today!")
                        action -= 1
                        
                case '418':  # Easter egg
                    print('🫖')
                    return
                    
                case _:
                    print('Wrong input, try again.')
                    action -= 1
                    
            if not mc.isAlive:
                print(f"Game Over! {mc.name} has died and wasn't able to survive the dungeon.")
                mc.printData()
                return
                
        # End of day
        print(f"{mc.name} has survived the day! They gain {DAILY_HEALING} ❤️.")
        mc.health += DAILY_HEALING
        print()
        
    # Game completion
    print(f'Congratulations! {mc.name} has beaten the dungeon and has come out alive! '
          f'They are now the champion! Here are their statistics')
    mc.printData()

if __name__ == "__main__":
    main()