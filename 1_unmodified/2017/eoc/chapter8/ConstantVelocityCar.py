# ==============================================================================
# Scene:      ConstantVelocityCar
# Source:     videos/_2017/eoc/chapter8.py (lines 529-541)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConstantVelocityCar.py ConstantVelocityCar -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConstantVelocityCar(Scene):
    def construct(self):
        car = Car()
        car.move_to(5*LEFT + 3*DOWN)

        self.add(car)
        self.wait()
        self.play(MoveCar(
            car, 7*RIGHT+3*DOWN,
            run_time = 5,
            rate_func=linear,
        ))
        self.wait()
