from Graph import Graph
from Stack import Stack
from Queue import Queue
from heuristic_func import *

def DFS(graph: Graph, custom_start=None, custom_end=None):
    # Kiểm tra người dùng có specify điểm bắt đầu và kết thúc tùy chỉnh hay không
    # Phục vụ cho phần điểm thưởng
    start_coord = custom_start if custom_start else graph.start
    end_coord = custom_end if custom_start else graph.end
    
    # Bộ nhớ fringe cho DFS là một stack
    fringe = Stack()
    # Tập đóng, chứa tọa độ các đỉnh đã đi qua
    visited_coords = set()
    # Đánh dấu node bắt đầu là đã đi
    visited_coords.add(start_coord)
    
    # Gắn node bắt đầu vào stack với chi phí 0
    fringe.push(start_coord, 0)
    
    while not fringe.is_empty():
        # Lấy ra tọa độ node kế trong stack
        current_node_coord, _ = fringe.pop()
        
        # Lấy ra danh sách các đỉnh kề với node này
        successors = graph.get_successor(current_node_coord)
        # Nếu là dead end: bỏ qua node này
        if len(successors) == 0:
            continue
        
        # Kiểm tra từng node kế
        for node in successors:
            # Nếu node chưa viếng
            if node['coord'] not in visited_coords:
                # Thêm tọa độ của node vào tập đóng
                visited_coords.add(node['coord'])
                # Cập nhật lại node liền trước
                graph.update_prev_node(node['coord'], current_node_coord)
                # Thêm vào fringe
                fringe.push(node['coord'], 0)
            
            # Nếu node kế là đích đến: ồ yeah
            if node['coord'] == end_coord:
                return True
            
    return False

def Astar(graph: Graph, hf, custom_start=None, custom_end=None):
    # Kiểm tra người dùng có specify điểm bắt đầu và kết thúc tùy chỉnh hay không
    # Phục vụ cho phần điểm thưởng
    start_coord = custom_start if custom_start else graph.start
    end_coord = custom_end if custom_start else graph.end
    
    # Bộ nhớ fringe cho A* là một priority queue
    fringe = Queue(priority=True)
    visited = set()
    
    # Đẩy node start vào fringe
    fringe.push(start_coord, 0)
    
    while not fringe.is_empty():
        # Lấy ra node có tổng chi phí thấp nhất
        current_node_coord, current_fcost = fringe.pop()
        visited.add(current_node_coord)
        # Nếu gặp được END: oh yeah!
        if current_node_coord == end_coord:
            return True
        # Lấy ra danh sách các node kề của node hiện tại 
        successors = graph.get_successor(current_node_coord)
        
        for succ in successors:
            # Nếu đã viếng: bỏ qua
            if succ['coord'] in visited:
                continue 
            visited.add(succ['coord'])
            # Nếu chưa có trong open list: thêm vào open list    
            if not fringe.contains(succ['coord']): 
                graph.update_prev_node(succ['coord'], current_node_coord)
                
                hcost = hf(succ['coord'], end_coord)
                gcost = graph.get_path_cost(current_node_coord) + succ['cost']
                fcost = hcost + gcost
                
                graph.set_path_cost(succ['coord'], gcost)
                fringe.push(succ['coord'], fcost)
            # Nếu có rồi
            else:
                # Tính toán lại chi phí đường đi xem đươngf đi mới có tốt hơn không
                gcost = graph.get_path_cost(succ['coord'])
                new_gcost = graph.get_path_cost(current_node_coord) + succ['cost']
                # Nếu đường đi mới tốt hơn, cập nhật lại chi phí
                if new_gcost < gcost:
                    graph.update_prev_node(succ['coord'], current_node_coord)
                    graph.set_path_cost(succ['coord'], new_gcost)
                    hcost = hf(succ['coord'], end_coord)
                    fcost = hcost + new_gcost
                    fringe.update_fcost(succ['coord'], fcost)                    
    return False
