# ==============================================================================
# Scene:      MandelbrotFunctions
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2163-2171)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MandelbrotFunctions.py MandelbrotFunctions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MandelbrotFunctions(Scene):
    def construct(self):
        kw = {"tex_to_color_map": {"c": YELLOW}}
        group = VGroup(
            OldTex("f(z) = z^2 + c", **kw),
            OldTex("f'(z) = 2z"),
        )
        group.arrange(DOWN, aligned_edge=LEFT)
        self.add(group)
