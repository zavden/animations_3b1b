# ==============================================================================
# Scene:      AutQ8
# Source:     videos/_2020/monster.py (lines 2915-2920)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AutQ8.py AutQ8 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AutQ8(Scene):
    def construct(self):
        tex = OldTex("\\text{Aut}(Q_8)", tex_to_color_map={"Q_8": BLUE})
        tex.scale(2)
        self.play(Write(tex))
        self.wait()
