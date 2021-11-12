from Graph import Graph
from Queue import Queue
from Stack import Stack
from maze_preprocess import Node
from copy import deepcopy

def make_routing_graph(g: Graph, hf):
    # Khởi tạo một đồ thị rỗng
    routing = Graph(None)
    start = g.start 
    end = g.end
    
    routing.start = start 
    routing.end = end 
    # Danh sách các node của đồ thị định hướng
    node_list = {
        start: Node(start),
        end: Node(end)
    }
    # Nối start và end
    node_list[start].neighbors.append({
        'coord': end, 
        'cost': hf(end, start)
    })
    
    # Danh sách các đỉnh tương ứng với từng điểm thưởng
    bonus_nodes = []
    bonus_values = {}
    
    # Với mỗi điểm thưởng 
    for bonus in g.bonus_points:
        new_coord = (bonus[0], bonus[1])
        new_cost = bonus[2]
        bonus_values[new_coord] = new_cost
        
        # Tạo một đỉnh tương ứng với tọa độ của nó
        new_node = Node(new_coord)
        # Kết nối đỉnh này với tất cả các đỉnh đang có của đồ thị
        for i, old_node in enumerate(bonus_nodes):
            distance = hf(old_node.coord, new_coord)
            new_old_cost = distance + bonus_values[old_node.coord]
            old_new_cost = distance + new_cost
            
            if new_old_cost < 0:
                new_old_cost = 0
            if old_new_cost < 0:
                old_new_cost = 0
            
            # Nối đỉnh này với đỉnh đang có
            new_node.neighbors.append({
                'coord': old_node.coord, 
                'cost': new_old_cost
            })
            # Nối đỉnh đang có với đỉnh này
            bonus_nodes[i].neighbors.append({
                'coord': new_coord, 
                'cost': old_new_cost
            })
        # Nối đỉnh này với đỉnh end
        new_node.neighbors.append({
            'coord': end, 
            'cost': hf(end, new_coord)
        })
        bonus_nodes.append(new_node)
    
    # Kết nối đỉnh start với tất cả các đỉnh thưởng
    # Thêm các đỉnh thưởng vào đồ thị định hướng
    for bonus_node in bonus_nodes:
        node_list[start].neighbors.append({
            'coord': bonus_node.coord, 
            'cost': hf(bonus_node.coord, start) + bonus_values[bonus_node.coord]
        })
        
        node_list[bonus_node.coord] = bonus_node
    
    routing.node_list = node_list
    return routing

def bonus_traversal_wrapper(g: Graph, algorithm, journey: list):  
    waiting_list = Queue(priority=True)
    
    for i, bonus in enumerate(journey):
        waiting_list.push(bonus, i)
        
    journey_data = Stack()
    traversed = Stack()
    
    prev_loc, prev_index = waiting_list.pop()
    
    while not waiting_list.is_empty():
        g.clear()
        next_dest, next_index = waiting_list.pop()
        print('Going from', prev_loc, 'to', next_index)
        
        result = algorithm(g, start=prev_loc, end=next_dest)
        
        if not result:
            print('Result not found, backtracking...')
            journey_data.pop()
            waiting_list.push(next_dest, next_index)
            prev_loc, prev_index = traversed.pop()
            continue
        
        print('Result found! Keep going!')
        visited, path, cost = g.get_visited(prev_loc, next_dest)
        journey_data.push({'visited': visited, 'path': path, 'cost': cost})
        traversed.push((prev_loc, prev_index))
        
        prev_loc, prev_index = next_dest, next_index
        
        if prev_loc == g.end:
            return journey_data
    
    return None

def process_journey(g: Graph, journey: list):
    path = []
    cost = 0
    visited = set()
    
    for segment in journey.stack:
        path += segment[0]['path']
        cost += segment[0]['cost']
        visited.union(segment[0]['visited'])
    
    visited = list(visited)
    for node in path:
        for bonus in g.bonus_points:
            if node == (bonus[0], bonus[1]):
                cost += bonus[2]
                print('Visited', node)
    
    return list(visited), path, cost