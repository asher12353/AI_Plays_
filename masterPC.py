import asyncio
import zmq.asyncio
import os
import random
import signal
import threading
import zmq
import pickle 
import keyboard

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

map_range = ((35, 60), (2140, 1440))
bottom_left = (45, 1430)

available_tower_types = [hero, boomerang, tack, glue, sub, plane, dartMonkey, canon, ice, sniper, boat, wizard, ninja, druid, factory, engineer, super, alchemist, farm, village, dino]
global num_towers
global individual_number
num_towers = 101

population_size = 500
num_generations = 100
mutation_rate = 7
global replay
replay = False

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

def select(population, num_parents):
    return sorted(population, key=lambda individual: individual['fitness_val'], reverse=True)[:num_parents]

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

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def send_individual_to_sim(individual, sim_pc_ip, sim_pc_port):
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{sim_pc_ip}:{sim_pc_port}")

    try:
        data = pickle.dumps(individual)
        await socket.send(data)
        fitness_score = pickle.loads(await socket.recv())
        individual['fitness_val'] = fitness_score
        return individual, fitness_score
    except Exception as e:
        print(f"Error communicating with {sim_pc_ip}: {e}")
        return individual, None

async def run_simulation_in_parallel(individuals, sim_pcs):
    tasks = []
    for i, individual in enumerate(individuals):
        sim_pc_ip, sim_pc_port = sim_pcs[i % len(sim_pcs)]  # Distribute to sim PCs
        tasks.append(send_individual_to_sim(individual, sim_pc_ip, sim_pc_port))

    # Await all tasks to finish
    results = await asyncio.gather(*tasks)
    return results


sim_pcs = [("169.254.57.20", 5555)]  # IPs and ports of sim PCs

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
        results = asyncio.run(run_simulation_in_parallel(population, sim_pcs))
        parents = select(population, population_size // 2)


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