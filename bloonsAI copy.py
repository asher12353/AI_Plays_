from pyautogui import *
from pathlib import Path
from PIL import Image
from PIL import ImageGrab
import pywinauto
import pytesseract
import pyautogui
import time
import keyboard
import random
import pywinauto.keyboard
import win32api, win32con
import os
import ast
import keyboard
import threading
import sys
import signal

script_dir = os.path.dirname(os.path.abspath(__file__))

paths = (os.path.join(script_dir, 'heroBuyable.png'), os.path.join(script_dir, 'boomerangBuyable.png'), os.path.join(script_dir, 'tackBuyable.png'), os.path.join(script_dir, 'glueBuyable.png'), os.path.join(script_dir, 'subBuyable.png'), os.path.join(script_dir, 'planeBuyable.png'), os.path.join(script_dir, 'dartMonkeyBuyable.png'), os.path.join(script_dir, 'canonBuyable.png'), os.path.join(script_dir, 'iceBuyable.png'), os.path.join(script_dir, 'sniperBuyable.png'), os.path.join(script_dir, 'boatBuyable.png'), os.path.join(script_dir, 'heliBuyable.png'), os.path.join(script_dir, 'mortarBuyable.png'), os.path.join(script_dir, 'wizardBuyable.png'), os.path.join(script_dir, 'ninjaBuyable.png'), os.path.join(script_dir, 'druidBuyable.png'), os.path.join(script_dir, 'factoryBuyable.png'), os.path.join(script_dir, 'engineerBuyable.png'), os.path.join(script_dir, 'turretBuyable.png'), os.path.join(script_dir, 'superBuyable.png'), os.path.join(script_dir, 'alchemistBuyable.png'), os.path.join(script_dir, 'farmBuyable.png'), os.path.join(script_dir, 'villageBuyable.png'), os.path.join(script_dir, 'dinoBuyable.png'),)

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

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

numScrollsToGoFromTopToBottom = 14

leftColumnLocation = 2340
rightColumnLocation = 2485

upperRowLocations = (230, 410, 585, 770, 950, 1120)
lowerRowLocations = (200, 385, 560, 750, 925, 1105)

map_range = ((35, 60), (2140, 1440))
bottom_left = (45, 1430)

pyautogui.FAILSAFE = False

def click(x, y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.09)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

on_top = True

def place(monkey, x, y, individual):
    global on_top
    global fitness_val
    # if monkey <= heli: # if it's on top
    #     if on_top == False:
    #         click(leftColumnLocation, lowerRowLocations[0])
    #         for _ in range(numScrollsToGoFromTopToBottom):
    #             pyautogui.scroll(1)
    #         on_top = True
    #     if monkey <= plane:
    #         column = leftColumnLocation
    #         row = upperRowLocations[monkey]
    #     else:
    #         column = rightColumnLocation
    #         row = upperRowLocations[monkey - dartMonkey]
    # elif monkey >= mortar:
    #     if on_top == True:
    #         click(leftColumnLocation, upperRowLocations[0])
    #         for _ in range(numScrollsToGoFromTopToBottom):
    #             pyautogui.scroll(-1)
    #         on_top = False
    #     if monkey <= engineer:
    #         column = leftColumnLocation
    #         row = lowerRowLocations[monkey - mortar]
    #     else:
    #         column = rightColumnLocation
    #         row = lowerRowLocations[monkey - turret]
    # location = pyautogui.locateOnScreen(paths[monkey], confidence=0.8)
    try:
        # click(column, row)
        try:
            check_defeat()
            return
        except pyautogui.ImageNotFoundException:
            sleep(0.01)
        keyboard.press_and_release(key_binds[monkey])
        # just trust me that these three sleeps cannot be reduced
        sleep(0.09)
        click(x, y)
        sleep(0.08)
        click(x, y)
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
            click(2550, 15)
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
            click(monkey[0], monkey[1])
        try:
            sell = os.path.join(script_dir, 'sell.png')
            sleep(0.08) # these two must be at least > 0.5
            sell_location = pyautogui.locateOnScreen(sell, confidence=0.8)
            upgrade_location = (sell_location[0] + 170, sell_location[1] - 130 - (individual['upgrades'][upgrade_index][1] * 200))
            click(upgrade_location[0], upgrade_location[1])
            fitness_val += 1
            sleep(0.01)
            if(monkey != individual['placed_towers'][individual['upgrades'][upgrade_index + 1][0] % len(individual['placed_towers'])]):
                click(45, 1430)
        except pyautogui.ImageNotFoundException:
            sleep(0.01)
    except:
        sleep(0.01)
    sleep(0.05)

