from Graph import Graph
from Stack import Stack
from Queue import Queue
from heuristic_func import *

def DFS(graph: Graph, custom_start=None, custom_end=None):
    """
    Hàm tìm kiếm theo giải thuật Deep First Search. Các tham số:
    - `graph`: đồ thị cần tìm kiếm.
    - `hf`: con trỏ đến hàm heuristics.
    `hf` phải có signature như sau: `hf(label1, label2, label_to_coord)`, trả về chi phí từ label1 đến label2.
    - `custom_start`: nhãn bắt đầu tùy chỉnh. Nếu không có thì lấy nhãn bắt đầu của đồ thị truyền vào.
    - `custom_end`: nhãn kết thúc tùy chỉnh. Hành xử tương tự như trên.
    """
    
    # Kiểm tra người dùng có specify điểm bắt đầu và kết thúc tùy chỉnh hay không
    start_label = custom_start if custom_start else graph.start_label
    end_label = custom_end if custom_start else graph.end_label
    
    # Bộ nhớ fringe cho DFS là một stack
    fringe = Stack()
    
    # Dictionary để truy ngược các node đã viếng (dưới dạng "giả" một DSLK đơn)
    # Key: Node cần truy, Value: tuple(nhãn node liền trước, chi phí đường đi)
    visited = {start_label: (None, 0)}
    
    # Gắn node bắt đầu vào hàng đợi với chi phí 0
    fringe.push(start_label, 0)
    
    while not fringe.is_empty():
        # Lấy ra node kế trong stack
        current_node, _ = fringe.pop()
        
        # Lấy ra danh sách các đỉnh kề với node này
        successors = graph.get_successor(current_node)
        # Nếu là dead end: bỏ qua node này và không đụng tới nữa
        if len(successors) == 0:
            fringe.pop()
            continue
        
        # Kiểm tra từng node kế
        for succ_node, succ_cost in successors:
            # Kiểm tra xem node đã viếng chưa. Nếu chưa thì thêm vào danh sách
            if succ_node not in visited:
                visited[succ_node] = (current_node, succ_cost)
                # DFS không có heuristic nên h(x) = 0
                fringe.push(succ_node, 0)
                
            # Nếu node kế là đích đến: ồ yeah
            if succ_node == end_label:
                return visited
            
    return None


def GBFS(graph: Graph, hf, custom_start=None, custom_end=None):
    """
    Hàm tìm kiếm theo giải thuật Greedy Best First Search. Các tham số:
    - `graph`: đồ thị cần tìm kiếm.
    - `hf`: con trỏ đến hàm heuristics.
    `hf` phải có signature như sau: `hf(label1, label2, label_to_coord)`, trả về chi phí từ label1 đến label2.
    - `custom_start`: nhãn bắt đầu tùy chỉnh. Nếu không có thì lấy nhãn bắt đầu của đồ thị truyền vào.
    - `custom_end`: nhãn kết thúc tùy chỉnh. Hành xử tương tự như trên.
    """
    
    # Kiểm tra người dùng có specify điểm bắt đầu và kết thúc tùy chỉnh hay không
    start_label = custom_start if custom_start else graph.start_label
    end_label = custom_end if custom_start else graph.end_label
    
    # Hàng đợi ưu tiên
    fringe = Queue(priority=True)
    
    # Dictionary để truy ngược các node đã viếng (dưới dạng "giả" một DSLK đơn)
    # Key: Node cần truy, Value: tuple(nhãn node liền trước, chi phí đường đi)
    visited = {start_label: (None, 0)}
    
    # Gắn node bắt đầu vào hàng đợi với chi phí 0
    fringe.push(start_label, 0)
    
    while not fringe.is_empty():
        # Lấy ra node có chi phí thấp nhất
        current_node, current_cost = fringe.pop()
        
        # Lấy ra danh sách các đỉnh kề với node này
        successors = graph.get_successor(current_node)
        
        # Kiểm tra từng node kế 
        for succ_node, succ_cost in successors:
            # Kiểm tra xem node đã viếng chưa. Nếu chưa thì thêm vào fringe
            if succ_node not in visited:
                heuristic_cost = hf(succ_node, end_label, graph.label_to_coord)
                visited[succ_node] = (current_node, succ_cost)
                fringe.push(succ_node, heuristic_cost)
                
            # Nếu node kế là đích đến: ồ yeah
            if succ_node == end_label:
                return visited
            
    return None