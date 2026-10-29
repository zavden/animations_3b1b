# ==============================================================================
# Scene:      SupportIcon
# Source:     videos/outside_videos/for_site.py (lines 78-95)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SupportIcon.py SupportIcon -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SupportIcon(Scene):
    def construct(self):
        randy = Randolph(mode="coin_flip_2")
        morty = Mortimer(mode="gracious")
        pis = VGroup(randy, morty)
        pis.arrange(RIGHT, buff=3)
        pis.to_edge(DOWN)
        randy.make_eye_contact(morty)
        heart = SuitSymbol("hearts")
        heart.set_height(1)
        heart.next_to(randy, UR, buff=-0.5)
        heart.shift(0.5 * RIGHT)

        # rect = FullScreenFadeRectangle(opacity=0.85)

        # self.add(rect)
        self.add(pis)
        self.add(heart)
