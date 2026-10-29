# ==============================================================================
# Scene:      DepressingForMedicalTestDesigners
# Source:     videos/_2018/eop/bayes_footnote.py (lines 756-805)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DepressingForMedicalTestDesigners.py DepressingForMedicalTestDesigners -w -m --fps 15
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


class DepressingForMedicalTestDesigners(TestScene):
    def construct(self):
        self.remove(self.pi_creature)
        self.show_99_percent_accuracy()
        self.reject_test()

    def show_99_percent_accuracy(self):
        title = OldTexText("99\\% Accuracy")
        title.to_edge(UP)
        title.generate_target()
        title.target.to_corner(UP+LEFT)

        checks = VGroup(*[
            VGroup(*[
                OldTex("\\checkmark").set_color(GREEN)
                for y in range(10)
            ]).arrange(DOWN)
            for x in range(10)
        ]).arrange(RIGHT)
        cross = OldTex("\\times")
        cross.replace(checks[-1][-1])
        cross.set_color(RED)
        Transform(checks[-1][-1], cross).update(1)
        checks.set_height(6)
        checks.next_to(title, DOWN)
        checks.generate_target()
        checks.target.scale(0.5)
        checks.target.next_to(title.target, DOWN)

        self.add(title)
        self.play(Write(checks))
        self.wait(2)
        self.play(*list(map(MoveToTarget, [title, checks])))

    def reject_test(self):
        randy = self.pi_creature
        randy.to_edge(DOWN)
        result = self.get_positive_result(randy)

        self.play(FadeIn(randy))
        self.play(
            FadeIn(result),
            randy.change_mode, "pondering"
        )
        self.wait()
        self.say(
            "Whatever, I'm 91\\% \\\\ sure that's wrong",
            target_mode = "shruggie"
        )
        self.wait(2)
