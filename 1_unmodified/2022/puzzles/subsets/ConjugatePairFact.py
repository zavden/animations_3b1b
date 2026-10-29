# ==============================================================================
# Scene:      ConjugatePairFact
# Source:     videos/_2022/puzzles/subsets.py (lines 5075-5127)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConjugatePairFact.py ConjugatePairFact -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConjugatePairFact(InteractiveScene):
    def construct(self):
        # Plane
        plane = ComplexPlane((-2, 2), (-1, 1))
        plane.set_height(3)
        plane.to_corner(DR)
        plane.add_coordinate_labels([-1, 0, 1, 2, -1j, 1j], font_size=18)
        plane.coordinate_labels[-2].set_y(plane.c2p(0, -1)[1] + SMALL_BUFF, DOWN)

        # Numbers
        z0 = complex(1.5, 0.5)
        zs = [z0, z0.conjugate()]
        points = [plane.n2p(z) for z in zs]
        dots = Group(*(GlowDot(point, color=RED) for point in points))
        lines = Line().replicate(2)
        lines.set_stroke(RED, 2)
        lines.add_updater(lambda ls: [line.put_start_and_end_on(plane.n2p(0), dot.get_center()) for line, dot in zip(ls, dots)])
        labels = VGroup(
            Tex("a + bi", font_size=24).next_to(points[0], UP, SMALL_BUFF),
            Tex("a - bi", font_size=24).next_to(points[1], DOWN, SMALL_BUFF),
        )

        # Equation
        lhs = "(a + bi)(a - bi)"
        rhs = "||a + bi|| \\cdot ||a - bi||"
        eq = Tex(
            lhs + " = a^2 + b^2 = " + rhs,
            isolate=[lhs, rhs]
        )
        eq.match_width(plane)
        eq.next_to(plane, UP)
        lhs_brace = Brace(eq.select_part(lhs), UP, buff=SMALL_BUFF)
        rhs_brace = Brace(eq.select_part(rhs), UP, buff=SMALL_BUFF)
        lhs_brace.add(lhs_brace.get_text("Product", font_size=30))
        rhs_brace.add(rhs_brace.get_text("Product of magnitudes", font_size=30))

        lines.update()
        self.play(
            FadeIn(VGroup(plane, labels), lag_ratio=0.01),
            ShowCreation(lines),
            FadeIn(dots),
        )
        self.play(FadeIn(eq, UP))
        self.wait()
        self.play(Swap(*dots))
        self.add(lines)
        self.add(dots)
        self.wait()
        self.play(LaggedStart(
            FadeIn(lhs_brace, 0.5 * UP),
            FadeIn(rhs_brace, 0.5 * UP),
        ))
        self.wait(4)
