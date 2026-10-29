# ==============================================================================
# Scene:      ForcedOscillatorEquation
# Source:     videos/_2025/laplace/derivatives.py (lines 11-37)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ForcedOscillatorEquation.py ForcedOscillatorEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ForcedOscillatorEquation(InteractiveScene):
    def construct(self):
        x_colors = color_gradient([TEAL, RED], 3, interp_by_hsl=True)
        t2c = {
            "x(t)": x_colors[0],
            "x'(t)": x_colors[1],
            "x''(t)": x_colors[2],
            "x_0": x_colors[0],
            "v_0": x_colors[1],
            R"\omega": PINK,
            "{s}": YELLOW,
        }
        ode = Tex(R"m x''(t) + \mu x'(t) + k x(t) = F_0 \cos(\omega t)", t2c=t2c)
        ode.to_edge(UP)

        self.add(ode)

        # Comment on third force
        rect = SurroundingRectangle(ode[R"F_0 \cos(\omega t)"], buff=0.2)
        rect.set_stroke(YELLOW, 2)

        self.play(ShowCreation(rect))
        self.wait()
        self.play(rect.animate.surround(ode[R"\omega"], buff=0.1))
        self.wait()
        self.play(FadeOut(rect))
        self.wait()
