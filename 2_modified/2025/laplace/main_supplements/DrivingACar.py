# ==============================================================================
# Scene:      DrivingACar
# Source:     videos/_2025/laplace/main_supplements.py (lines 82-90)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DrivingACar.py DrivingACar -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - MoveCar(4 * RIGHT) -> MoveCar(car, 4 * RIGHT): the class requires the car as its first argument
#
# Notes:
#   The bugs of Car.get_tires and of the operator import were fixed in _lib/custom/drawings.py.
# ==============================================================================

from manim_imports_ext import *

class DrivingACar(InteractiveScene):
    def construct(self):
        # Test
        car = Car()
        car.move_to(4 * LEFT)
        car[0][2].set_fill(BLUE).insert_n_curves(100)
        self.add(car)
        # CHANGE: _lib/custom's MoveCar receives (car, target_point); the original only passed the target point (TypeError).
        self.play(MoveCar(car, 4 * RIGHT), run_time=10)
        self.wait()
