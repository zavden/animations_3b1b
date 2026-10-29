# ==============================================================================
# Scene:      GroupOfCubeSymmetries
# Source:     videos/_2017/efvgt.py (lines 741-793)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GroupOfCubeSymmetries.py GroupOfCubeSymmetries -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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
