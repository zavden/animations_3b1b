# ==============================================================================
# Scene:      OldGigerenzerMaterial
# Source:     videos/_2020/med_test.py (lines 1737-1868)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl OldGigerenzerMaterial.py OldGigerenzerMaterial -w -m --fps 15
#
# Why it does not render:
#   Fragment of Grant's code without definitions: the scene starts by using `prompt`, `clipboard`, `title` and `h_line`, which are created at the end of another scene (GigerenzerSession, med_test.py:1491) and are not in OldGigerenzerMaterial. It is old material discarded from the video; it cannot be reconstructed without inventing the previous scene.
# ==============================================================================

from manim_imports_ext import *

class WomanIcon(SVGMobject):
    CONFIG = {
        "fill_color": GREY_B,
        "stroke_width": 0,
    }

    def __init__(self, **kwargs):
        super().__init__("woman_icon", **kwargs)
        self.remove(self[0])


class OldGigerenzerMaterial(Scene):
    def construct(self):
        # Test sensitivity
        prompt.generate_target()
        prompt.target.set_opacity(0.8)
        prompt.target.match_height(clipboard)
        prompt.target.scale(0.65)
        prompt.target.next_to(clipboard, RIGHT, MED_LARGE_BUFF)

        sensitivity_words = OldTex("90", "\\%", "\\text{ Sensitivity}")
        sensitivity_words.to_edge(UP)

        self.play(
            FadeIn(sensitivity_words),
            FadeOut(title, shift=UP),
            MoveToTarget(prompt),
            ShowCreation(h_line)
        )

        woman = WomanIcon()
        women = VGroup(*[woman.copy() for x in range(100)])
        women.arrange_in_grid(h_buff=2, v_buff=1)
        women.set_height(3)
        women.next_to(sensitivity_words, DOWN)
        women_rect = SurroundingRectangle(women, buff=0.15)
        women_rect.set_stroke(YELLOW, 2)

        with_bc_label = OldTexText(
            "Women\\\\with\\\\breast\\\\cancer",
            font_size=36,
            color=women_rect.get_color()
        )
        with_bc_label.next_to(women_rect, LEFT)

        women.generate_target()
        signs = VGroup()
        for n, woman in enumerate(women.target):
            if n < 90:
                sign = OldTex("+", color=GREEN)
                woman.set_color(GREEN)
            else:
                sign = OldTex("-", color=RED)
                woman.set_color(RED)
            sign.match_width(woman)
            sign.move_to(woman.get_corner(UR), LEFT)
            signs.add(sign)

        self.play(
            FadeIn(women_rect),
            FadeIn(with_bc_label),
            FadeIn(women, lag_ratio=0.01),
        )
        self.wait()
        self.play(
            MoveToTarget(women),
            FadeIn(signs, lag_ratio=0.01)
        )
        self.wait()

        sens_group = VGroup(
            sensitivity_words,
            with_bc_label,
            women_rect,
            women,
            signs
        )

        # Specificity
        specificity_words = OldTex("91", "\\%", "\\text{ Specificity}")
        specificity_words.move_to(sensitivity_words)
        spec_women = women.copy()
        spec_women.set_fill(GREY_C)
        spec_rect = women_rect.copy()
        spec_rect.set_color(interpolate_color(GREY_BROWN, WHITE, 0.5))
        wo_bc_label = OldTexText(
            "Women\\\\ \\emph{without} \\\\breast\\\\cancer",
            font_size=36,
        )
        wo_bc_label.next_to(spec_rect, LEFT)
        wo_bc_label.match_color(spec_rect)

        spec_group = VGroup(
            specificity_words,
            wo_bc_label,
            spec_rect,
            spec_women,
        )
        spec_group.next_to(ORIGIN, RIGHT, buff=1)
        spec_group.to_edge(UP)

        self.play(
            sens_group.next_to, ORIGIN, LEFT, {"buff": 2},
            sens_group.to_edge, UP,
            FadeIn(spec_group, shift=RIGHT),
        )
        self.wait()

        spec_women.generate_target()
        spec_signs = VGroup()
        for n, woman in enumerate(spec_women.target):
            if n < 9:
                sign = OldTex("+", color=GREEN)
                woman.set_color(GREEN)
            else:
                sign = OldTex("-", color=RED)
                woman.set_color(RED)
            sign.match_width(woman)
            sign.move_to(woman.get_corner(UR), LEFT)
            spec_signs.add(sign)

        self.play(
            MoveToTarget(spec_women),
            FadeIn(spec_signs, lag_ratio=0.01)
        )
        self.wait()
        spec_group.add(spec_signs)

        # False negatives/False positives
        fnr = OldTex(
            "\\leftarrow", "10", "\\%", " \\text{ false negative}",
            font_size=36,
        )
        fnr.next_to(women[-1], RIGHT, buff=0.3)

        fpr = OldTex(
            "9", "\\%", "\\text{ false positive}", "\\rightarrow",
            font_size=36,
        )
        fpr.next_to(spec_women[0], LEFT, buff=0.3)

        self.play(FadeIn(fnr, shift=0.2 * RIGHT, scale=2))
        self.play(FadeIn(fpr, shift=0.2 * LEFT, scale=2))
