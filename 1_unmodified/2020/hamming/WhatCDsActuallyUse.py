# ==============================================================================
# Scene:      WhatCDsActuallyUse
# Source:     videos/_2020/hamming.py (lines 1075-1087)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatCDsActuallyUse.py WhatCDsActuallyUse -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatCDsActuallyUse(Scene):
    def construct(self):
        arrow = Vector(2 * RIGHT + UP)
        words = OldTexText("What CDs/DVDs\\\\actually use")
        words.next_to(arrow.get_end(), RIGHT)
        arrow.set_color(YELLOW)
        words.set_color(YELLOW)

        self.play(
            GrowFromPoint(words, arrow.get_start()),
            GrowArrow(arrow)
        )
        self.wait()
