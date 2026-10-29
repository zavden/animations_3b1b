# ==============================================================================
# Scene:      VortexStretchingLabel
# Source:     videos/_2018/turbulence.py (lines 1547-1551)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VortexStretchingLabel.py VortexStretchingLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VortexStretchingLabel(Scene):
    def construct(self):
        title = OldTexText("Vortex stretching")
        self.play(Write(title))
        self.wait()
