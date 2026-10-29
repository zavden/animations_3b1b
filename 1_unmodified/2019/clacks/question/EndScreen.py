# ==============================================================================
# Scene:      EndScreen
# Source:     videos/_2019/clacks/question.py (lines 1528-1562)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EndScreen.py EndScreen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EndScreen(Scene):
    def construct(self):
        width = (475 / 1280) * FRAME_WIDTH
        height = width * (323 / 575)
        video_rect = Rectangle(
            width=width,
            height=height,
        )
        video_rect.shift(UP)
        video_rects = VGroup(*[
            video_rect.copy().set_color(color)
            for color in [BLUE_E, BLUE_C, BLUE_D, GREY_BROWN]
        ])
        for rect in video_rects[1::2]:
            rect.reverse_points()
        video_rect.set_fill(GREY_D, 0.5)
        video_rect.set_stroke(GREY_BROWN, 0.5)
        date = OldTexText(
            "Solution will be\\\\"
            "posted", "1/20/19",
        )
        date[1].set_color(YELLOW)
        date.set_width(video_rect.get_width() - 2 * MED_SMALL_BUFF)
        date.move_to(video_rect)

        handle = OldTexText("@3blue1brown")
        handle.next_to(video_rect, DOWN, MED_LARGE_BUFF)

        self.add(video_rect, date, handle)
        for n in range(10):
            self.play(
                FadeOut(video_rects[(n - 1) % 4]),
                ShowCreation(video_rects[n % 4]),
                run_time=2,
            )
