# ==============================================================================
# Scene:      MathAsDesign
# Source:     videos/_2020/med_test.py (lines 299-411)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MathAsDesign.py MathAsDesign -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MathAsDesign(Scene):
    def construct(self):
        # Setup
        design_word = OldTexText("Designed?", font_size=72)
        design_word.to_edge(UP)

        e_formula = OldTex(
            "e", "^{\\pi", "i}", "=", "-1",
            font_size=96,
        )
        e_formula[1].set_color(GREY_B)
        e_formula[2].set_color(YELLOW)
        e_formula[4].set_color(BLUE)

        l_formula = OldTex(
            "\\sum_{n = 0}^{\\infty} \\frac{(-1)^n}{2n + 1} = \\frac{\\pi}{4}",
            font_size=72,
        )

        buff = 1.5
        formulas = VGroup(e_formula, l_formula)
        formulas.arrange(DOWN, buff=buff)
        formulas.next_to(design_word, DOWN, buff=buff)

        original_ly = l_formula.get_y()
        l_formula.center()

        self.play(Write(l_formula, run_time=1))
        self.wait()
        self.play(FadeIn(design_word, 0.2 * UP, scale=1.1))
        self.wait()

        alt_l_formula = VGroup(
            VGroup(
                OldTex("\\pm").set_height(0.8),
                OldTex("k \\text{ odd}", font_size=36)
            ).arrange(DOWN, SMALL_BUFF),
            OldTex("\\frac{1}{k}"),
            OldTex("="),
            VGroup(
                Sector(
                    angle=PI / 2,
                    fill_color=BLUE,
                    fill_opacity=1,
                    stroke_color=WHITE,
                    stroke_width=2,
                ),
                Sector(
                    start_angle=PI / 2, angle=3 * PI / 2,
                    fill_color=GREY_E,
                    fill_opacity=1,
                    stroke_color=WHITE,
                    stroke_width=2,
                ),
            ).set_height(1)
        )
        alt_l_formula.arrange(RIGHT)
        alt_l_formula.match_height(l_formula)
        alt_l_formula.next_to(l_formula.get_center(), RIGHT, LARGE_BUFF)

        self.play(
            l_formula.next_to, l_formula.get_center(), LEFT, LARGE_BUFF,
            FadeIn(alt_l_formula, shift=2 * RIGHT)
        )
        self.wait(2)

        # Euler's formula
        e_formula.next_to(e_formula.get_y() * UP, LEFT, buff=1.5)
        self.play(
            l_formula.scale, 0.7,
            l_formula.set_y, original_ly,
            alt_l_formula.scale, 0.7,
            alt_l_formula.set_y, original_ly,
            FadeIn(e_formula, scale=1.1)
        )

        alt_e_formula = VGroup(
            OldTexText("exp", font_size=96),
            OldTex("(", font_size=96),
            Arrow(0.5 * RIGHT, 0.5 * LEFT, path_arc=PI, buff=0, color=GREY_B),
            Dot(radius=0.05, color=WHITE),
            Vector(0.75 * UP, fill_color=YELLOW),
            OldTex(")", font_size=96),
            OldTex("=", font_size=96),
            Vector(LEFT, fill_color=BLUE),
        )
        alt_e_formula.arrange(RIGHT, buff=MED_SMALL_BUFF)
        alt_e_formula[0].shift(0.15 * RIGHT)
        alt_e_formula[4:].shift(0.15 * LEFT)
        alt_e_formula.scale(0.8)
        alt_e_formula.next_to(e_formula.get_y() * UP, RIGHT, buff=1.0)
        alt_e_formula.shift(0.2 * DOWN)

        anims = []
        for i, j in enumerate([0, 2, 4, 6, 7]):
            src = e_formula[i].copy()
            dst = alt_e_formula[j]
            src.generate_target()
            src.target.replace(dst, stretch=True)
            src.target.set_opacity(0)
            dst.save_state()
            dst.replace(src, stretch=True)
            dst.set_opacity(0)
            anims.append(MoveToTarget(src, remover=True))
            anims.append(Restore(dst))
        anims.extend([
            FadeIn(alt_e_formula[1], shift=0.5 * UP, scale=3),
            FadeIn(alt_e_formula[5], shift=0.5 * UP, scale=3),
            GrowFromPoint(alt_e_formula[3], e_formula[1:3].get_center()),
        ])

        self.play(*anims)
        self.wait()
