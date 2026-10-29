# ==============================================================================
# Scene:      LaterWrapper
# Source:     videos/_2021/matrix_exp.py (lines 277-278)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LaterWrapper.py LaterWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VideoWrapper(Scene):
    title = ""

    def construct(self):
        self.add(FullScreenRectangle())
        screen_rect = ScreenRectangle(height=6)
        screen_rect.set_stroke(BLUE_D, 1)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.to_edge(DOWN)
        self.add(screen_rect)

        title = OldTexText(self.title, font_size=90)
        if title.get_width() > screen_rect.get_width():
            title.set_width(screen_rect.get_width())
        title.next_to(screen_rect, UP)

        self.play(Write(title))
        self.wait()


class LaterWrapper(VideoWrapper):
    title = "Later..."
