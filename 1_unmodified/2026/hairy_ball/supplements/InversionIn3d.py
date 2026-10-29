# ==============================================================================
# Scene:      InversionIn3d
# Source:     videos/_2026/hairy_ball/supplements.py (lines 908-943)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InversionIn3d.py InversionIn3d -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InversionIn3d(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        frame.add_ambient_rotation(1 * DEG)
        axes = ThreeDAxes((-3, 3), (-3, 3), (-3, 3))
        coord_range = list(range(-3, 3))
        cubes = VGroup(
            VCube(side_length=1).move_to([x, y, z], DL + IN)
            for x, y, z in it.product(* 3 * [coord_range])
        )
        cubes.set_fill(opacity=0)
        cubes.set_stroke(WHITE, 1, 0.25)

        basis_vectors = VGroup(
            Vector(RIGHT).set_color(GREEN),
            Vector(UP).set_color(RED),
            Vector(OUT).set_color(BLUE),
        )
        # for vect in basis_vectors:
        #     vect.set_perpendicular_to_camera(frame)

        frame.reorient(29, 72, 0, ORIGIN, 5)
        self.add(axes, cubes, basis_vectors)

        # Rotate
        rot_group = VGroup(cubes, basis_vectors)
        self.wait()
        self.play(
            Rotate(rot_group, PI, about_point=ORIGIN, run_time=3)
        )
        self.play(
            rot_group.animate.stretch(-1, 2, about_point=ORIGIN),
            run_time=2
        )
        self.wait(3)
