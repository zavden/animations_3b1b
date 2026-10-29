# ==============================================================================
# Scene:      WritePhaseFlow
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 372-380)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WritePhaseFlow.py WritePhaseFlow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WritePhaseFlow(Scene):
    def construct(self):
        words = OldTexText("Phase flow")
        words.scale(2)
        words.shift(FRAME_WIDTH * LEFT / 4)
        words.to_edge(UP)
        words.add_background_rectangle()
        self.play(Write(words))
        self.wait()
