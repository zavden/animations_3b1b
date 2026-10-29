# ==============================================================================
# Scene:      LessWrongCarJourneyApproximation
# Source:     videos/_2017/eoc/chapter8.py (lines 1406-1410)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LessWrongCarJourneyApproximation.py LessWrongCarJourneyApproximation -w -m --fps 15
# ==============================================================================

import scipy
from manim_imports_ext import *

def v_rate_func(t):
    return 4*t - 4*(t**2)


def s_rate_func(t):
    return 3*(t**2) - 2*(t**3)


class CarJourneyApproximation(Scene):
    CONFIG = {
        "n_jumps" : 5,
        "bottom_words" : "Approximated motion (5 jumps)",
    }
    def construct(self):
        points = [5*LEFT + v for v in (UP, 2*DOWN)]
        cars = [Car().move_to(point) for point in points]
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        words = [
            OldTexText("Real motion (smooth)").shift(3*UP),
            OldTexText(self.bottom_words).shift(0.5*DOWN),
        ]
        words[1].set_color(GREEN)


        self.add(h_line, *cars + words)
        self.wait()
        self.play(*[
            MoveCar(
                car, point+10*RIGHT,
                run_time = 5,
                rate_func = rf
            )
            for car, point, rf in zip(cars, points, [
                s_rate_func,
                self.get_approximated_rate_func(self.n_jumps)
            ])
        ])
        self.wait()

    def get_approximated_rate_func(self, n):
        new_v_rate_func = lambda t : v_rate_func(np.floor(t*n)/n)
        max_integral, err = scipy.integrate.quad(
            v_rate_func, 0, 1
        )
        def result(t):
            integral, err = scipy.integrate.quad(new_v_rate_func, 0, t)
            return integral/max_integral
        return result


class LessWrongCarJourneyApproximation(CarJourneyApproximation):
    CONFIG = {
        "n_jumps" : 20,
        "bottom_words" : "Better approximation (20 jumps)",
    }
