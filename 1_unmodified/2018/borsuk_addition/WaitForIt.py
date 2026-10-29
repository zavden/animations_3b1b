# ==============================================================================
# Scene:      WaitForIt
# Source:     videos/_2018/borsuk_addition.py (lines 1084-1090)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl WaitForIt.py WaitForIt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class WaitForIt(Scene):
    def construct(self):
        words = OldTexText("Wait for it", "$\\dots$", arg_separator="")
        words.scale(2)
        self.add(words[0])
        self.play(Write(words[1], run_time=3))
        self.wait()
