# ==============================================================================
# Scene:      OddNumberCountTo101
# Source:     videos/_2020/hamming.py (lines 2406-2418)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OddNumberCountTo101.py OddNumberCountTo101 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OddNumberCountTo101(Scene):
    def construct(self):
        group = VGroup(
            *[Integer(2 * n + 1) for n in range(1, 50)],
        )
        group.set_color(RED)
        group.scale(2)
        for mob in group[:2]:
            self.add(mob)
            self.wait()
            self.remove(mob)
        self.play(ShowSubmobjectsOneByOne(group[2:]), run_time=6, rate_func=bezier([0, 0, 1, 1]))
        self.wait()
