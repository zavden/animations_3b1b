# ==============================================================================
# Scene:      IntroduceSpheres
# Source:     videos/_2018/dandelin.py (lines 881-882)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl IntroduceSpheres.py IntroduceSpheres -w -m --fps 15
#
# Why it does not render:
#   Placeholder for an external video inherited from ExternallyAnimatedScene: the source is only `pass` and its construct raises "Don't actually run this class." on purpose. Grant animated it outside manim (the external video is not in the repo), so there is no animation to convert without inventing its content.
# ==============================================================================

from manim_imports_ext import *

class IntroduceSpheres(ExternallyAnimatedScene):
    pass
