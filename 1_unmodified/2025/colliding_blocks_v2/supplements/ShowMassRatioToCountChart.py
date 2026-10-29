# ==============================================================================
# Scene:      ShowMassRatioToCountChart
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 266-304)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowMassRatioToCountChart.py ShowMassRatioToCountChart -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowMassRatioToCountChart(InteractiveScene):
    def construct(self):
        # Chart
        n_terms = 6
        v_line = Line(UP, DOWN).set_height(6)
        points = [v_line.pfp(a) for a in np.linspace(0, 1, n_terms + 2)]
        h_lines = VGroup(Line(LEFT, RIGHT).set_width(7).move_to(p) for p in points)

        VGroup(v_line, h_lines).set_stroke(WHITE, 2)
        self.add(v_line, h_lines[1:-1])

        # Content
        titles = VGroup(
            Text("Mass ratio"),
            Text("#Collisions"),
        )
        mass_ratios = VGroup(
            Integer(int(10**n), unit=":1", font_size=42)
            for n in range(0, 2 * n_terms, 2)
        )
        counts = VGroup(
            Integer(int(PI * 10**n), font_size=42)
            for n in range(0, n_terms)
        )
        for point, ratio, count in zip(points[2:], mass_ratios, counts):
            ratio.next_to(point, UL, buff=0.2).shift(0.1 * LEFT)
            count.next_to(point, UR, buff=0.2).shift(0.1 * RIGHT)

        titles[0].next_to(points[1], UL).shift(0.25 * LEFT)
        titles[1].next_to(points[1], UR).shift(0.25 * RIGHT)
        titles[0].align_to(titles[1], UP)

        self.add(titles)
        for ratio, count in zip(mass_ratios, counts):
            ratio.align_to(count, UP)
            self.play(FadeIn(ratio))
            self.wait()
            self.play(TransformFromCopy(ratio, count))
            self.wait()
