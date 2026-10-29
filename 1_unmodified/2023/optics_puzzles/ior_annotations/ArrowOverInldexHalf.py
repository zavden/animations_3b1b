# ==============================================================================
# Scene:      ArrowOverInldexHalf
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1373-1392)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowOverInldexHalf.py ArrowOverInldexHalf -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArrowOverInldexHalf(InteractiveScene):
    speed = 1.0
    index = 0.68
    bounds = (-3, 3)

    def construct(self):
        arrow = Vector(0.5 * DOWN)
        arrow.next_to(UP, UP)
        arrow.to_edge(LEFT, buff=0)
        x_min, x_max = self.bounds

        def update_arrow(arr, dt):
            step = dt * self.speed
            if x_min < arr.get_x() < x_max:
                step /= self.index
            arr.shift(step * RIGHT)

        arrow.add_updater(update_arrow)
        self.add(arrow)
        self.wait_until(lambda: arrow.get_x() > FRAME_WIDTH / 2 + 2 * arrow.get_width())
