# ==============================================================================
# Scene:      AddCubeSymmetries
# Source:     videos/_2017/efvgt.py (lines 944-1031)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AddCubeSymmetries.py AddCubeSymmetries -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DrawBorderThenFill needs a VMobject; GL Cube is a Group of surfaces: fade it in
# ==============================================================================

from manim_imports_ext import *

def normalize(vect):
    norm = get_norm(vect)
    if norm == 0:
        return OUT
    else:
        return vect/norm


def get_composite_rotation_angle_and_axis(angles, axes):
    angle1, axis1 = 0, OUT
    for angle2, axis2 in zip(angles, axes):
        ## Figure out what (angle3, axis3) is the same 
        ## as first applying (angle1, axis1), then (angle2, axis2)
        axis2 = normalize(axis2)
        dot = np.dot(axis2, axis1)
        cross = np.cross(axis2, axis1)
        angle3 = 2*np.arccos(
            np.cos(angle2/2)*np.cos(angle1/2) - \
            np.sin(angle2/2)*np.sin(angle1/2)*dot
        )
        axis3 = (
            np.sin(angle2/2)*np.cos(angle1/2)*axis2 + \
            np.cos(angle2/2)*np.sin(angle1/2)*axis1 + \
            np.sin(angle2/2)*np.sin(angle1/2)*cross
        )
        axis3 = normalize(axis3)
        angle1, axis1 = angle3, axis3

    if angle1 > np.pi:
        angle1 -= 2*np.pi
    return angle1, axis1


class GroupOfCubeSymmetries(ThreeDScene):
    CONFIG = {
        "cube_opacity" : 0.5,
        "cube_colors" : [BLUE],
        "put_randy_on_cube" : True,
    }
    def construct(self):
        title = OldTexText("Group of cube symmetries")
        title.to_edge(UP)
        self.add(title)

        cube = self.get_cube()

        face_centers = [face.get_center() for face in cube[0:7:2]]
        angle_axis_pairs = list(zip(3*[np.pi/2], face_centers))
        for i in range(3):
            ones = np.ones(3)
            ones[i] = -1
            axis = np.dot(ones, face_centers)
            angle_axis_pairs.append((2*np.pi/3, axis))

        for angle, axis in angle_axis_pairs:
            self.play(Rotate(
                cube, angle = angle, axis = axis,
                run_time = 2
            ))
            self.wait()

    def get_cube(self):
        cube = Cube(fill_opacity = self.cube_opacity)
        cube.set_color_by_gradient(*self.cube_colors)
        if self.put_randy_on_cube:
            randy = Randolph(mode = "pondering")
            # randy.pupils.shift(0.01*OUT)
            # randy.add(randy.pupils.copy().shift(0.02*IN))
            # for submob in randy.get_family():
            #     submob.part_of_three_d_mobject = True
            randy.scale(0.5)
            face = cube[1]
            randy.move_to(face)
            face.add(randy)
        pose_matrix = self.get_pose_matrix()
        cube.apply_function(
            lambda p : np.dot(p, pose_matrix.T),
            maintain_smoothness = False
        )
        return cube

    def get_pose_matrix(self):
        return np.dot(
            rotation_matrix(np.pi/8, UP),
            rotation_matrix(np.pi/24, RIGHT)
        )


class AddCubeSymmetries(GroupOfCubeSymmetries):
    CONFIG = {
        "angle_axis_pairs" : [
            (np.pi/2, RIGHT),
            (np.pi/2, UP),
        ],
        "cube_opacity" : 0.5,
        "cube_colors" : [BLUE],
    }
    def construct(self):
        angle_axis_pairs = list(self.angle_axis_pairs)
        angle_axis_pairs.append(
            self.get_composition_angle_and_axis()
        )
        self.pose_matrix = self.get_pose_matrix()
        cube = self.get_cube()

        equation = cube1, plus, cube2, equals, cube3 = VGroup(
            cube, OldTex("+"), 
            cube.copy(), OldTex("="),
            cube.copy()
        )
        equation.arrange(RIGHT, buff = MED_LARGE_BUFF)
        equation.center()

        self.add(cube1)
        self.rotate_cube(cube1, *angle_axis_pairs[0])
        cube_copy = cube1.copy()
        cube_copy.set_fill(opacity = 0)
        self.play(
            cube_copy.move_to, cube2,
            cube_copy.set_fill, None, self.cube_opacity,
            Write(plus)
        )
        self.rotate_cube(cube_copy, *angle_axis_pairs[1])
        self.play(Write(equals))
        # CHANGE: DrawBorderThenFill needs a VMobject; GL Cube is a Group of surfaces: fade it in
        self.play(FadeIn(cube3, run_time = 1))
        self.rotate_cube(cube3, *angle_axis_pairs[2])
        self.wait(2)

        times = OldTex("\\times")
        times.scale(1.5)
        times.move_to(plus)
        times.set_color(RED)
        self.wait()
        self.play(ReplacementTransform(plus, times))
        self.play(Indicate(times))
        self.wait()
        for cube, (angle, axis) in zip([cube1, cube_copy, cube3], angle_axis_pairs):
            self.rotate_cube(
                cube, -angle, axis, add_arrows = False,
                rate_func = there_and_back,
                run_time = 1.5
            )
        self.wait()

    def rotate_cube(self, cube, angle, axis, add_arrows = True, **kwargs):
        axis = np.dot(axis, self.pose_matrix.T)
        anims = []
        if add_arrows:
            arrows = VGroup(*[
                Arc(
                    start_angle = np.pi/12+a, angle = 5*np.pi/6,
                    color = YELLOW
                ).add_tip()
                for a in (0, np.pi)
            ])
            arrows.set_height(1.5*cube.get_height())
            z_to_axis = z_to_vector(axis)
            arrows.apply_function(
                lambda p : np.dot(p, z_to_axis.T),
                maintain_smoothness = False
            )
            arrows.move_to(cube)
            arrows.shift(-axis*cube.get_height()/2/get_norm(axis))
            anims += list(map(ShowCreation, arrows))
        anims.append(
            Rotate(
                cube, axis = axis, angle = angle, in_place = True,
                **kwargs
            )
        )
        self.play(*anims, run_time = 1.5)

    def get_composition_angle_and_axis(self):
        return get_composite_rotation_angle_and_axis(
            *list(zip(*self.angle_axis_pairs))
        )
