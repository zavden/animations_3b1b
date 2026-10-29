# ==============================================================================
# Scene:      AccuracyImage
# Source:     videos/_2020/med_test.py (lines 2211-2228)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AccuracyImage.py AccuracyImage -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AccuracyImage(Scene):
    def construct(self):
        sens = 90
        spec = 91
        stats = VGroup(
            OldTexText("Sensitivity: ", f"{sens}\\%"),
            OldTexText("Specificity: ", f"{spec}\\%"),
        )
        stats.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        for stat, color in zip(stats, [GREEN_B, GREY_B]):
            stat[0].set_color(color)
            stat[1].align_to(stats[0][1], LEFT)

        rect = SurroundingRectangle(stats, buff=0.2)
        rect.set_fill(GREY_E, 1)
        rect.set_stroke(GREY_B, 2)
        stats.add_to_back(rect)
        self.add(stats)
