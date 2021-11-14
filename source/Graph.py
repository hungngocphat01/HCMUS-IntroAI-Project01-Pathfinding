from copy import deepcopy
from maze_preprocess import preprocess_maze
from teacher_utils import read_file, visualize_maze

class Graph:
    """
    Lớp đối tượng biểu diễn một đồ thị.
    Constructor nhận vào một tập tin chứa mê cung.
    """
    def __init__(self, filename):
        # Đọc thông tin từ file
        if filename is not None:
            bonus_points, self.ascii_matrix = read_file(filename)
            # Tiền xử lý mê cung
            out = preprocess_maze(self.ascii_matrix, bonus_points)
            # Trích xuất các thông tin từ bước tiền xử lý 
            self.start = out['start']
            self.end = out['end']
            self.node_list = out['node_list']
            
            self.bonus_points = []
            for point in bonus_points:
                self.bonus_points.append({
                    'coord': (point[0], point[1]), 'score': point[2]
                })
            
            print('Graph initialized from maze with size', len(self.ascii_matrix), 'x', len(self.ascii_matrix[0]))
        else:
            self.bonus_points, self.ascii_matrix = None, None
            self.start = None 
            self.end = None 
            self.node_list = None
    
    def get_successor(self, coord) -> list:
        """
        Lấy ra danh sách các điểm kề với điểm có label được truyền vào.
        Format kết quả trả về: một list có các phần tử là list các dictionary có các cặp key-value:
        - `coord`: ứng với tọa độ đỉnh kề.
        - `cost`: ứng với chi phí từ đỉnh đang xét đến đỉnh kề này.
        - `direction`: hướng của đỉnh kề so với đỉnh đang xét (L, R, U, D).
        """
        succs = []
        for node in self.node_list[coord].neighbors:
            succs.append(node)
        return succs

    def get_path_cost(self, coord):
        return self.node_list[coord].path_cost
    
    def set_path_cost(self, coord, path_cost):
        self.node_list[coord].path_cost = path_cost
    
    def update_prev_node(self, coord: tuple, prev_coord: tuple):
        """
        Cập nhật đỉnh liền trước có tọa độ `coord` thành `prev_coord`.
        """
        self.node_list[coord].prev = prev_coord
        # Lấy ra chi phí từ prev_coord -> coord
        prev_cost = 0
        # Nếu 2 đỉnh này không kề nhau, chi phí là 0 (phục vụ cho phần teleport nâng cao)
        for neighbor in self.node_list[prev_coord].neighbors:
            if neighbor['coord'] == coord:
                prev_cost = neighbor['cost']
        self.node_list[coord].prev_cost = prev_cost

    def get_path(self, custom_start=None, custom_end=None, no_bonus=False) -> tuple:
        """
        Lấy đường đi của mê cung sau khi đã giải xong.
        Trả về: danh sách các tọa độ từ START -> END và tổng chi phí.
        """
        start_coord = custom_start if custom_start else self.start
        end_coord = custom_end if custom_end else self.end

        node = self.node_list[end_coord]
        if node.prev == None:
            print('Không tìm được đường đi')
            return 
            
        path = []
        cost = 0
        while node.coord != start_coord:
            path.append(node.coord)
            cost += 1
            # Đến node tiếp theo
            node = self.node_list[node.prev]
        path.append(start_coord)
        
        if not no_bonus:
            for node in path:
                if self.bonus_points is not None:
                    for bonus in self.bonus_points:
                        if bonus['coord'] == node:
                            cost += bonus['score']
        path.reverse()
        return path, cost
    
    def get_visited(self, custom_start=None, custom_end=None) -> tuple:
        """
        Trả về các đỉnh đã viếng trong quá trình duyệt (để minh họa tốt hơn).
        Kết quả: các đỉnh đã viếng, đường đi từ START -> END, tổng chi phí đường đi
        """
        visited = set()
        for node in self.node_list:
            if self.node_list[node].prev != None:
                visited.add(node)
        path, cost = self.get_path(custom_start, custom_end)
        visited = visited - set(path)
        return visited, list(path), cost
    
    def visualize(self, route=None, visited=None, figsize=(5, 3), dont_show=False):
        """
        Vẽ mê cung của đồ thị này
        """
        return visualize_maze(self.ascii_matrix, self.bonus_points, 
                       self.start, self.end, route, figsize=figsize, visited=visited, dont_show=dont_show)
    
    def clear(self):
        """
        Xóa các thông tin về đường đi của đồ thị (để chạy thuật toán mới)
        """
        for node in self.node_list:
            self.node_list[node].prev = None
            self.node_list[node].prev_cost = None
            self.node_list[node].path_cost = 0
            
    def get_bonus_point(self, coord):
        for point in self.bonus_points:
            if point['coord'] == coord:
                return deepcopy(point)
        return {'coord': coord, 'score': 0}
    