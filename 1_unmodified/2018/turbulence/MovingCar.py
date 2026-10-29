# ==============================================================================
# Scene:      MovingCar
# Source:     videos/_2018/turbulence.py (lines 1299-1304)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MovingCar.py MovingCar -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MovingCar(Scene):
    def construct(self):
        car = Car()
        x = 3
        car.move_to(x * LEFT)
        self.play(MoveCar(car, x * RIGHT, run_time=4))
