# ==============================================================================
# Scene:      NextVideo
# Source:     videos/_2017/eoc/chapter7.py (lines 2836-2881)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NextVideo.py NextVideo -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class NextVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        next_video = series[7]
        brace = Brace(next_video, DOWN)

        integral = OldTex("\\int", "f(x)", "dx")
        ftc = OldTex(
            "F(b)", "-", "F(a)", "=", "\\int_a^b", 
            "{dF", "\\over \\,", "dx}", "(x)", "dx"
        )
        for tex_mob in integral, ftc:
            tex_mob.set_color_by_tex("dx", GREEN)
            tex_mob.set_color_by_tex("f", YELLOW)
            tex_mob.set_color_by_tex("F", YELLOW)
            tex_mob.next_to(brace, DOWN)

        self.add(series)
        self.play(
            GrowFromCenter(brace),
            next_video.set_color, YELLOW,
            self.get_teacher().change_mode, "raise_right_hand",
            self.get_teacher().look_at, next_video
        )
        self.play(Write(integral))
        self.wait(2)
        self.play(*[
            ReplacementTransform(
                VGroup(*integral.get_parts_by_tex(p1)),
                VGroup(*ftc.get_parts_by_tex(p2)),
                run_time = 2,
                path_arc = np.pi/2,
                rate_func = squish_rate_func(smooth, alpha, alpha+0.5)
            )
            for alpha, (p1, p2) in zip(np.linspace(0, 0.5, 3), [
                ("int", "int"),
                ("f", "F"),
                ("dx", "dx"),
            ])
        ]+[
            Write(VGroup(*ftc.get_parts_by_tex(part)))
            for part in ("-", "=", "over", "(x)")
        ])
        self.play_student_changes(*["pondering"]*3)
        self.wait(3)
