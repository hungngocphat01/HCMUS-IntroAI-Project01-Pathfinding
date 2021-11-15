from Graph import Graph
from Stack import Stack
from Queue import Queue
from heuristic_func import *
from copy import deepcopy

"""
Module cài đặt các hàm tìm kiếm không có điểm thưởng
Mỗi hàm đều có các tham số sau:
- `graph`: đồ thị cần chạy thuật toán tìm.
- `custom_start`: điểm bắt đầu tùy chọn. Nếu không có thì điểm bắt đầu sẽ được lấy là điểm start của đồ thị.
- `custom_end`: điểm kết thúc tùy chọn, tương tự như trên.
- `hf` (nếu có): con trỏ đến hàm heuristic.

Trả về: True nếu có đường đi, False nếu không có.
"""

def BFS(graph: Graph, custom_start=None, custom_end=None):
    # Kiểm tra người dùng có specify điểm bắt đầu và kết thúc tùy chỉnh hay không
    # Phục vụ cho phần điểm thưởng
    start_coord = custom_start if custom_start else graph.start
    end_coord = custom_end if custom_start else graph.end
     # Bộ nhớ fringe cho BFS là một queue
    fringe = Queue()
    # Tập đóng, chứa tọa độ các đỉnh đã đi qua
    visited_coords = set()
    # Đánh dấu node bắt đầu là đã đi
    visited_coords.add(start_coord)
    # Gắn node bắt đầu vào stack với chi phí 0
    fringe.push(start_coord, 0)

    while not fringe.is_empty():
        current_node_coord, _ = fringe.pop()
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
    
def DFS(graph: Graph, custom_start=None, custom_end=None):
    # Kiểm tra người dùng có specify điểm bắt đầu và kết thúc tùy chỉnh hay không
    # Phục vụ cho phần điểm thưởng
    start_coord = custom_start if custom_start else graph.start
    end_coord = custom_end if custom_end else graph.end
    
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


def GBFS(graph: Graph, hf, custom_start=None, custom_end=None, custom_visited=None):
    start_coord = custom_start if custom_start else graph.start
    end_coord = custom_end if custom_end else graph.end
    
    # Bộ nhớ fringe cho GBFS là một priority queue
    fringe = Queue(priority=True)
    # Tập đóng, chứa tọa độ các đỉnh đã đi qua
    visited_coords = custom_visited if custom_visited else set()
    
    # Đánh dấu node bắt đầu là đã đi
    visited_coords.add(start_coord)
    
    # Gắn node bắt đầu vào queue với chi phí 0
    fringe.push(start_coord, 0)
    
    while not fringe.is_empty():
        # Lấy ra tọa độ node kế trong queue
        current_node_coord, _ = fringe.pop()
        
        # Nếu node kế là đích đến: ồ yeah
        if current_node_coord == end_coord:
            return True
        
        # Lấy ra danh sách các đỉnh kề với node này
        successors = graph.get_successor(current_node_coord)
        
        # Kiểm tra từng node kế
        for node in successors:
            # Nếu node chưa viếng
            if node['coord'] not in visited_coords:
                # Thêm tọa độ của node vào tập đóng
                visited_coords.add(node['coord'])
                graph.update_prev_node(node['coord'], current_node_coord)
                # Thêm vào fringe
                fcost = hf(node['coord'], end_coord)
                fringe.push(node['coord'], fcost)
            
    return False

def Astar(graph: Graph, hf, custom_start=None, custom_end=None, custom_visited=None):
    # Kiểm tra người dùng có specify điểm bắt đầu và kết thúc tùy chỉnh hay không
    # Phục vụ cho phần điểm thưởng
    start_coord = custom_start if custom_start else graph.start
    end_coord = custom_end if custom_end else graph.end
    
    # Bộ nhớ fringe cho A* là một priority queue
    fringe = Queue(priority=True)
    visited = custom_visited if custom_visited else set()
    
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
            # Nếu chưa có trong open list: thêm vào open list    
            if not fringe.contains(succ['coord']): 
                graph.update_prev_node(succ['coord'], current_node_coord)
                
                hcost = hf(succ['coord'], end_coord)
                gcost = graph.get_path_cost(current_node_coord) + succ['cost']
                
                """
                Với bản đồ có điểm thưởng (gcost có thể âm) thì gán lại = 0.
                Khi bản đồ có điểm thưởng thì sẽ có cạnh trọng số âm, nó 
                nằm ngoài domain của A* rồi nên em nghĩ trường hợp này có 
                chỉnh lại A* tí cũng không sao ạ. Còn nếu bản đồ không có điểm
                thưởng thì statement này sẽ không bao giờ được kích hoạt.
                """
                gcost = 0 if gcost < 0 else gcost
                fcost = hcost + gcost
                
                graph.set_path_cost(succ['coord'], gcost)
                fringe.push(succ['coord'], fcost)
            # Nếu có rồi
            else:
                # Tính toán lại chi phí đường đi xem đươngf đi mới có tốt hơn không
                gcost = graph.get_path_cost(succ['coord'])
                new_gcost = graph.get_path_cost(current_node_coord) + succ['cost']
                new_gcost = 0 if new_gcost < 0 else new_gcost
                # Nếu đường đi mới tốt hơn, cập nhật lại chi phí
                if new_gcost < gcost:
                    graph.update_prev_node(succ['coord'], current_node_coord)
                    graph.set_path_cost(succ['coord'], new_gcost)
                    hcost = hf(succ['coord'], end_coord)
                    fcost = hcost + new_gcost
                    fringe.update_fcost(succ['coord'], fcost)                    
    return False

