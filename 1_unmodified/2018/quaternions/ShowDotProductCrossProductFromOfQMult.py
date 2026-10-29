# ==============================================================================
# Scene:      ShowDotProductCrossProductFromOfQMult
# Source:     videos/_2018/quaternions.py (lines 4369-4434)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowDotProductCrossProductFromOfQMult.py ShowDotProductCrossProductFromOfQMult -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowDotProductCrossProductFromOfQMult(Scene):
    def construct(self):
        v_tex = "\\vec{\\textbf{v}}"
        product = OldTex(
            "(", "w_1", "+",
            "x_1", "i", "+", "y_1", "j", "+", "z_1", "k", ")"
            "(", "w_2", "+",
            "x_2", "i", "+", "y_2", "j", "+", "z_2", "k", ")",
            "=",
            "(w_1", ",", v_tex + "_1", ")",
            "(w_2", ",", v_tex + "_2", ")",
            "="
        )
        product.set_width(FRAME_WIDTH - 1)

        i1 = product.index_of_part_by_tex("x_1")
        i2 = product.index_of_part_by_tex(")")
        i3 = product.index_of_part_by_tex("x_2")
        i4 = product.index_of_part_by_tex("z_2") + 2
        vector_parts = [product[i1:i2], product[i3:i4]]

        vector_defs = VGroup()
        braces = VGroup()
        for i, vp in zip(it.count(1), vector_parts):
            brace = Brace(vp, UP)
            vector = Matrix([
                ["x_" + str(i)],
                ["y_" + str(i)],
                ["z_" + str(i)],
            ])
            colors = [GREEN, RED, BLUE]
            for mob, color in zip(vector.get_entries(), colors):
                mob.set_color(color)
            group = VGroup(
                OldTex("{}_{} = ".format(v_tex, i)),
                vector,
            )
            group.arrange(RIGHT, SMALL_BUFF)
            group.next_to(brace, UP)

            braces.add(brace)
            vector_defs.add(group)

        result = OldTex(
            "\\left(", "w_1", "w_2",
            "-", v_tex + "_1", "\\cdot", v_tex, "_2", ",\\,",
            "w_1", v_tex + "_2", "+", "w_2", v_tex + "_1",
            "+", "{}_1 \\times {}_2".format(v_tex, v_tex),
            "\\right)"
        )
        result.match_width(product)
        result.next_to(product, DOWN, LARGE_BUFF)
        for mob in product, result:
            mob.set_color_by_tex_to_color_map({
                "w": YELLOW,
                "x": GREEN,
                "y": RED,
                "z": BLUE,
            })
            mob.set_color_by_tex(v_tex, WHITE)

        self.add(product)
        self.add(braces)
        self.add(vector_defs)
        self.play(LaggedStartMap(FadeInFromLarge, result))
        self.wait()
