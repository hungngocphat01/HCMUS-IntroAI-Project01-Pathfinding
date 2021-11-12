class Stack:
    """
    Biểu diễn một ngăn xếp
    """
    def __init__(self):
        self.stack = []
    
    def push(self, label, cost=None):
        """
        Hàm thêm phần tử vào ngăn xếp. Nhận 2 tham số:
        - `label`: nhãn của phần tử.
        - `cost`: chi phí của phần tử đó.
        """
        self.stack.append((label, cost))
    
    def peek(self):
        """
        Xem phần tử nằm ở đỉnh ngăn xếp.
        Trả về tuple: (label, cost)
        """
        if self.is_empty():
            return None
        return self.stack[-1]
    
    def pop(self):
        """
        Như `peek`, nhưng sau đó xóa phần tử nằm ở đỉnh ngăn xếp|.
        """
        if self.is_empty():
            return None
        element = self.stack[-1]
        del self.stack[-1]
        return element
    
    def is_empty(self):
        """
        Kiểm tra ngăn xếp có rỗng hay không.
        """
        return len(self.stack) == 0
    