# ==============================================================================
# Scene:      BayesFactor
# Source:     videos/_2020/med_test.py (lines 3006-3250)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BayesFactor.py BayesFactor -w -m --fps 15
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


class BayesFactor(Scene):
    def construct(self):
        # Test sensitivity
        woman = WomanIcon()
        bc_pop = VGroup(*[woman.copy() for x in range(100)])
        bc_pop.arrange_in_grid(h_buff=1.5, v_buff=1)
        bc_pop.set_height(4)
        bc_pop.next_to(ORIGIN, LEFT, MED_LARGE_BUFF)
        bc_rect = SurroundingRectangle(bc_pop, buff=0.15)
        bc_rect.set_stroke(YELLOW, 2)

        with_bc_label = OldTexText(
            "Patients with\\\\breast cancer",
            font_size=36,
            color=bc_rect.get_color()
        )
        with_bc_label.next_to(bc_rect, UP)

        bc_pop.generate_target()
        bc_signs = VGroup()
        for n, icon in enumerate(bc_pop.target):
            if n < 90:
                sign = OldTex("+", color=GREEN)
                icon.set_color(GREEN)
            else:
                sign = OldTex("-", color=RED)
                icon.set_color(RED)
            sign.match_width(icon)
            sign.move_to(icon.get_corner(UR), LEFT)
            bc_signs.add(sign)

        sens_brace = Brace(bc_pop[:90], LEFT, buff=MED_SMALL_BUFF)
        sens_word = sens_brace.get_text("90\\% Sens.")
        sens_word.set_color(GREEN)
        fnr_brace = Brace(bc_pop[90:], LEFT, buff=MED_SMALL_BUFF)
        fnr_word = fnr_brace.get_text("10\\% FNR")
        fnr_word.set_color(RED_E)

        bc_group = VGroup(
            with_bc_label,
            bc_rect,
            bc_pop,
            bc_signs,
            sens_brace,
            sens_word,
            fnr_brace,
            fnr_word,
        )

        # Specificity (too much copy paste)
        nc_pop = bc_pop.copy()
        nc_pop.next_to(ORIGIN, RIGHT, MED_LARGE_BUFF)
        nc_rect = SurroundingRectangle(nc_pop, buff=0.15)
        nc_rect.set_stroke(GREY_B, 2)

        without_bc_label = OldTexText(
            "Patients without\\\\breast cancer",
            font_size=36,
            color=nc_rect.get_color()
        )
        without_bc_label.next_to(nc_rect, UP)

        nc_pop.generate_target()
        nc_signs = VGroup()
        for n, icon in enumerate(nc_pop.target):
            if 0 < n < 10:
                sign = OldTex("+", color=GREEN)
                icon.set_color(GREEN)
            else:
                sign = OldTex("-", color=RED)
                icon.set_color(RED)
            sign.match_width(icon)
            sign.move_to(icon.get_corner(UR), LEFT)
            nc_signs.add(sign)

        spec_brace = Brace(nc_pop[10:], RIGHT, buff=MED_SMALL_BUFF)
        spec_word = spec_brace.get_text("91\\% Spec.")
        spec_word.set_color(RED)
        fpr_brace = Brace(nc_pop[:10], RIGHT, buff=MED_SMALL_BUFF)
        fpr_word = fpr_brace.get_text("9\\% FPR")
        fpr_word.set_color(GREEN_D)

        nc_group = VGroup(
            without_bc_label,
            nc_rect,
            nc_pop,
            nc_signs,
            spec_brace,
            spec_word,
            fpr_brace,
            fpr_word,
        )

        # Draw groups
        self.play(LaggedStart(
            FadeIn(with_bc_label),
            ShowCreation(bc_rect),
            ShowIncreasingSubsets(bc_pop),
            FadeIn(without_bc_label),
            ShowCreation(nc_rect),
            ShowIncreasingSubsets(nc_pop),
        ))
        self.play(LaggedStart(
            MoveToTarget(bc_pop),
            FadeIn(bc_signs, lag_ratio=0.02),
            GrowFromCenter(sens_brace),
            FadeIn(sens_word, shift=0.2 * LEFT),
            GrowFromCenter(fnr_brace),
            FadeIn(fnr_word, shift=0.2 * LEFT),
        ))
        self.play(LaggedStart(
            MoveToTarget(nc_pop),
            FadeIn(nc_signs, lag_ratio=0.02),
            GrowFromCenter(spec_brace),
            FadeIn(spec_word, shift=0.2 * RIGHT),
            GrowFromCenter(fpr_brace),
            FadeIn(fpr_word, shift=0.2 * RIGHT),
        ))
        self.wait()

        groups = VGroup(bc_group, nc_group)

        # Highlight relevant parts
        fade_rects = VGroup(*(BackgroundRectangle(group) for group in groups))
        fade_rects.set_fill(BLACK, 0.8)

        self.play(FadeIn(fade_rects[1]))
        self.play(LaggedStart(*(
            ShowCreationThenFadeOut(Underline(word))
            for word in [sens_word, fnr_word]
        ), lag_ratio=0.4))
        self.play(
            FadeIn(fade_rects[0]),
            FadeOut(fade_rects[1]),
        )
        self.play(LaggedStart(*(
            ShowCreationThenFadeOut(Underline(word))
            for word in [spec_word, fpr_word]
        ), lag_ratio=0.4))
        self.wait()
        self.play(FadeOut(fade_rects[0]))

        # None of these are your answer
        title = OldTex(
            "\\text{None of these tell you }",
            "P(\\text{Cancer} \\,|\\, +)",
            tex_to_color_map={
                "\\text{Cancer}": YELLOW,
                "+": GREEN,
            },
            font_size=72,
        )
        title.to_edge(UP)
        title_underline = Underline(title)

        self.play(
            FadeIn(title, lag_ratio=0.1),
            groups.to_edge, DOWN,
        )
        self.play(ShowCreation(title_underline))
        self.wait()
        title.add(title_underline)

        # Ask about update strength
        question = OldTexText("How strongly\\\\does it update?")
        question.set_height(1)
        question.to_corner(UL)
        question.save_state()
        question.replace(title, 1)
        question.set_opacity(0)

        self.play(
            Restore(question),
            title.replace, question.saved_state, 0,
            title.set_opacity, 0,
        )
        self.remove(title)
        self.wait()

        # Write Bayes factor
        frac = VGroup(
            sens_word.copy(),
            OldTex("\\qquad \\over \\qquad"),
            fpr_word.copy(),
        )
        frac[1].match_width(frac[0], stretch=True)
        frac.arrange(DOWN, SMALL_BUFF)
        frac.next_to(question, RIGHT, LARGE_BUFF)

        mid_rhs = OldTex(
            "= {P(+ \\,|\\, \\text{Cancer}) \\over P(+ \\,|\\, \\text{No cancer})}",
            tex_to_color_map={
                "+": GREEN,
                "\\text{Cancer}": YELLOW,
                "\\text{No cancer}": GREY_B,
            }
        )
        mid_rhs.next_to(frac, RIGHT)

        rhs = OldTex("= 10", font_size=72)
        rhs.next_to(mid_rhs, RIGHT)

        for part in frac[0::2]:
            part.save_state()
        frac[0].replace(sens_word)
        frac[2].replace(fpr_word)

        s_rect = SurroundingRectangle(frac[0])
        self.play(ShowCreation(s_rect))
        self.play(
            Restore(frac[0]),
            s_rect.move_to, frac[0].saved_state,
            s_rect.set_opacity, 0,
            Write(frac[1]),
            Restore(frac[2]),
        )
        self.wait(2)
        self.play(Write(mid_rhs))
        self.wait()
        self.play(Write(rhs))
        self.wait()

        # Name the Bayes factor
        bf_name = OldTexText("Bayes\\\\Factor ", font_size=72)
        equals = OldTex("=", font_size=72).next_to(frac, LEFT)
        bf_name.next_to(equals, LEFT)
        lr_name = OldTexText("Likelihood\\\\ratio")
        lr_name.next_to(equals, LEFT)

        self.play(
            FadeOut(question, UP),
            FadeIn(bf_name, UP),
            FadeIn(equals, UP),
        )
        self.wait()
        self.play(
            FadeOut(bf_name, UP),
            FadeIn(lr_name, UP),
        )
        self.wait()
        self.play(
            FadeIn(bf_name, DOWN),
            FadeOut(lr_name, DOWN),
        )
        self.wait(5)
