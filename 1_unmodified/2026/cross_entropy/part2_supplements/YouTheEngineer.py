# ==============================================================================
# Scene:      YouTheEngineer
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 128-151)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl YouTheEngineer.py YouTheEngineer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class YouTheEngineer(InteractiveScene):
    def construct(self):
        # test
        randy = Randolph()
        randy.to_edge(LEFT)

        self.play(randy.change("erm", RIGHT))
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("hesitant", RIGHT))
        self.play(Blink(randy))
        self.wait()
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("pondering", self.frame.get_corner(UL)))
        self.play(Blink(randy))

        # Away
        self.play(
            randy.change("horrified"),
            VFadeOut(randy),
            self.frame.animate.shift(2 * UP)
        )
        self.wait()
