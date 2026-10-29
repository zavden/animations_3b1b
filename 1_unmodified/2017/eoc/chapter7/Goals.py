# ==============================================================================
# Scene:      Goals
# Source:     videos/_2017/eoc/chapter7.py (lines 151-170)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Goals.py Goals -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class Goals(Scene):
    def construct(self):
        goals = [
            OldTexText("Goal %d:"%d, s)
            for d, s in [
                (1, "Formal definition of derivatives"),
                (2, "$(\\epsilon, \\delta)$ definition of a limit"),
                (3, "L'Hôpital's rule"),
            ]
        ]
        for goal in goals:
            goal.scale(1.3)
            goal.shift(3*DOWN).to_edge(LEFT)

        curr_goal = goals[0]
        self.play(FadeIn(curr_goal))
        self.wait(2)
        for goal in goals[1:]:
            self.play(Transform(curr_goal, goal))
            self.wait(2)