def display_individual(individual, round_number):
    #print(f"For round number {round_number}: this individual wants to place ", end="")

    tower_types = [
        "hero", "boomerang", "tack", "glue", "sub", "plane", "dart", "canon",
        "ice", "sniper", "boat", "heli", "mortar", "wizard", "ninja", "druid",
        "factory", "engineer", "turret", "super", "alchemist", "farm", "village", "dino"
    ]

    tower_type = individual['tower_types'][round_number]

    #if 0 <= tower_type < len(tower_types):
    #    print(f"{tower_types[tower_type]} monkey ")
    #else:
    #    print("Unknown tower type ")
    try:
        placed_towers_count = len(individual['placed_towers'])
        upgrade_index = individual['upgrades'][round_number][0] % placed_towers_count
        upgrade_kind = individual['upgrades'][round_number][1] + 1

        #print(f"and wants to upgrade their {upgrade_index}-th tower with upgrade #{upgrade_kind}")
    except:
        return


def capture_screenshot(filename='screenshot.png'):
    # Capture the screen and save it as an image file
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")

chromosome = {
    'tower_locations': [()],
    'tower_types': [],
    'fitness_val' : 0,
    'placed_towers' : [],
    'upgrades' : [],
    'wants_to_place': [],
    'wants_to_upgrade': []
}

def generate_individual():
    return {
        'tower_locations': [(random.randint(map_range[0][0], map_range[1][0]), random.randint(map_range[0][1], map_range[1][1])) for _ in range(num_towers)],
        'tower_types': [random.choice(available_tower_types) for _ in range(num_towers)],
        'fitness_val' : 0,
        'placed_towers' : [],
        'upgrades' : [(random.randint(0, num_towers), random.randint(0, 2)) for _ in range(num_towers)],
        'wants_to_place': [random.randint(0, 2) for _ in range(num_towers)],
        'wants_to_upgrade': [random.randint(0, 2) for _ in range(num_towers)]
    }

def select(population, fitness_fn, num_parents):
    return sorted(population, key=fitness_fn, reverse=True)[:num_parents]

def crossover(parent1, parent2):
    # Choose a random crossover point
    crossover_point = random.randint(0, len(parent1['tower_types']))

    # Create offspring by combining genetic material from parents
    offspring = {
        'tower_locations': parent1['tower_locations'][:crossover_point] + parent2['tower_locations'][crossover_point:],
        'tower_types': parent1['tower_types'][:crossover_point] + parent2['tower_types'][crossover_point:],
        'fitness_val': 0,
        'placed_towers': [],
        'upgrades': parent1['upgrades'][:crossover_point] + parent2['upgrades'][crossover_point:],
        'wants_to_place': parent1['wants_to_place'][:crossover_point] + parent2['wants_to_place'][crossover_point:],
        'wants_to_upgrade': parent1['wants_to_upgrade'][:crossover_point] + parent2['wants_to_upgrade'][crossover_point:]
        
    }

    return offspring

def mutate_tower_types(tower_types, mutation_rate):
    # Mutate tower types
    print("Mutating tower_types")
    for i in range(len(tower_types)):
        random_number = random.uniform(0, 1)
        if random_number >= 1 - mutation_rate * 0.05: #each value on the mutation rate gives it a 5% chance to mutate
            random_number = random.randint(-mutation_rate, mutation_rate)
            current_type_index = available_tower_types.index(tower_types[i])
            next_type_index = (current_type_index + random_number) % len(available_tower_types)
            tower_types[i] = available_tower_types[next_type_index]

def mutate_tower_locations(tower_locations, mutation_rate):
    # Mutate tower locations
    print("Mutating tower_locations")
    for i in range(len(tower_locations)):
        random_number = random.uniform(0, 1)
        if random_number >= 1 - mutation_rate * 0.05:
            x, y = tower_locations[i]
            x += random.randint(-mutation_rate, mutation_rate) * 10
            y += random.randint(-mutation_rate, mutation_rate) * 10
            tower_locations[i] = (x, y)

