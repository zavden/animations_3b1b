# ==============================================================================
# Scene:      JMultiplicationChart
# Source:     videos/_2018/quaternions.py (lines 5637-5689)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JMultiplicationChart.py JMultiplicationChart -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class JMultiplicationChart(Scene):
    def construct(self):
        # Largely copy-pasted....what are you gonna do about it?
        product = OldTex("j", "\\cdot", "p")
        product[0].set_color(RED)
        product.scale(2)
        product.to_edge(UP)

        underline = Line(LEFT, RIGHT)
        underline.set_width(product.get_width() + MED_SMALL_BUFF)
        underline.next_to(product, DOWN)

        kwargs = {
            "tex_to_color_map": {
                "i": GREEN,
                "j": RED,
                "k": BLUE
            }
        }
        j_products = VGroup(
            OldTex("j", "\\cdot", "1", "=", "j", **kwargs),
            OldTex("j", "\\cdot", "j", "=", "-1", **kwargs),
            OldTex("j", "\\cdot", "i", "=", "-k", **kwargs),
            OldTex("j", "\\cdot", "k", "=", "i", **kwargs),
        )
        j_products.scale(2)
        j_products.arrange(
            DOWN, buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        j_products.next_to(underline, DOWN, LARGE_BUFF)
        j_products.align_to(product, LEFT)

        self.play(FadeInFromDown(product))
        self.play(ShowCreation(underline))
        self.wait()
        for j_product in j_products:
            self.play(TransformFromCopy(
                product, j_product[:3]
            ))
            self.wait()
            self.play(TransformFromCopy(
                j_product[:3], j_product[3:],
            ))
            self.wait()

        rect = SurroundingRectangle(
            VGroup(product, j_products),
            buff=MED_SMALL_BUFF
        )
        rect.set_stroke(WHITE, width=5)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
