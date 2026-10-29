# ==============================================================================
# Scene:      BonusVideo
# Source:     videos/_2024/puzzles/supplements.py (lines 942-950)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BonusVideo.py BonusVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BonusVideo(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer(mode="tease", height=4)
        morty.to_edge(DOWN, buff=1).shift(2 * RIGHT)
        self.play(Blink(morty))
        self.play(morty.says("Bonus video!", mode="hooray"))
        self.play(Blink(morty))
        self.wait(2)
