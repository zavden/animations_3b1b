# ==============================================================================
# Scene:      ComingUp
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 126-144)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComingUp.py ComingUp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComingUp(Scene):
    CONFIG = {
        "camera_config": {"background_color": GREY_E}
    }

    def construct(self):
        frame = ScreenRectangle(
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=1,
            height=6
        )
        title = OldTexText("Coming up")
        title.scale(1.5)
        title.to_edge(UP)
        frame.next_to(title, DOWN)
        animated_frame = AnimatedBoundary(frame)
        self.add(frame, title, animated_frame)
        self.wait(10)
