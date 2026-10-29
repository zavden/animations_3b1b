# ==============================================================================
# Scene:      WavingRodLabel
# Source:     videos/_2018/turbulence.py (lines 640-646)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WavingRodLabel.py WavingRodLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WavingRodLabel(Scene):
    def construct(self):
        words = OldTexText(
            "(Waving a small flag \\\\ through the air)"
        )
        self.play(Write(words))
        self.wait()
