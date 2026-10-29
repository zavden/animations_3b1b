# ==============================================================================
# Scene:      IndicationOnPhotograph
# Source:     videos/_2024/holograms/supplements.py (lines 79-114)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IndicationOnPhotograph.py IndicationOnPhotograph -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private images from Grant's Dropbox (ContrastWithPhotography.png) replaced with regenerable placeholders
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/ContrastWithPhotography.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
# ==============================================================================

from manim_imports_ext import *

class IndicationOnPhotograph(InteractiveScene):
    def construct(self):
        # Image
        image = ImageMobject("ContrastWithPhotography")
        image.set_height(FRAME_HEIGHT)
        # self.add(image)

        # Dots
        p0 = (-3.82, 2.11, 0.0)
        p1 = (-3.14, 2.17, 0.0)
        p2 = (2.61, 2.82, 0.0)
        p3 = (3.53, 2.24, 0.0)

        dot1 = GlowDot(p0, color=TEAL)
        dot2 = GlowDot(p2, color=TEAL)

        arrow = StrokeArrow(p0, p2, buff=SMALL_BUFF, path_arc=-30 * DEGREES)
        arrow.set_stroke(TEAL)

        self.play(FadeIn(dot1), FlashAround(dot1, stroke_width=5, time_width=2, color=TEAL))
        self.play(
            TransformFromCopy(dot1, dot2, path_arc=-30 * DEGREES),
            ShowCreation(arrow, run_time=2),
        )
        self.play(
            dot1.animate.move_to(p1),
            dot2.animate.move_to(p3),
            arrow.animate.match_points(StrokeArrow(p1, p3, buff=0.1, path_arc=-30 * DEGREES)),
            rate_func=there_and_back,
            run_time=3
        )
        self.play(
            FadeOut(dot1),
            FadeOut(dot2),
            FadeOut(arrow),
        )
