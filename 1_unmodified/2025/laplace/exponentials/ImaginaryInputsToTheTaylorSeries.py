# ==============================================================================
# Scene:      ImaginaryInputsToTheTaylorSeries
# Source:     videos/_2025/laplace/exponentials.py (lines 375-568)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ImaginaryInputsToTheTaylorSeries.py ImaginaryInputsToTheTaylorSeries -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ImaginaryInputsToTheTaylorSeries(InteractiveScene):
    def construct(self):
        # Add complex plane
        plane = ComplexPlane(
            (-6, 6),
            (-4, 4),
            background_line_style=dict(stroke_color=BLUE, stroke_width=1),
            faded_line_style=dict(stroke_color=BLUE, stroke_width=0.5, stroke_opacity=0.5),
        )
        plane.set_height(5)
        plane.to_edge(DOWN, buff=0)
        plane.add_coordinate_labels(font_size=16)

        self.add(plane)

        # Add πi dot
        dot = GlowDot(color=YELLOW)
        dot.move_to(plane.n2p(PI * 1j))
        pi_i_label = Tex(R"\pi i", font_size=30).set_color(YELLOW)
        pi_i_label.next_to(dot, RIGHT, buff=-0.1).align_to(plane.n2p(3j), DOWN)

        self.add(dot, pi_i_label)

        # Show false equation
        false_eq = Tex(R"e^x = e \cdot e \cdots e \cdot e", t2c={"x": BLUE}, font_size=60)
        false_eq.to_edge(UP).shift(2 * LEFT)
        brace = Brace(false_eq[3:], DOWN)
        brace_tex = brace.get_tex(R"x \text{ times}")
        brace_tex[0].set_color(BLUE)

        nonsense = TexText(R"Nonsense if $x$ \\ is complex")
        nonsense.next_to(VGroup(false_eq, brace_tex), RIGHT, LARGE_BUFF)
        nonsense.set_color(RED)

        self.add(false_eq)
        self.play(GrowFromCenter(brace), FadeIn(brace_tex, lag_ratio=0.1))
        self.play(FadeIn(nonsense, lag_ratio=0.1))
        self.wait()

        # Make it the real equation
        gen_poly = self.get_series("x")
        gen_poly.to_edge(LEFT).to_edge(UP, MED_SMALL_BUFF)

        epii = self.get_series(R"\pi i", use_parens=True, in_tex_color=YELLOW)
        epii.next_to(gen_poly, DOWN, aligned_edge=LEFT)

        self.remove(false_eq)
        self.play(
            TransformFromCopy(false_eq[:2], gen_poly[0]),
            FadeOut(false_eq[2:], 0.5 * DOWN, lag_ratio=0.05),
            FadeOut(nonsense),
            FadeOut(brace, 0.5 * DOWN),
            FadeOut(brace_tex, 0.25 * DOWN),
            Write(gen_poly[1:])
        )
        self.wait()

        # Plug in πi
        vectors = self.get_spiral_vectors(plane, PI)
        buff = 0.5 * SMALL_BUFF
        labels = VGroup(
            Tex(R"\pi i", font_size=30).next_to(vectors[1], RIGHT, buff),
            Tex(R"(\pi^2 / 2) \cdot i^2", font_size=30).next_to(vectors[2], UP, buff),
            Tex(R"(\pi^3 / 6) \cdot i^3", font_size=30).next_to(vectors[3], LEFT, buff),
            Tex(R"(\pi^4 / 24) \cdot i^4", font_size=30).next_to(vectors[4], DOWN, buff),
        )
        labels.set_color(YELLOW)
        labels.set_backstroke(BLACK, 5)

        for n in range(0, len(gen_poly), 2):
            anims = [
                LaggedStart(
                    TransformMatchingTex(gen_poly[n].copy(), epii[n], run_time=1),
                    TransformFromCopy(gen_poly[n + 1], epii[n + 1]),
                    gen_poly[n + 2:].animate.align_to(epii[n + 2:], LEFT),
                    lag_ratio=0.05
                ),
            ]
            k = (n - 1) // 2
            if k >= 0:
                anims.append(GrowArrow(vectors[k]))
            if k == 1:
                anims.append(FadeTransform(pi_i_label, labels[0]))
            elif 2 <= k <= len(labels):
                anims.append(FadeIn(labels[k - 1]))
            if k >= 1:
                anims.append(dot.animate.set_width(0.5).move_to(vectors[k].get_end()))
            self.play(*anims)
        for vector in vectors[7:]:
            self.play(GrowArrow(vector), dot.animate.move_to(vector.get_end()))
        self.wait()

        # Step through terms individually
        labels.add_to_back(VectorizedPoint().move_to(vectors[0]))
        for n in range(5):
            rect1 = SurroundingRectangle(epii[2 * n + 2])
            rect2 = SurroundingRectangle(VGroup(vectors[n], labels[n]))
            self.play(
                FadeIn(rect1),
                self.fade_all_but(epii, 2 * n + 2),
                self.fade_all_but(vectors, n),
                self.fade_all_but(labels, n),
                dot.animate.set_opacity(0.1),
            )
            self.play(Transform(rect1, rect2))
            self.play(FadeOut(rect1))
        self.play(*(
            mob.animate.set_fill(opacity=1)
            for mob in [epii, vectors, labels]
        ))
        self.wait()

        # Swap out i for t
        e_to_it = self.get_series("it", use_parens=True, in_tex_color=GREEN)
        for sm1, sm2 in zip(e_to_it, epii):
            sm1.move_to(sm2)

        t_tracker = ValueTracker(PI)
        get_t = t_tracker.get_value

        t_label = Tex(R"t = 3.14", t2c={"t": GREEN})
        t_label.next_to(e_to_it, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        t_rhs = t_label.make_number_changeable("3.14")
        t_rhs.add_updater(lambda m: m.set_value(get_t()))

        vectors.add_updater(lambda m: m.become(self.get_spiral_vectors(plane, get_t(), 20)))
        dot.f_always.move_to(vectors[-1].get_end)

        max_theta = TAU
        semi_circle = Arc(0, max_theta, radius=plane.x_axis.get_unit_size(), arc_center=plane.n2p(0))
        semi_circle.set_stroke(TEAL, 3)

        self.play(
            ReplacementTransform(epii, e_to_it, lag_ratio=0.01, run_time=2),
            FadeOut(labels),
            FadeIn(t_label),
        )
        self.add(vectors)
        self.play(t_tracker.animate.set_value(0), run_time=5)
        self.play(
            t_tracker.animate.set_value(max_theta),
            ShowCreation(semi_circle),
            run_time=12
        )
        self.play(t_tracker.animate.set_value(PI), run_time=6)
        self.wait()

    def get_series(self, in_tex="x", use_parens=False, in_tex_color=BLUE, buff=0.2):
        paren_tex = f"({in_tex})" if use_parens else in_tex
        kw = dict(t2c={in_tex: in_tex_color})
        terms = VGroup(
            Tex(fR"e^{{{in_tex}}}", **kw),
            Tex("="),
            Tex(fR"1"),
            Tex(R"+"),
            Tex(fR"{in_tex}", **kw),
            Tex(R"+"),
            Tex(fR"\frac{{1}}{{2}} {paren_tex}^2", **kw),
            Tex(R"+"),
            Tex(fR"\frac{{1}}{{6}} {paren_tex}^3", **kw),
            Tex(R"+"),
            Tex(fR"\frac{{1}}{{24}} {paren_tex}^4", **kw),
            Tex(R"+"),
            Tex(R"\cdots", **kw),
            Tex(R"+"),
            Tex(fR"\frac{{1}}{{n!}} {paren_tex}^n", **kw),
            Tex(R"+"),
        )
        terms.arrange(RIGHT, buff=buff)
        terms[0].scale(1.25, about_edge=DR)
        return terms

    def get_spiral_vectors(
        self,
        plane,
        t,
        n_terms=10,
        # colors=[GREEN, YELLOW, GREEN_E, YELLOW_E]
        colors=[GREEN_E, GREEN_C, GREEN_B, GREEN_A],
    ):
        values = [(t * 1j)**n / math.factorial(n) for n in range(n_terms)]
        vectors = VGroup(
            Arrow(plane.n2p(0), plane.n2p(value), buff=0, fill_color=color)
            for value, color in zip(values, it.cycle(colors))
        )
        for v1, v2 in zip(vectors, vectors[1:]):
            v2.shift(v1.get_end() - v2.get_start())
        return vectors

    def fade_all_but(self, group, index):
        group.target = group.generate_target()
        group.target.set_fill(opacity=0.4)
        group.target[index].set_fill(opacity=1)
        return MoveToTarget(group)
