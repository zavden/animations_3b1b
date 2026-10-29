# ==============================================================================
# Scene:      CubeRotations
# Source:     videos/_2020/monster.py (lines 2473-2530)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CubeRotations.py CubeRotations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_glassy_cube(frame):
    verts = np.array(list(it.product(*3 * [[-1, 1]])))
    edges = [
        (v1, v2)
        for v1, v2 in it.combinations(verts, 2)
        if sum(v1 == v2) == 2
    ]
    corner_dots = Group(*[
        Sphere(resolution=(51, 26),).set_height(0.25).move_to(vert)
        for vert in verts
    ])
    corner_dots.set_color(GREY_B)
    edge_rods = Group(*[
        Line3D(v1, v2)
        for v1, v2 in edges
    ])

    faces = Cube(square_resolution=(10, 10))
    faces.set_height(2)
    faces.set_color(BLUE_E, 0.3)
    faces.add_updater(lambda m, f=frame: m.sort(lambda p: np.dot(p, [np.sign(f.euler_angles[0]) * 0.2, -1, 0.2])))

    cube = Group(corner_dots, edge_rods, faces)
    cube.corner_dots = corner_dots
    cube.edge_rods = edge_rods
    cube.faces = faces
    return cube


class CubeRotations(ThreeDScene):
    def construct(self):
        # Set frame motion
        frame = self.camera.frame
        frame.set_euler_angles(phi=80 * DEGREES)
        frame.add_updater(lambda m, sc=self: m.set_euler_angles(theta=-20 * DEGREES * np.cos(0.1 * sc.time)))
        self.add(frame)

        # Setup cube
        cube = get_glassy_cube(frame)
        cube.set_height(3)
        axes = ThreeDAxes(axis_config={"include_tip": False})
        axes.apply_depth_test()

        self.add(axes)
        self.add(cube)

        # Apply rotations
        quats = self.get_quaternions()
        self.wait()
        for quat in quats:
            angle, axis = angle_axis_from_quaternion(quat)

            line = Line3D(-5 * axis, 5 * axis, prefered_creation_axis=0)
            line.set_color(YELLOW)
            if angle < 1e-6:
                line.scale(0)
            # line.apply_depth_test()
            deg_label = Integer(int(np.round(angle / DEGREES)), unit="^\\circ")
            deg_label.scale(2)
            deg_label.to_edge(UP)
            deg_label.shift(2 * LEFT)
            deg_label.fix_in_frame()

            self.add(line, *self.mobjects)
            self.play(ShowCreation(line), FadeIn(deg_label))
            self.play(Rotate(cube, angle, axis=axis))
            line.scale(-1)
            self.play(Uncreate(line), FadeOut(deg_label))

    def get_quaternions(self, n_rotations=30):
        ijk = [
            quaternion_from_angle_axis(90 * DEGREES, axis)
            for axis in [RIGHT, UP, OUT]
        ]
        result = []
        for x in range(n_rotations):
            n = random.randint(1, 10)
            curr = quaternion_from_angle_axis(0, RIGHT)
            for y in range(n):
                curr = quaternion_mult(curr, random.choice(ijk))
            result.append(curr)

        # Add on those rotations around diagonals for the end
        for oi in [OUT, IN]:
            for vect in [UL, UR, DR, DL]:
                result.append(quaternion_from_angle_axis(120 * DEGREES, vect + oi))
        return result
