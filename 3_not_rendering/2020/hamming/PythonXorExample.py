# ==============================================================================
# Scene:      PythonXorExample
# Source:     videos/_2020/hamming.py (lines 5494-5495)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl PythonXorExample.py PythonXorExample -w -m --fps 15
#
# Why it does not render:
#   The scene has no code: it is just `class PythonXorExample(ExternallyAnimatedScene): pass`, Grant's marker for a clip animated outside manim (screen capture or recording). `ExternallyAnimatedScene.construct` deliberately raises `Exception("Don't actually run this class.")`, and there is nothing to substitute in the public repo.
# ==============================================================================

from manim_imports_ext import *

class PythonXorExample(ExternallyAnimatedScene):
    pass
