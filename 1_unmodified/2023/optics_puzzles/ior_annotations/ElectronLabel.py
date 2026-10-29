# ==============================================================================
# Scene:      ElectronLabel
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 650-661)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ElectronLabel.py ElectronLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ElectronLabel(InteractiveScene):
    def construct(self):
        # Test
        label = Text("An electron, say")
        label.set_backstroke(BLACK, 5)
        label.next_to(ORIGIN, UR, buff=LARGE_BUFF)
        arrow = Arrow(label, ORIGIN)
        self.play(
            FadeIn(label, lag_ratio=0.1),
            GrowArrow(arrow)
        )
        self.wait()
