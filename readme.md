## Terrains

- Lava
- Water
- Ice
- Obstacle
- Rubble
- Empty

## Entities

- 1-6: Your heroes
- A: Monster (killed in 1 hit)
- B: Monster (killed in 2 hits)
- C: Monster (killed in 3 hits)
- D: Monster (killed in 4 hits)

## Definitions


- Barrier: Anything a hero cannot move through (lava, water, block, rubble, monster)
- Chokepoint: An empty square in-between barriers or the edge of the map and empty squares in the other cardinal directions
- Deadend: A chokepoint where the path from one side to the other is only possible through the chokepoint
- Section: A part of the map seperated from other sections by barries.
- Zone: A part of the map within a section where a hero can move. Zones are seperated by deadends. 
- Deadend Zone: A deadend by itself is a seperate zone.
- Pivot hero: The hero moving first.
- Movable hero: The non-pivot heroes

## Exmaple Terrain Map

An example terrain map where 'O' = obstacle, '.' = empty square, 'c' = chokepoint, 'd' = deadend:

...O..
...O..
OOOO..
..d...
..O...
..OcOc
OOO...
......

In this example map, there are 2 sections. One section with 1 zone and another with 3 zones:

111 AA
111 AA
    AA
CCBAAA
CC AAA
CC A A
   AAA
AAAAAA

1: Section 1 (1 zone)
A: Section 2 Zone A
B: Section 2 Zone B (this is a deadend zone)
C: Section 2 Zone C

## Attack Types

- 1: Melee
- 2: Ranged
- 3: Melee/Ranged
- 4: Magic

## Support Type

- 1: Heal
- 2: Heal + Linger
- 3: Linger
- 4: Def buff
- 5: Def buff + Linger
- 6: Atk buff

## Classes

**Name          Atk Type    Main Dir    Alt Dir     Spt Type    Spt Dir**
- Monk          1           8
- Knight        1           4
- Warrior       1           4
- Assassin      1           4
- Guardian      1           4
- Rogue         1           8
- Pirate        3           8           4
- Ranger        2           8
- Archer        2           4
- Hunter        2           4
- Javeliner     3           4
- Mage          4           4
- Wizard        4           4
- Elementalist  4           8
- Warlock       3           4
- Healer        3           4
- Paladin       1           4
- Druid         1           4
- Princess      1           8
- Bard          3           8

## Rules

A pivot hero moves first
A pivot hero can move anywhere in his section
Movable heroes in the same section as the pivot can move anywhere in their zone
Movable heroes in the same section as the pivot can also move to any deadend zone connected to their zone
    (as long as the pivot does not pass through that deadend zone to the other zone)


## Algorithm

Init
    Parse the inputs into useable objects
Indentification
    Identify the chokepoints
    Identify the deadends by searching for alternate paths through the chokepoints
    Identify the zones by walking through the empty squares
        (Any left over empty squares not zoned will be seperate section(s))
        Repeat for all sections until all empty squares are assigned
Calculating Configurations
    Starting with the pivot hero
        Iterate through the available configurations of hero placements using the rules
            Calculate move difficulty for each configuration
            Calculate damage assessment for each configuration

## Damage Assessment



## Move Difficulty

**Simple**

- How many squares the pivot is displaced
- How many heroes the pivot moves
- How many squares the movable heroes are displaced

**Advanced**

- How many squares the pivot moves
- How many corners the pivot turns
- How many heroes the pivot moves
- How many squares the movable heroes move
- How many corners the movable heroes move

