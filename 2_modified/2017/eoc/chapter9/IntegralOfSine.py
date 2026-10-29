# ==============================================================================
# Scene:      IntegralOfSine
# Source:     videos/_2017/eoc/chapter9.py (lines 643-961)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntegralOfSine.py IntegralOfSine -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
# ==============================================================================

import fractions
from manim_imports_ext import *

class AverageOfContinuousVariable(GraphScene):
    CONFIG = {
        "bounds" : [1, 7],
        "bound_colors" : [RED, GREEN],
    }
    def construct(self):
        self.setup_axes()
        graph = self.get_graph(
            lambda x : 0.1*x*(x-3)*(x-6) + 4
        )
        graph_label = self.get_graph_label(graph, "f(x)")
        boundary_lines = self.get_vertical_lines_to_graph(
            graph, *self.bounds, num_lines = 2,
            line_class = DashedLine
        )
        for line, color in zip(boundary_lines, self.bound_colors):
            line.set_color(color)
        v_line = self.get_vertical_line_to_graph(
            self.bounds[0], graph, color = YELLOW,
        )

        question = OldTexText(
            "What is the average \\\\ value of $f(x)$?"
        )
        question.next_to(boundary_lines, UP)

        self.play(ShowCreation(graph), Write(graph_label))
        self.play(ShowCreation(boundary_lines))
        self.play(FadeIn(
            question,
            run_time = 2,
            lag_ratio = 0.5,
        ))
        self.play(ShowCreation(v_line))
        for bound in reversed(self.bounds):
            self.play(self.get_v_line_change_anim(
                v_line, graph, bound, 
                run_time = 3,
            ))
            self.wait()
        self.wait()

    def get_v_line_change_anim(self, v_line, graph, target_x, **kwargs):
        start_x = self.x_axis.point_to_number(v_line.get_bottom())
        def update(v_line, alpha):
            new_x = interpolate(start_x, target_x, alpha)
            v_line.put_start_and_end_on(
                self.coords_to_point(new_x, 0),
                self.input_to_graph_point(new_x, graph)
            )
            return v_line
        return UpdateFromAlphaFunc(v_line, update, **kwargs)


class AverageOfSineStart(AverageOfContinuousVariable):
    CONFIG = {
        "y_min" : -2, 
        "y_max" : 2,
        "x_min" : -1,
        "x_max" : 2.5*np.pi,
        "x_leftmost_tick" : 0,
        "x_tick_frequency" : np.pi/4,
        "x_axis_width" : 12,
        "graph_origin" : 5*LEFT,
        "x_label_scale_val" : 0.75,
        "func" : np.sin,
        "graph_color" : BLUE,
        "bounds" : [0, np.pi],
    }
    def construct(self):
        self.setup_axes()
        self.add_graph()
        self.ask_about_average()

    def add_graph(self, run_time = 1):
        graph = self.get_graph(self.func, color = self.graph_color)
        graph_label = self.get_graph_label(
            graph, "\\sin(x)",
            direction = UP
        )
        self.play(
            ShowCreation(graph),
            Write(graph_label),
            run_time = run_time
        )

        self.graph = graph
        self.graph_label = graph_label

    def ask_about_average(self):
        half_period_graph = self.get_graph_portion_between_bounds()
        question = OldTexText("Average height?")
        question.to_edge(UP)
        arrow = Arrow(question.get_bottom(), half_period_graph.get_top())
        midpoint = np.mean(self.bounds)
        v_line = self.get_vertical_line_to_graph(
            midpoint, self.graph,
            line_class = DashedLine,
            color = WHITE
        )

        self.play(FadeIn(half_period_graph))
        self.play(
            Write(question, run_time = 2),
            ShowCreation(arrow)
        )
        self.play(ShowCreation(v_line))
        for bound in self.bounds + [midpoint]:
            self.play(self.get_v_line_change_anim(
                v_line, self.graph, bound,
                run_time = 3
            ))

    #########

    def get_graph_portion_between_bounds(self):
        self.graph_portion_between_bounds = self.get_graph(
            self.func,
            x_min = self.bounds[0],
            x_max = self.bounds[1],
            color = YELLOW
        )
        return self.graph_portion_between_bounds

    def setup_axes(self):
        GraphScene.setup_axes(self)
        self.add_x_axis_labels()

    def add_x_axis_labels(self):
        labels_and_x_values = [
            ("\\pi/2", np.pi/2),
            ("\\pi", np.pi),
            ("3\\pi/2", 3*np.pi/2),
            ("2\\pi", 2*np.pi),
        ]
        self.x_axis_labels = VGroup()
        for label, x in labels_and_x_values:
            tex_mob = OldTex(label)
            tex_mob.scale(self.x_label_scale_val)
            tex_mob.move_to(
                self.coords_to_point(x, -3*self.x_axis.tick_size), 
            )
            self.add(tex_mob)
            self.x_axis_labels.add(tex_mob)


