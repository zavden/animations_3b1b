# ==============================================================================
# Scene:      FlatAtBoundaryWords
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 696-706)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FlatAtBoundaryWords.py FlatAtBoundaryWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FlatAtBoundaryWords(Scene):
    def construct(self):
        words = self.get_bc_words()
        self.play(Write(words))
        self.wait()

    def get_bc_words(self):
        return OldTexText(
            "Flat at boundary\\\\"
            "for all", "${t}$", "$> 0$",
        )
