# ==============================================================================
# Scene:      TwoErrorGrids
# Source:     videos/_2020/hamming.py (lines 6313-6348)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoErrorGrids.py TwoErrorGrids -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoErrorGrids(Scene):
    def construct(self):
        grid = VGroup(*[Square() for x in range(16)])
        grid.arrange_in_grid(buff=0)
        grid.set_stroke(WHITE, 1)
        grid.set_height(1)

        grids = VGroup(*[grid.copy() for x in range(16)])
        grids.arrange_in_grid(buff=MED_LARGE_BUFF)
        grids.set_height(7)
        grids.to_edge(RIGHT)

        self.add(grids)

        vects = [
            np.array(tup)
            for tup in it.product(*[[0, 1]] * 4)
        ]

        def vect_to_int(vect):
            return sum([b * (1 << i) for i, b in enumerate(reversed(vect))])

        for vect in vects:
            label = VGroup(*map(Integer, vect))
            label.arrange(RIGHT, buff=SMALL_BUFF)
            label.to_edge(LEFT)
            self.add(label)

            error_int = vect_to_int(vect)
            for i, grid in enumerate(grids):
                grid[i].set_fill(YELLOW, 1)
                grid[i ^ error_int].set_fill(TEAL, 1)

            self.wait()
            grids.set_fill(opacity=0)
            self.remove(label)
