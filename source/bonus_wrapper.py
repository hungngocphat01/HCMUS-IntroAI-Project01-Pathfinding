from Graph import Graph
from Queue import Queue
from Stack import Stack
from maze_preprocess import Node
from copy import deepcopy

def bonus_wrapper(g: Graph, algorithm, hf):
    traversable = []
    for node in g.bonus_points:
        traversable.append(node['coord'])
    traversable.append(g.end)
     
    forbidden = set()
    
    path_tracker = {}
    prev_node_tracker = {g.start: None}
    total_cost = 0
        
    visited = {node: set() for node in traversable}
    visited[None] = set()
    visited[g.start] = set()
    
    current = g.start
    while True:
        # Nếu tất cả các node đều bị cấm: không có đuòng đi
        if all([node in forbidden for node in traversable]) or current == None:
            print('Me cannot find a way.')
            return None, None
        
        # Thêm các điểm đã đi của node liền trước vào các điểm đã đi của node này
        for node in visited[prev_node_tracker[current]]:
            visited[current].add(node)
            
        # Tìm ra node gần nhất sao cho chưa đi
        fringe = Queue(priority=True)
        for node in traversable:
            if node not in visited[current] and node not in forbidden:
                f = hf(current, node) + hf(node, g.end) + g.get_bonus_point(node)['score']
                fringe.push(node, f)
        
        # Nếu không tìm ra được node nào mà current chưa đi (current là ngõ cụt)
        if fringe.is_empty():
            forbidden.add(current)
            current = prev_node_tracker[current]
            print('Hmmm, this seems to be a dead end. Me go back then.')
            continue 

        dest, _ = fringe.pop()
        
        path_to_current = set()
        if current != g.start:
            prev_node = prev_node_tracker[current]
            path_to_current, _ = path_tracker[(prev_node, current)]
            path_to_current = set(path_to_current)
            
        # Tìm đường đi từ current đến dest
        g.clear()
        print('Going from', current, 'to', dest)
        result = algorithm(g, hf, current, dest, path_to_current)
        visited[current].add(dest)
        # Nếu ko tồn tại đường đi: tìm node gần thứ nhì 
        if not result:
            continue 
            
        # Nếu có đường đi: ghi lại đường đi 
        path, cost = g.get_path(current, dest, no_bonus=True)
        
        print('Found a path! Keep going...')
        path_tracker[(current, dest)] = (path, cost)
        prev_node_tracker[dest] = current

        current = dest
        
        if current == g.end:
            print('Yay! Finished!')
            return path_tracker, prev_node_tracker
        
def process_path_bonus(start, end, path_tracker, prev_node_tracker):
    total_cost = 0
    node = end 
    
    paths = []
    while True:
        prev_node = prev_node_tracker[node]
        if prev_node is None:
            break 
        current_path, current_cost = path_tracker[(prev_node, node)]
        paths.append(current_path)
        total_cost += current_cost
        node = prev_node
    
    path = []
    for i in range(len(paths) - 1, -1, -1):
        # Lấy ra node cuối (để tránh trùng)
        paths[i].pop()
        path += paths[i]
    
    return path, total_cost

def process_path_total(g: Graph, path_tracker, prev_node_tracker):
    path, total_cost = process_path_bonus(g.start, g.end, path_tracker, prev_node_tracker)
    
    for node in path:
        if g.bonus_points is not None:
            for bonus in g.bonus_points:
                if bonus['coord'] == node:
                    total_cost += bonus['score']
    return path, total_cost