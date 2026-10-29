# ==============================================================================
# Scene:      ShrinkADime
# Source:     videos/_2025/cosmic_distance/part2.py (lines 1447-1471)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShrinkADime.py ShrinkADime -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses a placeholder coin (Dime.png in _lib/assets/raster_images/); the original photo is private to Grant.
#
# Placeholder assets (not Grant's originals):
#   - Dime.png (generic placeholder coin, in raster_images)
# ==============================================================================

from manim_imports_ext import *

class ShrinkADime(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        plane = NumberPlane(
            (0, 1000, 1),
            (-4, 4),
            background_line_style=dict(stroke_color=BLUE, stroke_width=1),
            faded_line_style=dict(stroke_color=BLUE, stroke_width=0.5, stroke_opacity=0.25),
            faded_line_ratio=0,
        )
        plane.move_to(5 * LEFT, LEFT)
        dime = ImageMobject("Dime")
        dime.set_height(1)
        dime.rotate(90 * DEG, RIGHT).rotate(90 * DEG, IN)
        dime.next_to(5 * LEFT, OUT)

        self.add(plane)
        self.play(
            frame.animate.reorient(-90, 84, 0, (-0.04, 0.01, -0.01), 8.00),
            run_time=2
        )
        self.play(FadeIn(dime, OUT))
        self.wait()
        self.play(dime.animate.next_to(1000 * RIGHT, OUT), run_time=8)
