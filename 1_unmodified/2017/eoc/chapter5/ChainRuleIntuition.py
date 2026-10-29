# ==============================================================================
# Scene:      ChainRuleIntuition
# Source:     videos/_2017/eoc/chapter5.py (lines 1284-1375)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter4.py
#
# Run from this folder:
#     manimgl ChainRuleIntuition.py ChainRuleIntuition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter4.py -----

SINE_COLOR = BLUE


X_SQUARED_COLOR = GREEN


class ThreeLinesChainRule(ReconfigurableScene):
    CONFIG = {
        "start_x" : 0.5,
        "max_x" : 1,
        "min_x" : 0,
        "top_x" : 3,
        "example_x" : 1.5,
        "dx" : 0.1,
        "line_configs" : [
            {
                "func" : lambda x : x,
                "func_label" : "x",
                "triangle_color" : WHITE,
                "center_y" : 3,
                "x_min" : 0,
                "x_max" : 3,
                "numbers_to_show" : list(range(4)),
                "big_tick_numbers" : list(range(4)),
                "tick_frequency" : 0.25,
            },
            {
                "func" : lambda x : x**2,
                "func_label" : "x^2",
                "triangle_color" : X_SQUARED_COLOR,
                "center_y" : 0.5,
                "x_min" : 0,
                "x_max" : 10,
                "numbers_to_show" : list(range(0, 11)),
                "big_tick_numbers" : list(range(0, 11, 1)),
                "tick_frequency" : 0.25,
            },
            {
                "func" : lambda x : np.sin(x**2),
                "func_label" : "\\sin(x^2)",
                "triangle_color" : SINE_COLOR,
                "center_y" : -2,
                "x_min" : -2,
                "x_max" : 2,
                "numbers_to_show" : list(range(-2, 3)),
                "big_tick_numbers" : list(range(-2, 3)),
                "tick_frequency" : 0.25,
            },
        ],
        "line_width" : 8,
        "triangle_height" : 0.25,
    }
    def construct(self):
        self.introduce_line_group()
        self.draw_function_arrows()
        self.talk_through_movement()
        self.nudge_x()
        self.give_example_of_meaning()

    def introduce_line_group(self):
        self.line_group = self.get_line_group(self.start_x)
        lines, labels = self.line_group

        for line in lines:
            self.play(Write(line, run_time = 2))
        self.wait()
        last_label = labels[0].copy()
        last_label.to_corner(UP+LEFT)
        last_label.set_fill(opacity = 0)
        for label in labels:
            self.play(ReplacementTransform(
                last_label.copy(), label
            ))
            self.wait()
            last_label = label
        for x in self.max_x, self.min_x, self.start_x:
            self.animate_x_change(x, run_time = 1)
        self.wait()

    def draw_function_arrows(self):
        lines, line_labels = self.line_group
        labels = VGroup(*[
            OldTex("(\\dots)^2").set_color(X_SQUARED_COLOR), 
            OldTex("\\sin(\\dots)").set_color(SINE_COLOR)
        ])
        arrows = VGroup()
        for lines_subset, label in zip([lines[:2], lines[1:]], labels):
            arrow = Arc(start_angle = np.pi/3, angle = -2*np.pi/3)
            arrow.add_tip()
            arrow.set_color(label.get_color())
            arrow.next_to(VGroup(*lines_subset))
            arrows.add(arrow)
            label.next_to(arrow, RIGHT)

            self.play(
                ShowCreation(arrow),
                Write(label)
            )
            self.wait()
        self.arrows = arrows
        self.arrow_labels = labels

    def talk_through_movement(self):
        lines, labels = self.line_group

        self.animate_x_change(self.top_x, run_time = 4)
        self.wait()
        for label in labels[0], labels[1]:
            oval = Circle(color = YELLOW)
            oval.replace(label, stretch = True)
            oval.scale(2.5)
            oval.move_to(label.get_bottom())
            self.play(ShowCreation(oval))
            self.wait()
            self.play(FadeOut(oval))
        sine_text = OldTex("\\sin(9) \\approx 0.412")
        sine_text.move_to(labels[-1][-1])
        sine_text.to_edge(DOWN)
        sine_arrow = Arrow(
            sine_text.get_top(),
            labels[-1][0].get_bottom(),
            buff = SMALL_BUFF,
        )
        self.play(
            FadeIn(sine_text),
            ShowCreation(sine_arrow)
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [sine_text, sine_arrow])))
        self.animate_x_change(self.example_x, run_time = 3)

    def nudge_x(self):
        lines, labels = self.line_group
        def get_value_points():
            return [
                label[0].get_bottom()
                for label in labels
            ]
        starts = get_value_points()
        self.animate_x_change(self.example_x + self.dx, run_time = 0)
        ends = get_value_points()
        self.animate_x_change(self.example_x, run_time = 0)

        nudge_lines = VGroup()
        braces = VGroup()
        numbers = VGroup()
        for start, end, line, label, config in zip(starts, ends, lines, labels, self.line_configs):
            color = label[0].get_color()
            nudge_line = Line(start, end)
            nudge_line.set_stroke(color, width = 6)
            brace = Brace(nudge_line, DOWN, buff = SMALL_BUFF)
            brace.set_color(color)
            func_label = config["func_label"]
            if len(func_label) == 1:
                text = "$d%s$"%func_label
            else:
                text = "$d(%s)$"%func_label
            brace.text = brace.get_text(text, buff = SMALL_BUFF)
            brace.text.set_color(color)
            brace.add(brace.text)

            line.add(nudge_line)
            nudge_lines.add(nudge_line)
            braces.add(brace)
            numbers.add(line.numbers)
            line.remove(*line.numbers)
        dx_brace, dx_squared_brace, dsine_brace = braces

        x_value = str(self.example_x)
        x_value_label = OldTex("=%s"%x_value)
        x_value_label.next_to(labels[0][1], RIGHT)
        dx_squared_value = OldTex(
            "= 2x\\,dx ", "\\\\ = 2(%s)dx"%x_value
        )
        dx_squared_value.shift(
            dx_squared_brace.text.get_right()+MED_SMALL_BUFF*RIGHT - \
            dx_squared_value[0].get_left()
        )
        dsine_value = OldTexText(
            "$=\\cos(%s)$"%self.line_configs[1]["func_label"],
            dx_squared_brace.text.get_tex()
        )
        dsine_value.next_to(dsine_brace.text)
        less_than_zero = OldTex("<0")
        less_than_zero.next_to(dsine_brace.text)

        all_x_squared_relevant_labels = VGroup(
            dx_squared_brace, dsine_brace,
            labels[1], labels[2],
            dsine_value,
        )
        all_x_squared_relevant_labels.save_state()

        self.play(FadeOut(numbers))
        self.animate_x_change(
            self.example_x + self.dx,
            run_time = 1,
            added_anims = it.chain(
                [GrowFromCenter(dx_brace)],
                list(map(ShowCreation, nudge_lines))
            )
        )
        self.animate_x_change(self.example_x)
        self.wait()
        self.play(Write(x_value_label))
        self.wait()
        self.play(FocusOn(dx_squared_brace))
        self.play(Write(dx_squared_brace))
        self.wiggle_by_dx()
        self.wait()
        for part in dx_squared_value:
            self.play(Write(part))
            self.wait()
        self.play(FadeOut(dx_squared_value))
        self.wait()
        #Needs to be part of everything for the reconfiguraiton
        dsine_brace.set_fill(opacity = 0)
        dsine_value.set_fill(opacity = 0)
        self.add(dsine_brace, dsine_value)
        self.replace_x_squared_with_h()
        self.wait()
        self.play(dsine_brace.set_fill, None, 1)
        self.discuss_dsine_sign(less_than_zero)
        self.wait()
        dsine_value.set_fill(opacity = 1)
        self.play(Write(dsine_value))
        self.wait()
        self.play(
            all_x_squared_relevant_labels.restore,
            lag_ratio = 0.5,
            run_time = 3,
        )
        self.__dict__.update(self.__class__.CONFIG)
        self.wait()
        for mob in dsine_value:
            self.play(Indicate(mob))
            self.wait()

        two_x_dx = dx_squared_value[0]
        dx_squared = dsine_value[1]
        two_x_dx_copy = VGroup(*two_x_dx[1:]).copy()
        self.play(FocusOn(two_x_dx))
        self.play(Write(two_x_dx))
        self.play(
            two_x_dx_copy.move_to, dx_squared, LEFT,
            dx_squared.next_to, dx_squared, UP,
            run_time = 2
        )
        self.play(FadeOut(dx_squared))
        for sublist in two_x_dx_copy[:2], two_x_dx_copy[2:]:
            self.play(Indicate(VGroup(*sublist)))
            self.wait()
        self.wait(2)

        self.final_derivative = dsine_value

    def discuss_dsine_sign(self, less_than_zero):
        self.wiggle_by_dx()
        self.wait()
        for x in self.example_x+self.dx, self.example_x:
            self.animate_x_change(x, run_time = 2)
            self.wait()
            if less_than_zero not in self.get_mobjects():
                self.play(Write(less_than_zero))
            else:
                self.play(FadeOut(less_than_zero))

    def replace_x_squared_with_h(self):
        new_config = copy.deepcopy(self.__class__.CONFIG)
        new_config["line_configs"][1]["func_label"] = "h"
        new_config["line_configs"][2]["func_label"] = "\\sin(h)"
        self.transition_to_alt_config(
            return_to_original_configuration = False,
            **new_config
        )

    def give_example_of_meaning(self):
        words = OldTexText("For example,")
        expression = OldTex("\\cos(1.5^2)\\cdot 2(1.5)\\,dx")
        group = VGroup(words, expression)
        group.arrange(DOWN, aligned_edge = LEFT)
        group.scale(0.8)
        group.to_edge(RIGHT)
        arrow = Arrow(group.get_bottom(), self.final_derivative[0].get_top())

        self.play(*list(map(FadeOut, [self.arrows, self.arrow_labels])))
        self.play(FadeIn(group))
        self.play(ShowCreation(arrow))
        self.wait()
        self.wiggle_by_dx()
        self.wait()


    ########

    def wiggle_by_dx(self, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1)
        kwargs["rate_func"] = kwargs.get("rate_func", there_and_back)
        target_x = self.line_group.x_val + self.dx
        self.animate_x_change(target_x, **kwargs)

    def animate_x_change(self, target_x, **kwargs):
        #Assume fixed lines, only update labels
        kwargs["run_time"] = kwargs.get("run_time", 2)
        added_anims = kwargs.get("added_anims", [])
        start_x = self.line_group.x_val
        def update(line_group, alpha):
            lines, labels = line_group
            new_x = interpolate(start_x, target_x, alpha)
            for line, label, config in zip(lines, labels, self.line_configs):
                new_label = self.get_line_label(
                    line, new_x, **config
                )
                Transform(label, new_label).update(1)
            line_group.x_val = new_x
        self.play(
            UpdateFromAlphaFunc(self.line_group, update),
            *added_anims,
            **kwargs
        )

    def get_line_group(self, x):
        group = VGroup()
        group.lines, group.labels = VGroup(), VGroup()
        for line_config in self.line_configs:
            number_line = self.get_number_line(**line_config)
            label = self.get_line_label(number_line, x, **line_config)
            group.lines.add(number_line)
            group.labels.add(label)
        group.add(group.lines, group.labels)
        group.x_val = x
        return group

    def get_number_line(
        self, center_y, **number_line_config
        ):
        number_line = NumberLine(color = GREY, **number_line_config)
        number_line.stretch_to_fit_width(self.line_width)
        number_line.add_numbers()
        number_line.shift(center_y*UP)
        number_line.to_edge(LEFT, buff = LARGE_BUFF)

        return number_line

    def get_line_label(
        self, number_line, x, func, func_label, triangle_color, 
        **spillover_kwargs
        ):
        triangle = RegularPolygon(
            n=3, start_angle = -np.pi/2,
            fill_color = triangle_color,
            fill_opacity = 0.75,
            stroke_width = 0,
        )
        triangle.set_height(self.triangle_height)
        triangle.move_to(
            number_line.number_to_point(func(x)), DOWN
        )

        label_mob = OldTex(func_label)
        label_mob.next_to(triangle, UP, buff = SMALL_BUFF, aligned_edge = LEFT)

        return VGroup(triangle, label_mob)



