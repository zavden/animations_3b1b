# ==============================================================================
# Scene:      IntersectionOfTwoFields
# Source:     videos/_2017/leibniz.py (lines 4617-4688)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntersectionOfTwoFields.py IntersectionOfTwoFields -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntersectionOfTwoFields(TeacherStudentsScene):
    def construct(self):
        circles = VGroup()
        for vect, color, adj in (LEFT, BLUE, "Algebraic"), (RIGHT, YELLOW, "Analytic"):
            circle = Circle(color = WHITE)
            circle.set_fill(color, opacity = 0.3)
            circle.stretch_to_fit_width(7)
            circle.stretch_to_fit_height(4)
            circle.shift(FRAME_X_RADIUS*vect/3.0 + LEFT)
            title = OldTexText("%s \\\\ number theory"%adj)
            title.scale(0.7)
            title.move_to(circle)
            title.to_edge(UP, buff = SMALL_BUFF)
            circle.next_to(title, DOWN, SMALL_BUFF)
            title.set_color(color)
            circle.title = title
            circles.add(circle)
        new_number_systems = OldTexText(
            "New \\\\ number systems"
        )
        gaussian_integers = OldTexText(
            "e.g. Gaussian \\\\ integers"
        )
        new_number_systems.next_to(circles[0].get_top(), DOWN, MED_SMALL_BUFF)
        new_number_systems.shift(MED_LARGE_BUFF*(DOWN+2*LEFT))
        gaussian_integers.next_to(new_number_systems, DOWN)
        gaussian_integers.set_color(BLUE)
        circles[0].words = VGroup(new_number_systems, gaussian_integers)

        zeta = OldTex("\\zeta(s) = \\sum_{n=1}^\\infty \\frac{1}{n^s}")
        L_function = OldTex(
            "L(s, \\chi) = \\sum_{n=1}^\\infty \\frac{\\chi(n)}{n^s}"
        )
        for mob in zeta, L_function:
            mob.scale(0.8)
        zeta.next_to(circles[1].get_top(), DOWN, MED_LARGE_BUFF)
        zeta.shift(MED_LARGE_BUFF*RIGHT)
        L_function.next_to(zeta, DOWN, MED_LARGE_BUFF)
        L_function.set_color(YELLOW)
        circles[1].words = VGroup(zeta, L_function)

        mid_words = OldTexText("Where\\\\ we \\\\ were")
        mid_words.scale(0.7)
        mid_words.move_to(circles)

        for circle in circles:
            self.play(
                Write(circle.title, run_time = 2),
                DrawBorderThenFill(circle, run_time = 2),
                self.teacher.change_mode, "raise_right_hand"
            )
        self.wait()
        for circle in circles:
            for word in circle.words:
                self.play(
                    Write(word, run_time = 2),
                    self.teacher.change, "speaking",
                    *[
                        ApplyMethod(pi.change, "pondering")
                        for pi in self.get_students()
                    ]
                )
                self.wait()
        self.play(
            Write(mid_words),
            self.teacher.change, "raise_right_hand"
        )
        self.play_student_changes(
            *["thinking"]*3,
            look_at = mid_words
        )
        self.wait(3)