class TryToAddInfinitelyManyPoints(AverageOfSineStart):
    CONFIG = {
        "max_denominator" : 40,
    }
    def construct(self):
        self.add_graph()
        self.try_to_add_infinitely_many_values()
        self.show_continuum()
        self.mention_integral()

    def add_graph(self):
        self.setup_axes()
        AverageOfSineStart.add_graph(self, run_time = 0)
        self.add(self.get_graph_portion_between_bounds())
        self.graph_label.to_edge(RIGHT)
        self.graph_label.shift(DOWN)

    def try_to_add_infinitely_many_values(self):
        v_lines = VGroup(*[
            self.get_vertical_line_to_graph(
                numerator*np.pi/denominator, self.graph,
                color = YELLOW,
                stroke_width = 6./denominator
            )
            for denominator in range(self.max_denominator)
            for numerator in range(1, denominator)
            if fractions.gcd(numerator, denominator) == 1
        ])
        ghost_lines = v_lines.copy().set_stroke(GREY)

        v_lines.generate_target()
        start_lines = VGroup(*v_lines.target[:15])
        end_lines = VGroup(*v_lines.target[15:])

        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        plusses = VGroup(*[OldTex("+") for x in start_lines])
        sum_eq = VGroup(*it.chain(*list(zip(start_lines, plusses))))
        sum_eq.add(*end_lines)
        sum_eq.arrange(RIGHT)
        sum_eq.next_to(v_lines[0], UP, aligned_edge = LEFT)
        sum_eq.to_edge(UP, buff = MED_SMALL_BUFF)

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(start_lines.get_width())
        h_line.set_color(WHITE)
        h_line.next_to(sum_eq, DOWN, aligned_edge = LEFT)

        infinity = OldTex("\\infty")
        infinity.next_to(h_line, DOWN)

        self.play(ShowCreation(
            v_lines, 
            run_time = 3,
        ))
        self.add(ghost_lines, v_lines)
        self.wait(2)
        self.play(
            MoveToTarget(
                v_lines,
                run_time = 3,
                lag_ratio = 0.5
            ),
            Write(plusses)
        )
        self.play(ShowCreation(h_line))
        self.play(Write(infinity))
        self.wait()

    def show_continuum(self):
        arrow = Arrow(ORIGIN, UP+LEFT)
        input_range = Line(*[
            self.coords_to_point(bound, 0)
            for bound in self.bounds
        ])
        VGroup(arrow, input_range).set_color(RED)

        self.play(FadeIn(arrow))
        self.play(
            arrow.next_to, input_range.get_start(), 
            DOWN+RIGHT, SMALL_BUFF
        )
        self.play(
            arrow.next_to, input_range.copy().get_end(), 
            DOWN+RIGHT, SMALL_BUFF,
            ShowCreation(input_range),
            run_time = 3,
        )
        self.play(
            arrow.next_to, input_range.get_start(), 
            DOWN+RIGHT, SMALL_BUFF,
            run_time = 3
        )
        self.play(FadeOut(arrow))
        self.wait()

    def mention_integral(self):
        randy = Randolph()
        randy.to_edge(DOWN)
        randy.shift(3*LEFT)

        self.play(FadeIn(randy))
        self.play(PiCreatureBubbleIntroduction(
            randy, "Use an integral!",
            bubble_type = ThoughtBubble,
            target_mode = "hooray"
        ))
        self.play(Blink(randy))
        curr_bubble = randy.bubble
        new_bubble = randy.get_bubble("Somehow...")
        self.play(
            Transform(curr_bubble, new_bubble),
            Transform(curr_bubble.content, new_bubble.content),
            randy.change_mode, "shruggie",
        )
        self.play(Blink(randy))
        self.wait()


