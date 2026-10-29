# ==============================================================================
# Scene:      KeyResult
# Source:     videos/_2021/shadows.py (lines 5496-5540)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl KeyResult.py KeyResult -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - construct used 'eq' (NameError in the original); changed to eq2, the equation that stays on screen
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


class KeyResult(Scene):
    def construct(self):
        eq1, eq2 = [
            get_key_result(word)
            for word in ("Cube", "Solid")
        ]
        VGroup(eq1, eq2).to_edge(UP)

        self.play(FadeIn(eq1, lag_ratio=0.1))
        self.wait()

        cube_underline = Underline(eq2.get_part_by_tex("Solid"), buff=0.05)
        cube_underline.set_stroke(BLUE, 1)
        general_words = Text("Assume convex", font_size=36)
        general_words.set_color(BLUE)
        general_words.next_to(cube_underline, DOWN, buff=1.0)
        general_words.shift(LEFT)
        general_arrow = Arrow(general_words, cube_underline.get_center(), buff=0.1)

        self.play(
            ShowCreation(cube_underline),
            FadeIn(general_words),
            ShowCreation(general_arrow),
            FadeTransformPieces(eq1, eq2),
        )
        self.wait()

        # CHANGE: `eq` does not exist in construct (NameError in the original); eq2 is used, the equation that stays on screen
        const_rect = SurroundingRectangle(VGroup(
            eq2.get_part_by_tex("frac"),
            eq2.get_part_by_tex("{c}")
        ), buff=SMALL_BUFF)
        const_rect.set_stroke(RED, 1)

        const_words = Text("Universal constant!", font_size=36)
        const_words.set_color(RED)
        const_words.match_y(general_words)
        const_words.set_x(const_rect.get_x() + 1)
        const_arrow = Arrow(const_words, const_rect, buff=0.1)

        self.play(
            ShowCreation(const_rect),
            FadeIn(const_words),
            ShowCreation(const_arrow),
        )
        self.wait()
