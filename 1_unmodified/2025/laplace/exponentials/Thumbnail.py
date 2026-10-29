# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2025/laplace/exponentials.py (lines 1581-1649)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(InteractiveScene):
    def construct(self):
        # Spiral
        spiral_color = TEAL
        s = -0.15 + 2j
        max_t = 3
        thick_stroke_width = (5, 25)

        plane = ComplexPlane(
            (-4, 4),
            (-2, 2)
        )
        plane.set_height(11)
        plane.center()
        plane.add_coordinate_labels(font_size=24)

        plane.axes.set_stroke(WHITE, 5)
        plane.background_lines.set_stroke(BLUE, 3)
        plane.faded_lines.set_stroke(BLUE, 2, 0.25)

        curve = ParametricCurve(
            lambda t: plane.n2p(np.exp(s * t)),
            t_range=(0, 40, 0.1)
        )
        partial_curve = ParametricCurve(
            lambda t: plane.n2p(np.exp(s * t)),
            t_range=(0, max_t, 0.1)
        )
        curve.set_stroke(spiral_color, 2, 0.5)
        partial_curve.set_stroke(spiral_color, width=thick_stroke_width, opacity=(0.5, 1))

        dot = Group(TrueDot(radius=0.2), GlowDot(radius=0.75))
        dot.set_color(spiral_color)
        dot.move_to(partial_curve.get_end())

        self.add(plane, curve)
        self.add(partial_curve)
        self.add(dot)

        vectors = VGroup(
            self.get_vector(plane, s, t, color=BLUE)
            for t in np.linspace(0, max_t, 10)
        )
        self.add(vectors)

    def get_vector(self, plane, s, t, scale_factor=0.5, thickness=5, color=YELLOW):
        vect = Vector(RIGHT, thickness=thickness, fill_color=color)
        vect.put_start_and_end_on(plane.n2p(0), scale_factor * plane.n2p(s * np.exp(s * t)))
        vect.shift(plane.n2p(np.exp(s * t)) - plane.n2p(0))
        return vect

    def get_formula(self):
        # Formula
        formula = Tex(R"e^{st}", t2c={"s": YELLOW, "t": BLUE}, font_size=200)
        formula.next_to(plane, LEFT, buff=2.0)

        s_rect = SurroundingRectangle(formula["s"], buff=0.1)
        s_rect.set_stroke(WHITE, 2)

        abi = Tex("a + bi", font_size=72)
        abi.next_to(formula, UP, LARGE_BUFF)
        abi.to_edge(LEFT, buff=LARGE_BUFF)

        arrow = Arrow(s_rect.get_top(), abi.get_corner(DR), buff=0.05)

        self.add(formula)
        self.add(s_rect)
        self.add(arrow)
        self.add(abi)
