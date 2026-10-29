# ==============================================================================
# Scene:      RectConvolutionFacts
# Source:     videos/_2023/convolutions2/continuous.py (lines 2265-2332)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/borwein/main.py
#
# Run from this folder:
#     manimgl RectConvolutionFacts.py RectConvolutionFacts -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex(src, VGroup) -> TransformMatchingShapes when the target is a VGroup of glyphs (i == 2): TransformMatchingTex requires a StringMobject (get_symbol_substrings)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2022/borwein/main.py -----

SUB_ONE_FACTOR = "0.99999999998529"



# ----- From _2023/convolutions2/continuous.py -----

class RectConvolutionFacts(InteractiveScene):
    def construct(self):
        # Equations
        equations = VGroup(
            Tex(R"\text{rect}", "(0)", "=", "1.0"),
            Tex(
                R"\big[",
                R"\text{rect}", "*",
                R"\text{rect}_3",
                R"\big]", "(0)", "=", "1.0"
            ),
            Tex(
                R"\big[",
                R"\text{rect}", "*",
                R"\text{rect}_3", "*",
                R"\text{rect}_5",
                R"\big]", "(0)", "=", "1.0"
            ),
            Tex(R"\vdots"),
            Tex(
                R"\big[",
                R"\text{rect}", "*",
                R"\text{rect}_3", "*", R"\cdots", "*",
                R"\text{rect}_{13}",
                R"\big]", "(0)", "=", "1.0"
            ),
            Tex(
                R"\big[",
                R"\text{rect}", "*",
                R"\text{rect}_3", "*", R"\cdots", "*",
                R"\text{rect}_{13}", "*",
                R"\text{rect}_{15}",
                R"\big]", "(0)", "=", SUB_ONE_FACTOR + R"\dots"
            ),
        )

        for eq in equations:
            eq.set_color_by_tex(R"\text{rect}", BLUE)
            eq.set_color_by_tex("_3", TEAL)
            eq.set_color_by_tex("_5", GREEN)
            eq.set_color_by_tex("_{13}", YELLOW)
            eq.set_color_by_tex("_{15}", RED_B)

        equations.arrange(DOWN, buff=0.75, aligned_edge=RIGHT)
        equations[3].match_x(equations[2][-1])
        equations[-1][:-1].align_to(equations[-2][-2], RIGHT)
        equations[-1][-1].next_to(equations[-1][:-1], RIGHT)
        equations.set_width(FRAME_WIDTH - 4)
        equations.center()

        # Show all (largely copy pasted...)
        self.add(equations[0])
        for i in range(4):
            if i < 3:
                src = equations[i].copy()
            else:
                src = equations[i + 1].copy()

            if i < 2:
                target = equations[i + 1]
            elif i == 2:
                target = VGroup(*equations[i + 1], *equations[i + 2])
            else:
                target = equations[i + 2]
            # CHANGE: TransformMatchingTex now requires a StringMobject (get_symbol_substrings); the target for i == 2 is a VGroup of glyphs
            if i == 2:
                self.play(TransformMatchingShapes(src, target))
            else:
                self.play(TransformMatchingTex(src, target))
            self.wait(0.5)

        self.wait()
