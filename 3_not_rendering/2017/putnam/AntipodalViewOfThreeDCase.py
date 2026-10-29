# ==============================================================================
# Scene:      AntipodalViewOfThreeDCase
# Source:     videos/_2017/putnam.py (lines 1251-1252)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl AntipodalViewOfThreeDCase.py AntipodalViewOfThreeDCase -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - none: category 3 (external video marker, same in Cairo)
#
# Why it does not render:
#   Placeholder for an external video: the class only inherits ExternallyAnimatedScene (body is pass) and its construct raises "Don't actually run this class." on purpose. Grant animated this clip outside manim, so there is nothing to render.
# ==============================================================================

from manim_imports_ext import *

class AntipodalViewOfThreeDCase(ExternallyAnimatedScene):
    pass
