import unittest
import volmdlr
from volmdlr import curves


class TestHyperbola2D(unittest.TestCase):
    def test_line_intersections(self):
        # Usage
        a = 2  # semi-major axis
        b = 1  # semi-minor axis
        u_vector = volmdlr.Vector2D(0.7071067811865475, 0.7071067811865475)
        v_vector = volmdlr.Vector2D(-0.7071067811865475, 0.7071067811865475)
        frame1 = volmdlr.Frame2D(volmdlr.O2D, u_vector, v_vector)
        frame2 = volmdlr.OXY
        hyperbola1 = curves.Hyperbola2D(frame1, a, b)
        hyperbola2 = curves.Hyperbola2D(frame2, a, b)
        line1 = curves.Line2D(volmdlr.Point2D(1, 0), volmdlr.Point2D(-6, 10))
        line2 = curves.Line2D(volmdlr.Point2D(-10, -5), volmdlr.Point2D(10, 5))
        line3 = curves.Line2D(volmdlr.Point2D(-10, -5), volmdlr.Point2D(5, 10))
        expected_results = [[[volmdlr.Point2D(3.414716821729969, 1.4411665257000275),
                              volmdlr.Point2D(1.4066104613103017, 3.2667177624451798)],
                             [volmdlr.Point2D(2.529822128134703, 1.2649110640673518)],
                             [volmdlr.Point2D(2.696152422706632, 7.696152422706632)]],
                            [[volmdlr.Point2D(10.884604683797278, -5.349640621633888),
                              volmdlr.Point2D(3.452312878926738, 1.40698829188478319)],
                             [],
                             []]]
        for i, hyperbola in enumerate([hyperbola1, hyperbola2]):
            for j, line in enumerate([line1, line2, line3]):
                line_intersections = hyperbola.line_intersections(line)
                for intersection, expected_result in zip(line_intersections, expected_results[i][j]):
                    self.assertTrue(intersection.is_close(expected_result))


class TestHyperbola3D(unittest.TestCase):
    def test_line_intersections(self):
        a = 2  # semi-major axis
        b = 1  # semi-minor axis

        vector1 = volmdlr.Vector3D(1, 1, 1)
        vector1 = vector1.unit_vector()
        vector2 = vector1.deterministic_unit_normal_vector()
        vector3 = vector1.cross(vector2)
        frame = volmdlr.Frame3D(volmdlr.O3D, vector1, vector2, vector3)
        hyperbola = curves.Hyperbola3D(frame, a, b)

        points = hyperbola.get_points(number_points=400)
        line3d_1 = curves.Line3D(points[20], points[250])
        line3d_2 = curves.Line3D(points[20], points[320])
        line3d_3 = curves.Line3D(points[50], volmdlr.Point3D(10, 15, -15))
        line3d_4 = curves.Line3D(volmdlr.Point3D(-20, -15, 15), volmdlr.Point3D(10, 15, -15))
        expected_results = [[volmdlr.Point3D(3.106958942196619, 14.126593248702392, 14.126593248702392),
                             volmdlr.Point3D(5.209563472536312, 2.1093320938257762, 2.1093320938257762)],
                            [volmdlr.Point3D(3.1069589421966235, 14.126593248702383, 14.126593248702383),
                             volmdlr.Point3D(12.001168238296865, 4.603586433650937, 4.603586433650937)],
                            [volmdlr.Point3D(2.6111150368875498, 11.789027732278152, 11.789027732278152)],
                            []]

        for i, line in enumerate([line3d_1, line3d_2, line3d_3, line3d_4]):
            intersections = hyperbola.line_intersections(line)
            for intersection, expected_result in zip(intersections, expected_results[i]):
                self.assertTrue(intersection.is_close(expected_result))


if __name__ == '__main__':
    unittest.main()
