# ==============================================================================
# Scene:      ASecondIntegralSensation
# Source:     videos/_2017/eoc/chapter9.py (lines 1943-2009)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ASecondIntegralSensation.py ASecondIntegralSensation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ASecondIntegralSensation(TeacherStudentsScene):
    def construct(self):
        finite_average = OldTex("{1+5+4+2 \\over 4}")
        numbers = VGroup(*finite_average[0:7:2])
        plusses = VGroup(*finite_average[1:7:2])
        denominator = VGroup(*finite_average[7:])
        finite_average.to_corner(UP+LEFT)
        finite_average.to_edge(LEFT)

        continuum = UnitInterval(
            color = GREY,
            unit_size = 6
        )
        continuum.next_to(finite_average, RIGHT, 2)
        line = Line(continuum.get_left(), continuum.get_right())
        line.set_color(YELLOW)
        arrow = Arrow(DOWN+RIGHT, ORIGIN)
        arrow.next_to(line.get_start(), DOWN+RIGHT, SMALL_BUFF)

        sigma_to_integral = OldTex(
            "\\sum \\Leftrightarrow \\int"
        )
        sigma_to_integral.next_to(
            self.teacher.get_corner(UP+LEFT), UP, MED_LARGE_BUFF
        )

        self.teacher_says(
            "A second integral \\\\ sensation"
        )
        self.play_student_changes(*["erm"]*3)
        self.wait()
        self.play(
            Write(numbers),
            RemovePiCreatureBubble(self.teacher),
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = numbers
        )
        self.play(Write(plusses))
        self.wait()
        self.play(Write(denominator))
        self.wait()

        self.play_student_changes(
            *["confused"]*3,
            look_at = continuum,
            added_anims = [Write(continuum, run_time = 2)]
        )
        self.play(ShowCreation(arrow))
        arrow.save_state()
        self.play(
            arrow.next_to, line.copy().get_end(), DOWN+RIGHT, SMALL_BUFF,
            ShowCreation(line),
            run_time = 2
        )
        self.play(*list(map(FadeOut, [arrow])))
        self.wait(2)
        self.play_student_changes(
            *["pondering"]*3,
            look_at = sigma_to_integral,
            added_anims = [
                Write(sigma_to_integral),
                self.teacher.change_mode, "raise_right_hand"
            ]
        )
        self.wait(3)
