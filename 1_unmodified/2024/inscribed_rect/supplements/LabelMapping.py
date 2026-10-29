# ==============================================================================
# Scene:      LabelMapping
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 202-238)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LabelMapping.py LabelMapping -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LabelMapping(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Mapping", font_size=72)
        title.to_edge(UP)
        title.set_color(BLUE)
        underline = Underline(title, buff=-0.1)
        underline.set_color(BLUE)

        body = VGroup(
            Text("Pair of\nloop points"),
            Vector(RIGHT),
            Text("3D space"),
        )
        body.arrange(RIGHT)
        body.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(title, 0.25 * UP), ShowCreation(underline))
        self.wait()
        self.play(FadeIn(body[0]))
        self.play(
            GrowArrow(body[1]),
            TransformFromCopy(*body[0::2])
        )
        self.wait()

        # Add continuity mention
        new_title = Text("Continuous Mapping", font_size=72)
        new_title.move_to(title, UP)
        new_title.match_style(title)

        self.play(
            Write(new_title["Continuous"]),
            Transform(title, new_title["Mapping"][0]),
            underline.animate.set_width(1.2 * new_title.get_width())
        )
        self.wait()
