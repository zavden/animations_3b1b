# ==============================================================================
# Scene:      MathematicianPlusX
# Source:     videos/_2019/QA_2to21.py (lines 66-74)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MathematicianPlusX.py MathematicianPlusX -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MathematicianPlusX(Scene):
    def construct(self):
        text = OldTexText(
            "Side note:\\\\",
            "``The Mathematician + X''\\\\",
            "would make a great band name.",
        )
        text.set_width(FRAME_WIDTH - 1)
        self.add(text)
