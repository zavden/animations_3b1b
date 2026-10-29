# ==============================================================================
# Scene:      ReviewWrapper
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 538-539)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReviewWrapper.py ReviewWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WrapperScene(Scene):
    CONFIG = {
        "title": "Title",
        "shade_of_grey": "#333333"
    }

    def construct(self):
        title = OldTexText(self.title)
        title.scale(1.5)
        title.to_edge(UP)
        big_rect = self.get_big_rect()
        screen_rect = self.get_screen_rect()
        screen_rect.next_to(title, DOWN)

        self.add(big_rect, screen_rect)
        self.play(
            FadeIn(big_rect),
            FadeIn(title, DOWN),
            FadeIn(screen_rect, UP),
        )
        self.wait()

    def get_big_rect(self):
        big_rect = FullScreenFadeRectangle()
        big_rect.set_fill(self.shade_of_grey, 1)
        return big_rect

    def get_screen_rect(self, height=6):
        screen_rect = ScreenRectangle(height=height)
        screen_rect.set_fill(BLACK, 1)
        return screen_rect


class ReviewWrapper(WrapperScene):
    CONFIG = {"title": "To review:"}
