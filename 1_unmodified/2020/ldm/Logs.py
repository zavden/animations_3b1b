# ==============================================================================
# Scene:      Logs
# Source:     videos/_2020/ldm.py (lines 903-914)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Logs.py Logs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Logs(Scene):
    def construct(self):
        log = OldTex(
            "&\\text{log}(ab) = \\\\ &\\text{log}(a) + \\text{log}(b)",
            tex_to_color_map={"a": BLUE, "b": YELLOW},
            alignment="",
        )
        
        log.scale(1.5)
        log.set_stroke(BLACK, 5, background=True)

        self.add(log)
