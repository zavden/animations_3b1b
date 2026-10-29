# ==============================================================================
# Scene:      DirectInterpretationOfDsDt
# Source:     videos/_2017/eoc/chapter8.py (lines 1757-1793)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl DirectInterpretationOfDsDt.py DirectInterpretationOfDsDt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

DISTANCE_COLOR = BLUE


TIME_COLOR = YELLOW


VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter8.py -----

class DirectInterpretationOfDsDt(TeacherStudentsScene):
    def construct(self):
        equation = OldTex("{ds", "\\over\\,", "dT}", "(T)", "=", "v(T)")
        ds, over, dt, of_T, equals, v = equation
        equation.next_to(self.get_pi_creatures(), UP, LARGE_BUFF)
        equation.shift(RIGHT)
        v.set_color(VELOCITY_COLOR)

        s_words = OldTexText("Tiny change in", "distance")
        s_words.next_to(ds, UP+LEFT, LARGE_BUFF)
        s_words.shift_onto_screen()
        s_arrow = Arrow(s_words[1].get_bottom(), ds.get_left())
        s_words.add(s_arrow)
        s_words.set_color(DISTANCE_COLOR)

        t_words = OldTexText("Tiny change in", "time")
        t_words.next_to(dt, DOWN+LEFT)
        t_words.to_edge(LEFT)
        t_arrow = Arrow(t_words[1].get_top(), dt.get_left())
        t_words.add(t_arrow)
        t_words.set_color(TIME_COLOR)

        self.add(ds, over, dt, of_T)
        for words, part in (s_words, ds), (t_words, dt):
            self.play(
                FadeIn(
                    words, 
                    run_time = 2,
                    lag_ratio = 0.5,
                ),
                self.students[1].change_mode, "raise_right_hand"
            )
            self.play(part.set_color, words.get_color())
        self.wait()
        self.play(Write(VGroup(equals, v)))
        self.play_student_changes(*["pondering"]*3)
        self.wait(3)
