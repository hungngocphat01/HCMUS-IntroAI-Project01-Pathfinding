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
    # Tập đóng, chứa tọa độ các đỉnh đã đi qua
    visited_coords = set()
    # Đánh dấu node bắt đầu là đã đi
    visited_coords.add(start_coord)
    
    # Gắn node bắt đầu vào queue với chi phí 0
    fringe.push(start_coord, 0)
    
    while not fringe.is_empty():
        # Lấy ra tọa độ node kế trong queue
        current_node_coord, current_node_cost = fringe.pop()
        
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
                # Tính heuristic
                heuristic_cost = hf(node['coord'], end_coord)
                # Tính chi phí từ start đến node hiện tại = chi phí từ start đến node trước + chi phí từ node trước đến node này
                path_cost = current_node_cost + node['cost']
                fringe.push(node['coord'], heuristic_cost + path_cost)
            
            # Nếu node kế là đích đến: ồ yeah
            if node['coord'] == end_coord:
                return True
            
    return False