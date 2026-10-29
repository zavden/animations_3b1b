# ==============================================================================
# Scene:      ExampleIntegralProblems
# Source:     videos/_2017/eoc/chapter1.py (lines 1793-1985)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExampleIntegralProblems.py ExampleIntegralProblems -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - class(PiCreatureScene, GraphScene): GL PiCreatureScene.setup does not chain to GraphScene.setup (default_graph_colors_cycle missing); call both
#   - Python 2 integer division used as list index
# ==============================================================================

from manim_imports_ext import *

class ExampleIntegralProblems(PiCreatureScene, GraphScene):
    CONFIG = {
        "dt" : 0.2,
        "t_max" : 7,
        "x_max" : 8,
        "y_axis_height" : 5.5,
        "x_axis_label" : "$t$",
        "y_axis_label" : "",
        # CHANGE: class(PiCreatureScene, GraphScene): GL PiCreatureScene.setup does not chain to GraphScene.setup (default_graph_colors_cycle missing); call both
        "graph_origin" : 3*DOWN + 4.5*LEFT
    }
    def setup(self):
        PiCreatureScene.setup(self)
        GraphScene.setup(self)
    def construct(self):
        self.write_integral_condition()
        self.show_car()
        self.show_graph()
        self.let_dt_approach_zero()
        self.show_confusion()

    def write_integral_condition(self):
        words = OldTexText(
            "Hard problem $\\Rightarrow$ Sum of many small values"
        )
        words.to_edge(UP)

        self.play(
            Write(words),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.wait()

        self.words = words

    def show_car(self):
        car = Car()
        start, end = 3*LEFT+UP, 5*RIGHT+UP
        car.move_to(start)

        line = Line(start, end)
        tick_height = MED_SMALL_BUFF
        ticks = VGroup(*[
            Line(
                p+tick_height*UP/2,
                p+tick_height*DOWN/2,
                color = YELLOW,
                stroke_width = 2
            )
            for t in np.arange(0, self.t_max, self.dt)
            for p in [
                line.point_from_proportion(smooth(t/self.t_max))
            ]
        ])

        index = int(len(ticks)/2)
        brace_ticks = VGroup(*ticks[index:index+2])
        brace = Brace(brace_ticks, UP)
        v_dt = OldTex("v(t)", "dt")
        v_dt.next_to(brace, UP, SMALL_BUFF)
        v_dt.set_color(YELLOW)
        v_dt_brace_group = VGroup(brace, v_dt)

        self.play(
            FadeIn(car),
            self.pi_creature.change_mode, "plain"
        )
        self.play(
            MoveCar(car, end),
            FadeIn(
                ticks, 
                lag_ratio=1,
                rate_func=linear,
            ),
            ShowCreation(line),
            FadeIn(
                v_dt_brace_group,
                rate_func = squish_rate_func(smooth, 0.6, 0.8)
            ),
            run_time = self.t_max
        )
        self.wait()
        for mob in v_dt:
            self.play(Indicate(mob))
            self.wait(2)

        self.v_dt_brace_group = v_dt_brace_group
        self.line = line
        self.ticks = ticks
        self.car = car

    def show_graph(self):
        self.setup_axes()
        self.remove(self.axes)
        s_graph = self.get_graph(
            lambda t : 1.8*self.y_max*smooth(t/self.t_max)
        )
        v_graph = self.get_derivative_graph(s_graph)
        rects = self.get_riemann_rectangles(
            v_graph,
            x_min = 0, 
            x_max = self.t_max,
            dx = self.dt
        )
        rects.set_fill(opacity = 0.5)
        pre_rects = rects.copy()
        pre_rects.rotate(-np.pi/2)
        for index, pre_rect in enumerate(pre_rects):
            # CHANGE: Python 2 integer division used as list index
            ti1 = len(self.ticks)*index//len(pre_rects)
            ti2 = min(ti1+1, len(self.ticks)-1)
            tick_pair = VGroup(self.ticks[ti1], self.ticks[ti2])
            pre_rect.stretch_to_fit_width(tick_pair.get_width())
            pre_rect.move_to(tick_pair)

        special_rect = rects[int(0.6*len(rects))]
        brace = Brace(special_rect, LEFT, buff = 0)

        v_dt_brace_group_copy = self.v_dt_brace_group.copy()
        start_brace, (v_t, dt) = v_dt_brace_group_copy

        self.play(
            FadeIn(
                pre_rects, 
                run_time = 2,
                lag_ratio = 0.5
            ),
            Animation(self.ticks)
        )
        self.play(
            ReplacementTransform(
                pre_rects, rects,
                run_time = 3,
                lag_ratio = 0.5
            ),
            Animation(self.ticks),
            Write(self.axes, run_time = 1)
        )
        self.play(ShowCreation(v_graph))
        self.change_mode("pondering")
        self.wait()
        self.play(
            v_t.next_to, brace, LEFT, SMALL_BUFF,
            dt.next_to, special_rect, DOWN,
            special_rect.set_fill, None, 1,
            ReplacementTransform(start_brace, brace),
        )
        self.wait(3)

        self.v_graph = v_graph
        self.rects = rects
        self.v_dt_brace_group_copy = v_dt_brace_group_copy

    def let_dt_approach_zero(self):
        thinner_rects_list = [
            self.get_riemann_rectangles(
                self.v_graph,
                x_min = 0,
                x_max = self.t_max,
                dx = self.dt/(2**n),
                stroke_width = 1./(2**n)
            )
            for n in range(1, 4)
        ]

        self.play(
            self.rects.set_fill, None, 1,
            Animation(self.x_axis),
            FadeOut(self.v_dt_brace_group_copy),
        )
        self.change_mode("thinking")
        self.wait()
        for thinner_rects in thinner_rects_list:
            self.play(
                Transform(
                    self.rects, thinner_rects,
                    run_time = 2,
                    lag_ratio = 0.5
                )
            )
            self.wait()

    def show_confusion(self):
        randy = Randolph(color = BLUE_C)
        randy.to_corner(DOWN+LEFT)
        randy.to_edge(LEFT, buff = MED_SMALL_BUFF)

        self.play(FadeIn(randy))
        self.play(
            randy.change_mode, "confused",
            randy.look_at, self.rects
        )
        self.play(
            self.pi_creature.change_mode, "confused",
            self.pi_creature.look_at, randy.eyes
        )
        self.play(Blink(randy))
        self.wait()
