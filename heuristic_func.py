def lnorm(vector: tuple, p: int):
    """
    Hàm tính norm p của một vector 
    """
    s = sum([pow(abs(v), p) for v in vector])
    return pow(s, 1/p)

def heuristics(label1: int, label2: int, label_to_coord: dict, p: int):
    """
    Hàm tính heuristic giữa 2 label trên ma trận bằng khoảng cách Manhattan/Euclide.
    Tham số:
    - `label1`, `label2`: nhãn của điểm 1, 2.
    - `label_to_coord`: ánh xạ từ nhãn sang tọa độ.
    - `p`: nếu bằng 1 thì tính khoảng cách Manhattan, 2 nếu tính khoảng cách Euclide.
    """
    coord1 = label_to_coord[label1]
    coord2 = label_to_coord[label2]
    
    distance_vector = (abs(c1 - c2) for c1, c2 in zip(coord1, coord2))
    return lnorm(distance_vector, p)

manhattan_heuristic = lambda label1, label2, label_to_coord: heuristics(label1, label2, label_to_coord, 1)
euclide_heuristic = lambda label1, label2, label_to_coord: heuristics(label1, label2, label_to_coord, 2)