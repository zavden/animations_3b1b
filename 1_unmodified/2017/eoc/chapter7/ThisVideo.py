# ==============================================================================
# Scene:      ThisVideo
# Source:     videos/_2017/eoc/chapter7.py (lines 25-76)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisVideo.py ThisVideo -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class ThisVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        deriv_videos = VGroup(*series[1:6])
        this_video = series[6]
        integral_videos = VGroup(*series[7:9])
        video_groups = [deriv_videos, this_video, integral_videos]

        braces = list(map(Brace, video_groups))
        deriv_brace, this_brace, integral_brace = braces

        tex_mobs = [
            OldTex(*args)
            for args in [
                ("{df ", " \\over \\, ", " dx}"),
                ("\\lim_{h \\to 0}",),
                ("\\int ", "f(x)", "\\,dx"),
            ]
        ]
        deriv_tex, this_tex, integral_tex = tex_mobs
        for tex_mob, brace in zip(tex_mobs, braces):
            tex_mob.set_color_by_tex("f", GREEN)
            tex_mob.set_color_by_tex("dx", YELLOW)
            tex_mob.next_to(brace, DOWN)
        integral_tex.shift(LARGE_BUFF*RIGHT)

        lim_to_deriv_arrow = Arrow(this_tex, deriv_tex, color = WHITE)

        self.add(series)
        for index in 0, 2:
            videos = video_groups[index]
            brace = braces[index]
            tex_mob = tex_mobs[index]
            self.play(ApplyWave(
                videos,
                direction = DOWN,
            ))
            self.play(
                GrowFromCenter(brace),
                Write(tex_mob, run_time = 2)
            )
        self.play(
            this_video.set_color, YELLOW,
            GrowFromCenter(this_brace),
            self.get_teacher().change_mode, "raise_right_hand",
            self.get_teacher().look_at, this_video
        )
        self.play(Write(this_tex))
        self.wait(2)
        self.play(self.get_teacher().change_mode, "sassy")
        self.wait(2)
