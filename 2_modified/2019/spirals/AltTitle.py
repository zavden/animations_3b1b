# ==============================================================================
# Scene:      AltTitle
# Source:     videos/_2019/spirals.py (lines 196-225)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AltTitle.py AltTitle -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class AltTitle(Scene):
    def construct(self):
        title_text = """
            How pretty but pointless patterns\\\\
            in polar plots of primes\\\\
            prompt pretty important ponderings\\\\
            on properties of those primes.
        """
        words = [w + " " for w in title_text.split(" ") if w]
        title = OldTexText(*words)
        title.set_width(FRAME_WIDTH - 1)

        title[2:5].set_color(TEAL)
        title[12:15].set_color(YELLOW)
        title.set_stroke(BLACK, 5, background=True)

        image = ImageMobject("PrimeSpiral")
        image.set_height(FRAME_HEIGHT)
        rect = FullScreenFadeRectangle(fill_opacity=0.25)

        self.add(image, rect)

        for word in title:
            self.play(
                FadeIn(
                    word, run_time=0.05 * len(word),
                    lag_ratio=0.4,
                )
            )
        self.wait()
