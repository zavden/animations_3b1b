# ==============================================================================
# Scene:      AskAboutZero
# Source:     videos/_2025/laplace/main_supplements.py (lines 548-555)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutZero.py AskAboutZero -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutZero(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph(height=2)
        self.play(randy.says(Tex(R"s = 0 ?"), mode="erm", look_at=3 * UP + 0.5 * RIGHT))
        for _ in range(2):
            self.play(Blink(randy))
            self.wait(2)