# ----- From _2017/eoc/chapter5.py -----

class ChainRuleIntuition(ThreeLinesChainRule):
    CONFIG = {
        "line_configs" : [
            {
                "func" : lambda t : t,
                "func_label" : "t",
                "triangle_color" : WHITE,
                "center_y" : 3,
                "x_min" : 0,
                "x_max" : 3,
                "numbers_to_show" : list(range(4)),
                "big_tick_numbers" : list(range(4)),
                "tick_frequency" : 1,
            },
            {
                "func" : lambda t : 3*t,
                "func_label" : "3t",
                "triangle_color" : GREEN,
                "center_y" : 0.5,
                "x_min" : 0,
                "x_max" : 3,
                "numbers_to_show" : list(range(0, 4)),
                "big_tick_numbers" : list(range(4)),
                "tick_frequency" : 1,
            },
            {
                "func" : lambda t : np.exp(3*t),
                "func_label" : "e^{3t}",
                "triangle_color" : BLUE,
                "center_y" : -2,
                "x_min" : 0,
                "x_max" : 10,
                "numbers_to_show" : list(range(0, 11, 3)),
                "big_tick_numbers" : list(range(11)),
                "tick_frequency" : 1,
            },
        ],
        "example_x" : 0.4,
        "start_x" : 0.4,
        "max_x" : 0.6,
        "min_x" : 0.2,
    }
    def construct(self):
        self.introduce_line_group()
        self.nudge_x()

    def nudge_x(self):
        lines, labels = self.line_group
        def get_value_points():
            return [
                label[0].get_bottom()
                for label in labels
            ]
        starts = get_value_points()
        self.animate_x_change(self.example_x + self.dx, run_time = 0)
        ends = get_value_points()
        self.animate_x_change(self.example_x, run_time = 0)

        nudge_lines = VGroup()
        braces = VGroup()
        numbers = VGroup()
        for start, end, line, label, config in zip(starts, ends, lines, labels, self.line_configs):
            color = label[0].get_color()
            nudge_line = Line(start, end)
            nudge_line.set_stroke(color, width = 6)
            brace = Brace(nudge_line, DOWN, buff = SMALL_BUFF)
            brace.set_color(color)
            func_label = config["func_label"]
            if len(func_label) == 1:
                text = "$d%s$"%func_label
            else:
                text = "$d(%s)$"%func_label
            brace.text = brace.get_text(text, buff = SMALL_BUFF)
            brace.text.set_color(color)
            brace.add(brace.text)

            line.add(nudge_line)
            nudge_lines.add(nudge_line)
            braces.add(brace)
            numbers.add(line.numbers)
            line.remove(*line.numbers)
        dt_brace, d3t_brace, dexp3t_brace = braces

        self.play(*list(map(FadeIn, [nudge_lines, braces])))
        self.wait()
        for count in range(3):
            for dx in self.dx, 0:
                self.animate_x_change(
                    self.example_x + dx, 
                    run_time = 2
                )
        self.wait()
