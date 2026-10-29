# ==============================================================================
# Scene:      DiscontinuousSphereOntoPlaneIn3D
# Source:     videos/_2017/borsuk.py (lines 573-574)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl DiscontinuousSphereOntoPlaneIn3D.py DiscontinuousSphereOntoPlaneIn3D -w -m --fps 15
#
# Why it does not render:
#   Placeholder for an external video inherited from ExternallyAnimatedScene: the source is only `pass` and its construct raises "Don't actually run this class." on purpose. Grant animated it outside manim (the external video is not in the repo), so there is no animation to convert without inventing its content.
# ==============================================================================

from manim_imports_ext import *

class ExternallyAnimatedScene(Scene):
    def construct(self):
        raise Exception("Don't actually run this class.")


class DiscontinuousSphereOntoPlaneIn3D(ExternallyAnimatedScene):
    pass
