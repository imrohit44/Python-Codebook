import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def cross_product(o, a, b):
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

def graham_scan(points):
    min_y_point = min(points, key=lambda p: (p.y, p.x))
    
    points.remove(min_y_point)
    
    points.sort(key=lambda p: (math.atan2(p.y - min_y_point.y, p.x - min_y_point.x), distance(min_y_point, p)))
    
    stack = [min_y_point, points[0], points[1]]
    
    for i in range(2, len(points)):
        while cross_product(stack[-2], stack[-1], points[i]) <= 0:
            stack.pop()
        stack.append(points[i])
        
    return stack

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

if __name__ == '__main__':
    points = [
        Point(0, 3), Point(1, 1), Point(2, 2), Point(4, 4),
        Point(0, 0), Point(1, 2), Point(3, 1), Point(3, 3)
    ]
    
    hull = graham_scan(points)
    print("Points on the convex hull:")
    for p in hull:
        print(f"({p.x}, {p.y})")