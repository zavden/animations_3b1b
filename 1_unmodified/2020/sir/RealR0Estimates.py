# ==============================================================================
# Scene:      RealR0Estimates
# Source:     videos/_2020/sir.py (lines 2874-2902)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RealR0Estimates.py RealR0Estimates -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RealR0Estimates(Scene):
    def construct(self):
        labels = VGroup(
            OldTexText("COVID-19\\\\", "$R_0 \\approx 2$"),
            OldTexText("1918 Spanish flu\\\\", "$R_0 \\approx 2$"),
            OldTexText("Usual seasonal flu\\\\", "$R_0 \\approx 1.3$"),
        )
        images = Group(
            ImageMobject("COVID-19_Map"),
            ImageMobject("spanish_flu"),
            ImageMobject("Influenza"),
        )
        for image in images:
            image.set_height(3)

        images.arrange(RIGHT, buff=0.5)
        images.to_edge(UP, buff=2)

        for label, image in zip(labels, images):
            label.next_to(image, DOWN)

        for label, image in zip(labels, images):
            self.play(
                FadeIn(image, DOWN),
                FadeIn(label, UP),
            )
            self.wait()

        self.embed()
