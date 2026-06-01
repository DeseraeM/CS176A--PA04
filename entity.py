'''
Code for an entity in the network. This is where you should implement the
distance-vector algorithm.
'''

import packet

class Entity:
    '''
    Entity that represents a node in the network.

    Each function should be implemented so that the Entity can be instantiated
    multiple times and successfully run a distance-vector routing algorithm.
    '''

    def __init__(self, entity_index, number_entities):
        '''
        This initialization function will be called at the beginning of the
        simulation to setup all entities.

        Arguments:
        - `entity_index`:    The id of this entity.
        - `number_entities`: Number of total entities in the network.

        Return Value: None.
        '''
        # Save state
        self.index = entity_index
        self.number_of_entities = number_entities
        #this keeps track of the rest of the distances but bc we don't know them it is set to infinity
        self.arr = [float('inf')] * number_entities
        self.arr[self.index] = 0
        #this keeps track of the next niehboors:
        self.next_arr = [self.index] * number_entities
        self.next_arr[self.index] = self.index
        self.dist_table = [{} for _ in range(number_entities)]

    def initialize_costs(self, neighbor_costs):
        '''
        This function will be called at the beginning of the simulation to
        provide a list of neighbors and the costs on those one-hop links.

        Arguments:
        - `neighbor_costs`:  Array of (entity_index, cost) tuples for
                             one-hop neighbors of this entity in this network.

        Return Value: This function should return an array of `Packet`s to be
        sent from this entity (if any) to neighboring entities.
        '''
        self.neighbor_costs = neighbor_costs
        new_list = []
        for i in range(len(neighbor_costs)):
            neighbor, c = neighbor_costs[i]
            self.arr[neighbor] = c
            self.dist_table[neighbor][neighbor] = c
        
        for j in range(len(neighbor_costs)):
            neighbor,c = neighbor_costs[j]
            n_packet = packet.Packet(neighbor, self.arr)
            new_list.append(n_packet)
            self.next_arr[neighbor] = neighbor
        return new_list

    def update(self, pkt):
        '''
        This function is called when a packet arrives for this entity.

        Arguments:
        - `pkt`: The incoming packet of type `Packet`.

        Return Value: This function should return an array of `Packet`s to be
        sent from this entity (if any) to neighboring entities.
        '''
        new_l = []
        old_source = pkt.get_source()
        cost_s = self.arr[old_source]
        for i in range(self.number_of_entities):
            self.dist_table[i][old_source] = cost_s + pkt.get_costs()[i]

        past = self.arr[:]
        for i in range(len(self.arr)):
            if i == self.index:
                continue
            best_cost = float('inf')
            best_hop = self.next_arr[i]
            for neighbor, c in self.neighbor_costs:
                via = self.dist_table[i].get(neighbor, float('inf'))
                if via < best_cost:
                    best_cost = via
                    best_hop = neighbor
            self.arr[i] = best_cost        
            self.next_arr[i] = best_hop
        if past != self.arr:
            for j in range(len(self.neighbor_costs)):
                neighbor, c = self.neighbor_costs[j]
                n_packet = packet.Packet(neighbor, self.arr)
                new_l.append(n_packet)
        return new_l

    def get_all_costs(self):
        '''
        This function is used by the simulator to retrieve the calculated routes
        and costs from an entity. This is most useful at the end of the
        simulation to collect the resulting routing state.

        Return Value: This function should return an array of (next_hop, cost)
        tuples for _every_ entity in the network based on the entity's current
        understanding of those costs. The array should be sorted such that the
        first element of the array is the next hop and cost to entity index 0,
        second element is to entity index 1, etc.
        '''
        c_results = []
        for i in range(len(self.arr)):
            c_results.append((self.next_arr[i], self.arr[i]))
        return c_results

    def forward_next_hop(self, destination):
        '''
        Return the best next hop for a packet with the given destination.

        Arguments:
        - `destination`: The final destination of the packet.

        Return Value: The index of the best neighboring entity to use as the
        next hop.
        '''
        return self.next_arr[destination]

