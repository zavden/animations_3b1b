# ==============================================================================
# Scene:      Introduce1DFunctionCase
# Source:     videos/_2018/WindingNumber_G.py (lines 162-533)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl Introduce1DFunctionCase.py Introduce1DFunctionCase -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class Introduce1DFunctionCase(Scene):
    CONFIG = {
        "search_range_rect_height" : 0.15,
        "arrow_opacity" : 1,
        "show_dotted_line_to_f" : True,
        "arrow_config": {
            "max_tip_length_to_length_ratio" : 0.5,
        },
        "show_midpoint_value" : True,
    }
    def construct(self):
        self.show_axes_one_at_a_time()
        self.show_two_graphs()
        self.transition_to_sqrt_2_case()
        self.show_example_binary_search()

    def show_axes_one_at_a_time(self):
        axes = Axes(
            x_min = -1, x_max = 3.2,
            x_axis_config = {
                "unit_size" : 3,
                "tick_frequency" : 0.25,
                "big_tick_numbers" : list(range(-1, 4))
            },
            y_min = -2, y_max = 4.5,
        )
        axes.to_corner(DOWN+LEFT)
        axes.x_axis.add_numbers(*list(range(-1, 4)))
        axes.y_axis.label_direction = LEFT
        axes.y_axis.add_numbers(-1, *list(range(1, 5)))

        inputs = OldTexText("Inputs")
        inputs.next_to(axes.x_axis, UP, aligned_edge = RIGHT)

        outputs = OldTexText("Outputs")
        outputs.next_to(axes.y_axis, UP, SMALL_BUFF)

        self.play(
            ShowCreation(axes.x_axis),
            Write(inputs)
        )
        self.wait()
        self.play(
            ShowCreation(axes.y_axis),
            FadeOut(axes.x_axis.numbers[1], rate_func = squish_rate_func(smooth, 0, 0.2)),
            Write(outputs)
        )
        self.wait()

        self.axes = axes
        self.inputs_label = inputs
        self.outputs_label = outputs

    def show_two_graphs(self):
        axes = self.axes
        f_graph = axes.get_graph(
            lambda x : 2*x*(x - 0.75)*(x - 1.5) + 1,
            color = BLUE
        )
        g_graph = axes.get_graph(
            lambda x : 1.8*np.cos(TAU*x/2),
            color = YELLOW
        )

        label_x_corod = 2
        f_label = OldTex("f(x)")
        f_label.match_color(f_graph)
        f_label.next_to(axes.input_to_graph_point(label_x_corod, f_graph), LEFT)

        g_label = OldTex("g(x)")
        g_label.match_color(g_graph)
        g_label.next_to(
            axes.input_to_graph_point(label_x_corod, g_graph), UP, SMALL_BUFF
        )

        solution = 0.24
        cross_point = axes.input_to_graph_point(solution, f_graph)
        l_v_line, r_v_line, v_line = [
            DashedLine(
                axes.coords_to_point(x, 0),
                axes.coords_to_point(x, f_graph.underlying_function(solution)),
            )
            for x in (axes.x_min, axes.x_max, solution)
        ]

        equation = OldTex("f(x)", "=", "g(x)")
        equation[0].match_color(f_label)
        equation[2].match_color(g_label)
        equation.next_to(cross_point, UP, buff = 1.5, aligned_edge = LEFT)
        equation_arrow = Arrow(
            equation.get_bottom(), cross_point,
            buff = SMALL_BUFF,
            color = WHITE
        )
        equation.target = OldTex("x^2", "=", "2")
        equation.target.match_style(equation)
        equation.target.to_edge(UP)

        for graph, label in (f_graph, f_label), (g_graph, g_label):
            self.play(
                ShowCreation(graph),
                Write(label, rate_func = squish_rate_func(smooth, 0.5, 1)),
                run_time = 2
            )
        self.wait()
        self.play(
            ReplacementTransform(r_v_line.copy().fade(1), v_line),
            ReplacementTransform(l_v_line.copy().fade(1), v_line),
            run_time = 2
        )
        self.play(
            ReplacementTransform(f_label.copy(), equation[0]),
            ReplacementTransform(g_label.copy(), equation[2]),
            Write(equation[1]),
            GrowArrow(equation_arrow),
        )
        for x in range(4):
            self.play(
                FadeOut(v_line.copy()),
                ShowCreation(v_line, rate_func = squish_rate_func(smooth, 0.5, 1)),
                run_time = 1.5
            )
        self.wait()
        self.play(
            MoveToTarget(equation, replace_mobject_with_target_in_scene = True),
            *list(map(FadeOut, [equation_arrow, v_line]))
        )

        self.set_variables_as_attrs(
            f_graph, f_label, g_graph, g_label,
            equation = equation.target
        )

    def transition_to_sqrt_2_case(self):
        f_graph = self.f_graph
        f_label = VGroup(self.f_label)
        g_graph = self.g_graph
        g_label = VGroup(self.g_label)
        axes = self.axes
        for label in f_label, g_label:
            for x in range(2):
                label.add(VectorizedPoint(label.get_center()))
        for number in axes.y_axis.numbers:
            number.add_background_rectangle()

        squared_graph = axes.get_graph(lambda x : x**2)
        squared_graph.match_style(f_graph)
        two_graph = axes.get_graph(lambda x : 2)
        two_graph.match_style(g_graph)

        squared_label = OldTex("f(x)", "=", "x^2")
        squared_label.next_to(
            axes.input_to_graph_point(2, squared_graph), RIGHT
        )
        squared_label.match_color(squared_graph)
        two_label = OldTex("g(x)", "=", "2")
        two_label.next_to(
            axes.input_to_graph_point(3, two_graph), UP,
        )
        two_label.match_color(two_graph)

        find_sqrt_2 = self.find_sqrt_2 = OldTexText("(Find $\\sqrt{2}$)")
        find_sqrt_2.next_to(self.equation, DOWN)

        self.play(
            ReplacementTransform(f_graph, squared_graph),
            ReplacementTransform(f_label, squared_label),
        )
        self.play(
            ReplacementTransform(g_graph, two_graph),
            ReplacementTransform(g_label, two_label),
            Animation(axes.y_axis.numbers)
        )
        self.wait()
        self.play(Write(find_sqrt_2))
        self.wait()

        self.set_variables_as_attrs(
            squared_graph, two_graph,
            squared_label, two_label,
        )

    def show_example_binary_search(self):
        self.binary_search(
            self.squared_graph, self.two_graph,
            x0 = 1, x1 = 2,
            n_iterations = 8
        )

    ##

    def binary_search(
        self, 
        f_graph, g_graph, 
        x0, x1, 
        n_iterations,
        n_iterations_with_sign_mention = 0,
        zoom = False,
        ):

        axes = self.axes
        rect = self.rect = Rectangle()
        rect.set_stroke(width = 0)
        rect.set_fill(YELLOW, 0.5)
        rect.replace(Line(
            axes.coords_to_point(x0, 0),
            axes.coords_to_point(x1, 0),
        ), dim_to_match = 0)
        rect.stretch_to_fit_height(self.search_range_rect_height)

        #Show first left and right
        mention_signs = n_iterations_with_sign_mention > 0
        kwargs = {"mention_signs" : mention_signs}
        leftovers0 = self.compare_graphs_at_x(f_graph, g_graph, x0, **kwargs)
        self.wait()
        leftovers1 = self.compare_graphs_at_x(f_graph, g_graph, x1, **kwargs)
        self.wait()
        self.play(GrowFromCenter(rect))
        self.wait()

        all_leftovers = VGroup(leftovers0, leftovers1)
        end_points = [x0, x1]
        if mention_signs:
            sign_word0 = leftovers0.sign_word
            sign_word1 = leftovers1.sign_word

        midpoint_line = Line(MED_SMALL_BUFF*UP, ORIGIN, color = YELLOW)
        midpoint_line_update = UpdateFromFunc(
            midpoint_line, lambda l : l.move_to(rect)
        )
        decimal = DecimalNumber(
            0,
            num_decimal_places = 3,
            show_ellipsis = True,
        )
        decimal.scale(0.7)
        decimal_update = ChangingDecimal(
            decimal, lambda a : axes.x_axis.point_to_number(rect.get_center()),
            position_update_func = lambda m : m.next_to(
                midpoint_line, DOWN, SMALL_BUFF,
                submobject_to_align = decimal[:-1],
            ),
        )
        if not self.show_midpoint_value:
            decimal.set_fill(opacity = 0)
            midpoint_line.set_stroke(width = 0)

        #Restrict to by a half each time
        kwargs = {
            "mention_signs" : False,
            "show_decimal" : zoom,
        } 
        for x in range(n_iterations - 1):
            x_mid = np.mean(end_points)
            leftovers_mid = self.compare_graphs_at_x(f_graph, g_graph, x_mid, **kwargs)
            if leftovers_mid.too_high == all_leftovers[0].too_high:
                index_to_fade = 0
            else:
                index_to_fade = 1
            edge = [RIGHT, LEFT][index_to_fade]
            to_fade = all_leftovers[index_to_fade]
            all_leftovers.submobjects[index_to_fade] = leftovers_mid
            end_points[index_to_fade] = x_mid

            added_anims = []
            if mention_signs:
                word = [leftovers0, leftovers1][index_to_fade].sign_word
                if x < n_iterations_with_sign_mention:
                    added_anims = [word.next_to, leftovers_mid[0].get_end(), -edge]
                elif word in self.camera.extract_mobject_family_members(self.mobjects):
                    added_anims = [FadeOut(word)]

            rect.generate_target()
            rect.target.stretch(0.5, 0, about_edge = edge)
            rect.target.stretch_to_fit_height(self.search_range_rect_height)
            self.play(
                MoveToTarget(rect),
                midpoint_line_update,
                decimal_update,
                Animation(all_leftovers),
                FadeOut(to_fade),
                *added_anims
            )
            if zoom:
                factor = 2.0/rect.get_width()
                everything = VGroup(*self.mobjects)
                decimal_index = everything.submobjects.index(decimal)
                midpoint_line_index = everything.submobjects.index(midpoint_line)
                everything.generate_target()
                everything.target.scale(factor, about_point = rect.get_center())
                everything.target[decimal_index].scale(1./factor, about_edge = UP)
                everything.target[midpoint_line_index].scale(1./factor)
                if factor > 1:
                    self.play(
                        everything.scale, factor, 
                        {"about_point" : rect.get_center()}
                    )
            else:
                self.wait()

    def compare_graphs_at_x(
        self, f_graph, g_graph, x, 
        mention_signs = False,
        show_decimal = False,
        ):
        axes = self.axes
        f_point = axes.input_to_graph_point(x, f_graph)
        g_point = axes.input_to_graph_point(x, g_graph)
        arrow = Arrow(
            g_point, f_point, buff = 0,
            **self.arrow_config
        )
        too_high = f_point[1] > g_point[1]
        if too_high:
            arrow.set_fill(GREEN, opacity = self.arrow_opacity)
        else:
            arrow.set_fill(RED, opacity = self.arrow_opacity)

        leftovers = VGroup(arrow)
        leftovers.too_high = too_high

        if self.show_dotted_line_to_f:
            v_line = DashedLine(axes.coords_to_point(x, 0), f_point)
            self.play(ShowCreation(v_line))
            leftovers.add(v_line)

        added_anims = []
        if show_decimal:
            decimal = DecimalNumber(
                axes.x_axis.point_to_number(arrow.get_start()),
                num_decimal_places = 3,
                # show_ellipsis = True,
            )
            height = self.rect.get_height()
            decimal.set_height(height)
            next_to_kwargs = {
                "buff" : height,
            }
            if too_high:
                decimal.next_to(arrow, DOWN, **next_to_kwargs)
                if hasattr(self, "last_up_arrow_decimal"):
                    added_anims += [FadeOut(self.last_up_arrow_decimal)]
                self.last_up_arrow_decimal = decimal
            else:
                decimal.next_to(arrow, UP, **next_to_kwargs)
                if hasattr(self, "last_down_arrow_decimal"):
                    added_anims += [FadeOut(self.last_down_arrow_decimal)]
                self.last_down_arrow_decimal = decimal
            line = Line(decimal, arrow, buff = 0)
            # line.match_color(arrow)
            line.set_stroke(WHITE, 1)
            decimal.add(line)
            added_anims += [FadeIn(decimal)]

        if mention_signs:
            if too_high:
                sign_word = OldTexText("Positive")
                sign_word.set_color(GREEN)
                sign_word.scale(0.7)
                sign_word.next_to(arrow.get_end(), RIGHT)
            else:
                sign_word = OldTexText("Negative")
                sign_word.set_color(RED)
                sign_word.scale(0.7)
                sign_word.next_to(arrow.get_end(), LEFT)
            sign_word.add_background_rectangle()
            added_anims += [FadeIn(sign_word)]
            leftovers.sign_word = sign_word

        self.play(GrowArrow(arrow), *added_anims)

        return leftovers
