# ==============================================================================
# Scene:      Over10KComparisons
# Source:     videos/_2022/some2/winners.py (lines 291-308)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Over10KComparisons.py Over10KComparisons -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Over10KComparisons(InteractiveScene):
    def construct(self):
        # Start
        count = VGroup(
            Integer(10000),
            Text("Comparisons")
        )
        count.arrange(DOWN)
        count.scale(2)
        plus = Text("+").scale(2)
        plus.next_to(count[0], RIGHT, buff=SMALL_BUFF)

        self.play(
            CountInFrom(count[0], 0, run_time=3),
            Write(count[1], run_time=1),
        )
        self.add(plus)
        self.wait()
