import numpy as np
import math

def cvtCoordinate(pt, H, W, type):
    if type == "ARRAY_TO_XY":
        r, c = pt
        x, y = c, -r
        x, y = x - W/2, y + H/2
        x, y = round(x), round(y)
        return [x,y]

    elif type == "XY_TO_ARRAY":
        x, y = pt
        x, y = x + W/2, y + H/2
        r, c = -y, x
        r, c = round(r), round(c)
        return [r,c]
    else:
        return None


def rotation(pt, angle_degree):
    angle_radian = angle_degree / 100 * math.pi
    rot_matrix = [[math.cos(angle_radian), -math.sin(angle_radian)], [math.sin(angle_radian), math.cos(angle_radian)]]
    return np.matmul(rot_matrix, pt)