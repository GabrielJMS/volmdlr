import unittest

import volmdlr
from volmdlr.edges import Arc2D


class TestArc2D(unittest.TestCase):
    arc2d = Arc2D(volmdlr.Point2D(-1, 0), volmdlr.Point2D(0, -1), volmdlr.Point2D(1, 0))
    arc1 = Arc2D(volmdlr.Point2D(0, -1), volmdlr.Point2D(1, 0), volmdlr.Point2D(0, 1))
    arc2 = Arc2D(volmdlr.Point2D(1, 0), volmdlr.Point2D(0, 1), volmdlr.Point2D(-1, 0))
    arc3 = Arc2D(1.5 * volmdlr.Point2D(0, -1), 1.5 * volmdlr.Point2D(1, 0), 1.5 * volmdlr.Point2D(0, 1))
    arc4 = Arc2D(volmdlr.Point2D(0.7071067811865475, -0.7071067811865475), volmdlr.Point2D(1, 0),
                 volmdlr.Point2D(0.7071067811865475, 0.7071067811865475))

    arc5 = Arc2D(volmdlr.Point2D(-0.7071067811865475, 0.7071067811865475), volmdlr.Point2D(-1, 0),
                 volmdlr.Point2D(-0.7071067811865475, -0.7071067811865475))
    arc6 = arc4.complementary()
    arc7 = Arc2D(volmdlr.Point2D(-0.7071067811865475, 0.7071067811865475), volmdlr.Point2D(0, 1),
                 volmdlr.Point2D(0.7071067811865475, 0.7071067811865475))
    arc8 = arc7.complementary()
    arc9 = Arc2D(volmdlr.Point2D(-0.7071067811865475, -0.7071067811865475), volmdlr.Point2D(0, 1),
                 volmdlr.Point2D(0.7071067811865475, -0.7071067811865475))
    arc10 = arc9.complementary()
    list_points = [volmdlr.Point2D(1, 0),
                   volmdlr.Point2D(0.7071067811865475, -0.7071067811865475),
                   volmdlr.Point2D(0, -1),
                   volmdlr.Point2D(-0.7071067811865475, -0.7071067811865475),
                   volmdlr.Point2D(-1, 0),
                   volmdlr.Point2D(-0.7071067811865475, 0.7071067811865475),
                   volmdlr.Point2D(0, 1),
                   volmdlr.Point2D(0.7071067811865475, 0.7071067811865475)]

    def test_split(self):
        arc_split1 = self.arc2d.split(self.arc2d.start)
        self.assertIsNone(arc_split1[0])
        self.assertEqual(arc_split1[1], self.arc2d)
        arc_split2 = self.arc2d.split(self.arc2d.end)
        self.assertEqual(arc_split2[0], self.arc2d)
        self.assertIsNone(arc_split2[1])
        arc_split3 = self.arc2d.split(self.arc2d.interior)
        self.assertTrue(arc_split3[0].start.is_close(self.arc2d.start))
        self.assertTrue(arc_split3[0].end.is_close(self.arc2d.interior))
        self.assertTrue(arc_split3[1].start.is_close(self.arc2d.interior))
        self.assertTrue(arc_split3[1].end.is_close(self.arc2d.end))

    def test_abscissa(self):
        expected_abscissa_results = [[1.5707963267948966, 0.7853981633974483, 0, 3.141592653589793, 2.356194490192345],
                                     [0, 3.141592653589793, 2.356194490192345, 1.5707963267948966, 0.7853981633974483],
                                     [], [0.7853981633974483, 0, 1.5707963267948966],
                                     [1.5707963267948961, 0.7853981633974481, 0],
                                     [0, 0.7853981633974482, 1.5707963267948966, 2.3561944901923444, 3.141592653589792,
                                      3.9269908169872405, 4.712388980384689],
                                     [0, 0.7853981633974485, 1.5707963267948968],
                                     [3.92699081698724, 3.141592653589792, 2.356194490192344, 1.5707963267948957,
                                      0.7853981633974476, 0, 4.712388980384689],
                                     [3.9269908169872414, 4.71238898038469, 0, 0.7853981633974483, 1.5707963267948966,
                                      2.356194490192345, 3.141592653589793],
                                     [1.5707963267948963, 0.7853981633974483, 0]]
        list_abscissas = []
        for arc in [self.arc1, self.arc2, self.arc3, self.arc4, self.arc5, self.arc6, self.arc7,
                    self.arc8, self.arc9, self.arc10]:
            abscissas_ = []
            for point in self.list_points:
                try:
                    abscissa = arc.abscissa(point)
                except ValueError:
                    continue
                abscissas_.append(abscissa)
            list_abscissas.append(abscissas_)
        for abscissas, expected_abscissas in zip(list_abscissas, expected_abscissa_results):
            for abscissa, expected_abscissa in zip(abscissas, expected_abscissas):
                self.assertAlmostEqual(abscissa, expected_abscissa)

    def test_point_belongs(self):
        expected_results = [[True, True, True, False, False, False, True, True],
                            [True, False, False, False, True, True, True, True],
                            [False, False, False, False, False, False, False, False],
                            [True, True, False, False, False, False, False, True],
                            [False, False, False, True, True, True, False, False],
                            [False, True, True, True, True, True, True, True],
                            [False, False, False, False, False, True, True, True],
                            [True, True, True, True, True, True, False, True],
                            [True, True, False, True, True, True, True, True],
                            [False, True, True, True, False, False, False, False]]
        list_point_belongs = []
        for arc in [self.arc1, self.arc2, self.arc3, self.arc4, self.arc5, self.arc6, self.arc7,
                    self.arc8, self.arc9, self.arc10]:
            point_belongs_ = []
            for point in self.list_points:
                point_belongs_.append(arc.point_belongs(point))
            list_point_belongs.append(point_belongs_)
        for result_list, expected_result_list in zip(list_point_belongs, expected_results):
            self.assertEqual(result_list, expected_result_list)


if __name__ == '__main__':
    unittest.main()
