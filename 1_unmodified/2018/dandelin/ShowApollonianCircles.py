# ==============================================================================
# Scene:      ShowApollonianCircles
# Source:     videos/_2018/dandelin.py (lines 1533-1577)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowApollonianCircles.py ShowApollonianCircles -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowApollonianCircles(Scene):
    def construct(self):
        radii = [1.0, 2.0, 3.0]
        curvatures = [1.0 / r for r in radii]
        k4 = sum(curvatures) - 2 * np.sqrt(
            sum([
                k1 * k2
                for k1, k2 in it.combinations(curvatures, 2)
            ])
        )
        radii.append(1.0 / k4)
        centers = [
            ORIGIN, 3 * RIGHT, 4 * UP,
            4 * UP + 3 * RIGHT,
        ]
        circles = VGroup(*[
            Circle(radius=r).shift(c)
            for r, c in zip(radii, centers)
        ])

        circles.set_height(FRAME_HEIGHT - 3)
        circles.center().to_edge(DOWN)
        # circles.set_fill(opacity=1)
        circles.submobjects.reverse()
        circles.set_stroke(width=5)
        circles.set_color_by_gradient(BLUE, YELLOW)

        equation = OldTex("""
            \\left(
            {1 \\over r_1} + {1 \\over r_2} +
            {1 \\over r_3} + {1 \\over r_4}
            \\right)^2 = 
            2\\left(
            {1 \\over r_1^2} + {1 \\over r_2^2} +
            {1 \\over r_3^2} + {1 \\over r_4^2}
            \\right)
        """)
        # equation.scale(1.5)
        equation.next_to(circles, UP)

        self.add(equation)
        self.play(LaggedStartMap(
            DrawBorderThenFill, circles
        ))
        self.wait()
