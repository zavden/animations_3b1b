# ==============================================================================
# Scene:      IntroducingTao
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 34-61)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroducingTao.py IntroducingTao -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses a placeholder image for TerryTaoFieldsMedal (in _lib/assets/raster_images/).
#
# Placeholder assets (not Grant's originals):
#   - TerryTaoFieldsMedal.png (placeholder image in raster_images)
# ==============================================================================

from manim_imports_ext import *

class IntroducingTao(InteractiveScene):
    def construct(self):
        # Add images
        with_erdos = ImageMobject("TerryTaoPaulErdos")
        at_imo = ImageMobject("TerryTaoIMO")
        fields_medal = ImageMobject("TerryTaoFieldsMedal")
        images = Group(with_erdos, at_imo, fields_medal)
        for image in images:
            image.set_height(3)

        images.arrange(RIGHT, buff=1.5)
        images.set_width(FRAME_WIDTH - 1)
        images[1].scale(1.25, about_edge=DOWN)

        labels = VGroup(
            Text("Age 10, with Paul Erdős"),
            Text("Age 13, Gold medal at the\nInternationalMath Olympiad"),
            Text("Age 31, Receiving the\n2006 Fields Medal"),
        )
        for image, label in zip(images, labels):
            label.scale(0.6)
            label.next_to(image, DOWN)
            self.play(
                FadeIn(image, 0.25 * UP, scale=1.2),
                FadeIn(label, lag_ratio=0.1)
            )
            self.wait(0.5)
        self.wait()
