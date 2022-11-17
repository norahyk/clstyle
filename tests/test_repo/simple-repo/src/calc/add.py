import rich

AAA = 1

class Class():
    def __init__(self):
        self.a = 1
    
    def method(self, b):
        return self.a + b

def add(a, b):
    """Return sum of a and b"""
    c = a + b
    return c