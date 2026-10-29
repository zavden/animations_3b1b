# ==============================================================================
# Scene:      SeekingMatchedParameters
# Source:     videos/_2024/transformers/supplements.py (lines 1159-1188)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeekingMatchedParameters.py SeekingMatchedParameters -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SeekingMatchedParameters(TeacherStudentsScene):
    def construct(self):
        # Test
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)
        equation = VGroup(
            Text("# Value params").set_color(RED),
            Tex("=", font_size=72).rotate(PI / 2),
            Text("(# Query params) + (# Key params)"),
        )
        equation[2].scale(0.75)
        equation[2]["# Query params"].set_color(YELLOW)
        equation[2]["# Key params"].set_color(TEAL)
        equation.arrange(DOWN, buff=MED_LARGE_BUFF)
        equation.move_to(self.hold_up_spot, DOWN)

        self.play(
            self.teacher.change("raise_right_hand", equation),
            FadeIn(equation, UP),
            self.change_students("erm", "confused", "sassy", look_at=equation),
        )
        self.wait(2)
        self.play(
            self.change_students("pondering", "confused", "hesitant", look_at=self.screen)
        )
        self.wait(4)
        self.play(
            self.change_students("erm", "confused", "sassy", look_at=equation)
        )
        self.wait(4)
