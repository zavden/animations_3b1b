# ==============================================================================
# Scene:      FiniteSampleWithMoreSamplePoints
# Source:     videos/_2017/eoc/chapter9.py (lines 629-632)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FiniteSampleWithMoreSamplePoints.py FiniteSampleWithMoreSamplePoints -w -m --fps 15
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


class FiniteSampleWithMoreSamplePoints(FiniteSample):
    CONFIG = {
        "dx" : 0.05
    }
