# ==============================================================================
# Scene:      ThumbnailOverlay
# Source:     videos/_2018/quaternions.py (lines 6400-6427)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThumbnailOverlay.py ThumbnailOverlay -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL Arrow has no separate head to rescale; a thicker stroke gives the same bigger-head look
# ==============================================================================

from manim_imports_ext import *

class ThumbnailOverlay(Scene):
    def construct(self):
        title = OldTexText("Quaternions \\\\", "visualized")
        title.set_width(7)
        # title[1].scale(0.7, about_edge=UP)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        v_line = Line(DOWN, UP)
        v_line.set_height(FRAME_HEIGHT)

        title.set_background_stroke(color=BLACK, width=1)

        for part in (title[0][4:6], title[1][4:5]):
            rect = BackgroundRectangle(part)
            rect.set_fill(opacity=1)
            rect.stretch(0.9, 0)
            rect.stretch(1.1, 1)
            title.add_to_back(rect)
        # title.add_to_back(BackgroundRectangle(title[0]))

        arrow = Arrow(LEFT, RIGHT)
        arrow.scale(1.5)
        # CHANGE: GL Arrow has no separate head to rescale; a thicker stroke gives the same bigger-head look
        arrow.set_stroke(width=14)
        arrow.set_stroke(width=10)
        arrow.set_color(YELLOW)

        self.add(v_line)
        self.add(arrow)
        self.add(title)
