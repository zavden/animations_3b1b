# ==============================================================================
# Scene:      OpenAndCloseAsideOnPdfs
# Source:     videos/_2020/beta/beta3.py (lines 1540-1553)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OpenAndCloseAsideOnPdfs.py OpenAndCloseAsideOnPdfs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OpenAndCloseAsideOnPdfs(Scene):
    def construct(self):
        labels = VGroup(
            OldTexText("$\\langle$", "Aside on", " pdfs", "$\\rangle$"),
            OldTexText("$\\langle$/", "Aside on", " pdfs", "$\\rangle$"),
        )
        labels.set_width(FRAME_WIDTH / 2)
        for label in labels:
            label.set_color_by_tex("pdfs", YELLOW)

        self.play(FadeInFromDown(labels[0]))
        self.wait()
        self.play(Transform(*labels))
        self.wait()
