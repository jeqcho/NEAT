import visualisation_lab as vl
import neural_network_lab as nnl
import random
import copy
import pygame
import math
# neural network of each blocky
neural_networks = {}

next_innov_num = 0

# results for the current round of each blocky
results = {}

# ranking (zero-indexed)
ranking = []

# record of all entities categorised by species
# key: species number, value: list of entities index in neural_network dict
community = {}
species_fitness = {}
species_new_num = {}

# key: species number, value: dictionary of network_id and score

# the top percentage where entities are allowed to randomly mate
merit_bias = .5

# initialise
ticks_per_test = 500
population_limit = 100
num_sensory = 7
num_food = 50
new_species_id = 1
excess_c = 1.0
disjoint_c = 1.0
weight_diff_c = 3.0
comp_threshold = 2.0

# statistics
species_mean_fitness = {}
species_num = {}


def cal_compatibility(network1_id, network2_id):
    network1 = neural_networks[network1_id]
    network2 = neural_networks[network2_id]
    total_weight_diff = 0
    num_match = 0
    num_excess = 0
    num_disjoint = 0
    if network1.synapse_genes.keys():
        max_innov1 = max(network1.synapse_genes.keys())
        min_innov1 = min(network1.synapse_genes.keys())
    else:
        max_innov1 = 0
        min_innov1 = 0
    if network2.synapse_genes.keys():
        max_innov2 = max(network2.synapse_genes.keys())
        min_innov2 = min(network2.synapse_genes.keys())
    else:
        max_innov2 = 0
        min_innov2 = 0
    max_size = max(len(network1.synapse_genes.keys()), len(network2.synapse_genes.keys()))
    min_innov = min(min_innov1, min_innov2)
    if max_innov1 > max_innov2:
        # network2 has excess
        network1, network2 = network2, network1
        max_innov1, max_innov2 = max_innov2, max_innov1
    for i in range(min_innov, max_innov2+1):
        if i in network1.synapse_genes:
            present1 = True
        else:
            present1 = False
        if i in network2.synapse_genes:
            present2 = True
        else:
            present2 = False
        if present1 and present2:
            total_weight_diff += abs(network1.synapse_genes[i].weight - network2.synapse_genes[i].weight)
            num_match += 1
        elif present1 or present2:
            if num_match > 0:
                num_disjoint += 1
            else:
                num_excess += 1
    dist_measure = 0
    if num_excess > 0:
        dist_measure += excess_c * num_excess / max_size
    if num_disjoint > 0:
        dist_measure += disjoint_c * num_disjoint / max_size
    if num_match > 0:
        avg_weight_diff = total_weight_diff / num_match
        dist_measure += weight_diff_c * avg_weight_diff
    return dist_measure


def find_species(network_id):
    global community, new_species_id
    for species_id, network_ids in community.items():
        # rand_sample_id = random.choice(network_ids)
        rand_sample_id = network_ids[0]
        if cal_compatibility(rand_sample_id, network_id) <= comp_threshold:
            network_ids.append(network_id)
            neural_networks[network_id].species = species_id
            return
    community[new_species_id] = [network_id]
    neural_networks[network_id].species = new_species_id
    new_species_id += 1


for x in range(0, population_limit):
    neural_networks[x] = nnl.Network(x, num_sensory, 4)
    next_innov_num = neural_networks[x].mutate(next_innov_num)

new_species_id = 1
next_network_id = population_limit


def test(network, animate_flag=False):
    vl.reset()
    feedback = [0, 0, 0]
    blocky = vl.Bot((200, 0, 0), spawn_left, spawn_top)
    for food_id in range(len(food_pos)):
        vl.Food(food_id, food_pos[food_id][0], food_pos[food_id][1])

    # clock = pygame.time.Clock()
    running = True
    tick_counter = 0

    while running:
        if tick_counter == ticks_per_test:
            return blocky.health_bar
        # clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # check for sight
        # find the nearest food and give distance and angle
        sight_info = pygame.sprite.groupcollide(vl.eyesights, vl.foods, 0, 0)
        blocky.eyesight.sense = [0] * num_sensory
        for eyesight in sight_info:
            food_is_detected = 1
            min_dist_to_food = eyesight.range * 2
            for food_detected in sight_info[eyesight]:
                dx = food_detected.x - eyesight.x
                dy = food_detected.y - eyesight.y
                dist = math.sqrt(dx ** 2 + dy ** 2)
                if dist < min_dist_to_food:
                    min_dist_to_food = dist
                    eyesight.sense = [food_is_detected, dx, dy] + feedback + [1]

        # think
        response = network.think(blocky.eyesight.sense)

        # allow movements and growth
        feedback = blocky.update(response)

        # check for feeding
        feeding_info = pygame.sprite.groupcollide(vl.bots, vl.foods, 0, 1)
        for bot in feeding_info:
            for food in feeding_info[bot]:
                bot.eat(food.energy_value)
                # vl.generate_food()

        # # check for fights
        # fight_info = pygame.sprite.groupcollide(bots, bots, 0, 0)
        # for bot in fight_info:
        #     for opponent in fight_info[bot]:
        #         if opponent is not bot:
        #             print(fight_info)
        #             compete(bot, opponent)

        # refresh the screen
        if animate_flag:
            vl.screen.blit(vl.background, (0, 0))
            vl.eyesight_surface.blit(vl.background, (0, 0))
            vl.all_sprites.draw(vl.screen)
            for bot in vl.bots:
                bot.eyesight.show()
                vl.screen.blit(vl.eyesight_surface, (0, 0))
            pygame.display.update()

        # count the number of ticks
        tick_counter += 1


