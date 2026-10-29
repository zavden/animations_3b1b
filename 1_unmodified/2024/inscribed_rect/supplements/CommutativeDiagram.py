# ==============================================================================
# Scene:      CommutativeDiagram
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 358-395)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CommutativeDiagram.py CommutativeDiagram -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CommutativeDiagram(InteractiveScene):
    samples = 4

    def construct(self):
        # Test
        objs = Square().set_height(3.5).replicate(3)
        objs[0].to_corner(UR).shift(0.5 * LEFT)
        objs[1].move_to(objs[0]).to_edge(DOWN)
        objs[2].next_to(objs[0], LEFT, buff=3)

        arrow_kw = dict(thickness=5)
        down_arrow = Arrow(
            objs[0].get_corner(DL) + UP,
            objs[1].get_left(),
            path_arc=PI,
            **arrow_kw
        )
        lr_arrow = VGroup(
            Arrow(objs[0], objs[2], **arrow_kw).shift(0.15 * UP),
            Arrow(objs[2], objs[0], **arrow_kw).shift(0.15 * DOWN),
        )

        words = Text("Another\nSurface", font_size=72)
        cloud = ThoughtBubble(words)[0][-1]
        cloud.add(words)
        cloud.move_to(objs[2], RIGHT).shift(0.25 * LEFT)

        dr_arrow = Arrow(cloud.get_bottom(), objs[1].get_left() + (-1, 0.25, 0), buff=0.3, **arrow_kw)

        self.play(Write(down_arrow))
        self.wait()
        self.play(
            *map(GrowArrow, lr_arrow),
            FadeIn(cloud, LEFT)
        )
        self.wait()
        self.play(GrowArrow(dr_arrow))
        self.wait()
