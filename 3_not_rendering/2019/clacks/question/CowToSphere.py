# ==============================================================================
# Scene:      CowToSphere
# Source:     videos/_2019/clacks/question.py (lines 630-631)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl CowToSphere.py CowToSphere -w -m --fps 15
#
# Why it does not render:
#   External video placeholder: the source only contains pass over ExternallyAnimatedScene, whose construct intentionally raises "Don't actually run this class.". The animation and the external video that would have to be inserted are not provided.
# ==============================================================================

from manim_imports_ext import *

class CowToSphere(ExternallyAnimatedScene):
    pass
