def lnorm(vector: tuple, p: int):
    """
    Hàm tính norm p của một vector 
    """
    s = sum([pow(abs(v), p) for v in vector])
    return pow(s, 1/p)

def heuristics(coord1: tuple, coord2: tuple, p: int):
    """
    Hàm tính heuristic giữa 2 điểm tọa độ bằng khoảng cách Manhattan/Euclide.
    """
    
    distance_vector = (abs(c1 - c2) for c1, c2 in zip(coord1, coord2))
    return lnorm(distance_vector, p)

# Hàm heuristic ứng với khoảng cách Manhattan và Euler
manhattan_heuristic = lambda coord1, coord2: heuristics(coord1, coord2, 1) 
euclide_heuristic = lambda coord1, coord2: heuristics(coord1, coord2, 2) 