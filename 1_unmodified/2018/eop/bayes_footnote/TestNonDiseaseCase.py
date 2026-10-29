# ==============================================================================
# Scene:      TestNonDiseaseCase
# Source:     videos/_2018/eop/bayes_footnote.py (lines 318-372)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TestNonDiseaseCase.py TestNonDiseaseCase -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


class TestScene(PiCreatureScene):
    def get_result(self, creature, word, color):
        arrow = self.get_test_arrow()
        test_result = OldTexText(word)
        test_result.set_color(color)
        test_result.next_to(arrow.get_end(), RIGHT)
        group = VGroup(arrow, test_result)
        group.next_to(creature, RIGHT, aligned_edge = UP)
        return group

    def get_positive_result(self, creature):
        return self.get_result(creature, "Diseased", SICKLY_GREEN)

    def get_negative_result(self, creature):
        return self.get_result(creature, "Healthy", GREEN)

    def get_test_arrow(self):
        arrow = Arrow(
            LEFT, RIGHT, 
            color = WHITE,
        )
        word = OldTexText("Test")
        word.scale(0.8)
        word.next_to(arrow, UP, buff = 0)
        arrow.add(word)
        return arrow

    def create_pi_creature(self):
        randy = Randolph()
        randy.next_to(ORIGIN, LEFT)
        return randy


class TestNonDiseaseCase(TestScene):
    def construct(self):
        randy = self.pi_creature
        randy.change_mode("happy")
        randy.next_to(ORIGIN, LEFT)
        result = self.get_negative_result(randy)
        accuracy = OldTexText("99\\% Accuracy")
        accuracy.next_to(VGroup(randy, result), UP)
        accuracy.to_edge(UP)

        all_creatures = VGroup(*[
            VGroup(*[
                randy.copy()
                for y in range(10)
            ]).arrange(DOWN)
            for y in range(10)
        ]).arrange(RIGHT)
        all_creatures.set_height(6)
        all_creatures.to_corner(DOWN+LEFT)
        last_guy = all_creatures[-1][-1]
        rect = SurroundingRectangle(last_guy, buff = 0)
        rect.set_color(YELLOW)

        self.add(randy, accuracy)
        self.play(FadeIn(result[0]))
        self.play(Write(result[1]))
        self.play(Blink(randy))
        self.play(
            ReplacementTransform(randy, all_creatures[0][0]),
            LaggedStartMap(FadeIn, all_creatures, run_time = 2),
            FadeOut(result)
        )
        self.play(ShowCreation(rect))
        self.play(
            last_guy.set_height, 2,
            last_guy.next_to, all_creatures, RIGHT
        )
        result = self.get_positive_result(last_guy)
        false_positive = OldTexText("False positive")
        false_positive.scale(0.8)
        false_positive.next_to(result, UP, LARGE_BUFF)
        false_positive.to_edge(RIGHT)
        arrow = Arrow(
            false_positive.get_bottom(), result[1].get_top(),
            buff = SMALL_BUFF
        )
        self.play(FadeIn(result))
        self.play(
            FadeIn(false_positive),
            ShowCreation(arrow),
            last_guy.change, "confused", result,
        )
        for x in range(2):
            self.play(Blink(last_guy))
            self.wait(2)
