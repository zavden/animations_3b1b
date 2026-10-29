# ==============================================================================
# Scene:      PrintGalleryTitle
# Source:     videos/_2026/print_gallery/supplements.py (lines 5-14)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrintGalleryTitle.py PrintGalleryTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PrintGalleryTitle(InteractiveScene):
    def construct(self):
        group = VGroup(
            Text("The Print Gallery", font_size=72),
            Text("M.C. Escher, 1956").set_fill(GREY_A),
        )
        group.arrange(DOWN)
        group.set_backstroke(BLACK, 2)
        self.play(FadeIn(group, lag_ratio=0.1, run_time=2))
        self.wait()
