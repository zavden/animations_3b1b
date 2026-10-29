# ==============================================================================
# Scene:      NextVideo
# Source:     videos/_2017/eoc/chapter8.py (lines 2683-2698)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NextVideo.py NextVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NextVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        next_video = series[8]
        integral = OldTex("\\int")
        integral.next_to(next_video, DOWN, LARGE_BUFF)

        self.play(FadeIn(series, lag_ratio = 0.5))
        self.play(
            next_video.set_color, YELLOW,
            next_video.shift, next_video.get_height()*DOWN/2,
            self.teacher.change_mode, "raise_right_hand"
        )
        self.play(Write(integral))
        self.wait(5)
