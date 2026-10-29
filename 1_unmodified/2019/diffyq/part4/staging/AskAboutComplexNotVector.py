# ==============================================================================
# Scene:      AskAboutComplexNotVector
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1156-1198)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutComplexNotVector.py AskAboutComplexNotVector -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutComplexNotVector(Scene):
    def construct(self):
        c_ex = DecimalNumber(
            complex(2, 1),
            num_decimal_places=0
        )
        i_part = c_ex[-1]
        v_ex = IntegerMatrix(
            [[2], [1]],
            bracket_h_buff=SMALL_BUFF,
            bracket_v_buff=SMALL_BUFF,
        )
        group = VGroup(v_ex, c_ex)
        group.scale(1.5)
        # group.arrange(RIGHT, buff=4)
        group.arrange(DOWN, buff=0.9)
        group.to_corner(UL, buff=0.2)

        q1, q2 = questions = VGroup(
            OldTexText("Why not this?").set_color(BLUE),
            OldTexText("Instead of this?").set_color(YELLOW),
        )
        questions.scale(1.5)
        for q, ex in zip(questions, group):
            ex.add_background_rectangle()
            q.add_background_rectangle()
            q.next_to(ex, RIGHT)

        plane = NumberPlane(axis_config={"unit_size": 2})
        vect = Vector([4, 2, 0])

        self.play(
            ShowCreation(plane, lag_ratio=0.1),
            FadeIn(vect),
        )
        for q, ex in zip(questions, group):
            self.play(
                FadeIn(q, LEFT),
                FadeIn(ex)
            )
        self.wait()
        self.play(ShowCreationThenFadeAround(i_part))
        self.wait()
