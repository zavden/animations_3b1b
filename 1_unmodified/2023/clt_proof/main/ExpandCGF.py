# ==============================================================================
# Scene:      ExpandCGF
# Source:     videos/_2023/clt_proof/main.py (lines 724-1026)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpandCGF.py ExpandCGF -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpandCGF(InteractiveScene):
    def construct(self):
        # Taylor series for log
        t2c = {
            "x": YELLOW,
            "{t}": MAROON_B,
            R"\frac{t^2}{2}": MAROON_B,
            R"\frac{t^3}{3!}": MAROON_B,
            R"\frac{t^m}{m!}": MAROON_B,
        }
        kw = dict(t2c=t2c)
        log_eq = VGroup(
            Tex(R"\log(1 + x)", **kw),
            Tex(R"= x -\frac{1}{2}x^{2} +\frac{1}{3}x^{3} -\frac{1}{4}x^{4} +\cdots", **kw)
        )
        log_eq.arrange(RIGHT, buff=0.15)
        log_eq.to_edge(UP)
        equals = log_eq[1][0]
        approx = Tex(R"\approx")
        approx.move_to(equals)
        taylor_label = Text("Taylor Series expansion")
        taylor_label.next_to(log_eq, DOWN, buff=MED_LARGE_BUFF)

        self.add(log_eq)
        self.add(taylor_label)

        # Graph of log
        bls = dict(
            stroke_color=GREY_B,
            stroke_width=1,
            stroke_opacity=0.5,
        )
        axes = NumberPlane(
            (-1, 10), (-3, 3),
            background_line_style=bls,
            faded_line_ratio=0,
            num_sampled_graph_points_per_tick=10,
        )
        axes.set_height(5)
        axes.to_edge(DOWN, buff=0.25)
        graph = axes.get_graph(lambda x: np.log(1.01 + x))
        graph.make_smooth()
        graph.set_stroke(BLUE, 3)

        self.add(axes, graph)

        # Approximations
        rects = VGroup(*(
            SurroundingRectangle(log_eq[1][s][0])
            for s in [
                R"x",
                R"x -\frac{1}{2}x^{2}",
                R"x -\frac{1}{2}x^{2} +\frac{1}{3}x^{3}",
                R"x -\frac{1}{2}x^{2} +\frac{1}{3}x^{3} -\frac{1}{4}x^{4}",
                R"x -\frac{1}{2}x^{2} +\frac{1}{3}x^{3} -\frac{1}{4}x^{4} +\cdots",
            ]
        ))
        rects.set_stroke(TEAL, 2)

        coefs = [0, *[(-1)**(n + 1) / n for n in range(1, 14)]]

        def poly(x, coefs):
            return sum(c * x**n for n, c in enumerate(coefs))

        approxs = VGroup(*(
            axes.get_graph(lambda x: poly(x, coefs[:N]))
            for N in range(2, len(coefs))
        ))
        approxs.set_stroke(YELLOW, 3, opacity=0.75)

        top_rect = FullScreenRectangle().set_fill(BLACK, 1)
        top_rect.set_height(
            FRAME_HEIGHT / 2 - axes.get_top()[1] - SMALL_BUFF,
            about_edge=UP,
            stretch=True
        )

        rect = rects[0].copy()
        rect.scale(1e-6).move_to(rects[0].get_corner(DL))
        approx = VectorizedPoint(axes.c2p(0, 0))

        self.add(approx, top_rect, log_eq, taylor_label)

        for target_rect, target_approx in zip(rects, approxs):
            self.play(
                Transform(rect, target_rect),
                FadeOut(approx),
                FadeIn(target_approx),
            )
            approx = target_approx
            self.wait()
        for target_approx in approxs[len(rects):]:
            self.play(
                FadeOut(approx),
                FadeIn(target_approx),
                rect.animate.stretch(1.02, 0, about_edge=LEFT),
            )
            approx = target_approx

        self.wait()

        self.remove(top_rect)
        self.play(LaggedStartMap(
            FadeOut,
            VGroup(axes, graph, approx, rect, taylor_label)
        ))

        # Set up expansion
        mgf_term = R"\mathds{E}[X]{t} + \mathds{E}[X^2]\frac{t^2}{2} + \mathds{E}[X^3]\frac{t^3}{3!} + \cdots"
        log_mgf = Tex(R"\log(M_X({t}))", **kw)
        log_mgf.next_to(log_eq[0], DOWN, buff=1.75, aligned_edge=RIGHT)
        kt = Tex("K_X({t}) = ", **kw)

        full_rhs = Tex(Rf"""
            &=\left({mgf_term}\right)\\
            &-\frac{{1}}{{2}} \left({mgf_term}\right)^{{2}}\\
            &+\frac{{1}}{{3}} \left({mgf_term}\right)^{{3}}\\
            &-\frac{{1}}{{4}} \left({mgf_term}\right)^{{4}}\\
            &+\cdots
        """, font_size=36, **kw)

        full_rhs.next_to(log_mgf, RIGHT, aligned_edge=UP)
        log_mgf.next_to(full_rhs["="], LEFT)
        kt.next_to(log_mgf, LEFT, buff=0.2)

        # Setup log anim
        self.play(
            TransformMatchingTex(log_eq[0].copy(), log_mgf),
            FadeIn(kt, DOWN),
            run_time=1
        )
        self.wait()
        self.play(LaggedStart(
            *(
                TransformFromCopy(log_eq[1][tex][0], full_rhs[tex][0])
                for tex in [
                    "=",
                    R"-\frac{1}{2}",
                    R"+\frac{1}{3}",
                    R"-\frac{1}{4}",
                    R"+\cdots",
                    "^{2}", "^{3}", "^{4}",
                ]
            ),
            *(
                AnimationGroup(
                    TransformFromCopy(x, lp),
                    TransformFromCopy(x, rp),
                )
                for x, lp, rp in zip(
                    log_eq[1]["x"],
                    full_rhs[R"\left("],
                    full_rhs[R"\right)"],
                )
            ),
            lag_ratio=0.1,
            run_time=4
        ))
        self.wait()

        # Interim equation
        frame = self.frame
        log_eq.generate_target()
        log_eq.target.shift(UP)
        mid_eq = Tex(f"x = M_X({{t}}) - 1 = {mgf_term}", font_size=42, **kw)
        mid_eq.set_y(midpoint(log_eq.target.get_y(DOWN), full_rhs.get_y(UP)))

        self.play(LaggedStart(
            frame.animate.set_height(10),
            MoveToTarget(log_eq),
            TransformFromCopy(log_eq[0]["x"][0], mid_eq["x"][0]),
            TransformFromCopy(log_mgf["M_X({t})"][0], mid_eq["M_X({t})"][0]),
            Write(mid_eq["="]),
            Write(mid_eq["- 1"]),
        ))
        self.wait()
        self.play(FadeIn(mid_eq[mgf_term][0], lag_ratio=0.1, run_time=2))
        self.wait()

        # Fill in parens
        self.play(LaggedStart(
            *(
                TransformFromCopy(mid_eq[mgf_term][0], term, path_arc=-60 * DEGREES)
                for term in full_rhs[f"{mgf_term}"]
            ),
            lag_ratio=0.2,
            run_time=4
        ))
        self.wait()

        # Reposition
        k_eq = VGroup(kt, log_mgf, full_rhs)
        self.play(
            k_eq.animate.align_to(mid_eq, UP),
            FadeOut(mid_eq, UP)
        )
        self.wait()

        # Expand out first order term
        term11, term21, term31 = full_rhs[R"\mathds{E}[X]{t}"][:3].copy()
        term12, term22 = full_rhs[R"\mathds{E}[X^2]\frac{t^2}{2}"][:2].copy()
        term13 = full_rhs[R"\mathds{E}[X^3]\frac{t^3}{3!}"][0].copy()

        parens2 = VGroup(
            full_rhs[R"-\frac{1}{2} \left("][0],
            full_rhs[R"\right)^{2}"][0],
        ).copy()
        parens3 = VGroup(
            full_rhs[R"+\frac{1}{3} \left("][0],
            full_rhs[R"\right)^{3}"][0],
        ).copy()

        expansion = Tex(R"""
            K_X({t}) =
            \mathds{E}[X]{t} + \text{Var}(X)\frac{t^2}{2}
            + K_3[X]\frac{t^3}{3!} + \cdots + K_m[X]\frac{t^m}{m!} + \cdots
        """, **kw)
        expansion[R"\text{Var}"].set_color(BLUE)

        expansion.next_to(k_eq, DOWN, buff=0.75, aligned_edge=LEFT)

        self.add(term11)
        self.play(full_rhs.animate.set_opacity(0.3))
        self.wait()
        self.play(
            TransformFromCopy(kt, expansion[R"K_X({t}) ="][0]),
            TransformFromCopy(term11, expansion[R"\mathds{E}[X]{t}"][0]),
        )
        self.wait()

        # Second order term
        full_second = Tex(
            R"\left(\mathds{E}[X^2] - \mathds{E}[X]^2 \right) \frac{t^2}{2}",
            **kw
        )
        plus = expansion["+"][0]
        full_second.next_to(plus, RIGHT, index_of_submobject_to_align=0)

        self.play(
            FadeOut(term11),
            FadeIn(term12),
            FadeIn(parens2),
            FadeIn(term21),
        )
        self.wait()
        self.play(FlashAround(term12, run_time=1.5))
        self.play(
            LaggedStart(*(
                TransformFromCopy(m1, full_second[tex][0])
                for m1, tex in [
                    (term12[:4], R"\mathds{E}[X^2]"),
                    (term12[4:], R"\frac{t^2}{2}"),
                ]
            )),
            Write(plus),
            Write(full_second[R"\left("][0]),
            Write(full_second[R"\right)"][0]),
        )
        self.wait()
        self.play(
            TransformFromCopy(term21, full_second[R"- \mathds{E}[X]^2"][0])
        )
        self.wait()

        # Highlight variance
        expanded_var = full_second[R"\left(\mathds{E}[X^2] - \mathds{E}[X]^2 \right)"]
        var_term = expansion[R"\text{Var}(X)"]
        rect = SurroundingRectangle(expanded_var, buff=0.05)
        rect.set_stroke(BLUE, 2)
        arrow = Vector(DR)
        arrow.next_to(var_term, UL, SMALL_BUFF)
        arrow.set_color(BLUE)

        self.play(
            VGroup(expanded_var, rect).animate.next_to(arrow.get_start(), UL, SMALL_BUFF),
            FadeIn(var_term),
            GrowArrow(arrow),
            ReplacementTransform(
                full_second[R"\frac{t^2}{2}"][0],
                expansion[R"\frac{t^2}{2}"][0],
            ),
        )
        self.wait()
        self.play(
            FadeOut(expanded_var),
            FadeOut(rect),
            FadeOut(arrow),
        )

        # Third term preview
        self.play(LaggedStart(
            FadeOut(term12),
            FadeIn(term13),
            FadeIn(term22),
            FadeIn(term31),
        ))
        self.play(Write(expansion[R"+ K_3[X]\frac{t^3}{3!}"]))
        self.wait()
        self.play(
            full_rhs.animate.set_opacity(1),
            Write(expansion[R"+ \cdots + K_m[X]\frac{t^m}{m!} + \cdots"])
        )
        self.wait()
