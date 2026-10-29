# ==============================================================================
# Scene:      QuinticAppletPlay
# Source:     videos/_2021/newton_fractal.py (lines 1398-1399)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl QuinticAppletPlay.py QuinticAppletPlay -w -m --fps 15
#
# Why it does not render:
#   The scene has no code: it is just `class QuinticAppletPlay(ExternallyAnimatedScene): pass`, Grant's marker for a recording of the interactive quintic applet (made outside manim). `ExternallyAnimatedScene.construct` deliberately raises `Exception("Don't actually run this class.")`, and there is nothing to substitute in the public repo (neither the video nor the applet).
# ==============================================================================

from manim_imports_ext import *

class QuinticAppletPlay(ExternallyAnimatedScene):
    pass
