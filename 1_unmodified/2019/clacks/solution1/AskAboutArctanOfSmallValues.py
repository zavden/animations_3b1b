# ==============================================================================
# Scene:      AskAboutArctanOfSmallValues
# Source:     videos/_2019/clacks/solution1.py (lines 2463-2517)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutArctanOfSmallValues.py AskAboutArctanOfSmallValues -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutArctanOfSmallValues(TeacherStudentsScene):
    def construct(self):
        self.add_title()

        equation1 = OldTex(
            "\\arctan", "(", "x", ")", "\\approx", "x"
        )
        equation1.set_color_by_tex("arctan", YELLOW)
        equation2 = OldTex(
            "x", "\\approx", "\\tan", "(", "x", ")",
        )
        equation2.set_color_by_tex("tan", BLUE)
        for mob in equation1, equation2:
            mob.move_to(self.hold_up_spot, DOWN)

        self.play(
            FadeInFromDown(equation1),
            self.teacher.change, "raise_right_hand",
            self.change_students(
                "erm", "sassy", "confused"
            )
        )
        self.look_at(3 * UL)
        self.play(equation1.shift, UP)
        self.play(
            TransformFromCopy(
                VGroup(*[equation1[i] for i in (2, 4, 5)]),
                VGroup(*[equation2[i] for i in (0, 1, 4)]),
            )
        )
        self.play(
            TransformFromCopy(
                VGroup(*[equation1[i] for i in (0, 1, 3)]),
                VGroup(*[equation2[i] for i in (2, 3, 5)]),
            ),
            self.change_students(
                "confused", "erm", "sassy",
            ),
        )
        self.look_at(3 * UL)
        self.wait(3)
        # self.student_says("Why?", target_mode="maybe")
        # self.wait(3)

    def add_title(self):
        title = OldTexText("For small $x$")
        subtitle = OldTexText("(e.g. $x = 0.001$)")
        subtitle.scale(0.75)
        subtitle.next_to(title, DOWN)
        title.add(subtitle)
        # title.scale(1.5)
        # title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.move_to(self.hold_up_spot)
        title.to_edge(UP)
        self.add(title)
