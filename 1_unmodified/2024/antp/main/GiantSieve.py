# ==============================================================================
# Scene:      GiantSieve
# Source:     videos/_2024/antp/main.py (lines 1066-1069)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GiantSieve.py GiantSieve -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SieveOfEratosthenes(InteractiveScene):
    grid_shape = (10, 10)
    n_iterations = 10
    rect_buff = 0.1

    def construct(self):
        # Initialize grid
        grid = Square().get_grid(*self.grid_shape, buff=0)
        grid.set_height(FRAME_HEIGHT - 1)
        grid.set_stroke(width=1)
        number_mobs = self.get_number_mobs(grid)
        number_mobs[0].set_opacity(0)

        self.add(grid, number_mobs)

        # Run the sieve
        modulus = 2
        numbers = list(range(2, len(grid) + 1))
        for n in range(self.n_iterations):
            numbers = list(filter(lambda n: n % modulus != 0, numbers))
            to_remove = VGroup(*(
                mob
                for mob in number_mobs
                if mob.get_value() % modulus == 0
            ))
            rects = VGroup(*(
                SurroundingRectangle(tr, buff=self.rect_buff)
                for tr in to_remove
                if tr.get_fill_opacity() > 0.5
            ))
            rects.set_stroke(RED, 1)

            self.play(
                to_remove.animate.set_color(RED),
                Write(rects, stroke_color=RED, stroke_width=2),
                lag_ratio=0.1,
                run_time=2
            )
            self.wait()
            self.play(
                to_remove[0].animate.set_color(WHITE),
                to_remove[1:].animate.set_opacity(0),
                number_mobs[0].animate.set_opacity(0),
                FadeOut(rects)
            )
            modulus = numbers[0]

    def get_number_mobs(self, grid):
        return VGroup(*(
            Integer(i).set_height(0.3 * box.get_height()).move_to(box)
            for i, box in zip(it.count(1), grid)
        ))


class GiantSieve(SieveOfEratosthenes):
    grid_shape = (25, 25)
    n_iterations = 30
    rect_buff = 0.02
