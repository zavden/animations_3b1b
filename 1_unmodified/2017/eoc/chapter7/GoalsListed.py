# ==============================================================================
# Scene:      GoalsListed
# Source:     videos/_2017/eoc/chapter7.py (lines 731-753)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GoalsListed.py GoalsListed -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class GoalsListed(Scene):
    def construct(self):
        goals = VGroup(*[
            OldTexText("Goal %d: %s"%(d, s))
            for d, s in zip(it.count(1), [
                "Formal definition of a derivative",
                "$(\\epsilon, \\delta)$ definition of limits",
                "L'Hôpital's rule",
            ])
        ])
        goals.arrange(
            DOWN, buff = LARGE_BUFF, aligned_edge = LEFT
        )

        for goal in goals:
            self.play(FadeIn(goal))
            self.wait()
        for i, goal in enumerate(goals):
            anims = [goal.set_color, YELLOW]
            if i > 0:
                anims += [goals[i-1].set_color, WHITE]
            self.play(*anims)
            self.wait()
