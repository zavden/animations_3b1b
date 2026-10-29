# ==============================================================================
# Scene:      ByLine
# Source:     videos/_2021/shadows.py (lines 6578-6590)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ByLine.py ByLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ByLine(Scene):
    def construct(self):
        lines = VGroup(
            OldTexText("Artwork by\\\\", "Kurt Bruns"),
            OldTexText("Music by\\\\", "Vince Rubinetti"),
            OldTexText("Other stuff\\\\", "Grant Sanderson"),
        )
        for line in lines:
            line[0].set_color(GREY_B)
            line[1].scale(1.2, about_edge=UP)

        lines.arrange(DOWN, buff=1.5)
        self.add(lines)