class FiniteSample(TryToAddInfinitelyManyPoints):
    CONFIG = {
        "dx" : 0.1,
        "graph_origin" : 6*LEFT + 0.5*DOWN,
    }
    def construct(self):
        self.add_graph()
        self.show_finite_sample()

    def show_finite_sample(self):
        v_lines = self.get_sample_lines(dx = self.dx)
        summed_v_lines = v_lines.copy()
        plusses = VGroup(*[
            OldTex("+").scale(0.75)
            for l in v_lines
        ])
        numerator = VGroup(*it.chain(*list(zip(summed_v_lines, plusses))))
        for group in numerator, plusses:
            group.remove(plusses[-1])
        numerator.arrange(
            RIGHT, 
            buff = SMALL_BUFF,
            aligned_edge = DOWN
        )
        # numerator.set_width(FRAME_X_RADIUS)
        numerator.scale(0.5)
        numerator.move_to(self.coords_to_point(3*np.pi/2, 0))
        numerator.to_edge(UP)
        frac_line = OldTex("\\over \\,")
        frac_line.stretch_to_fit_width(numerator.get_width())
        frac_line.next_to(numerator, DOWN)
        denominator = OldTexText("(Num. samples)")
        denominator.next_to(frac_line, DOWN)

        self.play(ShowCreation(v_lines, run_time = 3))
        self.wait()
        self.play(
            ReplacementTransform(
                v_lines.copy(),
                summed_v_lines,
                run_time = 3,
                lag_ratio = 0.5
            ),
            Write(
                plusses,
                rate_func = squish_rate_func(smooth, 0.3, 1)
            )
        )
        self.play(Write(frac_line, run_time = 1))
        self.play(Write(denominator))
        self.wait()

        self.plusses = plusses
        self.average = VGroup(numerator, frac_line, denominator)
        self.v_lines = v_lines

    ###

    def get_sample_lines(self, dx, color = YELLOW, stroke_width = 2):
        return VGroup(*[
            self.get_vertical_line_to_graph(
                x, self.graph,
                color = color,
                stroke_width = stroke_width,
            )
            for x in np.arange(
                self.bounds[0]+dx, 
                self.bounds[1], 
                dx
            )
        ])


