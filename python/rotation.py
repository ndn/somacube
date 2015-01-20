
"""
Some math.

Rotation matrixes:

                             1       0       0
rotate around x axis =       0  cos(a) -sin(a)
                             0  sin(a)  cos(a)

                        cos(a)       0  sin(a)
rotate around y axis =       0       1       0
                       -sin(a)       0  cos(a)

                        cos(a) -sin(a)       0
rotate around z axis =  sin(a)  cos(a)       0
                             0       0       1

Multiplied with a vector (x, y, z):

                       x
rotate around x axis = cos(a) * y - sin(a) * z
                       sin(a) * y + cos(a) * z

                       cos(a) * x + sin(a) * z
rotate around y axis = y
                       -sin(a) * x + cos(a) * z

                       cos(a) * x - sin(a) * y
rotate around z axis = sin(a) * x + cos(a) * y
                       z

With the following values:

Rotation in degrees  90  180  270
sin                   1    0   -1
cos                   0   -1    0


rot_x_90  = ( x, -z,  y)
rot_x_180 = ( x, -y, -z)
rot_x_270 = ( x,  z, -y)

rot_y_90  = ( z,  y, -x)
rot_y_180 = (-x,  y, -z)
rot_y_270 = (-z,  y,  x)

rot_z_90  = (-y,  x,  z)
rot_z_180 = (-x, -y,  z)
rot_z_270 = ( y, -x,  z)

"""

def rot_x_90(point):
    return (point[0], -point[2], point[1])

def rot_x_180(point):
    return (point[0], -point[1], -point[2])

def rot_x_270(point):
    return (point[0], point[2], -point[1])

def rot_y_90(point):
    return (point[2], point[1], -point[0])

def rot_y_180(point):
    return (-point[0], point[1], -point[2])

def rot_y_270(point):
    return (-point[2], point[1], point[0])

def rot_z_90(point):
    return (-point[1], point[0], point[2])

def rot_z_180(point):
    return (-point[0], -point[1], point[2])

def rot_z_270(point):
    return (point[1], -point[0], point[2])

def rot_any_0(point):
    return point

class Orientation(object):
    def __init__(self, rotations):
        self.rotations = rotations

    def rotate(self, point):
        for rotation in self.rotations:
            point = rotation(point)
        return point

_orientation_table = None

def _build_table():
    global _orientation_table

    xs = [ rot_any_0, rot_x_90, rot_x_180, rot_x_270 ]
    ys = [ rot_any_0, rot_y_90, rot_y_180, rot_y_270 ]
    zs = [ rot_any_0, rot_z_90, rot_z_180, rot_z_270 ]

    # Some random point
    point = (11, 22, 33)
    assert point[0] != point[1] != point[2]

    tmp_dict = {}

    for x in xs:
        new_point = x(point)

        for y in ys:
            new_point = y(new_point)

            for z in zs:
                new_point = z(new_point)

                # Up to this point we would get 4 * 4 * 4 = 64 orientations.

                # But geometrically there are only 24.
                # Compare http://en.wikipedia.org/wiki/Octahedral_symmetry#Chiral_octahedral_symmetry

                # Remember all functions used up to here and disregard rot_any_0
                new_orientation = [ function for function in [x, y, z] if function != rot_any_0 ]

                # If orientation is not yet know or shorter than a previous one, remember it
                if not new_point in tmp_dict.keys() or (len(new_orientation) < len(tmp_dict[new_point])):
                    tmp_dict[new_point] = new_orientation

    _orientation_table = [ Orientation(orientation) for orientation in tmp_dict.values() ]

    assert len(_orientation_table) == 24

def get_all_orientations():
    if _orientation_table == None:
        _build_table()
    return _orientation_table