# function for ranking
def rank(blocky_id_):
    return results[blocky_id_]


results = {}
new_networks = {}


def mate(network1, network2):
    global next_innov_num
    first_better = results[network1.id] > results[network2.id]
    if first_better:
        new_network = copy.deepcopy(network1)
    else:
        new_network = copy.deepcopy(network2)
    new_network.id = next_network_id
    next_innov_num = new_network.mutate(next_innov_num)
    return new_network


generation_num = 1
record_highscore = 0
running = True
while running:
    # start new round
    spawn_left = int(random.random() * (vl.screen_width - 20))
    spawn_top = int(random.random() * (vl.screen_height - 20))
    food_pos = []
    for i in range(num_food):
        x = random.random() * (vl.screen_width - vl.food_width)
        y = random.random() * (vl.screen_height - vl.food_height)
        food_pos.append([x, y])
    num_test = 0
    total_score = 0
    results = {}
    print("TRAINING...")
    for network_id in list(neural_networks.keys()):
        num_test += 1
        results[network_id] = test(neural_networks[network_id])
        total_score += results[network_id]
    mean_score = round(total_score / num_test, 2)

    # Species
    community.clear()
    new_species_id = 0
    for network_id, network in neural_networks.items():
        find_species(network_id)

    # rank each blocky by results
    ranking = []
    for network_id in results:
        ranking.append(network_id)
    ranking.sort(key=rank)
    ranking.reverse()
    highscore = results[ranking[0]]
    test(neural_networks[ranking[0]], True)

    # Record fitness of each species
    print("SPECIES NUMBER")
    total_fitness = 0
    species_mean_fitness.clear()
    species_fitness.clear()
    for species_id, network_ids in community.items():
        species_fitness[species_id] = 0
        for network_id in network_ids:
            species_fitness[species_id] += results[network_id] - 99
        total_fitness += species_fitness[species_id]
        print(species_id, ': ', len(network_ids))
        species_mean_fitness[species_id] = round(species_fitness[species_id] / len(network_ids), 2)
    print("SPECIES FITNESS")
    print(species_fitness)
    print("MEAN FITNESS")
    print(species_mean_fitness)
    mean_fitness = total_fitness / len(neural_networks)
    for species_id, fitness in species_fitness.items():
        species_new_num[species_id] = int(fitness / mean_fitness + .5)

    # reproduce
    new_networks.clear()
    next_network_id = 0
    for species_id, network_ids in community.items():
        ranking_in_species = sorted(network_ids, key=lambda network_id: results[network_id], reverse=True)
        t = 0
        mates = []
        while float(t/len(network_ids)) < merit_bias:
            mates.append(ranking_in_species[t])
            t += 1
        for i in range(0, species_new_num[species_id]):
            mate1 = random.choice(mates)
            mate2 = random.choice(mates)
            new_networks[next_network_id] = mate(neural_networks[mate1], neural_networks[mate2])
            next_network_id += 1
    while len(new_networks) < population_limit:
        mate1 = random.randrange(population_limit)
        mate2 = random.choice(community[neural_networks[mate1].species])
        new_networks[next_network_id] = mate(neural_networks[mate1], neural_networks[mate2])
        next_network_id += 1
    while len(new_networks) > population_limit:
        unlucky_network = random.choice(new_networks)
        del new_networks[unlucky_network.id]
    neural_networks = copy.deepcopy(new_networks)
    print("Current population: " + str(len(neural_networks)))

    # report highlights
    mean_score = round(mean_score - 100, 2)
    print("Mean score:", mean_score)
    highscore -= 100
    print("Highscore:", highscore)
    if highscore > record_highscore:
        print("NEW HIGHSCORE")
        record_highscore = highscore
    print("GENERATION NO:", generation_num)
    generation_num += 1
    vl.screen.blit(vl.background, (0, 0))
    pygame.display.update()
    # end current round
