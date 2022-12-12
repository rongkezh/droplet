class Drop:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size

    def __str__(self):
        return f"({self.x},{self.y}){self.size}"

drop1 = Drop(1,2,1)
print(drop1)