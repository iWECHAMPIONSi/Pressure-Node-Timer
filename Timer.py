import time, os
from pynput import keyboard
# Instructions: Anytime an angler spawns due to the node timer (meaning that it isn't likely due to late flicker)
# Press "]", Any time you open a door, press "[", and when fangler or blitz spawns in the ridge, press ";" to toggle, 
# (make sure to toggle off after)

start = time.time_ns()

average_time = 480
doors_opened = 0
current_doors = 0
global_percentage = 0
late_flick = 0
ridge = False
angler_timer = 50
fangler = False
loan_angler = 300
prev_angler = 0
current_door_time = time.time_ns()
hiding_spot = 0

def on_door():
    global doors_opened, current_doors, late_flick, prev_angler, angler_timer, current_door_time
    doors_opened += 1
    current_doors += 1
    late_flick = 3
    if 80 > doors_opened >= 20:
        late_flick = 30
    elif 100 >= doors_opened >= 80:
        late_flick = 60
    temp = angler_timer
    prev_angler = temp + 10
    if prev_angler > 50:
        prev_angler = 50
    angler_timer -= 10
    current_door_time = time.time_ns()

def on_spawn():
    global global_percentage, average_time, current_doors, late_flick, angler_timer, loan_angler
    current_doors = 0
    global_percentage = 0
    average_time = 480
    late_flick = 0
    angler_timer = 50
    loan_angler = 300
    
def on_hiding():
    global hiding_spot
    hiding_spot = doors_opened

def on_fangler():
    global fangler, angler_timer
    if not fangler:
        angler_timer = prev_angler
    fangler = not fangler

door_key = keyboard.HotKey(
    keyboard.HotKey.parse('['),
    on_door)

spawn_key = keyboard.HotKey(
    keyboard.HotKey.parse(']'),
    on_spawn)

hiding_key = keyboard.HotKey(
    keyboard.HotKey.parse('='),
    on_hiding)

fangler_key = keyboard.HotKey(
    keyboard.HotKey.parse(';'),
    on_fangler)



def for_door(f):
    return lambda k: f(door_listener.canonical(k))

def for_spawn(f):
    return lambda k: f(spawn_listener.canonical(k))

def for_hiding(f):
    return lambda k: f(hiding_listener.canonical(k))

def for_fangler(f):
    return lambda k: f(fangler_listener.canonical(k))

door_listener = keyboard.Listener(
        on_press=for_door(door_key.press),
        on_release=for_spawn(door_key.release))
door_listener.start()

spawn_listener = keyboard.Listener(
    on_press=for_spawn(spawn_key.press),
    on_release=for_spawn(spawn_key.release))
spawn_listener.start()

hiding_listener = keyboard.Listener(
    on_press=for_hiding(hiding_key.press),
    on_release=for_hiding(hiding_key.release))
hiding_listener.start()

fangler_listener = keyboard.Listener(
    on_press=for_fangler(fangler_key.press),
    on_release=for_fangler(fangler_key.release))
fangler_listener.start()

while True:
    if not fangler:
        angler_timer -= (time.time_ns() - start)/1000000000
        loan_angler -= (time.time_ns() - start)/1000000000
    average_time -= (time.time_ns() - start)/1000000000
    late_flick -= (time.time_ns() - start)/1000000000
    start = time.time_ns()
    room_timer = (start - current_door_time)/1000000000
    if doors_opened == 101:
        ridge = True
        doors_opened = 1
        angler_timer = 50
        fangler = False
        loan_angler = 300
        prev_angler = 50
    
    until_X = 5 - (doors_opened - hiding_spot)
    if not ridge:
        if average_time <= 0:
            average_time = 0
        if late_flick <= 0:
            late_flick = 0
        upper_limit = 30 * current_doors
        lower_limit = 15 * current_doors
        time_range = upper_limit - lower_limit
        upper_chance = average_time - upper_limit
        chance = 0
        if upper_chance < 0:
            chance = abs(upper_chance/time_range)
        global_percentage = chance
        status = ""
        if global_percentage == 0:
            status = "All clear!"
        elif .25 >= global_percentage > 0:
            status = "Likely safe, but be cautious"
        elif .5 > global_percentage > .25:
            status = "Be cautious, it's advised that you wait for a safe room before pushing"
        elif .75 >= global_percentage >= .5:
            status = "DANGER! A spawn is likely, you might want to wait for a spawn before moving up!"
        elif 1 > global_percentage > .75:
            status = "A spawn is almost gauranteed, prepare your party for a spawn!"
        else:
            status = "A SPAWN IS GAURANTEED NEXT AVAILABLE ROOM!"
        disp_time1 = average_time - upper_limit
        if disp_time1 < 0:
            disp_time1 = 0
        disp_time2 = average_time - lower_limit
        if disp_time2 < 0:
            disp_time2 = 0
        if global_percentage > 1:
            global_percentage = 1
        os.system('cls')
        print("Current door:", doors_opened, '\n'
            "Doors since last timer spawn:", current_doors, '\n'
            "Current hiding spot: Room", hiding_spot, '\n'
            "Doors until X:", until_X, '\n'
            "Time spent in room:", str(round(room_timer)) + "sec", '\n'
            "Late flicker timer:", str(round(late_flick)), '\n'
            "Max time remaining:", str(round(disp_time2)) + "sec", '\n'
            "Min time remaining:", str(round(disp_time1)) + "sec", '\n'
            "Node spawn chance:", str(round(global_percentage * 100, 2)) + '%', '\n'
            "Status:", status, '\n'
            "Keys: '[' is to advance a door, ']' is for when a node monster despawns due to node timer, '=' is to move hiding spot to current room")
    else:
        if angler_timer < 0:
            angler_timer = 0
        disp_time1 = angler_timer - 15
        if disp_time1 < 0:
            disp_time1 = 0
        if loan_angler < 0:
            loan_angler = 0
        status = ""
        if angler_timer > 45:
            status = "It is safe to move up a group 1-2 rooms"
        elif angler_timer > 35:
            status = "It is riskey to move a group up more than 1 room"
        elif angler_timer > 25:
            status = "It's not advised to move up a group"
        elif angler_timer > 0:
            status = "Prepare group for a spawn"
        else:
            status = "Possible dead period, watch for loan anglers"
        os.system('cls')
        print("RIDGE MODE", '\n'
              "Current door:", str(doors_opened) + "/15", '\n'
              "Current hiding spot: Room", str(hiding_spot) + "/15", '\n'
              "Doors until X:", until_X, '\n'
              "Time until normal angler:", round(angler_timer), '\n'
              "Time until angler variant can spawn:", round(disp_time1), '\n'
              "Loan angler timer (rough estimation):", round(loan_angler), '\n'
              "Front angler or blitz:", fangler, '\n'
              "Status:", status, '\n'
              "Keys: '[' is to advance a door, ']' is for when an angler variant despawns, ';' is to toggle front angler/blitz, '=' is to set hiding spot")
