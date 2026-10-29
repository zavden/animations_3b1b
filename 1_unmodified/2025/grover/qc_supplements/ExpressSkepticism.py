# ==============================================================================
# Scene:      ExpressSkepticism
# Source:     videos/_2025/grover/qc_supplements.py (lines 317-327)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpressSkepticism.py ExpressSkepticism -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpressSkepticism(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph(height=3.5)
        randy.flip()
        randy.to_corner(DR)
        for mood in ["sassy", "pondering", "confused"]:
            self.play(randy.change(mood, ORIGIN))
            for _ in range(2):
                self.play(Blink(randy))
                self.wait(2)
