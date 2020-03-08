import random


class Node:
    def __init__(self, node_id, activate_id, specialty):
        self.state = 0
        self.id = node_id
        self.specialty = specialty
        self.fired = False
        self.from_synapses_id = []
        # self.const = random.random()
        # if random.random() > 0.5:
        #     self.const = -self.const
        if activate_id == 0:
            self.activate = self.relu

    def relu(self, x):
        if x < 0:
            return 0
        else:
            return x


class Synapse:
    def __init__(self, synapse_id, from_node_id, to_node_id, weight, enabled=True):
        self.id = synapse_id
        self.weight = weight
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.enabled = enabled


class Network:
    def __init__(self, network_id, num_sensory=7, num_effector=4):
        self.id = network_id
        self.species = 0
        self.num_sensory = num_sensory
        self.num_effector = num_effector
        self.node_genes = {}
        self.effector_nodes_id = []
        self.sensory_nodes_id = []
        # self.control_nodes_id = []
        self.synapse_genes = {}
        self.next_node_id = 0
        self.ranking = -1
        self.mutation_history = []
        # add control nodes
        # for x in range(0, 2):
        #     activate_id = 0
        #     node = Node(self.next_node_id, activate_id, "control")
        #     self.node_genes[node.id] = node
        #     self.control_nodes_id.append(node.id)
        #     self.next_node_id += 1
        # add sensory nodes
        for x in range(0, num_sensory):
            activate_id = 0
            node = Node(self.next_node_id, activate_id, "sensory")
            self.node_genes[node.id] = node
            self.sensory_nodes_id.append(node.id)
            self.next_node_id += 1
        # add effector nodes
        for x in range(0, num_effector):
            activate_id = 0
            node = Node(self.next_node_id, activate_id, "effector")
            self.node_genes[node.id] = node
            self.effector_nodes_id.append(node.id)
            self.next_node_id += 1

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    @staticmethod
    def generate_weight():
        weight = round(random.random(), 2)
        if random.random() > 0.5:
            weight = -weight
        return weight

    def mutate(self, innov_num):
        node_add_chance = 0.1
        synapse_build_chance = 0.3
        synapse_remove_chance = 0.01
        synapse_edit_chance = 0.3
        if random.random() <= node_add_chance and self.synapse_genes:
            self.add_node(innov_num)
            innov_num += 2
            self.mutation_history.append("add_node")
        if random.random() <= synapse_build_chance:
            from_node_id = random.choice(list(self.node_genes.keys()))
            to_node_id = random.choice(list(self.node_genes.keys()))
            if from_node_id != to_node_id and \
                    self.node_genes[from_node_id].specialty != "effector" and \
                    self.node_genes[to_node_id].specialty != "sensory":
                self.build_synapse(innov_num, from_node_id, to_node_id, self.generate_weight())
                self.mutation_history.append("build_synapse")
                innov_num += 1
        if random.random() <= synapse_edit_chance and self.synapse_genes:
            synapse_id = random.choice(list(self.synapse_genes.keys()))
            self.edit_synapse(synapse_id)
            self.mutation_history.append("edit_synapse")
        if random.random() <= synapse_remove_chance and self.synapse_genes:
            synapse_id = random.choice(list(self.synapse_genes.keys()))
            self.disable_synapse(synapse_id)
            self.mutation_history.append("disable_synapse")
        return innov_num

    def build_synapse(self, innov_num, from_node_id, to_node_id, weight, enabled=True):
        new_synapse = Synapse(innov_num, from_node_id, to_node_id, weight, enabled)
        self.synapse_genes[new_synapse.id] = new_synapse
        self.node_genes[to_node_id].from_synapses_id.append(new_synapse.id)
        return 0

    def edit_synapse(self, synapse_id):
        self.synapse_genes[synapse_id].weight = self.generate_weight()
        return 0

    def disable_synapse(self, synapse_id):
        self.synapse_genes[synapse_id].enabled = False

    def build_node(self, node_id):
        activate_id = 0
        node = Node(node_id, activate_id, "inter")
        self.node_genes[node_id] = node
        return node

    def add_node(self, innov_num):
        synapse_id = random.choice(list(self.synapse_genes.keys()))
        synapse = self.synapse_genes[synapse_id]
        node = self.build_node(self.next_node_id)
        self.build_synapse(innov_num, synapse.from_node_id, node.id, synapse.weight)
        self.build_synapse(innov_num+1, node.id, synapse.to_node_id, synapse.weight)
        self.disable_synapse(synapse_id)
        self.next_node_id += 1
        return 0

    def update_node(self, node_id):
        # if loops back to this node, return old state, acting as a memory
        if (len(self.node_genes[node_id].from_synapses_id) == 0
                # or self.node_genes[node_id].specialty == "control"
                or self.node_genes[node_id].fired):
            return self.node_genes[node_id].state
        new_state = 0
        self.node_genes[node_id].fired = True
        for synapse_id in self.node_genes[node_id].from_synapses_id:
            if self.synapse_genes[synapse_id].enabled:
                synapse = self.synapse_genes[synapse_id]
                new_state += synapse.weight * self.update_node(synapse.from_node_id)
        self.node_genes[node_id].state = new_state
        return self.node_genes[node_id].state

    def think(self, sense):
        for node_id, node in self.node_genes.items():
            node.fired = False
        # if len(self.control_nodes_id) > 0:
        #     self.node_genes[0].state = 0
        # if len(self.control_nodes_id) > 1:
        #     self.node_genes[1].state = 1
        sense_counter = 0
        for x in self.sensory_nodes_id:
            self.node_genes[x].fired = True
            self.node_genes[x].state = sense[sense_counter]
            sense_counter += 1
        response = [0] * self.num_effector
        response_counter = 0
        for effector_id in self.effector_nodes_id:
            self.update_node(effector_id)
            response[response_counter] = self.node_genes[effector_id].state
            response_counter += 1
        return response

