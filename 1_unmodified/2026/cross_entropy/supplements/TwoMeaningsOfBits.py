# ==============================================================================
# Scene:      TwoMeaningsOfBits
# Source:     videos/_2026/cross_entropy/supplements.py (lines 910-939)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoMeaningsOfBits.py TwoMeaningsOfBits -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TwoMeaningsOfBits(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        meanings = VGroup(
            VGroup(
                Text("“Bits” as"),
                Tex(R"-\log_2(p)", t2c={R"-\log_2": BLUE, "p": TEAL}),
            ).arrange(RIGHT, MED_LARGE_BUFF),
            VGroup(
                Text("“Bits” as"),
                Text("# 1s and 0s")
            ).arrange(RIGHT, MED_LARGE_BUFF),
        )
        rects = Rectangle().get_grid(2, 1, buff=0).replace(self.frame, stretch=True)
        for meaning, rect in zip(meanings, rects):
            meaning.next_to(rect.get_corner(UL), DR)

        h_line = Line(LEFT, RIGHT).replace(rects, 0)

        frame.move_to(rects[1], UP)
        self.add(meanings[1])
        self.wait()
        self.play(LaggedStart(
            frame.animate.to_default_state(),
            FadeIn(h_line),
            FadeTransformPieces(meanings[1].copy(), meanings[0]),
            run_time=2
        ))
        self.wait()
