# ==============================================================================
# Scene:      IsThereAGeometry
# Source:     videos/_2022/puzzles/subsets.py (lines 4578-4593)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IsThereAGeometry.py IsThereAGeometry -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IsThereAGeometry(InteractiveScene):
    def construct(self):
        randy = Randolph(height=1.5)
        randy.shift(RIGHT)

        self.play(PiCreatureBubbleIntroduction(
            randy, OldTexText("Is there a\\\\geometric structure?"),
            target_mode="pondering",
            look_at=[10, -3, 0],
            bubble_type=ThoughtBubble,
            bubble_config=dict(width=3, height=1.75)
        ))
        for x in range(2):
            self.play(Blink(randy))
            self.wait(2)
            self.play(randy.change("thinking"))
