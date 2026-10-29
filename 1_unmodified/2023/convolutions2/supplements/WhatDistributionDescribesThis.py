# ==============================================================================
# Scene:      WhatDistributionDescribesThis
# Source:     videos/_2023/convolutions2/supplements.py (lines 67-73)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatDistributionDescribesThis.py WhatDistributionDescribesThis -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhatDistributionDescribesThis(InteractiveScene):
    def construct(self):
        words = Text("What distribution\ndescribes this?")
        arrow = Arrow(words.get_bottom(), words.get_bottom() + DL)
        VGroup(words, arrow).set_color(TEAL)
        self.play(Write(words), ShowCreation(arrow))
        self.wait()
