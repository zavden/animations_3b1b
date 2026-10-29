# ==============================================================================
# Scene:      MathExchange
# Source:     videos/_2019/spirals.py (lines 254-255)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl MathExchange.py MathExchange -w -m --fps 15
#
# Why it does not render:
#   External video placeholder inherited from ExternallyAnimatedScene: the source only contains pass and its construct intentionally raises "Don't actually run this class.". It includes neither an animation nor the external video that would be needed; there is no scene to convert without inventing its content.
# ==============================================================================

from manim_imports_ext import *

class MathExchange(ExternallyAnimatedScene):
    pass
