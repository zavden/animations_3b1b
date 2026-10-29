# ==============================================================================
# Scene:      ReadQuestions
# Source:     videos/_2019/windmill.py (lines 1134-1178)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ReadQuestions.py ReadQuestions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class ReadQuestions(Scene):
    def construct(self):
        background = ImageMobject("AskWhatsOnTest_final_image")
        background.set_height(FRAME_HEIGHT)
        self.add(background)

        lines = SVGMobject("imo_2011_2_underline-01")
        lines.set_width(FRAME_WIDTH - 1)
        lines.move_to(0.1 * DOWN)
        lines.set_stroke(TEAL, 3)

        clump_sizes = [1, 2, 3, 2, 1, 2]
        partial_sums = list(np.cumsum(clump_sizes))
        clumps = VGroup(*[
            lines[i:j]
            for i, j in zip(
                [0] + partial_sums,
                partial_sums,
            )
        ])

        faders = []
        for clump in clumps:
            rects = VGroup()
            for line in clump:
                rect = Rectangle()
                rect.set_stroke(width=0)
                rect.set_fill(TEAL, 0.25)
                rect.set_width(line.get_width() + SMALL_BUFF)
                rect.set_height(0.35, stretch=True)
                rect.move_to(line, DOWN)
                rects.add(rect)

            self.play(
                ShowCreation(clump, run_time=2),
                FadeIn(rects),
                *faders,
            )
            self.wait()
            faders = [
                FadeOut(clump),
                FadeOut(rects),
            ]
        self.play(*faders)
        self.wait()
