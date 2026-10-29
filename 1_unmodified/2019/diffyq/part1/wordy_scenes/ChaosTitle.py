# ==============================================================================
# Scene:      ChaosTitle
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 668-681)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChaosTitle.py ChaosTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ChaosTitle(Scene):
    def construct(self):
        title = OldTexText("Chaos theory")
        title.scale(1.5)
        title.to_edge(UP)
        line = Line(LEFT, RIGHT)
        line.set_width(FRAME_WIDTH - 1)
        line.next_to(title, DOWN)

        self.play(
            Write(title),
            ShowCreation(line),
        )
        self.wait()
