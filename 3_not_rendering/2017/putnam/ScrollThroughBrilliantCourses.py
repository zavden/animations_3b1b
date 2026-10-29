# ==============================================================================
# Scene:      ScrollThroughBrilliantCourses
# Source:     videos/_2017/putnam.py (lines 1452-1453)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl ScrollThroughBrilliantCourses.py ScrollThroughBrilliantCourses -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - none: category 3 (external video marker, same in Cairo)
#
# Why it does not render:
#   Placeholder for an external video: the class only inherits ExternallyAnimatedScene (body is pass) and its construct raises "Don't actually run this class." on purpose. Grant animated this clip outside manim, so there is nothing to render.
# ==============================================================================

from manim_imports_ext import *

class ScrollThroughBrilliantCourses(ExternallyAnimatedScene):
    pass
