# ==============================================================================
# Scene:      WonderAboutAverage
# Source:     videos/_2021/shadows.py (lines 2234-2246)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WonderAboutAverage.py WonderAboutAverage -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WonderAboutAverage(Scene):
    def construct(self):
        randy = Randolph()
        randy.to_edge(DOWN)
        randy.look(RIGHT)
        self.play(PiCreatureBubbleIntroduction(
            randy, OldTexText("How do you think\\\\about this average"),
            target_mode="confused",
            run_time=2
        ))
        for x in range(2):
            self.play(Blink(randy))
            self.wait(2)
