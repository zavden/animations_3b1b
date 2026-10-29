# ==============================================================================
# Scene:      DrawTorus
# Source:     videos/_2026/spheres_talk/supplements.py (lines 526-560)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DrawTorus.py DrawTorus -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DrawTorus(InteractiveScene):
    def construct(self):
        # Add torus
        frame = self.frame
        r1 = 3
        r2 = 1

        circle1 = Circle().set_fill(GREEN_E, 0.5).set_stroke(GREEN, 2)
        circle2 = Circle().set_stroke(RED, 2)
        circles = VGroup(circle1, circle2)
        circles.arrange(RIGHT, buff=LARGE_BUFF)

        self.add(circles)
        self.wait()
        self.play(
            frame.animate.reorient(19, 63, 0, (0.05, -0.15, -0.75), 9.57),
            circle1.animate.rotate(90 * DEG, LEFT).move_to(r1 * RIGHT),
            circle2.animate.set_width(2 * r1).move_to(ORIGIN),
            run_time=2
        )
        
        # Add torus
        torus = Torus(r1=r1, r2=r2)
        partial_torus = Torus()
        partial_torus.set_color(GREY, 0.5)
        partial_torus.always_sort_to_camera(self.camera)
        self.play(
            UpdateFromAlphaFunc(
                partial_torus,
                lambda m, a: m.pointwise_become_partial(torus, 0, a, axis=0),
            ),
            Rotate(circle1, TAU, about_point=ORIGIN),
            run_time=5
        )
        self.wait()
