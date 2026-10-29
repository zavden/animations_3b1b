# ==============================================================================
# Scene:      EndScreen
# Source:     videos/_2019/bayes/footnote.py (lines 1121-1152)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EndScreen.py EndScreen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EndScreen(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": GREY_E
        }
    }

    def construct(self):
        width = (475 / 1280) * FRAME_WIDTH
        height = width * (323 / 575)
        video_rect = Rectangle(
            width=width,
            height=height,
            fill_color=BLACK,
            fill_opacity=1,
        )
        video_rect.shift(UP)

        date = OldTexText(
            "Solution will be\\\\"
            "posted", "1/20/19",
        )
        date[1].set_color(YELLOW)
        date.set_width(video_rect.get_width() - 2 * MED_SMALL_BUFF)
        date.move_to(video_rect)

        handle = OldTexText("@3blue1brown")
        handle.next_to(video_rect, DOWN, MED_LARGE_BUFF)

        self.add(video_rect, handle)
        self.add(AnimatedBoundary(video_rect))
        self.wait(20)
