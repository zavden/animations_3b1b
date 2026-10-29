# ==============================================================================
# Scene:      DefineMGF
# Source:     videos/_2023/clt_proof/main.py (lines 318-457)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineMGF.py DefineMGF -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineMGF(InteractiveScene):
    def construct(self):
        # Equations
        mgf_name = Text("Moment Generating Function")
        mgf_name.to_corner(UL)

        kw = dict(t2c={
            "t": YELLOW,
            R"\frac{t^2}{2}": YELLOW,
            R"\frac{t^k}{k!}": YELLOW,
        })
        top_eq = Tex(R"M_X(t) = \mathds{E}[e^{tX}]", **kw)
        top_eq.next_to(mgf_name, DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        kw["font_size"] = 42
        lines = VGroup(
            Tex(R"\mathds{E}\left[1 + tX + \frac{t^2}{2} X^2 + \cdots + \frac{t^k}{k!} X^k + \cdots\right]", **kw),
            Tex(R"1 + \mathds{E}[X]t + \mathds{E}[X^2] \frac{t^2}{2} + \cdots + \mathds{E}[X^k] \frac{t^k}{k!} + \cdots", **kw),
        )
        stack_kw = dict(buff=1.75, aligned_edge=LEFT)
        lines.arrange(DOWN, **stack_kw)
        lines.next_to(top_eq, DOWN, **stack_kw)

        # Introduce the expression
        x_rect = SurroundingRectangle(top_eq["X"][0], buff=0.05)
        x_rect.set_stroke(BLUE, 2)
        indic_arrow = Vector(0.5 * UP)
        indic_arrow.next_to(x_rect, DOWN, SMALL_BUFF)
        indic_arrow.target = indic_arrow.generate_target()
        indic_arrow.target.next_to(top_eq["t"][0], DOWN, SMALL_BUFF)

        x_words, t_words = [
            Text(text, font_size=36)
            for text in ["Random variable", "Some real number"]
        ]
        x_words.next_to(indic_arrow, DOWN, SMALL_BUFF)
        x_words.shift_onto_screen()
        t_words.next_to(indic_arrow.target, DOWN, SMALL_BUFF)
        t_words.shift_onto_screen()

        self.play(Write(mgf_name, run_time=1))
        self.wait()
        self.play(
            FadeTransform(mgf_name[0].copy(), top_eq[0]),
            FadeIn(top_eq[1:5], lag_ratio=0.1)
        )
        self.play(
            GrowArrow(indic_arrow),
            FadeIn(x_words, 0.5 * DOWN),
            ShowCreation(x_rect),
        )
        self.wait()
        self.play(
            MoveToTarget(indic_arrow),
            FadeTransform(x_words, t_words),
            FadeOut(x_rect),
        )
        self.wait()
        self.play(
            TransformFromCopy(*top_eq["X"]),
            TransformFromCopy(*top_eq["t"]),
            Write(top_eq[R"= \mathds{E}[e"][0]),
            Write(top_eq[R"]"][0]),
        )
        self.play(FadeOut(indic_arrow), FadeOut(t_words))
        self.wait()

        # Expand series
        exp_term = top_eq[R"e^{tX}"]
        exp_series = lines[0][re.compile(r"1 +.*\\cdots")][0]
        exp_rects = VGroup(*(
            SurroundingRectangle(m, buff=0.05)
            for m in [exp_term, exp_series]
        ))
        exp_rects.set_stroke(BLUE, 2)

        arrow1 = Arrow(exp_term.get_bottom(), exp_series, stroke_color=BLUE, buff=0.3)
        arrow1_label = Text("Taylor series", font_size=32)
        arrow1_label.next_to(arrow1.get_center(), LEFT)

        gf_words = mgf_name["Generating Function"]
        gf_rect = SurroundingRectangle(gf_words, buff=0.05)
        gf_rect.set_stroke(TEAL, 2)
        gf_expl = Text("Focus on coefficients\nin a series expansion", font_size=36)
        gf_expl.next_to(gf_rect, DOWN)
        gf_expl.align_to(mgf_name["Function"], LEFT)

        self.play(
            ShowCreation(gf_rect),
            gf_words.animate.set_color(TEAL),
        )
        self.play(
            FadeIn(gf_expl, lag_ratio=0.1)
        )
        self.wait()
        self.play(ShowCreation(exp_rects[0]))
        self.play(
            ReplacementTransform(*exp_rects),
            TransformMatchingShapes(exp_term.copy(), exp_series, run_time=1),
            TransformFromCopy(top_eq[R"\mathds{E}["], lines[0][R"\mathds{E}\left["]),
            TransformFromCopy(top_eq[R"]"], lines[0][R"]"]),
            GrowArrow(arrow1),
            FadeIn(arrow1_label),
        )
        self.play(FadeOut(exp_rects[1]))
        self.wait()

        # Linearity of expectations
        frame = self.frame
        arrow2 = Arrow(*lines)
        arrow2.match_style(arrow1)
        arrow2.rotate(arrow1.get_angle() - arrow2.get_angle())
        arrow2_label = Text("Linearity of Expectation", font_size=32)
        arrow2_label.next_to(arrow2.get_center(), LEFT)

        self.play(
            frame.animate.align_to(top_eq, UP).shift(0.5 * UP),
            mgf_name.animate.next_to(top_eq, RIGHT, buff=1.0).set_color(WHITE),
            FadeOut(gf_expl, DOWN),
            FadeOut(gf_rect),
        )
        self.play(
            TransformMatchingTex(lines[0].copy(), lines[1]),
            GrowArrow(arrow2),
            FadeIn(arrow2_label),
        )
        self.wait()

        # Highlight term by term
        terms = VGroup(lines[1]["1"][0])
        terms.add(*lines[1][re.compile(r'(?<=\+)(.*?)(?=\+)')])
        terms.remove(terms[-2])
        rects = VGroup(*(SurroundingRectangle(term) for term in terms))
        rects.set_stroke(PINK, 2)

        last_rect = VMobject()
        for rect in rects:
            self.play(ShowCreation(rect), FadeOut(last_rect))
            self.wait()
            last_rect = rect
        self.play(FadeOut(last_rect))
