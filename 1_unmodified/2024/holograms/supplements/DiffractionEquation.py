# ==============================================================================
# Scene:      DiffractionEquation
# Source:     videos/_2024/holograms/supplements.py (lines 1839-1862)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiffractionEquation.py DiffractionEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DiffractionEquation(InteractiveScene):
    def construct(self):
        # Add equation
        equation = Tex(R"{d} \cdot \sin(\theta) = \lambda", font_size=60)
        equation.set_backstroke(BLACK)
        arrow = Vector(DOWN, thickness=4)
        arrow.set_color(BLUE)

        d, theta, lam = syms = [equation[s][0] for s in [R"{d}", R"\theta", R"\lambda"]]
        colors = [BLUE, YELLOW, TEAL]

        arrow.next_to(d, UP, LARGE_BUFF)
        arrow.set_fill(opacity=0)

        self.add(equation)

        for sym, color in zip(syms, colors):
            self.play(
                FlashAround(sym, color=color, time_span=(0.25, 1.25)),
                sym.animate.set_fill(color),
                arrow.animate.next_to(sym, UP).set_fill(color, 1),
            )
            self.wait()
        self.play(FadeOut(arrow))
