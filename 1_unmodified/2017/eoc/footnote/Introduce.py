# ==============================================================================
# Scene:      Introduce
# Source:     videos/_2017/eoc/footnote.py (lines 13-61)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Introduce.py Introduce -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Introduce(TeacherStudentsScene):
    def construct(self):
        words = OldTexText("Next up is \\\\", "Taylor series")
        words.set_color_by_tex("Taylor", BLUE)
        derivs = VGroup(*[
            OldTex(
                "{d", "^%d"%n, "f \\over dx", "^%d}"%n
            ).set_color_by_tex(str(n), YELLOW)
            for n in range(2, 5)
        ])
        derivs.next_to(self.teacher, UP, LARGE_BUFF)
        second_deriv = derivs[0]
        second_deriv.save_state()
        card_dot = Dot(radius = SMALL_BUFF)
        screen_rect = ScreenRectangle(height = 4)
        screen_rect.move_to(3*UP, UP)

        self.teacher_says(words, run_time = 2)
        taylor_series = words.get_part_by_tex("Taylor").copy()
        self.play_student_changes(*["happy"]*3)
        self.play(
            RemovePiCreatureBubble(
                self.teacher,
                target_mode = "raise_right_hand"
            ),
            taylor_series.next_to, screen_rect.copy(), UP,
            ShowCreation(screen_rect)
        )
        card_dot.move_to(taylor_series)
        card_dot.generate_target()
        card_dot.target.set_fill(opacity = 0)
        card_dot.target.to_edge(RIGHT, buff = MED_SMALL_BUFF)
        arrow = Arrow(
            taylor_series, card_dot.target,
            buff = MED_SMALL_BUFF,
            color = WHITE
        )
        self.play(FadeIn(second_deriv))
        self.wait(2)
        self.play(Transform(second_deriv, derivs[1]))
        self.wait(2)
        self.play(MoveToTarget(card_dot))
        self.play(ShowCreation(arrow))
        self.wait()
        self.play(Transform(second_deriv, derivs[2]))
        self.play_student_changes(*["erm"]*3)
        self.wait()
        self.play(second_deriv.restore)
        self.wait(2)
