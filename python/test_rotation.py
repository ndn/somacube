import unittest

from rotate_grid_points import *

class  TestRotateGridPoints(unittest.TestCase):

    def test_rot_90_vs_others(self):
        p = (11, 22, 33)
        new_x_p = p
        new_y_p = p
        new_z_p = p

        for i in range(4):
            new_x_p = rot_x_90(new_x_p)
            new_y_p = rot_y_90(new_y_p)
            new_z_p = rot_z_90(new_z_p)

            if i == 1:
                self.assertEqual(new_x_p, rot_x_180(p))
                self.assertEqual(new_y_p, rot_y_180(p))
                self.assertEqual(new_z_p, rot_z_180(p))

            if i == 2:
                self.assertEqual(new_x_p, rot_x_270(p))
                self.assertEqual(new_y_p, rot_y_270(p))
                self.assertEqual(new_z_p, rot_z_270(p))

        self.assertEqual(p, new_x_p)
        self.assertEqual(p, new_y_p)
        self.assertEqual(p, new_z_p)

    def test_all_orientations(self):
        import math

        def len_vect(p):
            return math.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2)

        p = (11, 22, 33)

        orientations = get_all_orientations()

        self.assertEqual(len(orientations), 24)

        for o in orientations:
            self.assertEqual(len_vect(o.rotate(p)), len_vect(p))

