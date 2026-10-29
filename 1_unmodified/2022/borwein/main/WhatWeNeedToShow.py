# ==============================================================================
# Scene:      WhatWeNeedToShow
# Source:     videos/_2022/borwein/main.py (lines 1325-1580)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatWeNeedToShow.py WhatWeNeedToShow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def rect_func(x):
    result = np.zeros_like(x)
    result[(-0.5 < x) & (x < 0.5)] = 1.0
    return result


class WhatWeNeedToShow(InteractiveScene):
    def construct(self):
        # Title
        title = Text("What we must show", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_backstroke(width=5)
        underline = Line(LEFT, RIGHT)
        underline.set_width(6)
        underline.set_stroke(GREY_A, width=(0, 3, 3, 3, 3, 0))
        underline.insert_n_curves(100)
        underline.next_to(title, DOWN, buff=0.05)

        self.add(underline, title)

        # Expressions
        t2c = {
            R"\mathcal{F}": TEAL,
            R"{t}": BLUE,
            R"{\omega}": YELLOW,
            R"{k}": RED,
        }
        kw = dict(tex_to_color_map=t2c, font_size=36)
        expressions = VGroup(
            Tex(R"\mathcal{F}\left[\frac{\sin(\pi {t})}{\pi {t}} \right]({\omega}) = \text{rect}({\omega})", **kw),
            Tex(R"\mathcal{F}\left[\frac{\sin(\pi {t} / {k})}{\pi {t} / {k}} \right]({\omega}) = {k} \cdot \text{rect}({k}{\omega})", **kw),
            Tex(R"\int_{-\infty}^\infty f({t}) dt = \mathcal{F}\left[ f({t}) \right](0)", **kw),
            Tex(R"\int_{-\infty}^\infty \frac{\sin(\pi {t})}{\pi {t}} dt = \text{rect}(0) = 1", **kw),
            Tex(R"\mathcal{F}\left[ f({t}) \cdot g({t}) \right] = \mathcal{F}[f({t})] * \mathcal{F}[g({t})]", **kw),
            Tex(
                R"""\mathcal{F}\left[ \frac{\sin(\pi {t})}{\pi {t}} \cdot \frac{\sin(\pi {t} / 3)}{\pi {t} / 3} \right]
                = \big[ \text{rect} * \text{rect}_3 \big]""",
                **kw
            ),
        )
        expressions.set_stroke(width=0)
        key_facts = expressions[0::2]
        examples = expressions[1::2]
        key_facts.arrange(DOWN, buff=1.5, aligned_edge=LEFT)
        key_facts.next_to(underline, DOWN, MED_LARGE_BUFF).to_edge(LEFT)
        for fact, example in zip(key_facts, examples):
            example.next_to(fact, RIGHT, buff=2.0)

        ft_sinc, int_to_eval, conv_theorem = key_facts
        ft_sinck, sinc_int_to_rect_0, conv_theorem_ex = examples

        # FT of sinc
        ft_sinc.next_to(underline, DOWN, MED_LARGE_BUFF)

        width = FRAME_WIDTH / 2 - 1
        axes1 = Axes((-4, 4), (-1, 1), width=width, height=3)
        axes2 = Axes((-1, 1, 0.25), (0, 2), width=width, height=1.5)

        axes1.to_corner(DL)
        axes2.shift(axes1.get_origin() - axes2.get_origin())
        axes2.to_edge(RIGHT)

        axes1.add(OldTex("t", color=BLUE, font_size=24).next_to(axes1.x_axis.get_right(), UP, 0.2))
        axes2.add(OldTex(R"\omega", color=YELLOW, font_size=24).next_to(axes2.x_axis.get_right(), UP, 0.2))
        axes1.add_coordinate_labels(font_size=20)
        axes2.add_coordinate_labels(x_values=np.arange(-1, 1.5, 0.5), font_size=20, num_decimal_places=1)

        k_tracker = ValueTracker(1)
        get_k = k_tracker.get_value

        graph1 = axes1.get_graph(lambda x: 0, color=BLUE)
        axes1.bind_graph_to_func(graph1, lambda x: np.sinc(x / get_k()))

        graph2 = VMobject().set_stroke(YELLOW, 3)

        def update_graph2(graph):
            k = get_k()
            graph.set_points_as_corners([
                axes2.c2p(-1, 0),
                axes2.c2p(-0.5 / k, 0),
                axes2.c2p(-0.5 / k, k),
                axes2.c2p(0.5 / k, k),
                axes2.c2p(0.5 / k, 0),
                axes2.c2p(1, 0),
            ])
            return graph

        graph2.add_updater(update_graph2)

        graph1_label = Tex(R"{\sin(\pi {t}) \over \pi {t} }", **kw)
        graph2_label = Tex(R"\text{rect}({\omega})", **kw)
        graph1_label.move_to(axes1.c2p(-2, 1))
        graph2_label.move_to(axes2.c2p(0.5, 2))

        arrow = Arrow(axes1.c2p(2, 0.5), axes2.c2p(-0.5, 1), path_arc=-PI / 3)
        arrow.set_color(TEAL)
        arrow_copy = arrow.copy()
        arrow_copy.rotate(PI, about_point=midpoint(axes1.c2p(4, 0), axes2.c2p(-1, 0)))
        arrow_label = Tex(R"\mathcal{F}", color=TEAL)
        arrow_label.next_to(arrow, UP, SMALL_BUFF)
        arrow_label_copy = arrow_label.copy()
        arrow_label_copy.next_to(arrow_copy.pfp(0.5), UP)

        self.play(
            FadeIn(axes1),
            ShowCreation(graph1),
            FadeIn(graph1_label, UP)
        )
        self.wait()
        self.play(
            ShowCreation(arrow),
            FadeIn(arrow_label, RIGHT + 0.2 * UP),
            FadeIn(axes2),
        )
        self.play(
            Write(graph2_label),
            ShowCreation(graph2)
        )
        self.wait()
        self.play(
            TransformFromCopy(arrow, arrow_copy, path_arc=PI / 2),
            TransformFromCopy(arrow_label, arrow_label_copy, path_arc=PI / 2),
        )
        self.wait()

        self.play(LaggedStart(
            FadeTransform(arrow_label.copy(), ft_sinc[0]),
            FadeTransform(graph1_label.copy(), ft_sinc[2:12]),
            Write(VGroup(ft_sinc[1], ft_sinc[12])),
        ))
        self.wait()
        self.play(Write(ft_sinc[13:17]))
        self.play(
            FadeTransform(graph2_label.copy(), ft_sinc[17:])
        )
        self.add(ft_sinc)
        self.wait()

        # Generalize
        graph1_gen_label = Tex(R"{\sin(\pi {t} / {k}) \over \pi {t} / {k} }", **kw)
        graph2_gen_label = Tex(R"{k} \cdot \text{rect}({k} {\omega})", **kw)
        graph1_gen_label.move_to(graph1_label)
        graph2_gen_label.move_to(graph2_label)
        ft_sinck.move_to(ft_sinc)

        self.play(LaggedStart(
            FadeOut(graph1_label, UP),
            FadeIn(graph1_gen_label, UP),
            FadeOut(graph2_label, UP),
            FadeIn(graph2_gen_label, UP),
        ))
        self.play(
            FadeOut(ft_sinc, UP),
            FadeIn(ft_sinck, UP)
        )
        self.wait()
        self.play(k_tracker.animate.set_value(3), run_time=3)
        self.wait()
        self.play(k_tracker.animate.set_value(1), run_time=3)
        self.wait()
        self.play(ft_sinck.animate.set_height(0.5).to_corner(UL))
        self.wait()

        # Area to evaluate
        k_tracker.set_value(1)
        int_to_eval.next_to(underline, DOWN, MED_LARGE_BUFF)
        sinc_int_to_rect_0.move_to(int_to_eval)

        area = axes1.get_riemann_rectangles(
            axes1.get_graph(np.sinc),
            colors=(BLUE, BLUE),
            dx=0.01
        )
        area.set_stroke(WHITE, 0)
        x0 = axes1.get_origin()[0]
        area.sort(lambda p, x0=x0: abs(p[0] - x0))

        dot = GlowDot(color=BLUE)
        dot.set_glow_factor(0.5)
        dot.set_radius(0.1)
        dot.move_to(int_to_eval[11:].get_center())

        self.play(FadeIn(int_to_eval, DOWN))
        self.play(FlashAround(int_to_eval[:10], run_time=2, time_width=1.5))
        self.play(Write(area))
        self.wait()
        self.play(FlashAround(int_to_eval[11:], run_time=2, time_width=1.5))
        self.play(dot.animate.move_to(axes2.c2p(0, 1)), run_time=1.5)
        self.wait()
        self.play(
            int_to_eval.animate.set_height(0.5).next_to(ft_sinck, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        )
        self.play(FadeIn(sinc_int_to_rect_0, RIGHT))
        self.wait()
        self.play(FadeOut(sinc_int_to_rect_0))

        # Many dots
        dx = 0.1
        dots = Group(*(
            GlowDot(
                axes2.c2p(x, rect_func(x)),
                color=TEAL
            )
            for x in np.arange(-1, 1 + dx, dx)
        ))
        thick_graph = VGroup(
            axes1.get_graph(np.sinc, x_range=(-1, 4)),
            axes1.get_graph(np.sinc, x_range=(-4, 1)).reverse_points(),
        )
        thick_graph.set_stroke(YELLOW, 6)

        self.play(FadeIn(dots, DOWN, lag_ratio=0.5, run_time=5))
        self.wait()
        self.play(
            VShowPassingFlash(thick_graph[0], run_time=4, time_width=1),
            VShowPassingFlash(thick_graph[1], run_time=4, time_width=1),
            FadeOut(area)
        )
        self.wait()
        self.play(FadeOut(dots))

        # Convolution fact
        conv_theorem.set_height(0.45)
        conv_theorem.next_to(underline, DOWN, MED_LARGE_BUFF)
        conv_theorem_ex.next_to(underline, DOWN, MED_LARGE_BUFF)
        conv_theorem_name = OldTexText("``Convolution theorem''", font_size=60)
        conv_theorem_name.next_to(conv_theorem, DOWN, buff=MED_LARGE_BUFF)
        conv_theorem_name.set_color(YELLOW)

        self.play(FadeIn(conv_theorem, DOWN))
        self.wait()
        self.play(
            FadeIn(conv_theorem_ex, DOWN),
            FadeOut(conv_theorem, DOWN),
        )
        self.wait()
        self.play(
            FadeOut(conv_theorem_ex, UP),
            FadeIn(conv_theorem, UP),
        )
        self.play(Write(conv_theorem_name))

        # Reorganize
        facts = VGroup(ft_sinck, int_to_eval, conv_theorem)
        facts.generate_target()
        facts.target[:2].scale(1.7)
        facts.target.scale(0.8)
        facts.target.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        facts.target.next_to(ORIGIN, RIGHT).to_edge(UP, buff=MED_SMALL_BUFF)
        bullets = VGroup(*(
            Dot().next_to(fact, LEFT)
            for fact in facts.target
        ))

        self.play(
            MoveToTarget(facts),
            title.animate.next_to(facts.target, LEFT, LARGE_BUFF),
            Uncreate(underline),
            FadeOut(conv_theorem_name),
            Write(bullets)
        )
        self.wait()
