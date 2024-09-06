import os
import pickle
import signal
import threading
import time
import keyboard
import pyautogui
import win32api, win32con
from pyautogui import *
import zmq

num_towers = 101

script_dir = os.path.dirname(os.path.abspath(__file__))

hero = 0
boomerang = 1
tack = 2
glue = 3
sub = 4
plane = 5
dartMonkey = 6
canon = 7
ice = 8
sniper = 9
boat = 10
heli = 11
mortar = 12
wizard = 13
ninja = 14
druid = 15
factory = 16
engineer = 17
turret = 18
super = 19
alchemist = 20
farm = 21
village = 22
dino = 23

key_binds = ['u', 'w', 'r', 'y', 'x', 'v', 'q', 'e', 't', 'z', 'c', 'b', 'n', 'a', 'd', 'g', 'j', 'l', 'm', 's', 'f', 'h', 'k', 'i']

pc_resolution = (2560, 1440)


leftColumnLocation = int(2340 * pc_resolution[0] / 2560)
lowerRowLocations = int(200 * pc_resolution[0] / 2560)

bottom_left = (45 * pc_resolution[0] / 2560, 1430 * pc_resolution[1] / 1440)

def click(x, y):
    x = int(x)
    y = int(y)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.09)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

on_top = True

def place(monkey, x, y, individual):
    global on_top
    global fitness_val
    try:
        try:
            check_defeat()
            return
        except pyautogui.ImageNotFoundException:
            sleep(0.01)
        keyboard.press_and_release(key_binds[monkey])
        # just trust me that these three sleeps cannot be reduced
        sleep(0.09)
        click(x  * pc_resolution[0] / 2560, y * pc_resolution[1] / 1440)
        sleep(0.08)
        click(x  * pc_resolution[0] / 2560, y * pc_resolution[1] / 1440)
        sleep(0.08)
        try:
            sell = os.path.join(script_dir, 'sell.png')
            pyautogui.locateOnScreen(sell, confidence=0.8)
            if monkey != hero:
                individual['placed_towers'].append([x, y, monkey])
            #click(bottom_left[0], bottom_left[1])
        except pyautogui.ImageNotFoundException:
            sleep(0.08)
            fitness_val -= 9
            click(2550 * pc_resolution[0] / 2560, 15 * pc_resolution[1] / 1440)
    except pyautogui.ImageNotFoundException:
        sleep(0.01)
    sleep(0.08)

