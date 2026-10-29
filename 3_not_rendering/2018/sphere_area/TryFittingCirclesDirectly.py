# ==============================================================================
# Scene:      TryFittingCirclesDirectly
# Source:     videos/_2018/sphere_area.py (lines 334-335)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl TryFittingCirclesDirectly.py TryFittingCirclesDirectly -w -m --fps 15
#
# Why it does not render:
#   External-video marker inherited from ExternallyAnimatedScene: the source only contains pass and its construct raises "Don't actually run this class." on purpose. Grant animated it outside manim; there is nothing to convert without inventing the content.
# ==============================================================================

from manim_imports_ext import *

class TryFittingCirclesDirectly(ExternallyAnimatedScene):
    pass
