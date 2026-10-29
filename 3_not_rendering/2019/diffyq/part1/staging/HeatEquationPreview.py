# ==============================================================================
# Scene:      HeatEquationPreview
# Source:     videos/_2019/diffyq/part1/staging.py (lines 279-280)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl HeatEquationPreview.py HeatEquationPreview -w -m --fps 15
#
# Why it does not render:
#   External video placeholder inherited from ExternallyAnimatedScene: the source only contains pass and its construct intentionally raises "Don't actually run this class.". Grant animated it outside manim (the external video does not exist in the repo); there is no animation to convert without inventing its content.
# ==============================================================================

from manim_imports_ext import *

class HeatEquationPreview(ExternallyAnimatedScene):
    pass
