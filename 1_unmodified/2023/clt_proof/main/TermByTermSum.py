# ==============================================================================
# Scene:      TermByTermSum
# Source:     videos/_2023/clt_proof/main.py (lines 1180-1257)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TermByTermSum.py TermByTermSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TermByTermSum(InteractiveScene):
    def construct(self):
        # One line equation
        top_eq = Tex("K_{X+Y}(t) = K_X(t) + K_Y(t)", t2c={"t": MAROON_B})
        top_eq.to_edge(UP)
        self.add(top_eq)
        self.wait()

        # Set up equations
        sum_eq, x_eq, y_eq = all_eqs = VGroup(*(
            VGroup(
                Tex(Rf"K_{{{sym}}}({{t}})"),
                Tex("="),
                Tex(Rf"\mathds{{E}}[{sym}] {{t}}"),
                Tex("+"),
                Tex(Rf"\text{{Var}}({sym}) \frac{{t^2}}{{2}}"),
                Tex("+"),
                Tex(Rf"K_3[{sym}] \frac{{t^3}}{{3!}}"),
                Tex(R"+ \cdots")
            )
            for sym in ["X + Y", "X", "Y"]
        ))
        for eq in all_eqs:
            eq.arrange(RIGHT, buff=SMALL_BUFF)

        all_eqs.arrange(DOWN, buff=LARGE_BUFF)
        for p1, p2, p3 in zip(x_eq, y_eq, sum_eq):
            for part in p1, p2, p3:
                part["{t}"].set_color(MAROON_B)
                part[R"\frac{t^2}{2}"].set_color(MAROON_B)
                part[R"\frac{t^3}{3!}"].set_color(MAROON_B)
            p1.match_x(p3)
            p2.match_x(p3)

        plus = Tex("+").scale(1.25)
        equals = Tex("=").scale(1.25).rotate(90 * DEGREES)
        plus.move_to(VGroup(x_eq[0], y_eq[0]))
        equals.move_to(VGroup(x_eq[0], sum_eq[0]))

        sum_eq[4].shift(0.05 * UP)

        anim_kw = dict(path_arc=-45 * DEGREES)
        self.play(LaggedStart(
            ReplacementTransform(top_eq["K_{X+Y}(t)"][0], sum_eq[0], **anim_kw),
            ReplacementTransform(top_eq["+"][1], plus, **anim_kw),
            ReplacementTransform(top_eq["K_X(t)"][0], x_eq[0], **anim_kw),
            ReplacementTransform(top_eq["="][0], equals, **anim_kw),
            ReplacementTransform(top_eq["K_Y(t)"][0], y_eq[0], **anim_kw),
            run_time=3,
        ))
        self.play(LaggedStartMap(FadeIn, sum_eq[1:]))
        self.play(FadeIn(x_eq[1:], DOWN))
        self.play(FadeIn(y_eq[1:], DOWN))
        self.wait()

        # Highlight variance
        pe_copy = VGroup(plus, equals).copy()
        rects = VGroup(*(
            SurroundingRectangle(VGroup(*(eq[i] for eq in all_eqs)))
            for i in [2, 4, 6]
        ))
        rects.set_stroke(YELLOW, 2)
        self.play(
            ShowCreation(rects[0]),
            pe_copy.animate.match_x(rects[0]),
        )
        self.wait()
        for r1, r2 in zip(rects, rects[1:]):
            self.play(
                ReplacementTransform(r1, r2),
                pe_copy.animate.match_x(r2),
            )
            self.wait()
        self.play(
            rects[2].animate.become(SurroundingRectangle(all_eqs).set_stroke(width=0)),
            FadeOut(pe_copy),
        )
        self.wait()
