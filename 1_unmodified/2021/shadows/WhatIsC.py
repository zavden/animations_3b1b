# ==============================================================================
# Scene:      WhatIsC
# Source:     videos/_2021/shadows.py (lines 5381-5390)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatIsC.py WhatIsC -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatIsC(Scene):
    def construct(self):
        words = OldTexText(
            "What is $c$?!",
            tex_to_color_map={"$c$": RED},
            font_size=72,
        )
        self.play(Write(words))
        self.play(FlashUnder(words, color=RED))
        self.wait()
