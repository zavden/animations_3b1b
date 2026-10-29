# ==============================================================================
# Scene:      RAddToRMult
# Source:     videos/_2020/monster.py (lines 2958-2959)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl RAddToRMult.py RAddToRMult -w -m --fps 15
#
# Why it does not render:
#   The scene has no code: it is just `class RAddToRMult(ExternallyAnimatedScene): pass`, Grant's marker for a clip animated outside manim (screen capture or recording). `ExternallyAnimatedScene.construct` deliberately raises `Exception("Don't actually run this class.")`, and there is nothing to substitute in the public repo.
# ==============================================================================

from manim_imports_ext import *

class RAddToRMult(ExternallyAnimatedScene):
    pass