def mutate_upgrades(upgrades):
    print("Mutating upgrades")
    for i in range(len(upgrades)):
        random_number = random.uniform(0, 1)
        if random_number >= 1 - mutation_rate * 0.05:
            x, y = upgrades[i]
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if y > 2:
                y = 2
            upgrades[i] = (x, y)

def mutate_wants(place, upgrade, mutation_rate):
    print("Mutating wants")
    for i in range(len(place)):
        random_number = random.uniform(0, 1)
        if random_number >= 1 - mutation_rate * 0.05:
            random_number = random.randint(-mutation_rate, mutation_rate)
            place[i] += random_number
            if place[i] < 0:
                place[i] = 0
    for i in range(len(upgrade)):
        random_number = random.uniform(0, 1)
        if random_number >= 1 - mutation_rate * 0.05:
            random_number = random.randint(-mutation_rate, mutation_rate)
            upgrade[i] += random_number
            if upgrade[i] < 0:
                upgrade[i] = 0


def mutate(individual, mutation_rate):
    mutated_individual = individual.copy()
    mutation_type = random.randint(0, 3)

    if mutation_type == 0:
        mutate_tower_types(mutated_individual['tower_types'], mutation_rate)

    if mutation_type == 1:
        mutate_tower_locations(mutated_individual['tower_locations'], mutation_rate)

    if mutation_type == 2:
        mutate_upgrades(mutated_individual['upgrades'])

    if mutation_type == 3:
        mutate_wants(mutated_individual['wants_to_place'], mutated_individual['wants_to_upgrade'], mutation_rate)

    return mutated_individual


def fitness(individual):
    round_number = 1
    global fitness_val
    global restart
    global individual_number
    global threshold_for_next_generation_index
    global threshold_for_next_generation
    individual_number += 1
    print("Individual #" + str(individual_number))
    print(str(population_size - individual_number) + " individuals left in this generation")
    print("Current weakest individual that is advancing to the next generation has a score of: " + str(threshold_for_next_generation))
    restart = False
    fitness_val = 0
    tower_index = 0
    upgrade_index = 0
    if individual['fitness_val'] > 0 and replay == False:
        return individual['fitness_val']
    click(leftColumnLocation, lowerRowLocations[0])
    # for _ in range(numScrollsToGoFromTopToBottom):
    #     pyautogui.scroll(1)
    global on_top
    on_top = True
    #start_time = time.time()
    while True:
        while exit_event.isSet():
            sleep(1)
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
                if fitness_val > threshold_for_next_generation:
                    print(GREEN + "This individual made it to the next generation!" + RESET)
                    threshold_for_next_generation_index -= 1
                    threshold_for_next_generation = population[threshold_for_next_generation_index]['fitness_val']
                else:
                    print(RED + "This individual did not make it to the next generation :(" + RESET)
                return fitness_val
            except pyautogui.ImageNotFoundException:
                sleep(0.001)
            try:
                check_defeat()
                restart_round()
                print(fitness_val)
                int(fitness_val)
                individual['fitness_val'] = fitness_val
                if fitness_val > threshold_for_next_generation:
                    print(GREEN + "This individual made it to the next generation!" + RESET)
                    threshold_for_next_generation_index -= 1
                    threshold_for_next_generation = population[threshold_for_next_generation_index]['fitness_val']
                else:
                    print(RED + "This individual did not make it to the next generation :(" + RESET)
                return fitness_val
            except pyautogui.ImageNotFoundException:
                sleep(0.001)
            #if it didn't lose, check if it's a new round
            try:
                tower_index, upgrade_index = start_round(individual, round_number, tower_index, upgrade_index)
                if individual['fitness_val'] > 0 and replay == False or restart:
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
    display_individual(individual, round_number)
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

available_tower_types = [hero, boomerang, tack, glue, sub, plane, dartMonkey, canon, ice, sniper, boat, wizard, ninja, druid, factory, engineer, super, alchemist, farm, village, dino]
global num_towers
global individual_number
num_towers = 101

population_size = 500
num_generations = 100
mutation_rate = 7
global replay
replay = True

