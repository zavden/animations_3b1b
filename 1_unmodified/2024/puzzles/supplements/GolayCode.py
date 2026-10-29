# ==============================================================================
# Scene:      GolayCode
# Source:     videos/_2024/puzzles/supplements.py (lines 814-846)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GolayCode.py GolayCode -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GolayCode(InteractiveScene):
    def construct(self):
        # Set up dots
        dots = Dot().get_grid(23, 12)
        dots.set_height(FRAME_HEIGHT - 1)
        dots.set_stroke(WHITE, 1)
        dots.set_fill(BLACK)
        self.add(dots)

        # Color
        for i in range(12):
            dots[12 * i + i].set_fill(GREY_B)
        pattern = np.array([
            [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
            [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        ])

        for i, row in zip(range(12, 23), pattern):
            for j, bit in enumerate(row):
                dots[12 * i + j].set_fill(GREY_B if bit else BLACK)

        self.play(Write(dots))
        self.wait()
