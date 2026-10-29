# ==============================================================================
# Scene:      YouAsAMathematician
# Source:     videos/_2026/hairy_ball/supplements.py (lines 217-233)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl YouAsAMathematician.py YouAsAMathematician -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class YouAsAMathematician(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph(height=4)
        randy.move_to(3 * LEFT)
        label = VGroup(
            Text("You", font_size=72),
            Text("The mathematician").set_color(GREY_B)
        )
        label.arrange(DOWN)
        label.next_to(randy, DOWN)

        self.add(randy, label)
        self.play(randy.change("pondering", 3 * RIGHT))
        self.play(Blink(randy))
        self.play(randy.change("tease", 3 * RIGHT))
        self.wait(3)
