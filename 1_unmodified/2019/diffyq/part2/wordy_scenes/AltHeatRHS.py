# ==============================================================================
# Scene:      AltHeatRHS
# Source:     videos/_2019/diffyq/part2/wordy_scenes.py (lines 495-506)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AltHeatRHS.py AltHeatRHS -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AltHeatRHS(Scene):
    def construct(self):
        formula = OldTex(
            "{\\alpha \\over 2}", "\\Big(",
            "T({x} - 1, {t}) + T({x} + 1, {t})"
            "\\Big)",
            tex_to_color_map={
                "{x}": GREEN,
                "{t}": YELLOW,
            }
        )
        self.add(formula)
