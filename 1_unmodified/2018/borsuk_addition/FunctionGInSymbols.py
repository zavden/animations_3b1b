# ==============================================================================
# Scene:      FunctionGInSymbols
# Source:     videos/_2018/borsuk_addition.py (lines 391-546)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl FunctionGInSymbols.py FunctionGInSymbols -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class FunctionGInSymbols(Scene):
    def construct(self):
        p_tex = "\\vec{\\textbf{p}}"
        neg_p_tex = "-\\vec{\\textbf{p}}"

        def color_tex(tex_mob):
            pairs = [
                (p_tex, YELLOW),
                (neg_p_tex, RED),
                ("{g}", GREEN),
            ]
            for tex, color in pairs:
                tex_mob.set_color_by_tex(
                    tex, color, substring=False
                )

        f_of_p = OldTex("f", "(", p_tex, ")")
        f_of_p.shift(2.5 * LEFT + 2.5 * UP)
        f_of_neg_p = OldTex("f", "(", neg_p_tex, ")")
        g_of_p = OldTex("g", "(", p_tex, ")")
        g_of_p[0].set_color(YELLOW)
        for mob in f_of_p, f_of_neg_p, g_of_p:
            color_tex(mob)
        dec_rhs = DecimalMatrix([[-0.9], [0.5]])
        dec_rhs.next_to(f_of_p, RIGHT)
        minus = OldTex("-")
        equals = OldTex("=")
        equals.next_to(f_of_p, RIGHT)
        zero_zero = IntegerMatrix([[0], [0]])

        for matrix in dec_rhs, zero_zero:
            matrix.space_out_submobjects(0.8)
            matrix.brackets.scale(0.9)
            matrix.next_to(equals, RIGHT)

        f_of_neg_p.next_to(equals, RIGHT)

        f = f_of_p.get_part_by_tex("f")
        p = f_of_p.get_part_by_tex(p_tex)
        f_brace = Brace(f, UP, buff=SMALL_BUFF)
        f_brace.add(f_brace.get_text("Continuous function"))
        p_brace = Brace(p, DOWN, buff=SMALL_BUFF)
        p_brace.add(p_brace.get_text("Sphere point").match_color(p))

        f_of_p.save_state()
        f_of_p.space_out_submobjects(2)
        f_of_p.scale(2)
        f_of_p.fade(1)

        self.play(f_of_p.restore)
        self.play(GrowFromCenter(f_brace))
        self.wait()
        self.play(GrowFromCenter(p_brace))
        self.wait()
        self.play(
            FadeInFromDown(equals),
            Write(dec_rhs),
            FadeOut(f_brace),
            FadeOut(p_brace),
        )
        self.wait(2)
        self.play(WiggleOutThenIn(f))
        self.wait()
        self.play(
            FadeOut(dec_rhs, DOWN),
            FadeInFromDown(f_of_neg_p)
        )
        self.wait()

        # Rearrange
        f_of_neg_p.generate_target()
        f_of_p.generate_target()
        group = VGroup(f_of_p.target, minus, f_of_neg_p.target)
        group.arrange(RIGHT, buff=SMALL_BUFF)
        group.next_to(equals, LEFT)

        self.play(
            MoveToTarget(f_of_p, path_arc=PI),
            MoveToTarget(f_of_neg_p, path_arc=-PI),
            FadeInFromLarge(minus),
            FadeIn(zero_zero, LEFT)
        )
        self.wait()

        # Define g
        def_eq = OldTex(":=")
        def_eq.next_to(f_of_p, LEFT)
        g_of_p.next_to(def_eq, LEFT)
        rect = SurroundingRectangle(VGroup(g_of_p, f_of_neg_p))
        rect.set_stroke(width=1)
        seeking_text = OldTex(
            "\\text{Looking for }", p_tex, "\\text{ where}"
        )
        color_tex(seeking_text)
        seeking_text.next_to(zero_zero, DOWN, MED_LARGE_BUFF)
        seeking_text.to_edge(LEFT)
        g_equals_zero = VGroup(
            g_of_p.copy(), equals, zero_zero
        )
        g_equals_zero.generate_target()
        g_equals_zero.target.arrange(RIGHT, SMALL_BUFF)
        g_equals_zero.target.next_to(seeking_text, DOWN)

        self.play(
            FadeInFromLarge(g_of_p),
            FadeIn(def_eq, LEFT)
        )
        self.play(
            FadeInFromDown(seeking_text),
            MoveToTarget(g_equals_zero)
        )
        self.play(ShowCreation(rect))
        self.wait()
        self.play(FadeOut(rect))

        # Show g is odd
        g_of_neg_p = OldTex("{g}", "(", neg_p_tex, ")")
        eq2 = OldTex("=")
        rhs = OldTex(
            "f", "(", neg_p_tex, ")", "-",
            "f", "(", p_tex, ")", "=",
            "-", "{g}", "(", p_tex, ")",
        )
        for mob in g_of_neg_p, rhs:
            color_tex(mob)
        g_of_neg_p.next_to(g_of_p, DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        eq2.next_to(g_of_neg_p, RIGHT, SMALL_BUFF)
        rhs.next_to(eq2, RIGHT, SMALL_BUFF)
        neg_g_of_p = rhs[-5:]
        neg_g_of_p.save_state()
        neg_g_of_p.next_to(eq2, RIGHT, SMALL_BUFF)

        self.play(
            FadeIn(g_of_neg_p),
            FadeIn(eq2),
            FadeIn(neg_g_of_p),
            VGroup(seeking_text, g_equals_zero).shift, 1.5 * DOWN
        )
        self.wait()
        self.play(ShowCreationThenFadeAround(g_of_neg_p[2]))
        self.wait()
        self.play(ShowCreationThenFadeAround(neg_g_of_p))
        self.wait()
        self.play(neg_g_of_p.restore)
        rects = VGroup(*map(SurroundingRectangle, [f_of_p, f_of_neg_p]))
        self.play(LaggedStartMap(
            ShowCreationThenDestruction, rects,
            lag_ratio=0.8
        ))
        self.play(
            TransformFromCopy(f_of_p, rhs[5:9]),
            TransformFromCopy(f_of_neg_p, rhs[:4]),
            FadeIn(rhs[4]),
            FadeIn(rhs[-6]),
        )
        self.wait()
