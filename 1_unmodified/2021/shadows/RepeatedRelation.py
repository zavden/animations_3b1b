# ==============================================================================
# Scene:      RepeatedRelation
# Source:     videos/_2021/shadows.py (lines 5845-5893)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RepeatedRelation.py RepeatedRelation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RepeatedRelation(Scene):
    def construct(self):
        # Relations
        relation = VGroup(
            Text("Average shadow"),
            OldTex("=").rotate(PI / 2),
            OldTex("\\frac{1}{2}", "c", "\\cdot (", "\\text{Surface area}", ")")
        )
        relation[0].set_color(GREY_A)
        relation[2][1].set_color(RED)
        relation[2][3].set_color(BLUE)
        relation.arrange(DOWN)
        relation.scale(0.6)
        repeats = relation.get_grid(1, 4, buff=0.8)
        repeats.to_edge(LEFT, buff=MED_LARGE_BUFF)
        repeats.shift(0.5 * DOWN)

        for repeat in repeats:
            self.play(FadeIn(repeat[0], lag_ratio=0.1))
            self.play(
                Write(repeat[1]),
                FadeIn(repeat[2], 0.5 * DOWN)
            )
        self.wait()

        # Limit
        limit = OldTex(
            "\\lim_{|F| \\to 0}",
            "\\left(", "{\\text{Average shadow}", "\\over ", "\\text{Surface area}}", "\\right)",
            "=", "\\frac{1}{2}", "{c}",
        )
        limit.set_color_by_tex("Average shadow", GREY_A)
        limit.set_color_by_tex("Surface area", BLUE)
        limit.set_color_by_tex("{c}", RED)
        limit.move_to(2.5 * DOWN)
        limit.match_x(repeats)

        new_rhs = OldTex("=", "{\\pi R^2", "\\over", "4\\pi R^2}")
        new_rhs.set_color_by_tex("\\pi R^2", GREY_A)
        new_rhs.set_color_by_tex("4\\pi R^2", BLUE)
        new_rhs.move_to(limit.get_part_by_tex("="), LEFT)

        self.play(Write(limit))
        self.wait()
        self.play(
            limit.slice_by_tex("=").animate.next_to(new_rhs, RIGHT),
            GrowFromCenter(new_rhs)
        )
        self.wait()
