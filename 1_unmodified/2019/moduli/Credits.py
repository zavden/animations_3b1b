# ==============================================================================
# Scene:      Credits
# Source:     videos/_2019/moduli.py (lines 909-928)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Credits.py Credits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Credits(Scene):
    def construct(self):
        items = VGroup(
            OldTexText("Written by\\\\Jayadev Athreya"),
            OldTexText("Illustrated and Narrated by\\\\Grant Sanderson"),
            OldTexText(
                "3Blue1Brown\\\\",
                "\\copyright {} Copyright 2019\\\\",
                "www.3blue1brown.com\\\\",
            ),
        )
        items.arrange(DOWN, buff=LARGE_BUFF)

        items[-1].set_color(GREY_B)
        items[-1].scale(0.8, about_edge=UP)
        items[-1].to_edge(DOWN)

        self.add(items[-1])
        self.play(LaggedStartMap(FadeInFromDown, items[:-1]))
        self.wait()
