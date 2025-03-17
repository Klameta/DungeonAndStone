import math
from contextlib import nullcontext
from importlib.resources import read_text
import os
import random
from Classes.fighter import *

def monsterSpawner(monstersList):
    file_path = os.path.join(os.path.dirname(__file__), "Seeders", "Monsters")
    monsterListPerDay= [];
    with open(file_path) as file:
        for line in file:
            if 'next' in line:
                monstersTemp = monsterListPerDay.copy()
                monstersList.append(monstersTemp)

                monsterListPerDay.clear()
                continue
            mNameAndStats = line.split(':')
            monsterStats = mNameAndStats[1].split()
            monsterStats = [int(stat) for stat in monsterStats]

            monster = Monster(mNameAndStats[0], monsterStats[0], monsterStats[1], monsterStats[2])

            monsterListPerDay.append(monster)
    return monstersList

def weaponSpawner(weaponList):
    file_path = os.path.join(os.path.dirname(__file__), "Seeders", "Weapons")
    with open(file_path) as file:
        for line in file:
            mNameAndStats = line.split(':')
            weaponStats = mNameAndStats[1].split()
            weaponStats = [int(stat) for stat in weaponStats]

            weapon = Weapon(mNameAndStats[0], weaponStats[0], weaponStats[1], weaponStats[2])

            weaponList.append(weapon)
    return weaponList
#Declaring and seeding
dayCnt = 0;
monsterList = []
monsterList = monsterSpawner(monsterList)

weaponList = []
weaponList = weaponSpawner(weaponList)


greetingText = '''Whether for glory, riches or martial prowess, you've decided to enter the deadly dungeon that is filled with both loot and monsters.

In order to come out alive you'll have to defeat monsters, collect the gold on them and purchase better equipment. You cant continue for forever as you only have 5 days to explore the dungeon before you're stuck here forever.
You have 4 actions per day - fight, rest, shop, do nothing.
When you attack, or are getting ambushed, first it's your ⚔️ that gets dealt first, then the monster attacks, dealing their attack. The ❤️ you lose equals their ⚔️ minus your weapon's 🛡.️
You can choose to rest once per day, healing 5 ❤️.
You can only visit the store once per day. Shopping gives you 5 random weapons.
There is no limit to how many times you can do nothing, but with each time the chances to get ambushed increase- it resets on a new day.

Each playthrough the monsters will be the same, but they will get more difficult as time goes on.

Good luck 🍀''';
print(greetingText)
mcName = input("Enter your character's name: ")
mc = Fighter(mcName)

while(dayCnt<5):
    print(f"Day {dayCnt+1} out of 5")
    monsterListToday = monsterList[dayCnt]

    mc.hasDoneNothing=0
    mc.hasRested=False
    mc.hasShopped = False
    hasShopped = False
    actCnt =0;

    while(actCnt<5):
        print(f"Action {actCnt +1} out of 5")
        mc.printData()
        print('')
        actName = input(f"Choose what to do: 1-fight, 2-rest, 3-nothing, 4-shop\n")
        print('')
        match actName:
            case '1':
                #Fighting
                monster = random.choice(monsterListToday)
                print(f'{mc.name} is fighting a/an {monster.name}!')
                monster.printData()
                result = mc.attack(monster)
                print('')
                while result == 0:
                    print(f'{monster.name} is still alive with {monster.health} ❤️! {mc.name} has {mc.health} ❤️. Attack again?\n0-No, 1-Yes')
                    atkChoice = (int)(input())
                    if atkChoice == 0:
                        print(f"{mc.name} has run away!")
                        result = 2
                    elif atkChoice ==1:
                        result = mc.attack(monster)
                    else:
                        print("Wrong input. Try again.")
                    print('')
                if result == 1 or result== 0:
                    monsterListToday.remove(monster)
            case '2':
                if not mc.hasRested:
                    mc.rest()
                    print(f"{mc.name} has rested and regained 5 ❤️. They now have {mc.health} ❤️")
                else:
                    print(f"{mc.name} has already rested!")
                    actCnt-=1
            case '3':
                #Doing nothing
                #Each time that the mc does nothing, the chance to land on a 5 increces. If it lands on a 5 that means that an encounter will happen
                encounterChance = random.randrange(mc.hasDoneNothing, 6)
                if encounterChance ==5:
                    monster = random.choice(monsterListToday)
                    print(f"{mc.name} has been ambushed by a {monster.name}!")
                    result = mc.attack(monster)
                    while result == 0:
                        print(f'{monster.name} is still alive with {monster.health} ❤️! {mc.name} has {mc.health} ❤️. Attack again?\n0-No, 1-Yes')
                        atkChoice = (int)(input())
                        if atkChoice == 0:
                            print(f"{mc.name} has run away!")
                            result =2
                        else:
                            result = mc.attack(monster)
                    if result == 1 or result ==0:
                        monsterListToday.remove(monster)
                else:
                    print(f'{mc.name} has succsefully done nothing.')
                mc.hasDoneNothing+=1
            case '4':
                if not mc.hasShopped:
                    print("Welcome to the shop! This is our current selection.")
                    mc.printData()
                    print()
                    weaponsToday = random.sample(weaponList, k=5)
                    wCnt =1
                    for weapon in weaponsToday:
                        print(f'{wCnt}. {weapon.printData()}')
                        wCnt+=1
                    choiceResult = -1;

                    while choiceResult <1:
                        print("Please type 1-5 to buy the desired item.\n"
                              "If you wish to exit type 6, but keep in mind that this will count as having shopped, and you wont be able to come here until tomorrow.")
                        choice = (int)(input())

                        if choice == 6:
                            print("You've exited the shop without buying anything.")
                            choiceResult = 1
                        elif choice>0 and choice<6:
                            weaponChoice = weaponsToday[choice-1]
                            choiceResult= mc.buying(weaponChoice)
                            if choiceResult ==1:
                                weaponList.remove(weaponChoice)
                        else:
                            print('Wrong input, try again.')
                            print()
                    mc.hasShopped = True
            case '418':
                print('🫖')
                exit()
            case _:
                print(f'Wrong input, try again.')
                actCnt-=1
        if not mc.isAlive:
            print(f"Game Over! {mc.name} has died and wasn't able to survive the dungeon.")
            mc.printData()
            exit()
        actCnt+=1
    print(f"{mc.name} has survied the day! They gains 15 ❤️.")
    mc.health +=15
    print()
    dayCnt+=1
print(f'Congratulations! {mc.name} has beaten the dungeon and has come out alive! They are now the champion! Here are their statistics')
mc.printData()