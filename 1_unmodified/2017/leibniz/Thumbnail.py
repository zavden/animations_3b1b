# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/leibniz.py (lines 4774-4814)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def chi_func(n):
    if n%2 == 0:
        return 0
    if n%4 == 1:
        return 1
    else:
        return -1


class Thumbnail(Scene):
    def construct(self):
        randy = Randolph()
        randy.set_height(5)
        body_copy = randy.body.copy()
        body_copy.set_stroke(YELLOW, width = 3)
        body_copy.set_fill(opacity = 0)
        self.add(randy)

        primes = [
            n for n in range(2, 1000)
            if all(n%k != 0 for k in list(range(2, n)))
        ]
        prime_mobs = VGroup()
        x_spacing = 1.7
        y_spacing = 1.5
        n_rows = 10
        n_cols = 8
        for i, prime in enumerate(primes[:n_rows*n_cols]):
            prime_mob = Integer(prime)
            prime_mob.scale(1.5)
            x = i%n_cols
            y = i//n_cols
            prime_mob.shift(x*x_spacing*RIGHT + y*y_spacing*DOWN)
            prime_mobs.add(prime_mob)
            prime_mob.set_color({
                -1 : YELLOW,
                0 : RED,
                1 : BLUE_C,
            }[chi_func(prime)])
        prime_mobs.center().to_edge(UP)
        for i in range(7):
            self.add(SurroundingRectangle(
                VGroup(*prime_mobs[n_cols*i:n_cols*(i+1)]),
                fill_opacity = 0.7,
                fill_color = BLACK,
                stroke_width = 0,
                buff = 0,
            ))
        self.add(prime_mobs)
        self.add(body_copy)
