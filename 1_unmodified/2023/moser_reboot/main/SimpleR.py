# ==============================================================================
# Scene:      SimpleR
# Source:     videos/_2023/moser_reboot/main.py (lines 684-686)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleR.py SimpleR -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleR(InteractiveScene):
    def construct(self):
        self.add(Tex("R").scale(2))
