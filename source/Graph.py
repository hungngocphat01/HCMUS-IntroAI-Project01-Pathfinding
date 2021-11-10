from maze_preprocess import preprocess_maze
from teacher_utils import read_file, visualize_maze

class Graph:
    """
    Lớp đối tượng biểu diễn một đồ thị.
    Constructor nhận vào một tập tin chứa mê cung.
    """
    def __init__(self, filename):
        # Đọc thông tin từ file
        self.bonus_points, self.ascii_matrix = read_file(filename)
        # Tiền xử lý mê cung
        out = preprocess_maze(self.ascii_matrix, self.bonus_points)
        # Trích xuất các thông tin từ bước tiền xử lý 
        self.start = out['start']
        self.end = out['end']
        self.node_list = out['node_list']
    
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

    def get_path(self):
        node = self.node_list[self.end]
        path = []
        cost = 0
        while node.coord != self.start:
            path.append(node.coord)
            cost += node.prev_cost
            node = self.node_list[node.prev]
        path.append(self.start)
        path.reverse()
        return path, cost
    
    def visualize(self, route=None, debug=False):
        """
        Vẽ mê cung của đồ thị này
        """
        visualize_maze(self.ascii_matrix, self.bonus_points, self.start, self.end, route)
    