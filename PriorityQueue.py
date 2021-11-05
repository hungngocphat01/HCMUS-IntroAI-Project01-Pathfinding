class PriorityQueue:
    """
    Biểu diễn một hàng đợi ưu tiên
    """
    def __init__(self):
        self.queue = []
    
    def push(self, label, cost):
        """
        Hàm thêm phần tử vào hàng đợi. Nhận 2 tham số:
        - `label`: nhãn của phần tử.
        - `cost`: chi phí của phần tử đó.
        """
        self.queue.append((label, cost))
        self.queue.sort(key=lambda node: node[1])
    
    def peek(self):
        """
        Xem phần tử nằm ở đỉnh hàng đợi.
        Trả về tuple: (label, cost)
        """
        if self.is_empty():
            return None
        return self.queue[0]
    
    def pop(self):
        """
        Như `peek`, nhưng sau đó xóa phần tử nằm ở đỉnh hàng đợi|.
        """
        if self.is_empty():
            return None
        element = self.queue[0]
        del self.queue[0]
        return element
    
    def is_empty(self):
        """
        Kiểm tra hàng đợi có rỗng hay không.
        """
        return len(self.queue) == 0
    