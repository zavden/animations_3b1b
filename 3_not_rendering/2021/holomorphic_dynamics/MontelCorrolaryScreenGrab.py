# ==============================================================================
# Scene:      MontelCorrolaryScreenGrab
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3184-3185)
# Category:   3 · Does not render
# Includes code copied from: _2021/newton_fractal.py
#
# Run from this folder:
#     manimgl MontelCorrolaryScreenGrab.py MontelCorrolaryScreenGrab -w -m --fps 15
#
# Why it does not render:
#   The scene has no code: it is just `class MontelCorrolaryScreenGrab(ExternallyAnimatedScene): pass`, Grant's marker for a screen capture animated outside manim. `ExternallyAnimatedScene.construct` deliberately raises `Exception("Don't actually run this class.")`, and there is nothing to substitute in the public repo.
# ==============================================================================

from manim_imports_ext import *


# ----- From _2021/newton_fractal.py -----

class MontelCorrolaryScreenGrab(Scene):
    def construct(self):
        pass



# ----- From _2021/holomorphic_dynamics.py -----

class MontelCorrolaryScreenGrab(ExternallyAnimatedScene):
    pass
