# ==============================================================================
# Scene:      ShowRepeatedApplication
# Source:     videos/_2018/alt_calc.py (lines 2555-2670)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowRepeatedApplication.py ShowRepeatedApplication -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

def get_nested_one_plus_one_over_x(n_terms, bottom_term="x"):
    tex = "1+ {1 \\over" * n_terms + bottom_term + "}" * n_terms
    return OldTex(tex, isolate=["1", "\\over", bottom_term])


class ShowRepeatedApplication(Scene):
    CONFIG = {
        "title_color": YELLOW,
    }

    def construct(self):
        self.add_func_title()
        self.show_repeated_iteration()

    def add_func_title(self):
        title = self.title = VGroup(
            OldTex("f(", "x", ")"),
            OldTex("="),
            get_nested_one_plus_one_over_x(1)
        )
        title.arrange(RIGHT)
        title.to_corner(UL)
        title.set_color(self.title_color)

        self.add(title)

    def show_repeated_iteration(self):
        line = VGroup()
        decimal_kwargs = {
            "num_decimal_places": 3,
            "show_ellipsis": True,
        }
        phi = (1 + np.sqrt(5)) / 2

        def func(x):
            return 1.0 + 1.0 / x

        initial_term = DecimalNumber(2.71828, **decimal_kwargs)
        line.add(initial_term)
        last_term = initial_term

        def get_arrow():
            arrow = OldTex("\\rightarrow")
            arrow.stretch(1.5, 0)
            arrow.next_to(line[-1], RIGHT)
            tex = OldTex("f(x)")
            tex.set_color(YELLOW)
            tex.match_width(arrow)
            tex.next_to(arrow, UP, SMALL_BUFF)
            return VGroup(arrow, tex)

        for x in range(2):
            arrow = get_arrow()
            line.add(arrow)

            new_term = DecimalNumber(
                func(last_term.number),
                **decimal_kwargs
            )
            new_term.next_to(arrow[0], RIGHT)
            last_term = new_term
            line.add(new_term)

        line.add(get_arrow())
        line.add(OldTex("\\dots\\dots").next_to(line[-1][0], RIGHT))
        num_phi_mob = DecimalNumber(phi, **decimal_kwargs)
        line.add(num_phi_mob.next_to(line[-1], RIGHT))
        line.move_to(DOWN)

        rects = VGroup(*[
            SurroundingRectangle(mob)
            for mob in (line[0], line[1:-1], line[-1])
        ])
        rects.set_stroke(BLUE, 2)

        braces = VGroup(*[
            Brace(rect, DOWN, buff=SMALL_BUFF)
            for rect in rects
        ])
        braces.set_color_by_gradient(GREEN, YELLOW)
        brace_texts = VGroup(*[
            brace.get_text(text).scale(0.75, about_edge=UP)
            for brace, text in zip(braces, [
                "Arbitrary \\\\ starting \\\\ value",
                "Repeatedly apply $f(x)$",
                "$\\varphi$ \\\\ ``Golden ratio''"
            ])
        ])
        var_phi_mob = brace_texts[2][0]
        var_phi_mob.scale(2, about_edge=UP).set_color(YELLOW)
        brace_texts[2][1:].next_to(var_phi_mob, DOWN, MED_SMALL_BUFF)

        # Animations
        self.add(line[0])
        self.play(
            GrowFromCenter(braces[0]),
            Write(brace_texts[0])
        )
        self.wait()
        self.play(
            GrowFromEdge(line[1], LEFT),
            FadeIn(braces[1]),
            FadeIn(brace_texts[1]),
        )
        self.play(ReplacementTransform(line[0].copy(), line[2]))
        self.wait()

        self.play(GrowFromEdge(line[3], LEFT))
        self.play(ReplacementTransform(line[2].copy(), line[4]))
        self.wait()

        self.play(GrowFromEdge(line[5], LEFT))
        self.play(LaggedStartMap(GrowFromCenter, line[6]))
        self.wait()

        self.play(FadeIn(line[7]))
        self.play(
            GrowFromCenter(braces[2]),
            FadeIn(brace_texts[2]),
        )
        self.wait()
