# ==============================================================================
# Scene:      SwapConstantForFourth
# Source:     videos/_2021/shadows.py (lines 5808-5827)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SwapConstantForFourth.py SwapConstantForFourth -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_overline(mob):
    overline = Underline(mob).next_to(mob, UP, buff=0.05)
    overline.set_stroke(WHITE, 2)
    return overline


def get_key_result(solid_name, color=BLUE):
    eq = OldTex(
        "\\text{Area}\\big(\\text{Shadow}(\\text{" + solid_name + "})\\big)",
        "=",
        "\\frac{1}{2}", "{c}", "\\cdot",
        "(\\text{Surface area})",
        tex_to_color_map={
            "\\text{Shadow}": GREY_B,
            f"\\text{{{solid_name}}}": color,
            "\\text{Solid}": BLUE,
            "{c}": RED,
        }
    )
    eq.add_to_back(get_overline(eq[:5]))
    return eq


class SwapConstantForFourth(Scene):
    def construct(self):
        eq = get_key_result("Dodecahedron")
        eq.to_edge(UP)
        parts = VGroup(
            eq.get_part_by_tex("frac"),
            eq.get_part_by_tex("{c}")
        )
        fourth = OldTex("\\frac{1}{4}")
        fourth.move_to(parts, LEFT)
        fourth.set_color(RED)

        self.add(eq)
        self.wait()
        self.play(
            FadeOut(parts, UP),
            FadeIn(fourth, UP),
            eq.slice_by_tex("\\cdot").animate.next_to(fourth, RIGHT),
        )
        self.wait()
