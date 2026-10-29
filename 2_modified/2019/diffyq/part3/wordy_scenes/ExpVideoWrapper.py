# ==============================================================================
# Scene:      ExpVideoWrapper
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 337-359)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExpVideoWrapper.py ExpVideoWrapper -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class ExpVideoWrapper(Scene):
    def construct(self):
        self.add(FullScreenFadeRectangle(
            fill_color=GREY_E,
            fill_opacity=1,
        ))

        screen = ImageMobject("eoc_chapter5_thumbnail")
        screen.set_height(6)
        rect = SurroundingRectangle(screen, buff=0)
        rect.set_stroke(WHITE, 2)
        screen.add(rect)
        title = OldTexText("Need a refresher?")
        title.scale(1.5)
        title.to_edge(UP)
        screen.next_to(title, DOWN)

        screen.center()
        self.play(
            # FadeIn(title, LEFT),
            FadeIn(screen, DOWN),
        )
        self.wait()
