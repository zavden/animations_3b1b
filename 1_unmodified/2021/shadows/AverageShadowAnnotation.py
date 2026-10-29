# ==============================================================================
# Scene:      AverageShadowAnnotation
# Source:     videos/_2021/shadows.py (lines 2448-2507)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AverageShadowAnnotation.py AverageShadowAnnotation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_overline(mob):
    overline = Underline(mob).next_to(mob, UP, buff=0.05)
    overline.set_stroke(WHITE, 2)
    return overline


class AverageShadowAnnotation(Scene):
    def construct(self):
        # Many shadows
        many_shadows = Text("Many shadows")
        many_shadows.move_to(3 * DOWN)

        self.play(Write(many_shadows))
        self.wait(2)

        # Formula
        # shape_name = "2d shape"
        shape_name = "Square"
        t2c = {
            "Shadow": GREY_B,
            shape_name: BLUE,
            "$c$": RED,
        }
        formula = VGroup(
            OldTexText(
                f"Area(Shadow({shape_name}))",
                tex_to_color_map=t2c,
            ),
            OldTex("=").rotate(PI / 2),
            OldTexText(
                "$c$", " $\\cdot$", f"(Area({shape_name}))",
                tex_to_color_map=t2c
            )
        )
        overline = get_overline(formula[0])
        formula[0].add(overline)
        formula.arrange(DOWN)
        formula.to_corner(UL)

        self.play(FadeTransform(many_shadows, formula[0]))
        self.wait()
        self.play(
            VShowPassingFlash(
                overline.copy().insert_n_curves(100).set_stroke(YELLOW, 5),
                time_width=0.75,
                run_time=2,
            )
        )
        self.wait()
        self.play(
            Write(formula[1]),
            FadeIn(formula[2], DOWN)
        )
        self.wait()

        # Append half
        half = OldTex("\\frac{1}{2}")
        half.set_color(RED)
        c = formula[2].get_part_by_tex("$c$")
        half.move_to(c, RIGHT)

        self.play(
            FadeOut(c, 0.5 * UP),
            FadeIn(half, 0.5 * UP),
        )
        self.wait()
