# Friends & Dragons

This script will determine the top bests moves in the App Friends & Dragons.

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

- Obstacle: Anything a hero cannot move through (lava, water, block, rubble, monster)
- Chokepoint: An empty square in-between barriers or the edge of the map and at least one empty 
    square in the other cardinal directions
- Deadend: DE: A chokepoint where the path from one side to the other is only possible through the 
    chokepoint, or if it is next to another deadend if only one empty square is adjacent
- Section: A part of the map separated from other sections by barries
- Zone: A part of the map within a section where a hero can move. Zones are seperated by deadends.
- Deadend Zone: A zone of one square that is a deadend (also just called a deadend)
- Pivot hero: The hero moving first (also just called pivot)
- Movable hero: The non-pivot heroes (also just called hero)
- Pivot point: The current point of the pivot being evaluated
- Pivot deadend: PDE: 
- Moveable point: The current point of the movable hero being evaluated
- Main Path: Shortest path from the pivot's starting zone to the current pivot point being 
    evaluated. This is the main path of the pivot that he must make.
- Alt Path: Shortest path from the pivot's starting zone to the starting zone of a native hero. 
    These are alternate paths that the pivot must move through to move all moveable heroes but 
    the pivot will move back to the original start after doing so and continue through the main 
    path.
- Native hero: Heroes that are in a zone of the main path
- Stranded hero: Heroes that are in the same section as the pivot hero but not in the main path
- Alien hero: Heroes that are in a different section than the pivot hero
- Downstream: Any item in a list that is further than a designated point (e.g. 20 is downstream from 8 in this list: [1,3,5,6,8,2,20,28,13])
- Upstream: Any item in a list that is previous than a designated point (e.g. 3 is upstream from 8 in this list: [1,3,5,6,8,2,20,28,13])


## Example Terrain Map

An example terrain map where 'O' = obstacle, '.' = empty square, 'c' = chokepoint, 'd' = deadend:

```
...O..
...O..
OOOO..
..d...
..O...
..OcOc
OOO...
......
```

In this example map, there are 2 sections. One section with 1 zone and another with 3 zones:

```
111 AA
111 AA
    AA
CCBAAA
CC AAA
CC A A
   AAA
AAAAAA
```

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

| Name | Atk Type | Main Dir | Alt Dir | Spt Type | Spt Dir |
|-|-|-|-|-|-|
| Monk | 1 | 8 | | | | |
| Monk | 1 | 8 | | | |
| Knight | 1 | 4 | | | |
| Warrior | 1 | 4 | | | |
| Assassin | 1 | 4 | | | |
| Guardian | 1 | 4 | | | |
| Rogue | 1 | 8 | | | |
| Pirate | 3 | 8 | 4 | | |
| Ranger | 2 | 8 | | | |
| Archer | 2 | 4 | | | |
| Hunter | 2 | 4 | | | |
| Javeliner | 3 | 4 | | | |
| Mage | 4 | 4 | | | |
| Wizard | 4 | 4 | | | |
| Elementalist | 4 | 8 | | | |
| Warlock | 3 | 4 | | | |
| Healer | 3 | 4 | | | |
| Paladin | 1 | 4 | | | |
| Druid | 1 | 4 | | | |
| Princess | 1 | 8 | | | |
| Bard | 3 | 8 | | | |

## Algorithm

Init
    Parse the inputs into useable objects
Indentification
    Identify the chokepoints
    Identify the deadends
    Identify the zones
    Identify the sections
    Identify the shortests paths from all zones to each other zones
Move Init
    Identify all allowable moves of the pivot hero
    Identify all allowable moves of the moveable heros
Brute Force Loop:
    Pivot hero loop through all allowable points (current pivot point)
        # Current moveable points:
        Hero 2 loop through all allowable points
            Hero 3 loop through all allowable points
                Hero 4 loop through all allowable points
                    Hero 5 loop through all allowable points
                        Hero 6 loop through all allowable points
                            Evaluate configuration and move difficulty

## Move Rules

A pivot hero moves first and can move anywhere in his section. The loop for the pivot hero evaluates all 
allowable points of the pivot hero. The current point being evaluated here is called the current pivot point.

All other heroes move in their allowable moves until all configurations have been evaluated. These points are 
called the current moveable points.

## 

Pivot hero can move anywhere in his section. The obstacle board he uses corresponds to his traits. For example, a lava walker will use the board_lava.
Moveable heroes can move anywhere in their zones if in the same section as the pivot, else they cannot move. A moveable hero with the same trait
    as the pivot hero will use that same board. For example, if the pivot and the movable hero are a lava walker, both will use the board_lava as their
    obstacle board.
Moveable heroes can move to some deadends considering the following:
    Case 1: Native hero:
        A moveable hero can move to any deaded connected to his starting zone if the deadend zone is not in the main path. 
        He can also move to any deadend lower on the main path stack. For example, if the main path is
        3-5d-6-8d-9, this means the pivot starts in zone 3, moves through zone 5 which is a deadend, to zone 6,
        through zone 8 another deadend, and landing in zone 9. In such a case, if a moveable hero starts in zone 6, 
        he can move to zone 5d but not to 8d.
    Case 2: Stranded hero:
        A moveable hero can move to any deaded connected to his starting zone if the deadend zone is not in the alt path. 
        He can also move to any deadend higher on the alt path stack. For example, if the alt path is
        3-10d-11-15d-16, this means the pivot starts in zone 3, moves through zone 10 which is a deadend, to zone 11,
        through zone 15 another deadend, and landing in zone 16. In such a case, if a moveable hero starts in zone 11, 
        he can move to zone 15d but not to 10d.
    
## Move cases

A hero can always move anywhere in his start zone if in the same section as the pivot. In addition:

Hero on Main path (2 cases):

Hero starts on a deadend zone: 
    If there is a previous zone:
        Anywhere in previous zone
        Any connected deadend in the previous zone (except his start zone)

Hero starts on a nondeadend zone: 
    Any connected deadend (except the downstream deadend)

=================================================
Hero on Alt path (cases):

Case 1: Hero starts on a deadend zone: 
    case 1a: previous zone on the alt path is a deadend zone:
        <none>
    case 1b: previous zone on the alt path is a nondeadend zone on the main path:
        hero can move to any square in the previous zone
        hero can move to any connected deadend zone to the previous zone (except downstream from the previous zone on the main path)
    case 1c: previous zone on the alt path is a nondeadend zone not on the main path:
        hero can move to any square in the previous zone
        hero can move to any connected deadend zone to the previous zone (except upstream from the previous zone on the alt path)

Case 2: Hero starts on a nondeadend zone: 
    Any connected deadend zone (except upstream from the alt path)

## Pivot walker moving basic heros

PDE = pivot deadend

Both the pivot and the hero will have different maps (pivot map, hero map)

If the pivot has a path through his map to reach the hero:
    The hero can move to anywhere in his current zone
    if the hero is on a non-PDE:
        The hero can move to any connected zone in his section as long as the zone point is not a PDE 
    if the hero is on a PDE or if a PDE is connected to the hero's connected zones:    
            Case 1: The pivot path goes to or through the PDE
                The hero can move to the zones upstream from the PDE
            Case 2: The pivot path doesn't go to or through the PDE
                The hero can occupy the PDE and the connected zone to the left or up from the PDE
            Case 2b: The pivot path doesn't go through the PDE, pivot is on the right or down
                The hero can occupy the PDE and the connected zone to the right or down from the PDE


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

