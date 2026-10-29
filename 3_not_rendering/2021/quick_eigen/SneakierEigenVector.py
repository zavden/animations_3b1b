# ==============================================================================
# Scene:      SneakierEigenVector
# Source:     videos/_2021/quick_eigen.py (lines 482-483)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl SneakierEigenVector.py SneakierEigenVector -w -m --fps 15
#
# Why it does not render:
#   The scene has no code: it is just `class SneakierEigenVector(ExternallyAnimatedScene): pass`, Grant's marker for a clip animated outside manim (its video is not in the public repo). `ExternallyAnimatedScene.construct` deliberately raises `Exception("Don't actually run this class.")` and there is nothing to substitute.
# ==============================================================================

from manim_imports_ext import *

class SneakierEigenVector(ExternallyAnimatedScene):
    pass
