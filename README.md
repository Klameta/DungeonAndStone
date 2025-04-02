# Dungeon and Stone

A text-based RPG game where players battle monsters, collect loot, and try to survive in a dungeon for 5 days.

## Game Overview

Dungeon and Stone is a turn-based RPG where players take on the role of a fighter trying to survive in a dangerous dungeon. The game features:

- 5-day survival challenge
- Turn-based combat system
- Weapon management and shopping
- Monster encounters with varying difficulty
- Resource management (health, money)

## Game Mechanics

### Core Features
- Players have 4 actions per day: fight, rest, shop, or do nothing
- Combat system based on weapon damage (⚔️) and defense (🛡️)
- Health (❤️) management through resting and daily recovery
- Gold (💰) collection from defeated monsters
- Shop system for purchasing better weapons

### Daily Actions
1. **Fight**: Battle a random monster from the current day's pool
2. **Rest**: Heal 5 ❤️ (once per day)
3. **Shop**: Get 5 random weapon choices (once per day)
4. **Do Nothing**: Risk getting ambushed (chance increases with each use)

### Combat System
- Combat is turn-based
- Damage calculation: Monster's ⚔️ - Weapon's 🛡️ = Health lost
- Players can choose to continue fighting or flee
- Defeating monsters rewards gold and increases kill count

## Project Structure

```
DungeonAndStone/
├── Classes/
│   ├── fighter.py    # Player character class
│   ├── monster.py    # Monster class
│   └── weapon.py     # Weapon class
├── Seeders/
│   ├── Monsters      # Monster data
│   └── Weapons       # Weapon data
└── main.py           # Game logic and main loop
```

## Getting Started

1. Ensure you have Python 3.x installed
2. Clone the repository
3. Run the game:
   ```bash
   python main.py
   ```

## Game Controls

- 1: Fight
- 2: Rest
- 3: Do Nothing
- 4: Shop
- 418: Easter Egg (Exit)

## Contributing

Feel free to submit issues and enhancement requests!
