# ==============================================================================
# Scene:      SimpleRect
# Source:     videos/_2023/moser_reboot/main.py (lines 597-604)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRect.py SimpleRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleRect(InteractiveScene):
    def construct(self):
        self.play(FlashAround(
            Tex("1.2.3.4").scale(2),
            time_width=1.5,
            run_time=3,
            stroke_width=8,
        ))
