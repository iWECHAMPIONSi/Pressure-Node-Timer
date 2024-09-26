# Pressure-Node-Timer
This is for those who want an easier way to estimate when a node monster spawns.
When you start this, it's automatically set at door 0
Features:
  - Displays the current room you are at in the program
  - Displays the number of doors you have passed since the last node timer spawn
  - Displays the room number of the hiding spot
  - Displays how many rooms until X for the hiding spot
  - Displays the amount of time you have spent in a room
  - Late flicker timer based on room number
  - Displays the minimum and maximum amount of time until a node entity can spawn from node timer
  - Gives a percent chance that a node entity will spawn from the node timer
  - Rolls over into Ridge Mode when you have passed room 100
      - Displays how many doors until the Ridge is over (Assuming the Ridge is 15 doors)
      - Displays an estimated time until a node monster will spawn in the Ridge
      - Displays an estimated time until a loan angler will spawn (assuming it's a dead period)
      - Ability to toggle when blitz or a front angler spawns/despawns
          - Note that it assumes a door was opened before being toggled, as it adds 10 seconds to the spawn timer (doors subtract 10 seconds)
Hotkeys:
  '[': Press when you open a door
  ']': Press whenever a node monster despawns due to node timer
  '=': Press to set the current room to a hiding spot (Mainly for GOS and TBS)
  ';': (RIDGE ONLY) Press to toggle if blitz or a front angler spawns (remember to toggle again after they despawn)
  
