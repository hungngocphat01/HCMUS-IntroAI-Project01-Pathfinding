class Node:
    def __init__(self, coord):
        # Tọa độ của node hiện tại 
        self.coord = coord
        # Node liền truớc và chi phí đi từ node liền trước (cập nhât khi duyệt)
        self.prev = None 
        self.prev_cost = 0
        # Danh sách kề
        self.neighbors = []
        self.path_cost = 1e9

    def __repr__(self):
        return f'<Node coord={self.coord} prev={self.prev} neighbors={self.neighbors}>'
        
def get_neighbor_cost(i: int, j: int, bonus_points: list, default_cost=50):
    """
    Hàm trả về 1 tuple 3 tham số gồm tọa độ và chi phí đường đi đến node kề. 
    Returns: dictionary, có các key:
    - `coord`: tọa độ của vị trí đang xét.
    - `cost`: trọng số của đường đi từ vị trí 
    """
    for bonus in bonus_points:
        if (bonus[0], bonus[1]) == (i, j):
            return {'coord': (i, j), 'cost': default_cost + bonus[2]}
    return {'coord': (i, j), 'cost': default_cost}

def is_not_wall(matrix: list, i: int, j: int):
    """
    Hàm kiểm tra xem một tọa độ nào đó có phải là tường không
    """
    rows, cols = len(matrix), len(matrix[0])
    if any((i < 0, i >= rows, j < 0, j >= cols)) or matrix[i][j] == 'x':
        return False
    return True

def append_neighbor(i, j, neighbors: list, matrix: list, bonus_points: list, direction: str):
    """
    Hàm kiểm tra xem một điểm (i, j) có phải là tường không.
    Nếu không phải thì tính chi phí đường đi đến điểm đó rồi thêm điểm đó vào mảng neighbors.
    - `i`, `j`: tọa độ của điểm.
    - `neighbors`: mảng chứa các tọa độ kề.
    - `matrix`: ma trận ASCII.
    - `bonus_points`: mảng danh sách các điểm thưởng.
    - `direction`: điểm này nằm ở phía nào so với điểm đang xét. Chấp nhận: `L, R, U, D`
    """
    assert direction in ('L', 'R', 'U', 'D')
    if is_not_wall(matrix, i, j):
        neighbor = get_neighbor_cost(i, j, bonus_points)
        neighbor['direction'] = direction
        neighbors.append(neighbor)
        
def discover_neighbors(i: int, j: int, matrix: list, bonus_points):
    """
    Hàm trả về các node lân cận của một node có tọa độ `coord`
    """
    neighbors = []
    append_neighbor(i - 1, j, neighbors, matrix, bonus_points, 'U')
    append_neighbor(i + 1, j, neighbors, matrix, bonus_points, 'D')
    append_neighbor(i, j + 1, neighbors, matrix, bonus_points, 'R')
    append_neighbor(i, j - 1, neighbors, matrix, bonus_points, 'L')
    return neighbors

def get_traversable_nodes(matrix):
    """
    Hàm xác định điểm bắt đầu, kết thúc và danh sách các ô có thể đi được trong mê cung.
    Trả về: (traversable_nodes, start, end): (list, tuple, tuple)
    """
    nrows, ncols = len(matrix), len(matrix[0])
    traversable_nodes = []

    for i in range(nrows):
        for j in range(ncols):
            if matrix[i][j] != 'x':
                traversable_nodes.append((i, j))
            if matrix[i][j] == 'S':
                start = (i, j)
            elif matrix[i][j] == ' ' and any((i == 0, i == nrows - 1, j == 0, j == ncols - 1)):
                end = (i, j)
    return traversable_nodes, start, end


def build_adjacency_list(trvsbl_nodes, matrix, bonus_points):
    """
    Hàm xây dựng danh sách kề.
    Nhận vào: 
    - `trvsbl_nodes`: Danh sách các node có thể đi được trong mê cung
    - `coord_to_label`: Ánh xạ từ tọa độ sang nhãn.
    - `matrix`: mê cung dạng ascii.
    - `bonus_points`: danh sách các điểm thưởng.
    Trả về: một dictionary có:
    - Các key: các tọa độ của các ô đi được.
    - Các value: một object Node tương ứng (giữ thông tin danh sách kề với node đó cùng với các thông tin về đường đi khác).
    """
    trvsbl_count = len(trvsbl_nodes)
    
    # Tạo ra danh sách map từ tọa độ các đỉnh sang 1 object chứa các thông tin về đỉnh đó
    node_list = {node: Node(node) for node in trvsbl_nodes}
    
    for node in trvsbl_nodes:
        # Tìm các đỉnh kề
        node_list[node].neighbors = discover_neighbors(*node, matrix, bonus_points)
        
    return node_list


def preprocess_maze(matrix, bonus_points):
    """
    Tiền xử lý dữ liệu nhập vào.
    Trả về một dictionary có các key:
    - `node_list`: danh sách các node của mê cung.
    - `start`: tọa độ của điểm bắt đầu.
    - `end`: tọa độ của điểm kết thúc.
    """
    # Lấy các thông tin về điểm bắt đầu, kết thúc và danh sách các đỉnh của đồ thị
    trvsbl_nodes, start, end = get_traversable_nodes(matrix)
    
    # Ma trận kề 
    node_list = build_adjacency_list(trvsbl_nodes, matrix, bonus_points)
    
    return {
        'node_list': node_list, 
        'start': start, 
        'end': end
    }