try:
    population = []

    tower_locations = []
    with open('current_ai/tower_locations.txt', 'r') as file:
        content = file.readlines()
    for line in content:
        individual_chromosome = eval(line)
        tower_locations.append(individual_chromosome)
    
    tower_types = []
    with open('current_ai/tower_types.txt', 'r') as file:
        content = file.readlines()
    for line in content:
        individual_chromosome = eval(line)
        tower_types.append(individual_chromosome)
        num_towers = len(individual_chromosome)
    
    fitness_val = []
    try:
        with open('current_ai/fitness_val.txt', 'r') as file:
            content = file.readlines()
        for line in content:
            individual_chromosome = int(eval(line))  # Convert to int
            fitness_val.append(individual_chromosome)
    except:
        for _ in range(len(tower_locations)):
            fitness_val.append(0)

    upgrades = []
    with open('current_ai/upgrades.txt', 'r') as file:
        content = file.readlines()
    for line in content:
        individual_chromosome = eval(line)
        upgrades.append(individual_chromosome)

    wants_to_place = []
    try:
        with open('current_ai/wants_to_place.txt', 'r') as file:
            content = file.readlines()
        for line in content:
            individual_chromosome = eval(line)
            wants_to_place.append(individual_chromosome)
    except:
        temp = []
        for _ in range(len(tower_locations)):
            for _ in range(num_towers):
                temp.append(1)
            wants_to_place.append(temp)

    wants_to_upgrade = []
    try:
        with open('current_ai/wants_to_upgrade.txt', 'r') as file:
            content = file.readlines()
        for line in content:
            individual_chromosome = eval(line)
            wants_to_upgrade.append(individual_chromosome)
    except:
        temp = []
        for _ in range(len(tower_locations)):
            for _ in range(num_towers):
                temp.append(1)
            wants_to_upgrade.append(temp)
        
    for i in range(len(tower_locations)):
        individual = {
            'tower_locations': tower_locations[i],
            'tower_types': tower_types[i],
            'fitness_val': fitness_val[i],
            'placed_towers': [],
            'upgrades': upgrades[i],
            'wants_to_place': wants_to_place[i],
            'wants_to_upgrade': wants_to_upgrade[i]
        }
        population.append(individual)
    for _ in range(population_size - len(population)):
        population.append(generate_individual())
    print("imported population")
except FileNotFoundError:
    population = [generate_individual() for _ in range(population_size)]
    print("making a new population")

def save():
    f1 = open("current_ai/tower_locations.txt", "w")
    f2 = open("current_ai/tower_types.txt", "w")
    f3 = open("current_ai/fitness_val.txt", "w")
    f4 = open("current_ai/upgrades.txt", "w")
    f5 = open("current_ai/wants_to_place.txt", "w")
    f6 = open("current_ai/wants_to_upgrade.txt", "w")

    for individual in population:
        f1.write(repr(individual['tower_locations']) + '\n')
        f2.write(repr(individual['tower_types']) + '\n')
        f3.write(repr(individual['fitness_val']) + '\n')
        f4.write(repr(individual['upgrades']) + '\n')
        f5.write(repr(individual['wants_to_place']) + '\n')
        f6.write(repr(individual['wants_to_upgrade']) + '\n')

    # Close the files after writing all individuals
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    f6.close()

def listen_for_key():
    keyboard.wait('/')
    print("You pressed '/'. Exiting the program.")
    save()
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

try:
    for generation in range(num_generations):
        print("Starting generation")
        print(generation)
        global threshold_for_next_generation
        global threshold_for_next_generation_index
        threshold_for_next_generation_index = (int)(population_size/2) - 1
        threshold_for_next_generation = population[threshold_for_next_generation_index]['fitness_val']
        
        individual_number = 0
        
        # Step 5: Selection
        parents = select(population, fitness, population_size // 2)

        #while len(parents) < population_size // 2 + 1:
        #    random_individual = random.choice(population)
        #    if random_individual not in parents:
        #        parents.append(random_individual)


        # Step 6: Crossover
        offspring = [crossover(random.choice(parents), random.choice(parents)) for _ in range(population_size - len(parents))]

        # Step 7: Mutation
        offspring = [mutate(individual, mutation_rate) for individual in offspring]

        # Step 8: Replace Old Population
        population = parents + offspring

        
        save()

        replay = False
except KeyboardInterrupt:
    print("ending")