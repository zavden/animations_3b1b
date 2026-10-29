# ==============================================================================
# Scene:      ShowALens
# Source:     videos/_2024/holograms/supplements.py (lines 398-433)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowALens.py ShowALens -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowALens(InteractiveScene):
    def construct(self):
        # Add lens
        arc = Arc(-30 * DEGREES, 60 * DEGREES)
        flipped = arc.copy().rotate(PI).next_to(arc, LEFT, buff=0)
        arc.append_vectorized_mobject(flipped)
        lens = arc
        lens.set_stroke(WHITE, 2)
        lens.set_fill(GREY_E, 1)
        lens.set_shading(0.1, 0.5, 0)
        lens.set_height(3)

        # Add lines
        n_lines = 20
        points = np.linspace(lens.get_top(), lens.get_bottom(), n_lines)
        focal_point = lens.get_left() + 2 * LEFT
        in_lines = VGroup(Line(point + 8 * RIGHT, point) for point in points)
        out_lines = VGroup(Line(point, focal_point) for point in points)
        for in_line, out_line in zip(in_lines, out_lines):
            out_line.scale(1.25, about_point=out_line.get_start())
            in_line.append_vectorized_mobject(out_line)

        in_lines.set_stroke(WHITE, 1)
        in_lines.insert_n_curves(100)

        self.add(in_lines, lens)
        self.play(ShowCreation(in_lines, lag_ratio=0.01, run_time=2, rate_func=linear))
        self.wait()

        # Label viewing angle
        text = Text("Single viewing angle")
        text.next_to(lens.get_top(), UR)
        arrow = Vector(RIGHT).next_to(text, RIGHT)

        self.play(LaggedStart(Write(text, run_time=1), GrowArrow(arrow), lag_ratio=0.5))
        self.wait()
