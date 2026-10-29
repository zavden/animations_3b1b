# ==============================================================================
# Scene:      LastVideoFrame
# Source:     videos/_2023/gauss_int/supplements.py (lines 174-206)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastVideoFrame.py LastVideoFrame -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LastVideoFrame(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle().set_fill(GREY_E, 1))
        screen = ScreenRectangle(height=6.5)
        screen.to_edge(DOWN, buff=MED_SMALL_BUFF)
        screen.set_fill(BLACK, 1)
        screen.set_stroke(BLACK, 0)
        screen_outline = screen.copy().set_stroke(BLUE_D, 2)
        self.add(screen)

        # Test
        titles = VGroup(
            Text("Central Limit Theorem"),
            Text("Normal Distribution"),
            Text("Normal Distribution (aka a Gaussian)"),
        )
        for title in titles:
            title.scale(56 / 48)
            title.move_to(midpoint(screen.get_top(), TOP))

        self.add(titles[0])
        self.play(ShowCreation(screen_outline, run_time=3))
        self.wait(2)
        self.play(
            FadeOut(titles[0], UP),
            FadeIn(titles[1], UP),
        )
        self.wait()
        self.play(
            ReplacementTransform(titles[1], titles[2]["Normal Distribution"][0]),
            Write(titles[2]["(aka a Gaussian)"])
        )
        self.wait(3)
