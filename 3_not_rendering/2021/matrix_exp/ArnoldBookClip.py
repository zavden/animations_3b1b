# ==============================================================================
# Scene:      ArnoldBookClip
# Source:     videos/_2021/matrix_exp.py (lines 133-134)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl ArnoldBookClip.py ArnoldBookClip -w -m --fps 15
#
# Why it does not render:
#   It is an ExternallyAnimatedScene: in the original the class is just a marker (it inherits from ExternallyAnimatedScene, whose construct raises "Don't actually run this class") because the animation (a clip from Arnold's book) was made outside manim and is not in the repo; there is no code to render and no way to substitute it.
# ==============================================================================

from manim_imports_ext import *

class ArnoldBookClip(ExternallyAnimatedScene):
    pass
