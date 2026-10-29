# ==============================================================================
# Scene:      PiecewiseConstantCar
# Source:     videos/_2017/eoc/chapter8.py (lines 704-723)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiecewiseConstantCar.py PiecewiseConstantCar -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiecewiseConstantCar(Scene):
    def construct(self):
        car = Car()
        start_point = 5*LEFT
        car.move_to(start_point)

        self.add(car)
        self.wait()
        for shift in 2, 6, 12:
            car.randy.rotate(np.pi/8)
            anim = MoveCar(
                car, start_point+shift*RIGHT,
                rate_func=linear
            )

            anim.target_mobject[0].rotate(-np.pi/8)
            # for mob in anim.starting_mobject, anim.mobject:
            #     mob.randy.rotate(np.pi/6)
            self.play(anim)
        self.wait()
