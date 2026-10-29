# ==============================================================================
# Scene:      UnitArcLengthsOnCircle
# Source:     videos/_2025/laplace/prequel_equations.py (lines 545-578)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnitArcLengthsOnCircle.py UnitArcLengthsOnCircle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UnitArcLengthsOnCircle(InteractiveScene):
    def construct(self):
        # Moving sectors
        arc = Arc(0, 1, radius=2.5, stroke_color=GREEN, stroke_width=8)
        sector = Sector(angle=1, radius=2.5).set_fill(GREEN, 0.25)
        v_line = Line(ORIGIN, 2.5 * UP)
        v_line.match_style(arc)
        v_line.move_to(arc.get_start(), DOWN)

        self.add(v_line)
        self.play(
            FadeIn(sector),
            ReplacementTransform(v_line, arc),
        )

        group = VGroup(sector, arc)
        self.add(group)

        for n in range(5):
            self.wait(2)
            group.rotate(1, about_point=ORIGIN)

        return

        # Previous
        colors = [RED, BLUE]
        arcs = VGroup(
            Arc(n, 1, radius=2.5, stroke_color=colors[n % 2], stroke_width=8)
            for n in range(6)
        )
        for arc in arcs:
            one = Integer(1, font_size=24).move_to(1.0 * arc.get_center())
            self.play(ShowCreation(arc, rate_func=linear, run_time=2))
        self.wait()
