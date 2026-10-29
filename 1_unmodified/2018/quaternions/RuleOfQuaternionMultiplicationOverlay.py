# ==============================================================================
# Scene:      RuleOfQuaternionMultiplicationOverlay
# Source:     videos/_2018/quaternions.py (lines 5126-5214)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RuleOfQuaternionMultiplicationOverlay.py RuleOfQuaternionMultiplicationOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RuleOfQuaternionMultiplicationOverlay(Scene):
    def construct(self):
        q_mob, times_mob, p_mob = q_times_p = OldTex(
            "q", "\\cdot", "p"
        )
        q_times_p.scale(2)
        q_mob.set_color(MAROON_B)
        p_mob.set_color(YELLOW)
        q_arrow = Vector(DOWN, color=WHITE)
        q_arrow.next_to(q_mob, UP)
        p_arrow = Vector(UP, color=WHITE)
        p_arrow.next_to(p_mob, DOWN)

        q_words = OldTexText("Think of as\\\\ an action")
        q_words.next_to(q_arrow, UP)
        p_words = OldTexText("Think of as\\\\ a point")
        p_words.next_to(p_arrow, DOWN)

        i_mob = OldTex("i")[0]
        i_mob.scale(2)
        i_mob.move_to(q_mob, RIGHT)
        i_mob.set_color(GREEN)

        self.add(q_times_p)
        self.play(
            FadeIn(q_words, UP),
            GrowArrow(q_arrow),
        )
        self.play(
            FadeIn(p_words, DOWN),
            GrowArrow(p_arrow),
        )
        self.wait()
        self.play(*map(FadeOut, [
            q_words, q_arrow,
            p_words, p_arrow,
        ]))
        self.play(
            FadeInFromDown(i_mob),
            FadeOut(q_mob, UP)
        )
        product = VGroup(i_mob, times_mob, p_mob)
        self.play(product.to_edge, UP)

        # Show i products
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
        i_products = VGroup(
            OldTex("i", "\\cdot", "1", "=", "i", **kwargs),
            OldTex("i", "\\cdot", "i", "=", "-1", **kwargs),
            OldTex("i", "\\cdot", "j", "=", "k", **kwargs),
            OldTex("i", "\\cdot", "k", "=", "-j", **kwargs),
        )
        i_products.scale(2)
        i_products.arrange(
            DOWN, buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        i_products.next_to(underline, DOWN, LARGE_BUFF)
        i_products.align_to(i_mob, LEFT)

        self.play(ShowCreation(underline))
        self.wait()
        for i_product in i_products:
            self.play(TransformFromCopy(
                product, i_product[:3]
            ))
            self.wait()
            self.play(TransformFromCopy(
                i_product[:3], i_product[3:],
            ))
            self.wait()

        rect = SurroundingRectangle(
            VGroup(product, i_products),
            buff=0.4
        )
        rect.set_stroke(WHITE, width=5)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
