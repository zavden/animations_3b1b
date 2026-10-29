# ==============================================================================
# Scene:      LaplaceFourierContrast
# Source:     videos/_2025/laplace/main_supplements.py (lines 687-717)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LaplaceFourierContrast.py LaplaceFourierContrast -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LaplaceFourierContrast(InteractiveScene):
    def construct(self):
        # Titles and definitions
        self.add(FullScreenRectangle())

        titles = VGroup(
            Text("Laplace Transform"),
            Text("Fourier Transform"),
        )
        t2c = {"{t}": BLUE, "{s}": YELLOW, R"\xi": RED}
        formulas = VGroup(
            Tex(R"F({s}) = \int^\infty_0 f({t}) e^{\minus {s}{t}} d{t}", t2c=t2c),
            Tex(R"\hat f(\xi) = \int^\infty_{\minus \infty} f({t}) e^{\minus 2\pi i \xi {t}} d{t}", t2c=t2c),
        )
        formulas.scale(0.75)

        for title, formula, sign in zip(titles, formulas, [-1, 1]):
            for mob in [title, formula]:
                mob.next_to(1.5 * UP, UP)
                mob.set_x(sign * FRAME_WIDTH / 4)
        titles[0].align_to(titles[1], UP)

        self.play(
            LaggedStartMap(FadeIn, titles, shift=0.5 * UP, lag_ratio=0.5)
        )
        self.wait()
        self.play(
            titles.animate.to_edge(UP),
            FadeIn(formulas, 0.5 * UP)
        )
        self.wait()
