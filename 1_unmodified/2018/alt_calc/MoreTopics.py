# ==============================================================================
# Scene:      MoreTopics
# Source:     videos/_2018/alt_calc.py (lines 984-1020)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreTopics.py MoreTopics -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class MoreTopics(Scene):
    def construct(self):
        calculus = OldTexText("Calculus")
        calculus.next_to(LEFT, LEFT)
        calculus.set_color(YELLOW)
        calculus.add_background_rectangle()
        others = VGroup(
            OldTexText("Multivariable calculus"),
            OldTexText("Complex analysis"),
            OldTexText("Differential geometry"),
            OldTexText("$\\vdots$")
        )
        for word in others:
            word.add_background_rectangle()
        others.arrange(
            DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT,
        )
        others.next_to(RIGHT, RIGHT)
        lines = VGroup(*[
            Line(calculus.get_right(), word.get_left(), buff=MED_SMALL_BUFF)
            for word in others
        ])

        rect = FullScreenFadeRectangle(fill_opacity=0.7)
        self.add(rect)

        self.add(calculus)
        self.play(
            LaggedStartMap(ShowCreation, lines),
            LaggedStartMap(Write, others),
        )
        self.wait()

        self.calculus = calculus
        self.lines = lines
        self.full_screen_rect = rect
        self.other_topics = others
