# ==============================================================================
# Scene:      FermatsDreamExcerptWrapper
# Source:     videos/_2017/leibniz.py (lines 382-390)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FermatsDreamExcerptWrapper.py FermatsDreamExcerptWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FermatsDreamExcerptWrapper(Scene):
    def construct(self):
        words = OldTexText(
            "From ``Fermat's dream'' by Kato, Kurokawa and Saito"
        )
        words.scale(0.8)
        words.to_edge(UP)
        self.add(words)
        self.wait()
