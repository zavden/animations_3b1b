# ==============================================================================
# Scene:      ThreePis
# Source:     videos/_2021/siggraph.py (lines 4-27)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreePis.py ThreePis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreePis(Scene):
    def construct(self):
        pis = VGroup(*(PiCreature() for x in range(3)))
        for pi, color in zip(pis, (BLUE_E, BLUE_C, BLUE_D)):
            pi.set_color(color)
        pis.set_height(2)
        pis.arrange(RIGHT, buff=2)
        pis.to_corner(DR)
        pis[2].flip()

        words = ["Choas", "Linear\nalgebra", "Quaternions"]
        modes = ["speaking", "tease", "hooray"]
        for pi, word, mode in zip(pis, words, modes):
            bubble = pi.get_bubble(
                word,
                bubble_type=SpeechBubble,
                height=3, width=3, direction=RIGHT
            )
            bubble.add(bubble.content)
            bubble.next_to(pi, UL)
            bubble.shift(RIGHT)
            pi.change(mode, bubble.content)
            self.add(pi, bubble)
        self.wait()
