# ==============================================================================
# Scene:      TopicsAfterSingleVariable
# Source:     videos/_2018/alt_calc.py (lines 3408-3456)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TopicsAfterSingleVariable.py TopicsAfterSingleVariable -w -m --fps 15
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


class TopicsAfterSingleVariable(PiCreatureScene, MoreTopics):
    CONFIG = {
        "pi_creatures_start_on_screen": False,
    }

    def construct(self):
        MoreTopics.construct(self)
        self.show_horror()
        self.zero_in_on_complex_analysis()

    def create_pi_creatures(self):
        creatures = VGroup(*[
            PiCreature(color=color)
            for color in [BLUE_E, BLUE_C, BLUE_D]
        ])
        creatures.arrange(RIGHT, buff=LARGE_BUFF)
        creatures.scale(0.5)
        creatures.to_corner(DR)
        return creatures

    def show_horror(self):
        creatures = self.get_pi_creatures()
        modes = ["horrified", "tired", "horrified"]
        for creature, mode in zip(creatures, modes):
            creature.generate_target()
            creature.target.change(mode, self.other_topics)
        creatures.fade(1)

        self.play(LaggedStartMap(MoveToTarget, creatures))
        self.wait(2)

    def zero_in_on_complex_analysis(self):
        creatures = self.get_pi_creatures()
        complex_analysis = self.other_topics[1]
        self.other_topics.remove(complex_analysis)

        self.play(
            complex_analysis.scale, 1.25,
            complex_analysis.center,
            complex_analysis.to_edge, UP,
            LaggedStartMap(FadeOut, self.other_topics),
            LaggedStartMap(FadeOut, self.lines),
            FadeOut(self.calculus),
            *[
                ApplyMethod(creature.change, "pondering")
                for creature in creatures
            ]
        )
        self.wait(4)
