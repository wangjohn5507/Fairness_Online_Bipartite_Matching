import heapq
import copy
from collections import defaultdict
import random
import matplotlib.pyplot as plt
import numpy as np
from draw_plot import draw_plot


random.seed(36)

def update_heap(heap, old_item, new_item):
    """
    Update an item in the heap from old_item to new_item and re-heapify.

    :param heap: List representing the heap.
    :param old_item: The item in the heap to be updated.
    :param new_item: The new value for the item.
    """
    # Find the index of the old item
    index = heap.index(old_item)  # This might raise ValueError if the item is not found

    # Replace the old item with the new item
    heap[index] = new_item

    # Since we've manually replaced an item, the heap property might be violated
    # We need to re-heapify the heap
    heapq.heapify(heap)

def find_key_by_value(dictionary, search_value):
    """
    Find the key in the dictionary corresponding to the given value.

    :param dictionary: The dictionary to search.
    :param search_value: The value for which to find the corresponding key.
    :return: The key corresponding to the search_value or None if not found.
    """
    for key, value in dictionary.items():
        for v in value:
            if v == search_value:
                return key
    return None


class OnlineBipartiteMatcher_Priority:
    def __init__(self):
        # Priority queue to store groups with their priority values (min-heap)
        self.priority_queue = []
        # Map to store group details and their corresponding vertices
        self.groups = defaultdict(list)
        # Map to track the available vertices for matching
        self.available_vertices = set()
        self.group_weight = defaultdict(list)

    def add_group(self, group_id, initial_priority=0):
        # Each group entry in the heap is a tuple (priority, group_id)
        heapq.heappush(self.priority_queue, (initial_priority, group_id))
        self.groups[group_id] = []
        self.group_weight[group_id] = 0

    def add_vertex_to_group(self, vertex, group_id):
        # Add vertex to the specified group
        self.groups[group_id].append(vertex)
        self.available_vertices.add(vertex)

    def process_new_vertex(self, v, adjacent_vertices):
        # Try to match the new vertex v
        tried_groups = set()
        fixed_priority_queue = copy.deepcopy(self.priority_queue)

        while fixed_priority_queue:
            # Get the group with the lowest priority value
            priority, group_id = heapq.heappop(fixed_priority_queue)


            # Sort adjacent vertices by edge weight in descending order
            sorted_vertices = sorted(adjacent_vertices, key=lambda x: x[1], reverse=True)
            print(sorted_vertices)
            matched = False

            for u, weight in sorted_vertices:
                if u in self.available_vertices:
                    if self.group_weight[find_key_by_value(self.groups, u)] == 0:
                        # print('hi')
                        self.available_vertices.remove(u)
                        self.group_weight[find_key_by_value(self.groups, u)] += weight
                        update_heap(self.priority_queue, (priority, find_key_by_value(self.groups, u)), (priority + weight, find_key_by_value(self.groups, u)))
                        print(f"Matched vertex {v} with {u} from group {find_key_by_value(self.groups, u)}")
                        matched = True
                        break
                    if u in self.groups[group_id]:
                        # Match found
                        self.available_vertices.remove(u)
                        self.group_weight[group_id] += weight
                        # Increase the priority value of the group by the weight of the edge
                        update_heap(self.priority_queue, (priority, group_id), (priority + weight, group_id))
                        # heapq.heappop(self.priority_queue)
                        # heapq.heappush(self.priority_queue, (priority + weight, group_id))
                        print(f"Matched vertex {v} with {u} from group {group_id}")
                        matched = True
                        break
                    else:
                        continue

            if matched:
                break

        if not matched:
            # No match found, the vertex v is dropped
            print(f"Vertex {v} could not be matched and was dropped")

        print(self.priority_queue)

class OnlineBipartiteMatcher_Greedy:
    def __init__(self):
        # Priority queue to store groups with their priority values (min-heap)
        self.priority_queue = []
        # Map to store group details and their corresponding vertices
        self.groups = defaultdict(list)
        # Set to track the available vertices for matching
        self.available_vertices = set()
        self.group_weight = defaultdict(list)

    def add_group(self, group_id, initial_priority=0):
        # Each group entry in the heap is a tuple (priority, group_id)
        heapq.heappush(self.priority_queue, (initial_priority, group_id))
        self.groups[group_id] = []
        self.group_weight[group_id] = 0

    def add_vertex_to_group(self, vertex, group_id):
        # Add vertex to the specified group
        self.groups[group_id].append(vertex)
        self.available_vertices.add(vertex)

    def process_new_vertex(self, v, adjacent_vertices):
        # Greedy matching: Try to match the new vertex v with the highest weight connection available
        # Sort adjacent vertices by edge weight in descending order
        sorted_vertices = sorted(adjacent_vertices, key=lambda x: x[1], reverse=True)
        matched = False

        for u, weight in sorted_vertices:
            if u in self.available_vertices:
                # Group ID lookup for the vertex u
                for group_id, vertices in self.groups.items():
                    if u in vertices:
                        # Match found
                        self.available_vertices.remove(u)
                        self.group_weight[group_id] += weight
                        matched = True
                        print(f"Matched vertex {v} with {u} from group {group_id}")
                        print(self.group_weight)
                        return  # Stop once a match is found for this vertex

        # If no match is found
        if not matched:
            print(f"Vertex {v} could not be matched and was dropped")
        # Optional: Handle unmatched vertex v here
        print(self.group_weight)




def main(groups, agents, vertex):
    matcherP = OnlineBipartiteMatcher_Priority()
    matcherG = OnlineBipartiteMatcher_Greedy()
    # Add groups with initial priority
    for i in range(groups):
      matcherP.add_group(str(i+1))
      matcherG.add_group(str(i+1))

    # Simulate adding vertices to groups
    for i in range(agents):
      # print('u'+str(i+1), int(i/(agents/groups)+1))
      matcherP.add_vertex_to_group(f'u{i+1}', f'{int(i/(agents/groups)+1)}')
      matcherG.add_vertex_to_group(f'u{i+1}', f'{int(i/(agents/groups)+1)}')

    # New vertex arrives with edges and their weights
    for i in range(vertex):
      labels = ['u{}'.format(i + 1) for i in range(agents)]
      random.shuffle(labels)
      # Randomize the total number of pairs
      num_pairs = random.randint(1, agents)
      # Generate the list of vertex-weight pairs
      vertex_list = [(labels[j], random.randint(1, 100)) for j in range(num_pairs)]
      print(f'v{i+1}', vertex_list)
      matcherP.process_new_vertex(f'v{i+1}', vertex_list)
      matcherG.process_new_vertex(f'v{i+1}', vertex_list)
    
    data_p = matcherP.group_weight
    data_g = matcherG.group_weight

    return data_p, data_g

if __name__ == "__main__":
    groups = 4
    agents = 100
    vertex = 20
    data_p, data_g = main(groups, agents, vertex)
    draw_plot(data_p, data_g, 'Metrics of Two Algorithms', 'combined_metrics_visualization_20.png')

