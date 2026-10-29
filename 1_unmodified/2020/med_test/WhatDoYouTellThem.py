# ==============================================================================
# Scene:      WhatDoYouTellThem
# Source:     videos/_2020/med_test.py (lines 2203-2208)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatDoYouTellThem.py WhatDoYouTellThem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatDoYouTellThem(Scene):
    def construct(self):
        text = OldTexText("What do you tell them?", font_size=72)
        text.set_color(BLUE)
        self.play(Write(text))
        self.wait(5)
