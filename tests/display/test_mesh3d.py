import os
import unittest

import numpy as np
import trimesh
from dessia_common.serialization import BinaryFile

from volmdlr import Point3D
from volmdlr.display import Mesh3D
from volmdlr.faces import Triangle3D

SHOW_BABYLONJS = True

FOLDER = os.path.dirname(os.path.realpath(__file__))


class TestMesh3D(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.vertices1 = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
        self.triangles1 = np.array([[0, 1, 2]])
        self.mesh1 = Mesh3D(self.vertices1, self.triangles1, "Mesh1")

        self.vertices2 = np.array([[0, 1, 0], [1, 1, 0], [1, 0, 0]])  # Note shared vertex with mesh1
        self.triangles2 = np.array([[0, 1, 2]])
        self.mesh2 = Mesh3D(self.vertices2, self.triangles2, "Mesh2")

        self.vertices3 = np.array(
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 0.0],
                [0.0, 1.0, 1.0],
                [1.0, 0.0, 0.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 0.0],
                [1.0, 1.0, 1.0],
            ]
        )
        self.triangles3 = np.array(
            [
                [2, 6, 7],
                [0, 4, 5],
                [1, 7, 5],
                [0, 2, 6],
                [4, 6, 7],
                [1, 3, 7],
                [0, 2, 3],
                [2, 7, 3],
                [0, 6, 4],
                [4, 7, 5],
                [0, 5, 1],
                [0, 3, 1],
            ]
        )
        self.mesh3 = Mesh3D(self.vertices3, self.triangles3, "Mesh3")

        self.vertices4 = np.array(
            [
                [0.0, 0.0, 1.0],
                [0.0, 0.0, 2.0],
                [0.0, 1.0, 1.0],
                [0.0, 1.0, 2.0],
                [1.0, 0.0, 1.0],
                [1.0, 0.0, 2.0],
                [1.0, 1.0, 1.0],
                [1.0, 1.0, 2.0],
            ]
        )
        self.triangles4 = np.array(
            [
                [2, 7, 3],
                [1, 7, 5],
                [0, 6, 4],
                [4, 7, 5],
                [0, 3, 1],
                [0, 2, 6],
                [4, 6, 7],
                [2, 6, 7],
                [0, 4, 5],
                [1, 3, 7],
                [0, 2, 3],
                [0, 5, 1],
            ]
        )
        self.mesh4 = Mesh3D(self.vertices4, self.triangles4, "Mesh4")

    def test_merge_without_mutualization(self):
        merged_meshes = self.mesh1.merge(self.mesh2, False, False)
        expected_vertices = np.array([[0, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [1, 1, 0]])

        np.testing.assert_array_equal(np.sort(merged_meshes.vertices, axis=0), np.sort(expected_vertices, axis=0))

    def test_merge_with_mutualization(self):
        merged_meshes = self.mesh1.merge(self.mesh2, True, True)
        expected_vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]])

        np.testing.assert_array_equal(np.sort(merged_meshes.vertices, axis=0), np.sort(expected_vertices, axis=0))

    def test_add_operator(self):
        # No mutualization
        added_mesh = self.mesh1 + self.mesh2
        expected_vertices = np.array([[0, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [1, 1, 0]])

        np.testing.assert_array_equal(np.sort(added_mesh.vertices, axis=0), np.sort(expected_vertices, axis=0))

    def test_union_operator(self):
        # Mutualization
        added_mesh = self.mesh1 | self.mesh2
        expected_vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]])

        np.testing.assert_array_equal(np.sort(added_mesh.vertices, axis=0), np.sort(expected_vertices, axis=0))

    def test_merge_cube_without_mutualization(self):
        merged_mesh_1 = self.mesh3.merge(self.mesh4, merge_vertices=False, merge_triangles=False)

        self.assertEqual(24, len(merged_mesh_1.triangles))
        self.assertEqual(16, len(merged_mesh_1.vertices))

    def test_merge_cube_with_mutualization(self):
        merged_mesh_2 = self.mesh3.merge(self.mesh4, merge_vertices=True, merge_triangles=True)

        self.assertEqual(22, len(merged_mesh_2.triangles))
        self.assertEqual(12, len(merged_mesh_2.vertices))

    def test_equality(self):
        self.assertNotEqual(self.mesh1, self.mesh2)
        self.assertEqual(self.mesh1, self.mesh1)
        self.assertFalse(self.mesh1._data_eq(self.mesh2))
        self.assertTrue(self.mesh1._data_eq(self.mesh1))

    def test_concatenate_empty(self):
        empty_mesh = Mesh3D(np.array([]), np.array([]))

        self.assertEqual(self.mesh1, self.mesh1 + empty_mesh)
        self.assertEqual(self.mesh1, empty_mesh + self.mesh1)
        self.assertNotEqual(self.mesh1, self.mesh1 + self.mesh2)


class TestMesh3DImport(unittest.TestCase):
    def setUp(self) -> None:
        self.stl_file_path = os.path.join(FOLDER, "models", "simple.stl")

    def test_from_trimesh(self):
        mesh = Mesh3D.from_trimesh(trimesh.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0]], faces=[[0, 1, 2]]))

        if SHOW_BABYLONJS:
            mesh.babylonjs()

    def test_from_stl_file(self):
        mesh = Mesh3D.from_stl_file(self.stl_file_path)

        if SHOW_BABYLONJS:
            mesh.babylonjs()

    def test_from_stl_stream(self):
        with open(self.stl_file_path, "rb") as file:
            binary_content = BinaryFile()
            binary_content.write(file.read())

        mesh = Mesh3D.from_stl_stream(binary_content)

        if SHOW_BABYLONJS:
            mesh.babylonjs()


class TestMesh3DExport(unittest.TestCase):
    def setUp(self) -> None:
        self.mesh = Mesh3D(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]]), np.array([[0, 1, 2]]))
        self.degenerated_mesh = Mesh3D(np.array([[0, 0, 0], [0, 0, 1]]), np.array([[0, 1, 1]]))

    def test_to_triangles3d(self):
        self.assertEqual(
            [Triangle3D(Point3D(*[0, 0, 0]), Point3D(*[0, 0, 1]), Point3D(*[0, 1, 0]))], self.mesh.to_triangles3d()
        )
        self.assertEqual([], self.degenerated_mesh.to_triangles3d())


if __name__ == "__main__":
    unittest.main()
