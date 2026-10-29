# ==============================================================================
# Scene:      BuildUpGaussian
# Source:     videos/_2023/clt/main.py (lines 1476-2073)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BuildUpGaussian.py BuildUpGaussian -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def gauss_func(x, mu, sigma):
    pre_factor = 1 / (sigma * math.sqrt(2 * PI))
    return pre_factor * np.exp(-0.5 * ((x - mu) / sigma)**2)


class BuildUpGaussian(InteractiveScene):
    def construct(self):
        # Axes and graph
        axes = self.get_axes()
        bell_graph = axes.get_graph(lambda x: gauss_func(x, 0, 0.5))
        bell_graph.set_stroke(YELLOW, 3)

        def get_graph(func, **kwargs):
            return axes.get_graph(func, **kwargs).match_style(bell_graph)

        self.add(axes)
        self.add(bell_graph)

        # Peel off from full Gaussian
        kw = dict(
            tex_to_color_map={
                R"\mu": PINK,
                R"\sigma": RED,
            },
            font_size=72
        )

        formulas = VGroup(*(
            Tex(tex, **kw)
            for tex in [
                "e^x",
                "e^{-x}",
                "e^{-x^2}",
                R"e^{-{1 \over 2} x^2}",
                R"{1 \over \sqrt{2\pi}} e^{-{1 \over 2} x^2}",
                R"{1 \over \sigma \sqrt{2\pi}} e^{-{1 \over 2} \left({x \over \sigma}\right)^2}",
                R"{1 \over \sigma \sqrt{2\pi}} e^{-{1 \over 2} \left({x - \mu \over \sigma}\right)^2}",
            ]
        ))
        saved_formulas = formulas.copy()

        morty = Mortimer()
        morty.to_edge(DOWN).shift(3 * RIGHT)

        formulas[-1].set_max_height(1.25)
        formulas[-1].to_edge(UP)
        self.add(formulas[-1])
        self.play(FlashAround(formulas[-1], run_time=2, time_width=1.5))
        self.wait()
        self.play(
            FadeOut(axes, 2 * DOWN),
            FadeOut(bell_graph, DOWN),
            VFadeIn(morty),
            morty.change("raise_right_hand"),
            formulas[-1].animate.next_to(morty.get_corner(UL), UP)
        )

        for form1, form2 in zip(formulas[::-1], formulas[-2::-1]):
            form2.next_to(morty.get_corner(UL), UP)
            self.play(TransformMatchingTex(form1, form2), run_time=1)

        self.play(
            formulas[0].animate.center().to_edge(UP),
            FadeIn(axes, 3 * UP),
            FadeOut(morty, DOWN)
        )
        self.wait()

        # Show decay
        self.remove(formulas[0])
        formulas = saved_formulas
        for form in formulas:
            form.center().to_edge(UP)
        self.add(formulas[0])

        def decay_anim(graph):
            dot = GlowDot(color=WHITE)
            dot.move_to(graph.pfp(0.5))
            sub_graph = VMobject()
            sub_graph.set_points(graph.get_points()[graph.get_num_points() // 2::])
            return AnimationGroup(
                MoveAlongPath(dot, sub_graph),
                UpdateFromAlphaFunc(
                    VectorizedPoint(),
                    lambda m, a: dot.set_radius(0.2 * clip(10 * there_and_back(a), 0, 1)),
                    remover=True
                ),
                run_time=1.5,
                remover=True
            )

        graph = get_graph(np.exp)

        self.play(ShowCreation(graph))
        self.wait()
        self.play(LaggedStart(
            TransformMatchingTex(formulas[0], formulas[1]),
            graph.animate.stretch(-1, 0).set_anim_args(run_time=2),
            lag_ratio=0.5
        ))
        graph.become(get_graph(lambda x: np.exp(-x)))
        self.play(LaggedStart(*(
            decay_anim(graph)
            for x in range(8)
        ), lag_ratio=0.15, run_time=4))

        # Decay in both directions
        abs_formula = Tex("e^{-|x|}", **kw)
        abs_formula.to_edge(UP)
        abs_graph = get_graph(
            lambda x: np.exp(-np.abs(x)),
        )
        abs_graph.make_jagged()
        smooth_graph = get_graph(lambda x: np.exp(-x**2))

        self.play(
            TransformMatchingTex(formulas[1], abs_formula),
            Transform(graph, abs_graph)
        )
        self.wait()
        self.play(Flash(axes.c2p(0, 1)))
        self.wait()
        self.play(
            TransformMatchingTex(abs_formula, formulas[2]),
            Transform(graph, smooth_graph)
        )
        self.wait()

        # Tweak the spread
        form_with_const = Tex("e^{-c x^2}", **kw)
        form_with_const["c"].set_color(RED)
        form_with_const.move_to(formulas[2])

        c_display, c_tracker = self.get_variable_display("c", RED, (0, 5))
        base_tracker = ValueTracker(math.exp(1))

        get_c = c_tracker.get_value
        get_base = base_tracker.get_value

        axes.bind_graph_to_func(
            graph,
            lambda x: np.exp(-get_c() * np.log(get_base()) * x**2)
        )

        self.play(
            TransformMatchingTex(formulas[2], form_with_const),
            FadeIn(c_display),
        )
        self.wait()
        for value in [5.0, 0.2, 1.0]:
            self.play(c_tracker.animate.set_value(value), run_time=2)
            self.wait()

        # Show effective base
        rhs = Tex(R"= \left(e^c\right)^{-x^2}", **kw)
        rhs["c"].set_color(RED)
        rhs.next_to(form_with_const)

        self.play(
            Write(rhs.shift(2 * LEFT)),
            form_with_const.animate.shift(2 * LEFT)
        )
        self.wait()

        alt_base_form = Tex(R"=(2.718)^{-x^2}", **kw)
        alt_base_form.next_to(rhs, RIGHT)
        base = alt_base_form.make_number_changeable("2.718")
        base_width = base.get_width()
        base.set_color(TEAL)
        base.edge_to_fix = ORIGIN
        base.add_updater(lambda m: m.set_value(
            np.exp(get_c() * np.log(get_base()))
        ))
        base.add_updater(lambda m: m.set_width(base_width))

        self.play(
            FadeIn(alt_base_form, RIGHT),
        )
        self.wait()
        for value in [2.2, 0.1, 1.0]:
            self.play(c_tracker.animate.set_value(value), run_time=2)
            self.wait()

        # Writing this family with "e" is a choice that we're making
        es = VGroup(form_with_const[0], rhs[2])
        pis, twos, threes = [
            VGroup(*(
                Tex(tex, **kw).move_to(e, DR)
                for e in es
            ))
            for tex in [R"\pi", "2", "3"]
        ]

        note = TexText("$e$ is not special here")
        note.next_to(es[0], DOWN, buff=1.5, aligned_edge=RIGHT)
        note.set_backstroke(width=5)
        arrow = Arrow(note, es[0])

        self.play(
            FlashAround(es[0], run_time=2),
            FadeIn(note),
            GrowArrow(arrow),
        )
        self.wait()
        last_mobs = es
        for mobs, value in [(pis, PI), (twos, 2), (threes, 3), (es, math.exp(1))]:
            base.suspend_updating()
            self.play(
                FadeOut(last_mobs, 0.25 * UP, lag_ratio=0.2),
                FadeIn(mobs, 0.25 * UP, lag_ratio=0.2),
                c_tracker.animate.set_value(1 / math.log(value)),
                base_tracker.animate.set_value(value),
            )
            base.resume_updating()
            self.wait()
            for c in [3, 0.5, 1]:
                self.play(c_tracker.animate.set_value(c), run_time=2)
                self.wait()

            last_mobs = mobs

        # Introduce sigma
        self.play(
            form_with_const.animate.set_x(0),
            FadeOut(rhs, RIGHT),
            FadeOut(alt_base_form, RIGHT),
            FadeOut(note, RIGHT),
            FadeOut(arrow, RIGHT),
        )
        self.play(FlashAround(form_with_const["c"], color=RED))

        form_with_sigma = Tex(
            R"e^{-{1 \over 2} \left({x / \sigma}\right)^2}",
            **kw
        )
        form_with_sigma.to_edge(UP)

        sigma_display, sigma_tracker = self.get_variable_display(R"\sigma", RED, (0, 3))
        sigma_tracker.set_value(math.sqrt(0.5))
        get_sigma = sigma_tracker.get_value
        sigma_display.update()
        graph.clear_updaters()
        axes.bind_graph_to_func(graph, lambda x: np.exp(
            -0.5 * (x / get_sigma())**2
        ))
        graph.update()

        self.play(
            TransformMatchingTex(form_with_const, form_with_sigma),
            FadeOut(c_display, UP),
            FadeIn(sigma_display, UP),
            run_time=1
        )
        self.wait()

        # Show standard deviation
        v_lines = Line(axes.c2p(0, 0), axes.c2p(0, 0.75 * axes.y_axis.x_max)).replicate(2)
        v_lines.set_stroke(RED, 2)
        v_lines[0].add_updater(lambda m: m.move_to(axes.c2p(-get_sigma(), 0), DOWN))
        v_lines[1].add_updater(lambda m: m.move_to(axes.c2p(get_sigma(), 0), DOWN))

        arrows = VGroup(Vector(LEFT), Vector(RIGHT))
        arrows.arrange(RIGHT, buff=0.25)
        arrows.match_color(v_lines)
        arrows.add_updater(lambda m: m.set_width(max(0.9 * v_lines.get_width(), 1e-5)))
        arrows.add_updater(lambda m: m.move_to(axes.c2p(0, 0.575 * axes.y_axis.x_max)))

        sigma_labels = Tex(R"\sigma").replicate(2)
        sigma_labels.set_color(RED)
        sigma_labels[0].add_updater(lambda m: m.next_to(arrows[0], UP, 0.15))
        sigma_labels[1].add_updater(lambda m: m.next_to(arrows[1], UP, 0.15))

        v_lines.suspend_updating()
        v_lines.save_state()
        v_lines.stretch(0.1, 0)
        v_lines.set_opacity(0)
        self.play(
            Restore(v_lines),
            ShowCreation(arrows, lag_ratio=0),
            FadeIn(sigma_labels)
        )
        v_lines.resume_updating()
        sd_group = VGroup(v_lines, arrows, sigma_labels)
        self.wait()
        for value in [2, math.sqrt(0.5)]:
            self.play(sigma_tracker.animate.set_value(value), run_time=3)
            self.wait()

        # Back to simple e^(-x^2)
        simple_form = Tex("e^{-x^2}", **kw)
        simple_form.to_edge(UP)

        self.remove(form_with_sigma)
        sd_group.save_state()
        self.play(
            FadeOut(sd_group),
            FadeOut(sigma_display),
            TransformMatchingTex(form_with_sigma.copy(), simple_form)
        )

        # We want the area to be 1
        ab_tracker = ValueTracker(np.array([-4, 4]))
        area = graph.copy()
        area.set_stroke(width=0)
        area.set_fill(YELLOW, 0.5)
        area.set_shading(0.5, 0.5)

        def update_area(area):
            a, b = ab_tracker.get_value()
            x_min, x_max = axes.x_range[:2]
            area.pointwise_become_partial(
                graph,
                (a - x_min) / (x_max - x_min),
                (b - x_min) / (x_max - x_min),
            )
            area.add_line_to(axes.c2p(b, 0))
            area.add_line_to(axes.c2p(a, 0))
            area.add_line_to(area.get_start())

        area.add_updater(update_area)

        note = Text("We want this area\nto be 1")
        note.next_to(axes.get_top(), DOWN)
        note.match_x(axes.c2p(2, 0))
        note.set_backstroke(width=5)
        note_arrow = Arrow(note.get_bottom() + LEFT, area.get_center())

        prob_label = Tex("p(a < x < b)")
        prob_label.move_to(axes.c2p(-2, 1.5))
        prob_arrow = Arrow(LEFT, RIGHT)
        prob_arrow.add_updater(lambda m: m.put_start_and_end_on(
            prob_label.get_bottom() + SMALL_BUFF * DOWN,
            area.get_center(),
        ))

        self.add(area, graph)
        self.play(
            FadeIn(area),
            Write(note, run_time=1),
            ShowCreation(note_arrow),
        )
        self.wait()
        self.play(
            Write(prob_label),
            ShowCreation(prob_arrow),
            ab_tracker.animate.set_value([-1, 0]),
            FadeOut(note),
            FadeOut(note_arrow),
        )
        self.wait()
        for value in [(-0.5, 0.5), (-1.5, -0.5), (0, 1), (-2, 1), (-4, 4)]:
            self.play(ab_tracker.animate.set_value(value), run_time=3)
            self.wait()
        self.play(
            FadeOut(prob_label),
            FadeOut(prob_arrow),
            FadeIn(note),
            FadeIn(note_arrow),
        )
        self.wait()

        self.remove(area)
        graph.set_fill(area.get_fill_color(), area.get_fill_opacity())

        # Normalize
        area_label = TexText(R"Area = $\sqrt{\pi}$", **kw)
        area_label.next_to(note_arrow.get_start(), UR, SMALL_BUFF)
        area_label.set_backstroke(width=5)
        graph.clear_updaters()

        normalized_form = Tex(R"{1 \over \sqrt{\pi}} e^{-x^2}", **kw)
        normalized_form[R"{1 \over \sqrt{\pi}}"].scale(0.8, about_edge=RIGHT)
        normalized_form.to_edge(UP, buff=MED_SMALL_BUFF)

        one = Tex("1", **kw)
        one.move_to(area_label[R"\sqrt{\pi}"], LEFT)
        one.align_to(area_label[0], DOWN)

        self.play(
            FadeOut(note, 0.5 * UP),
            FadeIn(area_label, 0.5 * UP),
        )
        self.wait()
        self.play(
            TransformMatchingTex(simple_form, normalized_form, run_time=1),
            FadeTransform(area_label[R"\sqrt{\pi}"], normalized_form[R"\sqrt{\pi}"]),
            graph.animate.stretch(1 / math.sqrt(PI), 1, about_edge=DOWN),
            note_arrow.animate.put_start_and_end_on(
                note_arrow.get_start(),
                note_arrow.get_end() + 0.5 * DOWN,
            )
        )
        self.play(Write(one))
        self.play(FlashAround(one))
        self.wait()

        # Show normalized form with sigma
        sigma_forms = [
            Tex(R"{1 \over \sqrt{\pi}} e^{-{1 \over 2}(x / \sigma)^2}", **kw),
            Tex(R"{1 \over \sigma \sqrt{2}} {1 \over \sqrt{\pi}} e^{-{1 \over 2}(x / \sigma)^2}", **kw),
            Tex(R"{1 \over \sigma \sqrt{2\pi}} e^{-{1 \over 2}(x / \sigma)^2}", **kw),
        ]
        for form in sigma_forms:
            e = form["e^"][0][0]
            form[:form.submobjects.index(e)].scale(0.7, about_edge=RIGHT)
            form.to_edge(UP, buff=MED_SMALL_BUFF)

        sqrt2_sigma = Tex(R"\sigma \sqrt{2}", **kw)
        sqrt2_sigma.move_to(one, LEFT)

        sigma_display.update()
        sd_group.restore().update()
        self.play(
            TransformMatchingTex(normalized_form, sigma_forms[0]),
            FadeIn(sigma_display),
            FadeIn(sd_group),
        )
        self.play(
            FadeOut(one, UP),
            FadeIn(sqrt2_sigma, UP),
            sigma_tracker.animate.set_value(1),
            graph.animate.stretch(math.sqrt(2), 0),
        )
        self.wait()
        self.play(
            TransformMatchingTex(*sigma_forms[:2], run_time=1),
            FadeTransform(sqrt2_sigma, sigma_forms[1][R"\sigma \sqrt{2}"][0]),
            graph.animate.stretch(1 / math.sqrt(2) / get_sigma(), 1, about_edge=DOWN),
            FadeIn(one),
        )
        self.wait()
        self.play(TransformMatchingTex(*sigma_forms[1:3]))
        self.play(FlashAround(sigma_forms[2][R"{1 \over \sigma \sqrt{2\pi}}"], run_time=3))
        self.wait()
        self.play(FlashAround(sigma_forms[2], run_time=3, time_width=1.0))

        axes.bind_graph_to_func(
            graph, lambda x: gauss_func(x, 0, get_sigma())
        )
        for value in [0.2, 0.5, math.sqrt(0.5)]:
            self.play(sigma_tracker.animate.set_value(value), run_time=3)
            self.wait()

        area_label[R"\sqrt{\pi}"].set_opacity(0)
        self.play(LaggedStartMap(FadeOut, VGroup(area_label, one, note_arrow)))
        self.wait()

        # Show standard form
        curr_form = sigma_forms[2].copy()
        self.remove(*sigma_forms)
        self.add(curr_form)
        standard_form = Tex(R"{1 \over \sqrt{2\pi}} e^{-{1 \over 2} x^2}", **kw)
        standard_form[R"{1 \over \sqrt{2\pi}}"].scale(0.7, about_edge=RIGHT)
        standard_form.move_to(curr_form)

        rect = SurroundingRectangle(standard_form)
        rect.set_stroke(BLUE, 2)
        std_words = Text("Standard\nnormal\ndistribution", alignment="LEFT")
        std_words.match_height(rect)
        std_words.scale(0.9)
        std_words.next_to(rect, RIGHT, buff=MED_LARGE_BUFF)
        std_words.set_color(BLUE)

        self.play(sigma_tracker.animate.set_value(1))
        self.play(TransformMatchingTex(curr_form, standard_form, run_time=1))

        one_labels = Integer(1).replicate(2)
        for ol, sl in zip(one_labels, sigma_labels):
            ol.match_style(sl)
            ol.move_to(sl)
            ol.shift(SMALL_BUFF * UP)

        self.play(
            FadeOut(sigma_labels, 0.1 * UP, lag_ratio=0.1),
            FadeIn(one_labels, 0.1 * UP, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            ShowCreation(rect),
            Write(std_words)
        )
        self.wait()

        self.play(
            FadeOut(rect),
            FadeOut(std_words),
            FadeOut(one_labels, 0.2 * DOWN),
            FadeIn(sigma_labels, 0.2 * DOWN),
            TransformMatchingTex(standard_form, sigma_forms[2])
        )

        # Add the mean
        final_form = formulas[-1].copy()
        final_form[:final_form.submobjects.index(final_form["e^"][0][0])].scale(0.75, about_edge=RIGHT)
        final_form.to_edge(UP, buff=MED_SMALL_BUFF)

        mu_display, mu_tracker = self.get_variable_display(R"\mu", PINK, (-2, 2))
        mu_tracker.set_value(0)
        mu_display.update()
        get_mu = mu_tracker.get_value
        mu_display.to_corner(UR, buff=MED_SMALL_BUFF)

        mu_line = v_lines[0].copy()
        mu_line.clear_updaters()
        mu_line.set_stroke(PINK, 3)
        mu_line.add_updater(lambda m: m.move_to(axes.c2p(get_mu(), 0), DOWN))
        mu_label = Tex(R"\mu")
        mu_label.match_color(mu_line)
        mu_label.set_backstroke(width=10)
        mu_label.add_updater(lambda m: m.next_to(mu_line, UP))
        sd_group.add_updater(lambda m: m.match_x(mu_line))
        self.add(sd_group)

        axes.bind_graph_to_func(graph, lambda x: gauss_func(x, get_mu(), get_sigma()))

        self.add(mu_label)
        self.play(
            TransformMatchingTex(
                sigma_forms[2], final_form,
                matched_pairs=[
                    (sigma_forms[2][R"/ \sigma"], final_form[R"\over \sigma"][1]),
                ],
                match_animation=FadeTransform,
                mismatch_animation=FadeTransform,
            ),
            ShowCreation(mu_line),
            FadeIn(mu_display),
        )
        self.wait()

        for value in [2, -2, 1]:
            self.play(mu_tracker.animate.set_value(value), run_time=3)
            self.wait()
        for value in [0.5, 1.5, 0.8]:
            self.play(sigma_tracker.animate.set_value(value), run_time=2)
            self.wait()

        # Added animations for an opening scene
        mu_tracker.set_value(0)
        sigma_tracker.set_value(0.5)

        ms_mobs = VGroup(
            mu_display,
            sigma_display,
            mu_line, mu_label,
            sd_group
        )

        self.remove(ms_mobs)
        self.wait()
        self.play(LaggedStartMap(FadeIn, ms_mobs, lag_ratio=0.2))
        pairs = [(1, 1.5), (1, 1.0), (1.5, 1.0), (1, 0.7), (0, 1)]
        for mu, sigma in pairs:
            self.play(
                mu_tracker.animate.set_value(mu),
                sigma_tracker.animate.set_value(sigma),
                run_time=3
            )
            self.wait()

    def get_variable_display(self, name, color, value_range):
        eq = Tex(f"{name} = 1.00", t2c={name: color})
        number = eq.make_number_changeable("1.00")

        tracker = ValueTracker(1)
        get_value = tracker.get_value
        number.add_updater(lambda c: c.set_value(get_value()))

        number_line = NumberLine(
            value_range,
            width=1.25,
            tick_size=0.05
        )
        number_line.rotate(90 * DEGREES)
        number_line.next_to(eq, RIGHT, MED_LARGE_BUFF)
        number_line.add_numbers(font_size=14, direction=LEFT, buff=0.15)
        slider = ArrowTip(angle=PI).set_width(0.15)
        slider.set_color(color)
        slider.add_updater(lambda m: m.move_to(number_line.n2p(get_value()), LEFT))

        display = VGroup(eq, number_line, slider)
        display.to_corner(UL, buff=MED_SMALL_BUFF)
        return display, tracker

    def get_axes(
        self,
        x_range=(-4, 4),
        y_range=(-1.0, 2.0, 1.0),
    ):
        axes = NumberPlane(
            x_range, y_range,
            width=FRAME_WIDTH,
            height=6,
            background_line_style=dict(
                stroke_color=GREY_A,
                stroke_width=2,
                stroke_opacity=0.5
            )
        )
        axes.shift(BOTTOM - axes.c2p(0, y_range[0]))
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers(num_decimal_places=1)
        return axes
