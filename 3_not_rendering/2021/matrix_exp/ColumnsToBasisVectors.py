# ==============================================================================
# Scene:      ColumnsToBasisVectors
# Source:     videos/_2021/matrix_exp.py (lines 4150-4151)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl ColumnsToBasisVectors.py ColumnsToBasisVectors -w -m --fps 15
#
# Why it does not render:
#   It is an ExternallyAnimatedScene: in the original the class is just a marker (body `pass`; its construct raises 'Don't actually run this class') because the animation (a clip with the matrix columns carried to the basis vectors) was made outside manim and is not in the repo; there is no code to render and no way to substitute it.
# ==============================================================================

from manim_imports_ext import *

class ColumnsToBasisVectors(ExternallyAnimatedScene):
    pass