class IntegralOfSine(FiniteSample):
    CONFIG = {
        "thin_dx" : 0.01,
        "rect_opacity" : 0.75,
    }
    def construct(self):
        self.force_skipping()
        FiniteSample.construct(self)
        self.remove(self.y_axis_label_mob)
        self.remove(*self.x_axis_labels[::2])
        self.revert_to_original_skipping_status()

        self.put_average_in_corner()
        self.write_integral()
        self.show_riemann_rectangles()
        self.let_dx_approach_zero()
        self.bring_back_average()
        self.distribute_dx()
        self.let_dx_approach_zero(restore = False)
        self.write_area_over_width()
        self.show_moving_v_line()

    def put_average_in_corner(self):
        self.average.save_state()
        self.plusses.set_stroke(width = 0.5)
        self.play(
            self.average.scale, 0.75,
            self.average.to_corner, DOWN+RIGHT,
        )

    def write_integral(self):
        integral = OldTex("\\int_0^\\pi", "\\sin(x)", "\\,dx")
        integral.move_to(self.graph_portion_between_bounds)
        integral.to_edge(UP)

        self.play(Write(integral))
        self.wait(2)

        self.integral = integral

    def show_riemann_rectangles(self):
        kwargs = {
            "dx" : self.dx,
            "x_min" : self.bounds[0],
            "x_max" : self.bounds[1],
            "fill_opacity" : self.rect_opacity,
        }
        rects = self.get_riemann_rectangles(self.graph, **kwargs)
        rects.set_stroke(YELLOW, width = 1)
        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda x : 0),
            **kwargs
        )
        thin_kwargs = dict(kwargs)
        thin_kwargs["dx"] = self.thin_dx
        thin_kwargs["stroke_width"] = 0
        self.thin_rects = self.get_riemann_rectangles(
            self.graph,
            **thin_kwargs
        )


        start_index = 20
        end_index = start_index + 5
        low_opacity = 0.5
        high_opacity = 1

        start_rect = rects[start_index]
        side_brace = Brace(start_rect, LEFT, buff = SMALL_BUFF)
        bottom_brace = Brace(start_rect, DOWN, buff = SMALL_BUFF)
        sin_x = OldTex("\\sin(x)")
        sin_x.next_to(side_brace, LEFT, SMALL_BUFF)
        dx = bottom_brace.get_text("$dx$", buff = SMALL_BUFF)

        self.transform_between_riemann_rects(
            flat_rects, rects,
            replace_mobject_with_target_in_scene = True,
        )
        self.remove(self.v_lines)
        self.wait()

        rects.save_state()
        self.play(*it.chain(
            [
                ApplyMethod(
                    rect.set_style_data, BLACK, 1,
                    None, #Fill color
                    high_opacity if rect is start_rect else low_opacity
                )
                for rect in rects
            ],
            list(map(GrowFromCenter, [side_brace, bottom_brace])),
            list(map(Write, [sin_x, dx])),
        ))
        self.wait()
        for i in range(start_index+1, end_index):
            self.play(
                rects[i-1].set_fill, None, low_opacity,
                rects[i].set_fill, None, high_opacity,
                side_brace.set_height, rects[i].get_height(),
                side_brace.next_to, rects[i], LEFT, SMALL_BUFF,
                bottom_brace.next_to, rects[i], DOWN, SMALL_BUFF,
                MaintainPositionRelativeTo(sin_x, side_brace),
                MaintainPositionRelativeTo(dx, bottom_brace),
            )
            self.wait()
        self.play(
            rects.restore,
            *list(map(FadeOut, [sin_x, dx, side_brace, bottom_brace]))
        )

        self.rects = rects
        self.dx_brace = bottom_brace
        self.dx_label = dx

    def let_dx_approach_zero(self, restore = True):
        start_state = self.rects.copy()
        self.transform_between_riemann_rects(
            self.rects, self.thin_rects,
            run_time = 3
        )
        self.wait(2)
        if restore:
            self.transform_between_riemann_rects(
                self.rects, start_state.copy(),
                run_time = 2,
            )
            self.remove(self.rects)
            self.rects = start_state
            self.rects.set_fill(opacity = 1)
            self.play(
                self.rects.set_fill, None,
                    self.rect_opacity,
            )
            self.wait()

    def bring_back_average(self):
        num_samples = self.average[-1]

        example_dx = OldTex("0.1")
        example_dx.move_to(self.dx_label)

        input_range = Line(*[
            self.coords_to_point(bound, 0)
            for bound in self.bounds
        ])
        input_range.set_color(RED)

        #Bring back average
        self.play(
            self.average.restore,
            self.average.center,
            self.average.to_edge, UP,
            self.integral.to_edge, DOWN,
            run_time = 2
        )
        self.wait()
        self.play(
            Write(self.dx_brace),
            Write(self.dx_label),
        )
        self.wait()
        self.play(
            FadeOut(self.dx_label),
            FadeIn(example_dx)
        )
        self.play(Indicate(example_dx))
        self.wait()
        self.play(ShowCreation(input_range))
        self.play(FadeOut(input_range))
        self.wait()

        #Ask how many there are
        num_samples_copy = num_samples.copy()
        v_lines = self.v_lines
        self.play(*[
            ApplyFunction(
                lambda l : l.shift(0.5*UP).set_color(GREEN),
                line,
                rate_func = squish_rate_func(
                    there_and_back, a, a+0.3
                ),
                run_time = 3,
            )
            for line, a in zip(
                self.v_lines, 
                np.linspace(0, 0.7, len(self.v_lines))
            )
        ] + [
            num_samples_copy.set_color, GREEN
        ])
        self.play(FadeOut(v_lines))
        self.wait()

        #Count number of samples
        num_samples_copy.generate_target()
        num_samples_copy.target.shift(DOWN + 0.5*LEFT)
        rhs = OldTex("\\approx", "\\pi", "/", "0.1")
        rhs.next_to(num_samples_copy.target, RIGHT)
        self.play(
            MoveToTarget(num_samples_copy),
            Write(rhs.get_part_by_tex("approx")),
        )
        self.play(ShowCreation(input_range))
        self.play(ReplacementTransform(
            self.x_axis_labels[1].copy(), 
            rhs.get_part_by_tex("pi")
        ))
        self.play(FadeOut(input_range))
        self.play(
            ReplacementTransform(
                example_dx.copy(), 
                rhs.get_part_by_tex("0.1")
            ),
            Write(rhs.get_part_by_tex("/"))
        )
        self.wait(2)

        #Substitute number of samples
        self.play(ReplacementTransform(
            example_dx, self.dx_label
        ))
        dx = rhs.get_part_by_tex("0.1") 
        self.play(Transform(
            dx, OldTex("dx").move_to(dx)
        ))
        self.wait(2)
        approx = rhs.get_part_by_tex("approx")
        rhs.remove(approx)
        self.play(
            FadeOut(num_samples),
            FadeOut(num_samples_copy),
            FadeOut(approx),
            rhs.next_to, self.average[1], DOWN
        )
        self.wait()

        self.pi_over_dx = rhs

    def distribute_dx(self):
        numerator, frac_line, denominator = self.average
        pi, over, dx = self.pi_over_dx
        integral = self.integral

        dx.generate_target()
        lp, rp = parens = OldTex("()")
        parens.set_height(numerator.get_height())
        lp.next_to(numerator, LEFT)
        rp.next_to(numerator, RIGHT)
        dx.target.next_to(rp, RIGHT)

        self.play(
            MoveToTarget(dx, path_arc = np.pi/2),
            Write(parens),
            frac_line.stretch_to_fit_width, 
                parens.get_width() + dx.get_width(),
            frac_line.shift, dx.get_width()*RIGHT/2,
            FadeOut(over)
        )
        self.wait(2)

        average = VGroup(parens, numerator, dx, frac_line, pi)
        integral.generate_target()
        over_pi = OldTex("\\frac{\\phantom{\\int \\sin(x)\\dx}}{\\pi}")
        integral.target.set_width(over_pi.get_width())
        integral.target.next_to(over_pi, UP)
        integral_over_pi = VGroup(integral.target, over_pi)
        integral_over_pi.to_corner(UP+RIGHT)
        arrow = Arrow(LEFT, RIGHT)
        arrow.next_to(integral.target, LEFT)

        self.play(
            average.scale, 0.9,
            average.next_to, arrow, LEFT,
            average.shift_onto_screen,
            ShowCreation(arrow),
            Write(over_pi),
            MoveToTarget(integral, run_time = 2)
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [self.dx_label, self.dx_brace])))

        self.integral_over_pi = VGroup(integral, over_pi)
        self.average = average
        self.average_arrow = arrow

    def write_area_over_width(self):
        self.play(
            self.integral_over_pi.shift, 2*LEFT,
            *list(map(FadeOut, [self.average, self.average_arrow]))
        )

        average_height = OldTexText("Average height = ")
        area_over_width = OldTex(
            "{\\text{Area}", "\\over\\,", "\\text{Width}}", "="
        )
        area_over_width.get_part_by_tex("Area").set_color_by_gradient(
            BLUE, GREEN
        )
        area_over_width.next_to(self.integral_over_pi[1][0], LEFT)
        average_height.next_to(area_over_width, LEFT)

        self.play(*list(map(FadeIn, [average_height, area_over_width])))
        self.wait()

    def show_moving_v_line(self):
        mean = np.mean(self.bounds)
        v_line = self.get_vertical_line_to_graph(
            mean, self.graph,
            line_class = DashedLine,
            color = WHITE,
        )
        self.play(ShowCreation(v_line))
        for count in range(2):
            for x in self.bounds + [mean]:
                self.play(self.get_v_line_change_anim(
                    v_line, self.graph, x,
                    run_time = 3
                ))
