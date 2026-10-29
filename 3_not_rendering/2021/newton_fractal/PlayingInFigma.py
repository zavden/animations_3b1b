# ==============================================================================
# Scene:      PlayingInFigma
# Source:     videos/_2021/newton_fractal.py (lines 640-641)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl PlayingInFigma.py PlayingInFigma -w -m --fps 15
#
# Why it does not render:
#   The scene has no code: it is just `class PlayingInFigma(ExternallyAnimatedScene): pass`, Grant's marker for a clip of Grant playing in Figma (the animation was recorded outside manim). `ExternallyAnimatedScene.construct` deliberately raises `Exception("Don't actually run this class.")`, and there is nothing to substitute in the public repo (neither the video nor the applet).
# ==============================================================================

from manim_imports_ext import *

class PlayingInFigma(ExternallyAnimatedScene):
    pass
