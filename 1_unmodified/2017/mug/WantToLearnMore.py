# ==============================================================================
# Scene:      WantToLearnMore
# Source:     videos/_2017/mug.py (lines 1974-1978)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WantToLearnMore.py WantToLearnMore -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WantToLearnMore(Scene):
    def construct(self):
        text = OldTexText("Want to learn more?")
        self.play(Write(text))
        self.wait()
