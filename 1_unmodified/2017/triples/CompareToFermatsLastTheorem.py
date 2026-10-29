# ==============================================================================
# Scene:      CompareToFermatsLastTheorem
# Source:     videos/_2017/triples.py (lines 123-176)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareToFermatsLastTheorem.py CompareToFermatsLastTheorem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

A_COLOR = BLUE


B_COLOR = GREEN


C_COLOR = YELLOW


SIDE_COLORS = [A_COLOR, B_COLOR, C_COLOR]


class CompareToFermatsLastTheorem(TeacherStudentsScene):
    def construct(self):
        expressions = [
            OldTex(
                "a", "^%d"%d, "+", "b", "^%d"%d, 
                "=", "c", "^%d"%d
            )
            for d in range(2, 9)
        ]
        for expression in expressions:
            for char, color in zip("abc", SIDE_COLORS):
                expression.set_color_by_tex(char, color)
            expression.next_to(self.get_pi_creatures(), UP, buff = 1.3)
        square_expression = expressions[0]
        low_expression = expressions[1]
        square_expression.to_edge(UP, buff = 1.3)
        top_brace = Brace(square_expression, UP, buff = SMALL_BUFF)
        top_text = top_brace.get_text(
            "Abundant integer solutions", buff = SMALL_BUFF
        )
        low_brace = Brace(low_expression, DOWN, buff = SMALL_BUFF)
        low_text = low_brace.get_text(
            "No integer solutions", buff = SMALL_BUFF
        )
        low_text.set_color(RED)

        self.add(square_expression, top_brace, top_text)
        self.play_student_changes(*["pondering"]*3)
        self.play(self.teacher.change, "happy", run_time = 0)
        self.play(
            ReplacementTransform(
                square_expression.copy(),
                low_expression
            ),
            self.teacher.change_mode, "raise_right_hand",
            *[
                ApplyMethod(pi.change, "confused", expressions[1])
                for pi in self.get_students()
            ]
        )
        self.wait()
        self.play(Transform(low_expression, expressions[2]))
        self.play(
            GrowFromCenter(low_brace),
            FadeIn(low_text),
        )
        self.play_student_changes(
            "sassy", "angry", "erm",
            look_at = low_expression,
            added_anims = [Transform(low_expression, expressions[3])]
        )
        for expression in expressions[4:]:
            self.play(Transform(low_expression, expression))
            self.wait()
