from teacher_utils import visualize_maze

def get_neighbor_cost(i: int, j: int, bonus_points: list, default_cost=50):
    """
    Hàm trả về 1 tuple 3 tham số gồm tọa độ và chi phí đường đi đến node kề. 
    Mặc định là 50. Nếu có điểm thưởng thì trừ đi bớt chi phí.
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


def append_neighbor(i, j, neighbors: list, matrix: list, bonus_points: list):
    """
    Hàm kiểm tra xem một điểm (i, j) có phải là tường không.
    Nếu không phải thì tính chi phí đường đi đến điểm đó rồi thêm điểm đó vào mảng neighbors.
    """
    if is_not_wall(matrix, i, j):
        neighbors.append(get_neighbor_cost(i, j, bonus_points))


def discover_neighbors(i: int, j: int, matrix: list, bonus_points):
    """
    Hàm trả về các node lân cận của một node có tọa độ `coord`
    """
    neighbors = []
    append_neighbor(i - 1, j, neighbors, matrix, bonus_points)
    append_neighbor(i + 1, j, neighbors, matrix, bonus_points)
    append_neighbor(i, j + 1, neighbors, matrix, bonus_points)
    append_neighbor(i, j - 1, neighbors, matrix, bonus_points)
    return neighbors

def get_traversable_nodes(matrix):
    """
    Hàm xác định điểm bắt đầu, kết thúc và danh sách các ô có thể đi được trong mê cung.
    Trả về: (traversable_nodes, start, end): (set, tuple, tuple)
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

def map_node_to_label(nodes):
    """
    Hàm đánh dấu (map) các tọa độ từ mê cung đã cho sang các nhãn là số nguyên.
    Bước tiền xử lý cần thiết để biến mê cung thành ma trận kề.
    Vd: (1, 1) -> 0, (1, 2) -> 1, ... (nhãn được đánh theo thứ tự duyệt).
    
    Nhận vào: danh sách các tuple là các tọa độ các node.
    
    Trả về 2 dictionary: 
    - label_to_coord: key là các nhãn, value là các tọa độ tương ứng.
    - coord_to_label: ngược lại.
    """
    label_to_coord = {}
    coord_to_label = {}
    
    for i, node in enumerate(nodes):
        label_to_coord[i] = node
        coord_to_label[node] = i
    
    return label_to_coord, coord_to_label


def build_adjacency_matrix(trvsbl_nodes, coord_to_label, matrix, bonus_points):
    """
    Hàm xây dựng ma trận kề.
    Nhận vào: 
    - `trvsbl_nodes`: Danh sách các node có thể đi được trong mê cung
    - `coord_to_label`: Ánh xạ từ tọa độ sang nhãn.
    - `matrix`: mê cung dạng ascii.
    - `bonus_points`: danh sách các điểm thưởng.
    Trả về: ma trận kề.
    """
    trvsbl_count = len(trvsbl_nodes)
    
    adj_matrix = [[0 for j in range(trvsbl_count)] for i in range(trvsbl_count)]
    for node in trvsbl_nodes:
        # Nhãn của node hiện tại trên ma trận kề 
        current_node_label = coord_to_label[node]
        # Tìm các đỉnh kề
        neighbors = discover_neighbors(*node, matrix, bonus_points)
        for neighbor in neighbors:
            coord = neighbor['coord']
            cost = neighbor['cost']
            # Nhãn của node kề (hiên tại) trên ma trận kề
            label = coord_to_label[coord]
            adj_matrix[current_node_label][label] = cost
    
    return adj_matrix

def preprocess_maze(matrix, bonus_points):
    """
    Tiền xử lý dữ liệu nhập vào.
    Trả về một dictionary có các key:
    - `adj_matrix`: ma trận kề của mê cung (list).
    - `label_to_coord`: dictionary map từ nhãn trên đồ thị sang tọa độ trên mê cung.
    - `coord_to_label`: dictionary làm điều ngược lại.
    - `start`: tọa độ của điểm bắt đầu.
    - `end`: tọa độ của điểm kết thúc.
    """
    # Lấy các thông tin về điểm bắt đầu, kết thúc và danh sách các đỉnh của đồ thị
    trvsbl_nodes, start, end = get_traversable_nodes(matrix)
    # Tạo map từ tọa độ các điểm trong mê cung -> nhãn các đỉnh trên đồ thị
    label_to_coord, coord_to_label = map_node_to_label(trvsbl_nodes)
    
    # Ma trận kề 
    adj_matrix = build_adjacency_matrix(trvsbl_nodes, coord_to_label, matrix, bonus_points)
    
    return {
        'adj_matrix': adj_matrix, 
        'label_to_coord': label_to_coord, 
        'coord_to_label': coord_to_label, 
        'start': start, 
        'end': end
    }

