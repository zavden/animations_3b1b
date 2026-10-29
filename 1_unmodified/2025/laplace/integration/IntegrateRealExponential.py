# ==============================================================================
# Scene:      IntegrateRealExponential
# Source:     videos/_2025/laplace/integration.py (lines 119-576)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntegrateRealExponential.py IntegrateRealExponential -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntegrateRealExponential(InteractiveScene):
    def construct(self):
        # Add integral expression
        t2c = {R"{s}": YELLOW}
        integral = Tex(R"\int^\infty_0 e^{\minus {s}t} dt", t2c=t2c)
        integral.set_x(1)
        integral.to_edge(UP)
        integral.save_state()
        integral.scale(1.5, about_edge=UP)
        self.add(integral)

        # Add the graph of e^{-st}
        max_x = 15
        unit_size = 4
        axes = Axes((0, max_x, 0.25), (0, 1, 0.25), unit_size=unit_size)
        axes.to_edge(DL, buff=1.0)
        axes.add_coordinate_labels(num_decimal_places=2, font_size=20)

        def exp_func(t):
            return np.exp(-get_s() * t)

        s_tracker = ValueTracker(1)
        get_s = s_tracker.get_value
        graph = axes.get_graph(np.exp)
        graph.set_stroke(BLUE, 3)
        axes.bind_graph_to_func(graph, exp_func)

        graph_label = Tex(R"e^{\minus {s}t}", t2c=t2c, font_size=72)
        graph_label.next_to(axes.y_axis.get_top(), UR).shift(0.5 * RIGHT)

        self.play(
            FadeIn(axes),
            TransformFromCopy(integral[R"e^{\minus {s}t}"], graph_label),
            ShowCreation(graph, suspend_mobject_updating=True, run_time=3),
            Restore(integral),
        )

        # Add a slider for s
        s_slider = Slider(s_tracker, x_range=(0, 5), var_name="s")
        s_slider.scale(1.5)
        s_slider.to_edge(UP, buff=MED_LARGE_BUFF)
        s_slider.align_to(axes.c2p(0, 0), LEFT)

        self.play(VFadeIn(s_slider))
        for value in [5, 0.25, 1]:
            self.play(
                s_tracker.animate.set_value(value),
                run_time=4
            )
            self.wait()

        # Show integral as area
        equals = Tex(R"=", font_size=72).rotate(90 * DEG)
        equals.next_to(integral, DOWN)
        area_word = Text("Area", font_size=60)
        area_word.next_to(equals, DOWN)

        area = axes.get_area_under_graph(graph)

        def update_area(area):
            area.become(axes.get_area_under_graph(graph))

        arrow = Arrow(area_word.get_corner(DL), axes.c2p(0.75, 0.5), thickness=4)

        self.play(
            LaggedStart(
                Animation(graph.copy(), remover=True),
                Write(equals),
                FadeIn(area_word, DOWN),
                GrowArrow(arrow),
                UpdateFromFunc(area, update_area),
                lag_ratio=0.25
            ),
            ShowCreation(graph, suspend_mobject_updating=True, run_time=3),
        )
        self.wait()

        # Try altenrate s value
        frame = self.frame

        area.clear_updaters()
        area.add_updater(update_area)
        self.play(
            s_tracker.animate.set_value(-0.2),
            frame.animate.reorient(0, 0, 0, (16.79, 7.82, 0.0), 28.01).set_anim_args(time_span=(2, 5)),
            run_time=5
        )

        # Show area = 1 from s = 1
        simple_integral = Tex(R"\int^\infty_0 e^{\minus t} dt")
        simple_integral.move_to(integral)
        simple_exp = Tex(R"e^{\minus t}")
        simple_exp.move_to(graph_label)

        anti_deriv = Tex(R"=\big[\minus e^{\minus t} \big]^\infty_0")
        simple_rhs = Tex(R"=0 - (\minus 1)")
        anti_deriv.next_to(simple_integral, RIGHT)
        simple_rhs.next_to(anti_deriv, RIGHT)

        equals_one = Tex(R"= 1", font_size=60)
        equals_one.next_to(area_word)

        area_one_label = Tex(R"1", font_size=60)
        area_one_label.move_to(axes.c2p(0.35, 0.35))
        area_one_label.set_z_index(1)

        self.remove(integral, graph_label)
        self.play(
            TransformMatchingTex(integral.copy(), simple_integral),
            TransformMatchingTex(graph_label.copy(), simple_exp),
            run_time=1
        )
        self.play(
            TransformMatchingTex(simple_integral.copy(), anti_deriv, run_time=1.5, path_arc=30 * DEG),
        )
        rect_kw = dict(buff=0.05, stroke_width=1.5)
        self.play(
            FadeIn(simple_rhs[:2], time_span=(0, 1)),
            VFadeInThenOut(SurroundingRectangle(anti_deriv[R"\minus e^{\minus t}"], **rect_kw)),
            VFadeInThenOut(SurroundingRectangle(anti_deriv[R"\infty"], **rect_kw)),
            VFadeInThenOut(SurroundingRectangle(simple_rhs[:2], **rect_kw)),
            run_time=1.5
        )
        self.play(
            FadeIn(simple_rhs[2:], time_span=(0, 1)),
            VFadeInThenOut(SurroundingRectangle(anti_deriv[R"\minus e^{\minus t}"], **rect_kw)),
            VFadeInThenOut(SurroundingRectangle(anti_deriv[R"0"], **rect_kw)),
            VFadeInThenOut(SurroundingRectangle(simple_rhs[2:], **rect_kw)),
            run_time=1.5
        )
        self.wait()
        self.play(TransformMatchingTex(simple_rhs.copy(), equals_one, run_time=1))
        self.play(TransformFromCopy(equals_one["1"], area_one_label))
        self.wait()

        # Comapre to unit square
        square = Polygon(
            axes.c2p(0, 1),
            axes.c2p(1, 1),
            axes.c2p(1, 0),
            axes.c2p(0, 0),
        )
        square.set_stroke(WHITE, 3)
        square.set_fill(BLUE, 0.0)

        area_s_tracker = ValueTracker(get_s())
        area_x_max_tracker = ValueTracker(graph.x_range[1])
        squishy_area = always_redraw(  # Currently unused
            lambda: axes.get_area_under_graph(axes.get_graph(
                lambda t: np.exp(-area_s_tracker.get_value() * t),
                x_range=(0, area_x_max_tracker.get_value())
            ))
        )

        tail_area = axes.get_area_under_graph(graph, x_range=(1, 6))
        tail_area.set_fill(RED_E, 0.75)
        corner_area = axes.get_graph(lambda t: np.exp(-get_s() * t), (0, 1))
        corner_area.add_line_to(axes.c2p(1, 1))
        corner_area.add_line_to(axes.c2p(0, 1))
        corner_area.match_style(tail_area)
        corner_area.set_z_index(-2)

        area_one_label.save_state()

        self.play(FadeIn(tail_area))
        self.wait()
        self.play(
            ShowCreation(square),
            FadeIn(corner_area),
            area_one_label.animate.move_to(square),
        )
        self.wait()
        self.play(
            FadeOut(square),
            FadeOut(corner_area),
            FadeOut(tail_area),
            Restore(area_one_label),
            FadeOut(anti_deriv),
            FadeOut(simple_rhs)
        )
        self.wait()

        # Show squishing the area
        stretch_label = VGroup(
            TexText(R"Squish by $\frac{1}{s}$", t2c=t2c),
            Vector(2 * LEFT, thickness=5, fill_color=YELLOW)
        )
        stretch_label.arrange(DOWN, buff=MED_SMALL_BUFF)
        stretch_label.move_to(axes.c2p(0.5, 0.5))

        area_word.set_z_index(1)
        area_word.target = area_word.generate_target()
        area_word.target.move_to(axes.c2p(0.6, 0.33))

        rhs = Tex(R"= \frac{1}{s}", t2c=t2c, font_size=60)
        rhs.next_to(area_word.target, RIGHT)

        area.set_z_index(-1)
        area.add_updater(update_area)

        self.play(LaggedStart(
            TransformMatchingTex(simple_integral, integral, run_time=1),
            FadeIn(graph_label, 0.5 * DOWN),
            FadeOut(simple_exp, 0.5 * DOWN),
            FadeOut(equals_one, 0.5 * DOWN),
            FadeOut(area_one_label),
            lag_ratio=0.1
        ))
        self.play(
            s_tracker.animate.set_value(5).set_anim_args(run_time=8),
            FadeIn(stretch_label, 1.5 * LEFT, time_span=(1, 5)),
            FadeOut(arrow),
        )
        self.wait()
        self.play(
            LaggedStart(
                FadeOut(stretch_label),
                MoveToTarget(area_word),
                FadeTransform(stretch_label[0][-3:].copy(), rhs[1:]),
                FadeTransform(stretch_label[1].copy(), rhs[0]),
                FadeOut(equals),
                run_time=2,
                lag_ratio=0.1
            )
        )

        # Show area value
        dec_rhs = Tex(R"= 1.00", font_size=60)
        dec_rhs.make_number_changeable("1.00").add_updater(lambda m: m.set_value(1 / get_s()))
        dec_rhs.always.next_to(rhs, RIGHT)

        self.play(
            VFadeIn(dec_rhs),
            s_tracker.animate.set_value(0.01).set_anim_args(run_time=12, rate_func=bezier([0, 1, 1, 1])),
            self.frame.animate.reorient(0, 0, 0, (15.36, 0, 0.0), 30).set_anim_args(time_span=(6, 11)),
        )
        self.wait()
        self.play(
            VGroup(area_word, rhs).animate.next_to(axes.c2p(0, 0), UR, MED_LARGE_BUFF).set_anim_args(time_span=(1, 3)),
            s_tracker.animate.set_value(0.75),
            VFadeOut(dec_rhs, time_span=(2, 4)),
            self.frame.animate.to_default_state(),
            run_time=4,
        )
        self.wait()

        # Averages over intervals
        v_lines = VGroup(
            DashedLine(axes.c2p(0, 0), axes.c2p(0, 1.25)),
            DashedLine(axes.c2p(1, 0), axes.c2p(1, 1.25)),
        )
        v_lines.set_stroke(WHITE, 1)

        unit_int = Tex(R"\int^1_0 e^{\minus {s}t} dt", t2c=t2c, font_size=60)
        unit_int.move_to(v_lines, UP)

        graph_for_unit_area = axes.get_graph(exp_func)
        graph_for_unit_area.set_stroke(width=0)
        unit_int_area = always_redraw(
            lambda: axes.get_area_under_graph(graph_for_unit_area, (0, 1))
        )
        avg_value = exp_func(np.linspace(0, 1, 1000)).mean()

        def slosh_rate_func(t, cycles=3):
            return min(smooth(2 * cycles * t), 1) + 0.7 * math.sin(cycles * TAU * t) * (t - 1)**2

        self.remove(integral)
        area.clear_updaters()
        self.play(
            *map(FadeOut, [area_word, rhs, graph_label, s_slider]),
            *map(ShowCreation, v_lines),
            TransformMatchingTex(integral.copy(), unit_int),
            FadeOut(area),
            FadeIn(unit_int_area, time_span=(0.5, 1), suspend_mobject_updating=True),
        )
        self.wait()
        self.play(
            Transform(
                graph_for_unit_area,
                axes.get_graph(lambda t: avg_value).set_stroke(width=0),
                run_time=3,
                rate_func=slosh_rate_func,
            ),
        )
        unit_int_area.suspend_updating()

        # Show average
        avg_label1 = self.get_avg_label(unit_int_area, 0, 1)
        avg_label1.save_state()
        avg_label1.space_out_submobjects(0.5)
        avg_label1.set_opacity(0)
        self.play(Restore(avg_label1))
        self.wait()

        # Emphasize that it's a unit interval
        frame = self.frame
        unit_line = Line(axes.c2p(0, 0), axes.c2p(1, 0))
        unit_line.set_stroke(YELLOW, 5)
        brace = Brace(unit_line, DOWN, buff=MED_LARGE_BUFF)
        unit_label = brace.get_tex("1", buff=MED_SMALL_BUFF, font_size=72)
        unit_group = VGroup(brace, unit_line, unit_label)

        self.play(LaggedStart(
            GrowFromCenter(brace),
            ShowCreation(unit_line),
            FadeIn(unit_label, 0.25 * DOWN),
            frame.animate.set_y(-1.5),
            run_time=1.5
        ))
        self.wait()

        # Area = height
        height_line = Line(unit_int_area.get_corner(DL), unit_int_area.get_corner(UL))
        height_line.set_stroke(RED, 5)

        area_eq_height = TexText(R"= Area = Width $\times$ Height", t2c={"Area": BLUE, "Height": RED, "Width": YELLOW})
        area_eq_height.next_to(unit_int, RIGHT)
        fade_rect = BackgroundRectangle(area_eq_height, buff=0.25, fill_opacity=1)
        fade_rect.stretch(2, 1, about_edge=DOWN)

        sample_dots = DotCloud([axes.c2p(a, exp_func(a)) for a in np.linspace(0, 1, 30)])
        sample_dots.set_color(WHITE)
        sample_dots.set_glow_factor(2)
        sample_dots.set_radius(0.15)

        self.play(
            FadeIn(fade_rect),
            FadeIn(area_eq_height),
            ShowCreation(height_line),
        )
        self.wait()
        self.play(
            area_eq_height[R"Width $\times$"].animate.set_opacity(0),
            area_eq_height[R"Height"].animate.move_to(area_eq_height["Width"], UL),
        )
        self.wait()
        self.play(FlashAround(unit_int, run_time=2, time_width=1.5))
        self.wait()

        self.play(ShowCreation(sample_dots))
        self.play(sample_dots.animate.stretch(0, 1).match_y(axes.c2p(0, avg_value)), rate_func=lambda t: slosh_rate_func(t, 2), run_time=3)
        self.play(FadeOut(sample_dots), FadeOut(height_line), FadeOut(area_eq_height))

        # Average over next interval
        v_lines2 = v_lines.copy()
        v_lines2.move_to(axes.c2p(1, 0), DL)
        unit_int2 = Tex(R"\int^2_1 e^{\minus {s}t} dt", t2c=t2c, font_size=60)
        unit_int2.move_to(v_lines2, UP)

        area2_graph = graph.copy().clear_updaters().set_stroke(width=0)
        pile2 = always_redraw(lambda: axes.get_area_under_graph(area2_graph, (1, 2)))
        avg_value2 = get_norm(pile2.get_area_vector()) / (axes.x_axis.get_unit_size()**2)
        avg_label2 = self.get_avg_label(
            pile2.copy().set_height(axes.y_axis.get_unit_size() * avg_value2, stretch=True, about_edge=DOWN),
            1, 2
        )

        self.add(v_lines[0])
        self.play(
            TransformFromCopy(v_lines, v_lines2, path_arc=-20 * DEG),
            TransformMatchingTex(
                unit_int.copy(),
                unit_int2,
                path_arc=-20 * DEG,
                run_time=1,
                key_map={"0": "1", "1": 2},
            ),
            FadeIn(pile2, suspend_mobject_updating=True),
            unit_group.animate.match_x(pile2),
        )
        self.play(
            area2_graph.animate.stretch(0, 1).match_y(axes.y_axis.n2p(avg_value2)).set_anim_args(
                rate_func=slosh_rate_func,
                run_time=3,
            ),
            FadeIn(avg_label2)
        )
        pile2.clear_updaters()
        self.wait()

        # Show all integrals
        new_groups = VGroup()
        piles = VGroup(unit_int_area, pile2)
        avg_labels = VGroup(avg_label1, avg_label2)

        for n in range(2, 6):
            new_v_lines = v_lines.copy()
            new_v_lines.move_to(axes.c2p(n, 0), DL)
            new_unit_int = Tex(Rf"\int^{n + 1}_{n} " + R"e^{\minus {s}t} dt", t2c=t2c, font_size=60)
            if n == 5:
                new_unit_int = Tex(R"\cdots", font_size=90)
            new_unit_int.match_y(unit_int)
            new_unit_int.match_x(new_v_lines)
            s = get_s()
            avg_y = np.mean([np.exp(-s * t) for t in np.arange(n, n + 1, 1e-3)])
            new_pile = pile2.copy().clear_updaters()
            new_pile.set_height(avg_y * axes.y_axis.get_unit_size(), stretch=True)
            new_pile.move_to(axes.c2p(n, 0), DL)
            new_avg_label = self.get_avg_label(new_pile, n, n + 1)

            new_group = VGroup(new_v_lines, new_unit_int, new_pile, new_avg_label)
            new_groups.add(new_group)
            piles.add(new_pile)
            avg_labels.add(new_avg_label)

        big_brace = Brace(VGroup(unit_int, new_groups[-1][1]), UP, font_size=90, buff=LARGE_BUFF)
        integral.set_height(3)
        integral.next_to(big_brace, UP, buff=LARGE_BUFF)

        self.play(
            self.frame.animate.reorient(0, 0, 0, (5.34, 2.63, 0.0), 13.89),
            LaggedStartMap(FadeIn, new_groups, lag_ratio=0.75),
            FadeOut(unit_group, time_span=(0, 2)),
            run_time=4
        )
        self.play(
            GrowFromCenter(big_brace),
            FadeIn(integral),
        )
        self.wait()

        # Show adding all the heights
        height_vects = VGroup(
            Arrow(pile.get_bottom(), pile.get_top(), buff=0, thickness=6, fill_color=RED)
            for pile in piles
        )

        equals = Tex(R"=", font_size=120)
        equals.move_to(integral).shift(RIGHT)

        stacked_vects = height_vects.copy()
        stacked_vects.arrange(UP, buff=SMALL_BUFF)
        stacked_vects.scale(0.9)
        stacked_vects.next_to(equals, RIGHT, LARGE_BUFF)

        self.play(
            LaggedStartMap(FadeOut, avg_labels, lag_ratio=0.2),
            LaggedStartMap(FadeIn, height_vects, lag_ratio=0.2),
            run_time=1,
        )
        self.wait()
        self.play(
            TransformFromCopy(height_vects, stacked_vects, lag_ratio=0.05, run_time=2),
            integral.animate.next_to(equals, LEFT, LARGE_BUFF),
            Write(equals),
        )
        self.wait()

    def get_avg_label(self, pile, start=0, end=1, font_size=30):
        word = Text(f"Average over [{start}, {end}]", font_size=font_size)
        word.move_to(pile)
        word.set_max_height(pile.get_height() / 4)
        buff = min(SMALL_BUFF, 0.05 * pile.get_height())
        arrows = VGroup(
            Arrow(word.get_top() + buff * UP, pile.get_top(), buff=0),
            Arrow(word.get_bottom() + buff * DOWN, pile.get_bottom(), buff=0),
        )
        return VGroup(word, arrows)
