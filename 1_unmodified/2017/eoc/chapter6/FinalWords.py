# ==============================================================================
# Scene:      FinalWords
# Source:     videos/_2017/eoc/chapter6.py (lines 2563-2613)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FinalWords.py FinalWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FinalWords(TeacherStudentsScene):
    def construct(self):
        words = OldTexText(
            "This is a peek into \\\\",
            "Multivariable", "calculus"
        )
        mvc = VGroup(*words[1:])
        words.set_color_by_tex("Multivariable", YELLOW)
        formula = OldTex("f(x, y) = \\sin(x)y^2")
        formula.next_to(self.get_teacher().get_corner(UP+LEFT), UP)

        self.teacher_says(words)
        self.play_student_changes("erm", "hooray", "sassy")
        self.play(
            FadeOut(self.teacher.bubble),
            FadeOut(VGroup(*words[:1])),
            mvc.to_corner, UP+LEFT,
            self.teacher.change_mode, "raise_right_hand",
            self.teacher.look_at, formula,
            Write(formula, run_time = 2),
        )
        self.play_student_changes("pondering", "confused", "thinking")
        self.wait(3)

        ##Show series
        series = VideoSeries()
        series.to_edge(UP)
        video = series[5]
        lim = OldTex("\\lim_{h \\to 0} \\frac{f(x+h)-f(x)}{h}")
        self.play(
            FadeOut(mvc),
            FadeOut(formula),
            self.teacher.change_mode, "plain",
            FadeIn(
                series, run_time = 2,
                lag_ratio = 0.5,
            ),
        )
        self.play(
            video.set_color, YELLOW,
            video.shift, video.get_height()*DOWN/2
        )
        lim.next_to(video, DOWN)
        self.play(
            Write(lim),
            *it.chain(*[
                [pi.change_mode, "pondering", pi.look_at, lim]
                for pi in self.get_pi_creatures()
            ])
        )
        self.wait(3)
