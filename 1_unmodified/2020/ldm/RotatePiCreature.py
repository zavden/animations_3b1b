# ==============================================================================
# Scene:      RotatePiCreature
# Source:     videos/_2020/ldm.py (lines 605-656)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotatePiCreature.py RotatePiCreature -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RotatePiCreature(Scene):
    def construct(self):
        randy = Randolph(mode="thinking")
        randy.set_height(6)

        plane = ComplexPlane(x_min=-12, x_max=12)
        plane.add_coordinates()

        self.camera.frame.move_to(3 * RIGHT)

        self.add(randy)
        self.wait()
        self.play(Rotate(randy, 30 * DEGREES, run_time=3))
        self.wait()
        self.play(Rotate(randy, -30 * DEGREES))

        self.add(plane, randy)
        self.play(
            ShowCreation(plane),
            randy.set_opacity, 0.75,
        )
        self.wait()

        dots = VGroup()
        for mob in randy.family_members_with_points():
            for point in mob.get_anchors():
                dot = Dot(point)
                dot.set_height(0.05)
                dots.add(dot)

        self.play(ShowIncreasingSubsets(dots))
        self.wait()

        label = VGroup(
            OldTex("(x + iy)"),
            Vector(DOWN),
            OldTex("(\\cos(30^\\circ) + i\\sin(30^\\circ))", "(x + iy)"),
        )
        label[2][0].set_color(YELLOW)
        label.arrange(DOWN)
        label.to_corner(DR)
        label.shift(3 * RIGHT)

        for mob in label:
            mob.add_background_rectangle()

        self.play(FadeIn(label))
        self.wait()

        randy.add(dots)
        self.play(Rotate(randy, 30 * DEGREES), run_time=3)
        self.wait()
