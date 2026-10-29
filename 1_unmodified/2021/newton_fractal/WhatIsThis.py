# ==============================================================================
# Scene:      WhatIsThis
# Source:     videos/_2021/newton_fractal.py (lines 1999-2006)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatIsThis.py WhatIsThis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatIsThis(Scene):
    def construct(self):
        words = Text("What is this", color=RED)
        arrow = Vector(UR)
        arrow.set_color(RED)
        words.next_to(ORIGIN, DOWN)
        self.play(FadeIn(words, lag_ratio=0.1), ShowCreation(arrow))
        self.wait()
