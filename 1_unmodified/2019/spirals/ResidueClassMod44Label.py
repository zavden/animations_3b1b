# ==============================================================================
# Scene:      ResidueClassMod44Label
# Source:     videos/_2019/spirals.py (lines 2418-2427)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ResidueClassMod44Label.py ResidueClassMod44Label -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ResidueClassMod44Label(Scene):
    def construct(self):
        text = OldTexText(
            "``Residue class mod 44''"
        )
        text.scale(2)
        text.to_corner(UL)

        self.play(Write(text))
        self.wait()
