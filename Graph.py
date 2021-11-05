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
        self.start_coord = out['start']
        self.end_coord = out['end']
        self.matrix = out['adj_matrix']
        self.coord_to_label = out['coord_to_label']
        self.label_to_coord = out['label_to_coord']
        
        self.start_label = self.coord_to_label[self.start_coord]
        self.end_label = self.coord_to_label[self.end_coord]
    
    def get_successor(self, label) -> list:
        """
        Lấy ra danh sách các điểm kề với điểm có label được truyền vào.
        Format kết quả trả về: một list có các phần tử theo dạng:
        [(label1, cost1), (label2, cost2), ...]
        """
        succ = []
        for i in range(len(self.matrix)):
            if self.matrix[label][i] > 0:
                succ.append((i, self.matrix[label][i]))
        return succ
    
    def backtrack(self, backtrack_list):
        """
        Lần ngược lại danh sách các đỉnh đã viếng để tìm ra đường đi.
        Nhận vào: backtracking list của thuật toán.
        Trả về: đường đi (xếp theo thứ tự start -> end).
        """
        if backtrack_list == None:
            return None 
        
        path = []
        current_node = self.end_label
        while current_node is not None:
            path.append(current_node)
            current_node = backtrack_list[current_node]
        path.reverse()
        return path
        
    
    def convert_path_to_coord(self, path: list) -> list:
        """
        Hàm chuyển đổi đường đi từ danh sách các nhãn sang danh sách các tọa độ
        """
        if path is None:
            return None
        return [self.label_to_coord[i] for i in path]
    
    def visualize(self, route=None, debug=False):
        """
        Vẽ mê cung của đồ thị này
        """
        if debug:
            visualize_maze(self.ascii_matrix, self.bonus_points, self.start_coord, self.end_coord, route, self.coord_to_label)
        else: 
            visualize_maze(self.ascii_matrix, self.bonus_points, self.start_coord, self.end_coord, route)
    