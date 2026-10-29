# ==============================================================================
# Scene:      NextVideo
# Source:     videos/_2017/eoc/chapter3.py (lines 2691-2729)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NextVideo.py NextVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NextVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        next_video = series[3]
        series.to_edge(UP)

        d_sum = OldTex("\\frac{d}{dx}(x^3 + x^2)")
        d_product = OldTex("\\frac{d}{dx} \\sin(x)x^2")
        d_composition = OldTex("\\frac{d}{dx} \\cos\\left(\\frac{1}{x}\\right)")

        group = VGroup(d_sum, d_product, d_composition)
        group.arrange(RIGHT, buff = 2*LARGE_BUFF)
        group.next_to(VGroup(*self.get_pi_creatures()), UP, buff = LARGE_BUFF)

        self.play(
            FadeIn(
                series,
                lag_ratio = 0.5,
                run_time = 3,
            ),
            *[
                ApplyMethod(pi.look_at, next_video)
                for pi in self.get_pi_creatures()
            ]
        )
        self.play(
            next_video.set_color, YELLOW,
            next_video.shift, MED_LARGE_BUFF*DOWN
        )
        self.wait()
        for mob in group:
            self.play(
                Write(mob, run_time = 1),
                *[
                    ApplyMethod(pi.look_at, mob)
                    for pi in self.get_pi_creatures()
                ]
            )
        self.wait(3)
