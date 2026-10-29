# ==============================================================================
# Scene:      SphereInfo
# Source:     videos/_2021/shadows.py (lines 5766-5797)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SphereInfo.py SphereInfo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SphereInfo(Scene):
    def construct(self):
        kw = {
            "tex_to_color_map": {
                "{c}": RED,
                "=": WHITE,
                "R": BLUE
            },
            "font_size": 36
        }
        shadow = OldTex("\\text{Average shadow area} = \\pi R^2", **kw)
        surface = OldTex("\\text{Surface area} = 4 \\pi R^2", **kw)
        conclusion = OldTex("\\frac{1}{2}", "{c}", "=", "\\frac{1}{4}", **kw)

        eqs = VGroup(shadow, surface, conclusion)
        eqs.arrange(DOWN, buff=MED_LARGE_BUFF)
        for eq in eqs:
            eq.shift(eq.get_part_by_tex("=").get_x() * LEFT)
        eqs.to_corner(UR)

        for eq in eqs[:2]:
            eq[0].set_color(GREY_A)

        for eq in eqs:
            self.play(FadeIn(eq, lag_ratio=0.1))
            self.wait()

        self.play(eqs[2].animate.scale(2, about_edge=UP))
        rect = SurroundingRectangle(eqs[2])
        rect.set_stroke(YELLOW, 2)
        self.play(ShowCreation(rect))
        self.wait()
