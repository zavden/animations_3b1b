# ==============================================================================
# Scene:      WhatsThat
# Source:     videos/_2022/borwein/supplements.py (lines 399-404)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatsThat.py WhatsThat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatsThat(InteractiveScene):
    def construct(self):
        randy = Randolph(height=2)
        self.play(randy.says("...meaning?", mode="maybe", look_at=DR))
        self.play(Blink(randy))
        self.wait()