def upgrade(individual, upgrade_index):
    global fitness_val
    #sleep(0.05)
    try:
        check_defeat()
        return
    except pyautogui.ImageNotFoundException:
        sleep(0.05)
    try:
        monkey = individual['placed_towers'][individual['upgrades'][upgrade_index][0] % len(individual['placed_towers'])]
        index = individual['placed_towers'].index(monkey)
        try:
            sell = os.path.join(script_dir, 'sell.png')
            sleep(0.06) # these two must be at least > 0.5
            sell_location = pyautogui.locateOnScreen(sell, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            click(monkey[0]  * pc_resolution[0] / 2560, monkey[1] * pc_resolution[1] / 1440)
        try:
            sell = os.path.join(script_dir, 'sell.png')
            sleep(0.08) # these two must be at least > 0.5
            sell_location = pyautogui.locateOnScreen(sell, confidence=0.8)
            upgrade_location = (sell_location[0] + 170 * pc_resolution[0] / 2560, sell_location[1] - 130 * pc_resolution[1] / 1440 - (individual['upgrades'][upgrade_index][1] * 200 * pc_resolution[1] / 1440))
            click(upgrade_location[0], upgrade_location[1])
            fitness_val += 1
            sleep(0.01)
            if(monkey != individual['placed_towers'][individual['upgrades'][upgrade_index + 1][0] % len(individual['placed_towers'])]):
                click(bottom_left[0], bottom_left[1])
        except pyautogui.ImageNotFoundException:
            sleep(0.01)
    except:
        sleep(0.01)
    sleep(0.05)

def fitness(individual):
    round_number = 1
    global fitness_val
    global restart
    # global individual_number
    # global threshold_for_next_generation_index
    # global threshold_for_next_generation
    # individual_number += 1
    # print("Individual #" + str(individual_number))
    # print(str(population_size - individual_number) + " individuals left in this generation")
    # print("Current weakest individual that is advancing to the next generation has a score of: " + str(threshold_for_next_generation))
    restart = False
    fitness_val = 0
    tower_index = 0
    upgrade_index = 0
    if individual['fitness_val'] > 0:# and replay == False:
        return individual['fitness_val']
    click(leftColumnLocation, lowerRowLocations)
    # for _ in range(numScrollsToGoFromTopToBottom):
    #     pyautogui.scroll(1)
    global on_top
    on_top = True
    #start_time = time.time()
    while True:
        # while exit_event.isSet():
        #     sleep(1)
        #here it checks if it won, if it does continue to freeplay
        try:
            check_victory()
        except pyautogui.ImageNotFoundException:
            #here it checks if it lost, if it did hand the controller to the next player
            try:
                check_game_over()
                print(fitness_val)
                fitness_val = int(fitness_val)
                individual['fitness_val'] = fitness_val
                # if fitness_val > threshold_for_next_generation:
                #     # print(GREEN + "This individual made it to the next generation!" + RESET)
                #     threshold_for_next_generation_index -= 1
                #     threshold_for_next_generation = population[threshold_for_next_generation_index]['fitness_val']
                # else:
                #     print(RED + "This individual did not make it to the next generation :(" + RESET)
                return fitness_val
            except pyautogui.ImageNotFoundException:
                sleep(0.001)
            try:
                check_defeat()
                restart_round()
                print(fitness_val)
                int(fitness_val)
                individual['fitness_val'] = fitness_val
                # if fitness_val > threshold_for_next_generation:
                #     print(GREEN + "This individual made it to the next generation!" + RESET)
                #     threshold_for_next_generation_index -= 1
                #     threshold_for_next_generation = population[threshold_for_next_generation_index]['fitness_val']
                # else:
                #     print(RED + "This individual did not make it to the next generation :(" + RESET)
                return fitness_val
            except pyautogui.ImageNotFoundException:
                sleep(0.001)
            #if it didn't lose, check if it's a new round
            try:
                tower_index, upgrade_index = start_round(individual, round_number, tower_index, upgrade_index)
                if individual['fitness_val'] > 0 or restart:#and replay == False or restart:
                    return fitness_val
                round_number += 1
                fitness_val += 100
                #end_time = time.time()
                #fitness_val -= end_time - start_time
                #start_time = end_time
            except pyautogui.ImageNotFoundException:
                sleep(0.25)

def check_victory():
    victory = os.path.join(script_dir, 'victory.png')
    next = os.path.join(script_dir, 'next.png')
    ok = os.path.join(script_dir, 'ok.png')
    freeplay = os.path.join(script_dir, 'freeplay.png')
    pyautogui.locateOnScreen(victory, confidence=0.8)
    try:
        next_location = pyautogui.locateOnScreen(next, confidence=0.8)
        click(next_location[0], next_location[1])
        sleep(2)
        ok_location = pyautogui.locateOnScreen(ok, confidence=0.8)
        click(ok_location[0], ok_location[1])
        sleep(2)
    except:
        sleep(1)
    freeplay_location = pyautogui.locateOnScreen(freeplay, confidence=0.8)
    click(freeplay_location[0], freeplay_location[1])
    sleep(1)

def check_game_over():
    try:
        game_over = os.path.join(script_dir, 'game_over.png')
        next = os.path.join(script_dir, 'next.png')
        pyautogui.locateOnScreen(game_over, confidence=0.8)
        next_location = pyautogui.locateOnScreen(next, confidence=0.8)
        click(next_location[0], next_location[1])
        sleep(0.75)
        restart = os.path.join(script_dir, 'restart.png')
        restartPrompt = os.path.join(script_dir, 'restartPrompt.png')
        restart_location = pyautogui.locateOnScreen(restart, confidence=0.8)
        click(restart_location[0], restart_location[1])
        sleep(0.75)
        restartPrompt_location = pyautogui.locateOnScreen(restartPrompt, confidence=0.8)
        click(restartPrompt_location[0], restartPrompt_location[1])
        sleep(0.75)
    except pyautogui.ImageNotFoundException:
        game_over = os.path.join(script_dir, 'game_over2.png')
        pyautogui.locateOnScreen(game_over, confidence=0.8)
        restart = os.path.join(script_dir, 'restart.png')
        restartPrompt = os.path.join(script_dir, 'restartPrompt.png')
        restart_location = pyautogui.locateOnScreen(restart, confidence=0.8)
        click(restart_location[0], restart_location[1])
        sleep(0.75)
        restartPrompt_location = pyautogui.locateOnScreen(restartPrompt, confidence=0.8)
        click(restartPrompt_location[0], restartPrompt_location[1])
        sleep(0.75)

def check_defeat():
    defeat = os.path.join(script_dir, 'defeat.png')
    pyautogui.locateOnScreen(defeat, confidence=0.8)

def restart_round():
    restart = os.path.join(script_dir, 'restart.png')
    restartPrompt = os.path.join(script_dir, 'restartPrompt.png')
    restart_location = pyautogui.locateOnScreen(restart, confidence=0.8)
    click(restart_location[0], restart_location[1])
    sleep(0.4)
    restartPrompt_location = pyautogui.locateOnScreen(restartPrompt, confidence=0.8)
    click(restartPrompt_location[0], restartPrompt_location[1])
    sleep(0.20)

def start_round(individual, round_number, tower_index, upgrade_index):
    global num_towers
    global fitness_val
    global restart
    play = os.path.join(script_dir, 'play.png')
    play_location = pyautogui.locateOnScreen(play, confidence=0.80)
    #display_individual(individual, round_number)
    for _ in range (individual['wants_to_place'][round_number]):
        if tower_index < num_towers:
            try:
                check_defeat()
                restart_round()
                restart = True
                print(fitness_val)
                individual['fitness_val'] = fitness_val
            except pyautogui.ImageNotFoundException:
                place(individual['tower_types'][tower_index], individual['tower_locations'][tower_index][0], individual['tower_locations'][tower_index][1], individual)
                tower_index += 1
    for _ in range (individual['wants_to_upgrade'][round_number]):
        if upgrade_index < num_towers:
            try:
                check_defeat()
                restart_round()
                restart = True
                print(fitness_val)
                individual['fitness_val'] = fitness_val
            except pyautogui.ImageNotFoundException:
                upgrade(individual, upgrade_index)
                upgrade_index += 1
        else:
            print("I'm out of upgrades :(")
    for i in individual['placed_towers']:
            if i[2] == farm:
                click(i[0], i[1])
    try:
        sell = os.path.join(script_dir, 'sell.png')
        sell_location = pyautogui.locateOnScreen(sell, confidence=0.8)
        sleep(0.08)
        click(bottom_left[0], bottom_left[1])
        sleep(0.08)
    except pyautogui.ImageNotFoundException:
        #print("not seeing sell")
        sleep(0.0001)
    
    click(play_location[0], play_location[1])
    sleep(0.08)
    if(round_number == 1):
        sleep(0.08)
        click(play_location[0], play_location[1])
    sleep(0.08)
    return tower_index, upgrade_index

def listen_for_key():
    keyboard.wait('/')
    print("You pressed '/'. Exiting the program.")
    os.kill(os.getpid(), signal.SIGINT)

exit_event = threading.Event()

def listen_for_key_to_pause():
    while True:
        keyboard.wait(',')
        print("You pressed ','. Pausing")
        if exit_event.is_set():
            exit_event.clear() # Set the event to signal the main thread to stop
        else:
            exit_event.set()

# Start the key listener in a separate thread
listener_thread = threading.Thread(target=listen_for_key_to_pause)
listener_thread.daemon = True  # Allows the program to exit even if the thread is running
listener_thread.start()

# Start the key listener in a separate thread
listener_thread = threading.Thread(target=listen_for_key)
listener_thread.daemon = True  # Allows the program to exit even if the thread is running
listener_thread.start()


context = zmq.Context()
socket = context.socket(zmq.REP)  # Reply pattern
socket.bind("tcp://*:5555")

while True:
    data = socket.recv()
    individual = pickle.loads(data)
    fitness_score = fitness(individual)  # Simulate and calculate fitness
    socket.send(pickle.dumps(fitness_score))