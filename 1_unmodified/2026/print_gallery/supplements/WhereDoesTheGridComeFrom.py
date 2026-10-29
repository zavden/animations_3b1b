# ==============================================================================
# Scene:      WhereDoesTheGridComeFrom
# Source:     videos/_2026/print_gallery/supplements.py (lines 167-176)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhereDoesTheGridComeFrom.py WhereDoesTheGridComeFrom -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhereDoesTheGridComeFrom(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.to_corner(DL)
        self.play(
            randy.says("Where does this\ncome from?", mode="confused")
        )
        self.play(Blink(randy))
        self.wait()
