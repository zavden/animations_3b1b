# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2022/some2/announcement.py (lines 249-268)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(InteractiveScene):
    def construct(self):
        # text = Text("More\nMath\nPlease", alignment="LEFT")
        # text.set_height(6)
        # text.to_edge(LEFT, buff=1.0)
        text = Text("Summer\nof\nMath\nExposition", alignment="LEFT")
        text.set_height(FRAME_HEIGHT - 1)
        text.to_edge(LEFT)
        self.add(text)

        randy = Randolph(mode="thinking", color=YELLOW, height=5)
        randy.to_corner(UR, buff=1.0)
        randy.look_at(text)
        self.add(randy)

        two = Text("Round 2")
        two.set_height(1)
        two.set_color(YELLOW)
        two.next_to(text[-1], RIGHT, buff=0.7, aligned_edge=DOWN)
        self.add(two)
