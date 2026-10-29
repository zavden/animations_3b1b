# ==============================================================================
# Scene:      SimplifyingMessiness
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 1122-1158)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimplifyingMessiness.py SimplifyingMessiness -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimplifyingMessiness(InteractiveScene):
    samples = 4

    def construct(self):
        # Test
        circle = Circle(radius=2)
        circle.set_stroke(WHITE, 3)

        rough_points = np.array([np.random.uniform(0.95, 1.05) * circle.pfp(a) for a in np.linspace(0, 1, 200)])
        rough_points[-1] = rough_points[0]
        rough_circle = VMobject().set_points_as_corners(rough_points)

        circles = VGroup(rough_circle, circle)
        circles.arrange(RIGHT, buff=3.0)

        arrows = VGroup(
            Arrow(rough_circle.get_right(), circle.get_left(), path_arc=-sgn * 90 * DEG, thickness=5).shift(sgn * UP)
            for sgn in [+1, -1]
        )
        mid_arrow = Arrow(rough_circle, circle, buff=0.25, thickness=5, path_arc=1 * DEG)

        self.play(ShowCreation(rough_circle))
        self.wait()
        self.play(
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.7),
            TransformFromCopy(rough_circle, circle, run_time=2),
        )
        self.wait()
        self.play(ReplacementTransform(arrows[0], mid_arrow))
        self.wait()
        self.play(ReplacementTransform(mid_arrow, arrows[1]))
        self.play(
            circle.animate.center(),
            FadeOut(rough_circle, 2 * LEFT),
            FadeOut(arrows[1], 2 * LEFT),
        )
        self.wait()