"""
Đây là hàm cài đặt A* cho trường hợp có điểm thưởng, với một hàm heuristic tùy chinhr để "thu hút" agent đi về phía các điểm thưởng, nhưng thất bại nên tụi em đã bỏ nó.
"""
# def Astar_bonus(graph: Graph, hf, custom_start=None, custom_end=None, custom_visited=None):
#     # Kiểm tra người dùng có specify điểm bắt đầu và kết thúc tùy chỉnh hay không
#     # Phục vụ cho phần điểm thưởng
#     start_coord = custom_start if custom_start else graph.start
#     end_coord = custom_end if custom_end else graph.end
    
#     # Bộ nhớ fringe cho A* là một priority queue
#     fringe = Queue(priority=True)
#     visited = custom_visited if custom_visited else set()
    
#     # Đẩy node start vào fringe
#     fringe.push(start_coord, 0)
    
#     start_end_length = hf(start_coord, end_coord)
    
#     def bonus_heuristic(coord):
#         # Hàm tính heuristic với điểm thưởng 
#         # Điểm nào càng gần điểm thưởng thì heuristic sẽ càng nhỏ (âm)
#         # Để "kéo" agent đi về phía điểm thưởng.
        
#         # Lấy ra tất cả điểm thưởng
#         bonus_points = deepcopy(graph.bonus_points)
        
#         i = 0
#         while i < len(bonus_points):
#             point = bonus_points[i]
#             bonus_coord = point['coord']
#             bonus_score = point['score']
#             # "Tỉa" bớt các điểm thưởng đã viếng hoặc trùng với điểm đang xét
#             if bonus_coord == coord: #or bonus_coord in visited:
#                 return 1
#             # Tính khoảng cách heuristic đến từng điểm thưởng
#             else:
#                 point['distance'] = hf(bonus_coord, coord)
#                 i += 1
        
#         # Nếu không còn bonus point nào (tức tất cả đã viếng)
#         if len(bonus_points) == 0:
#             return 0
#         # Xếp theo heuristic: khoảng cách + điểm thưởng (đt < 0)
#         bonus_points.sort(key=lambda point: point['distance'] + point['score'])
        
#         next_point = bonus_points[0]
        
#         # Heuristic tỉ lệ thuận với k/c: kc càng nhỏ, heuristic càng nhỏ
#         # Tỉ lệ thuận với độ lớn điểm: điểm có trị tuyệt đối càng lớn, heuristic càng nhỏ
#         return -abs(next_point['distance'] - next_point['score'])

        
#     while not fringe.is_empty():
#         # Lấy ra node có tổng chi phí thấp nhất
#         current_node_coord, current_fcost = fringe.pop()
# #         print('Standing at', current_node_coord)
#         visited.add(current_node_coord)
#         # Nếu gặp được END: oh yeah!
#         if current_node_coord == end_coord:
#             return True
#         # Lấy ra danh sách các node kề của node hiện tại 
#         successors = graph.get_successor(current_node_coord)
        
#         for succ in successors:
#             # Nếu đã viếng: bỏ qua
#             if succ['coord'] in visited:
#                 continue 

#             bonus = bonus_heuristic(succ['coord'])
#             # Nếu chưa có trong open list: thêm vào open list    
#             if not fringe.contains(succ['coord']): 
#                 graph.update_prev_node(succ['coord'], current_node_coord)
                
#                 hcost = hf(succ['coord'], end_coord)
                
#                 gcost = graph.get_path_cost(current_node_coord) + succ['cost']
#                 gcost = gcost if gcost > 0 else 0
                
#                 fcost = hcost + gcost + bonus
# #                 print('Neighbor', succ['coord'], 'has f', fcost, 'bonus', bonus)

#                 graph.set_path_cost(succ['coord'], gcost)
#                 fringe.push(succ['coord'], fcost)
#             # Nếu có rồi
#             else:
#                 # Tính toán lại chi phí đường đi xem đươngf đi mới có tốt hơn không
#                 gcost = graph.get_path_cost(succ['coord'])
#                 new_gcost = graph.get_path_cost(current_node_coord) + succ['cost'] + bonus
#                 new_gcost = new_gcost if new_gcost > 0 else 0
                
#                 # Nếu đường đi mới tốt hơn, cập nhật lại chi phí
#                 if new_gcost < gcost:
#                     graph.update_prev_node(succ['coord'], current_node_coord)
#                     graph.set_path_cost(succ['coord'], new_gcost)
#                     hcost = hf(succ['coord'], end_coord)
#                     fcost = hcost + new_gcost
# #                     print('Neighbor updated', succ['coord'], 'has f', fcost, 'bonus', bonus)

#                     fringe.update_fcost(succ['coord'], fcost)                    
#     return False