# ==============================================================================
# Scene:      ThisVideo
# Source:     videos/_2017/eoc/chapter8.py (lines 83-122)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl ThisVideo.py ThisVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter8.py -----

class ThisVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        this_video = series[7]
        this_video.save_state()
        next_video = series[8]

        deriv, integral, v_t, dt, equals, v_T = formula = OldTex(
            "\\frac{d}{dT}", 
            "\\int_0^T", "v(t)", "\\,dt", 
            "=", "v(T)"
        )
        formula.set_color_by_tex("v", VELOCITY_COLOR)
        formula.next_to(self.teacher.get_corner(UP+LEFT), UP, MED_LARGE_BUFF)

        self.play(FadeIn(series, lag_ratio = 0.5))
        self.play(
            this_video.shift, this_video.get_height()*DOWN/2,
            this_video.set_color, YELLOW,
            self.teacher.change_mode, "raise_right_hand",
        )
        self.play(Write(VGroup(integral, v_t, dt)))
        self.play_student_changes(*["erm"]*3)
        self.wait()
        self.play(Write(VGroup(deriv, equals, v_T)), )
        self.play_student_changes(*["confused"]*3)
        self.wait(3)
        self.play(
            this_video.restore,
            next_video.shift, next_video.get_height()*DOWN/2,
            next_video.set_color, YELLOW,
            integral[0].copy().next_to, next_video, DOWN, MED_LARGE_BUFF,
            FadeOut(formula),
            *it.chain(*[
                [pi.change_mode, "plain", pi.look_at, next_video]
                for pi in self.pi_creatures
            ])
        )
        self.wait(2)
