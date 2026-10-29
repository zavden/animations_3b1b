# ==============================================================================
# Scene:      DodecahedronFaceSum
# Source:     videos/_2021/shadows.py (lines 5705-5726)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DodecahedronFaceSum.py DodecahedronFaceSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DodecahedronFaceSum(Scene):
    def construct(self):
        expr = OldTexText(
            "Area(Shadow(Dodecahedron))", "=",
            "$\\displaystyle \\frac{1}{2}$",
            " $\\displaystyle \\sum_{j=1}^{12}$ ",
            "Area(Shadow(Face$_j$))",
            tex_to_color_map={
                "Shadow": GREY_B,
                "Dodecahedron": BLUE_D,
                "Face$_j$": YELLOW,
            }
        )
        expr.to_edge(UP, buff=MED_SMALL_BUFF)

        self.add(expr.slice_by_tex(None, "="))
        self.wait()
        self.play(FadeIn(expr.slice_by_tex("="), shift=0.25 * UP))
        self.wait()
        self.play(FlashAround(expr.get_part_by_tex("frac"), run_time=2))
        self.play(FlashUnder(expr[-5:], run_time=2))
        self.wait(2)
