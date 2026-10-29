# ==============================================================================
# Scene:      VariableInputs
# Source:     videos/_2023/gauss_int/herschel.py (lines 406-428)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VariableInputs.py VariableInputs -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class VariableInputs(InteractiveScene):
    def construct(self):
        equation = Tex(R"f(\sqrt{(1.00)^2 + (0.00)^2}) = f(1.00)f(0.00)")
        xs = equation.make_number_changeable("1.00", replace_all=True)
        ys = equation.make_number_changeable("0.00", replace_all=True)

        xs.set_color(BLUE)
        ys.set_color(YELLOW)

        x_tracker = ValueTracker(1.0)
        y_tracker = ValueTracker(1.0)

        for mob in xs:
            mob.add_updater(lambda m: m.set_value(x_tracker.get_value()))

        for mob in ys:
            mob.add_updater(lambda m: m.set_value(y_tracker.get_value()))

        self.add(equation)
        for n in range(30):
            self.play(x_tracker.animate.set_value(random.random() * 10))
            self.play(y_tracker.animate.set_value(random.random() * 10))
            self.wait(0.5)
