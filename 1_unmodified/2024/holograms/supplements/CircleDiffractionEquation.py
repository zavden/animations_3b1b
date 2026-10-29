# ==============================================================================
# Scene:      CircleDiffractionEquation
# Source:     videos/_2024/holograms/supplements.py (lines 783-803)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircleDiffractionEquation.py CircleDiffractionEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CircleDiffractionEquation(InteractiveScene):
    def construct(self):
        # Add equation
        self.add(FullScreenRectangle())
        equation = Tex(
            R"{d} \cdot \sin(\theta) = n \lambda",
            font_size=72,
            t2c={R"{d}": BLUE, R"\theta": YELLOW, R"\lambda": TEAL}
        )
        equation.set_backstroke(BLACK)
        title = Text("The Diffraction Equation", font_size=60)
        title.set_color(GREY_A)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        equation.next_to(title, DOWN, MED_LARGE_BUFF)

        self.add(title)
        self.add(equation)
        self.play(
            FlashAround(equation, run_time=4, time_width=1.5, buff=MED_SMALL_BUFF),
        )
        self.wait()
