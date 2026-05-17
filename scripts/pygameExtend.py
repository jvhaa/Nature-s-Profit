import math

def angleBetweenTwoPoints(x1, y1, x2, y2):
    return math.atan2(y1 - y2, x2 - x1) / math.pi * 180

def sin(angle):
    rad = angle/180*math.pi
    return -math.sin(rad)

def cos(angle):
    rad = angle/180*math.pi
    return math.cos(rad)

def get_axes(corners):
    if corners == [(0, 0), (0, 0), (0, 0), (0, 0)]:
        return []
    axes = []
    for i in range(len(corners)):
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % len(corners)]

        edge = (x2 - x1, y2 - y1)
        normal = (-edge[1], edge[0])
        length = math.hypot(normal[0], normal[1])

        axes.append((normal[0]/length, normal[1]/length))

    return axes

def project(corners, axis):
    dots = []

    for x, y in corners:
        dots.append(x * axis[0] + y * axis[1])

    return min(dots), max(dots)

def collision(poly1, poly2):
    axis1 = get_axes(poly1)
    axis2 = get_axes(poly2)
    if axis2 == []:
        return False
    axes = axis1 + axis2

    for axis in axes:
        min1, max1 = project(poly1, axis)
        min2, max2 = project(poly2, axis)

        if max1 < min2 or max2 < min1:
            return False

    return True