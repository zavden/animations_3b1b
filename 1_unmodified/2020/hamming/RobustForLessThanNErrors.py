# ==============================================================================
# Scene:      RobustForLessThanNErrors
# Source:     videos/_2020/hamming.py (lines 2577-2599)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RobustForLessThanNErrors.py RobustForLessThanNErrors -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RobustForLessThanNErrors(Scene):
    def construct(self):
        words = OldTexText(
            "Robust for ", "$\\le N$", " errors",
        )
        words.to_edge(UP)
        words[1].set_color(YELLOW)
        words[2].shift(0.15 * RIGHT)
        N = words[1][-1]

        num = Integer(1)
        num.set_color(YELLOW)
        num.move_to(N, LEFT)
        num.set_value(1)

        self.play(Write(words, run_time=2))
        self.wait()
        self.remove(N)
        self.add(num)
        self.play(ChangeDecimalToValue(num, 20, run_time=3))
        self.remove(num)
        self.add(N)
        self.wait()
