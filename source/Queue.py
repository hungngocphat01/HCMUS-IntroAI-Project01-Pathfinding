class Queue:
    """
    Biểu diễn một hàng đợi
    """
    def __init__(self, priority=False):
        # priority=True: bật mode hàng đợi ưu tiên. Nếu cờ này bằng False: hàng đợi thường
        self.queue = []
        self.priority = priority
    
    def push(self, label, cost):
        """
        Hàm thêm phần tử vào hàng đợi. Nhận 2 tham số:
        - `label`: nhãn của phần tử.
        - `cost`: chi phí của phần tử đó.
        """
        self.queue.append((label, cost))
        if self.priority:
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
    
    def contains(self, element):
        """
        Hàm kiểm tra một phần tử nào đó có trong hàng đợi hay không
        """
        for e in self.queue:
            if element == e[0]:
                return True
        return False
    
    def update_fcost(self, element, cost):
        """
        Cập nhật lại fcost của 1 node nào đó (và sắp xếp lại hàng đợi).
        Có vẻ không "tự nhiên" lắm với định nghĩa của CTDL này nhưng để tiện thì tụi em đành phải làm vậy.
        """
        for i, e in enumerate(self.queue):
            if e == element:
                self.queue[i][1] = cost
        if self.priority:
            self.queue.sort(key=lambda node: node[1])
    
    def is_empty(self):
        """
        Kiểm tra hàng đợi có rỗng hay không.
        """
        return len(self.queue) == 0
    
    def clear(self):
        """
        Dọn dẹp hàng đợi (xóa tất cả phần tử)
        """
        self.queue.clear()
