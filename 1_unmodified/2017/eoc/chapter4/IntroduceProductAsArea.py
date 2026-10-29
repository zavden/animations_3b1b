# ==============================================================================
# Scene:      IntroduceProductAsArea
# Source:     videos/_2017/eoc/chapter4.py (lines 773-1358)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceProductAsArea.py IntroduceProductAsArea -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SINE_COLOR = BLUE


class IntroduceProductAsArea(ReconfigurableScene):
    CONFIG = {
        "top_func" : np.sin,
        "top_func_label" : "\\sin(x)",
        "top_func_nudge_label" : "d(\\sin(x))",
        "top_func_derivative" : "\\cos(x)",
        "side_func" : lambda x : x**2,
        "side_func_label" : "x^2",
        "side_func_nudge_label" : "d(x^2)",
        "side_func_derivative" : "2x",
        "x_unit_to_space_unit" : 3,
        "box_kwargs" : {
            "fill_color" : YELLOW,
            "fill_opacity" : 0.75,
            "stroke_width" : 1,
        },
        "df_box_kwargs" : {
            "fill_color" : GREEN,
            "fill_opacity" : 0.75,
            "stroke_width" : 0,
        },
        "box_corner_location" : 6*LEFT+2.5*UP,
        "slider_center" : 3.5*RIGHT+2*DOWN,
        "slider_width" : 6,
        "slider_x_max" : 3,
        "x_slider_handle_height" : 0.25,
        "slider_handle_color" : BLUE,
        "default_x" : .75,
        "dx" : 0.1,
        "tiny_dx" : 0.01,
    }
    def construct(self):
        self.introduce_box()
        self.talk_though_sine()
        self.define_f_of_x()
        self.nudge_x()
        self.write_df()
        self.show_thinner_dx()
        self.expand_derivative()
        self.write_derivative_abstractly()
        self.write_mneumonic()

    def introduce_box(self):
        box, labels = self.box_label_group = self.get_box_label_group(self.default_x)
        self.x_slider = self.get_x_slider(self.default_x)

        self.play(Write(labels))
        self.play(DrawBorderThenFill(box))
        self.wait()
        for mob in self.x_slider:
            self.play(Write(mob, run_time = 1))
        self.wait()
        for new_x in 0.5, 2, self.default_x:
            self.animate_x_change(
                new_x, run_time = 2
            )
        self.wait()

    def talk_though_sine(self):
        x_axis = self.x_slider[0]
        graph = FunctionGraph(
            np.sin, x_min = 0, x_max = np.pi,
            color = SINE_COLOR
        )
        scale_factor = self.x_slider.get_width()/self.slider_x_max
        graph.scale(scale_factor)
        graph.move_to(x_axis.number_to_point(0), DOWN+LEFT)

        label = OldTex("\\sin(x)")
        label.set_color(SINE_COLOR)
        label.next_to(graph, UP)

        y_axis = x_axis.copy()
        y_axis.remove(*y_axis.numbers)

        v_line = Line(ORIGIN, UP, color = WHITE, stroke_width = 2)
        def v_line_update(v_line):
            x = x_axis.point_to_number(self.x_slider[1].get_top())
            v_line.set_height(np.sin(x)*scale_factor)
            v_line.move_to(x_axis.number_to_point(x), DOWN)
        v_line_update(v_line)

        self.play(
            Rotate(y_axis, np.pi/2, about_point = y_axis.get_left()),
            Animation(x_axis)
        )
        self.play(
            ShowCreation(graph),
            Write(label, run_time = 1)
        )
        self.play(ShowCreation(v_line))
        for x, rt in zip([0.25, np.pi/2, 3, self.default_x], [2, 4, 4, 2]):
            self.animate_x_change(
                x, run_time = rt, 
                added_anims = [
                    UpdateFromFunc(v_line, v_line_update)
                ]
            )
            self.wait()
        self.play(*it.chain(
            list(map(FadeOut, [y_axis, graph, label, v_line])),
            [Animation(x_axis)]
        ))
        self.wait()
        for x in 1, 0.5, self.default_x:
            self.animate_x_change(x)
        self.wait()

    def define_f_of_x(self):
        f_def = OldTex(
            "f(x)", "=",
            self.top_func_label,
            self.side_func_label,
            "=", 
            "\\text{Area}"
        )
        f_def.to_corner(UP+RIGHT)
        f_def[-1].set_color(self.box_kwargs["fill_color"])

        box, labels = self.box_label_group

        self.play(Write(VGroup(*f_def[:-1])))
        self.play(Transform(
            box.copy().set_fill(opacity = 0), f_def[-1],
            run_time = 1.5,
        ))
        self.wait()

        self.f_def = f_def

    def nudge_x(self):
        box, labels = self.box_label_group
        nudge_label_group = self.get_nudge_label_group()
        original_dx = self.dx
        self.dx = self.tiny_dx
        thin_df_boxes = self.get_df_boxes()
        self.dx = original_dx
        df_boxes = self.get_df_boxes()
        right_box, corner_box, right_box = df_boxes

        self.play(FocusOn(nudge_label_group))
        self.play(*list(map(GrowFromCenter, nudge_label_group)))
        self.animate_x_change(
            self.default_x+self.dx,
            rate_func = there_and_back,
            run_time = 2,
            added_anims = [Animation(nudge_label_group)]
        ) 
        self.wait()
        self.play(
            ReplacementTransform(thin_df_boxes, df_boxes),
            VGroup(*labels[1]).shift, right_box.get_width()*RIGHT,
        )
        self.play(
            df_boxes.space_out_submobjects, 1.1,
            df_boxes.move_to, box, UP+LEFT,
        )
        self.wait()

        self.df_boxes = df_boxes
        self.df_box_labels = self.get_df_box_labels(df_boxes)
        self.x_slider.add(nudge_label_group)

    def get_nudge_label_group(self):
        line, triangle, x_mob = self.x_slider
        dx_line = Line(*[
            line.number_to_point(self.x_slider.x_val + num)
            for num in (0, self.dx,)
        ])
        dx_line.set_stroke(
            self.df_box_kwargs["fill_color"], 
            width = 6
        )
        brace = Brace(dx_line, UP, buff = SMALL_BUFF)
        brace.stretch_to_fit_height(0.2)
        brace.next_to(dx_line, UP, buff = SMALL_BUFF)
        brace.set_stroke(width = 1)
        dx = OldTex("dx")
        dx.scale(0.7)
        dx.next_to(brace, UP, buff = SMALL_BUFF)
        dx.set_color(dx_line.get_color())

        return VGroup(dx_line, brace, dx)

    def get_df_boxes(self):
        box, labels = self.box_label_group
        alt_box = self.get_box(self.x_slider.x_val + self.dx)

        h, w = box.get_height(), box.get_width()
        dh, dw = alt_box.get_height()-h, alt_box.get_width()-w
        heights_and_widths = [(dh, w), (dh, dw), (h, dw)]
        vects = [DOWN, DOWN+RIGHT, RIGHT]
        df_boxes = VGroup(*[
            Rectangle(
                height = height, width = width, **self.df_box_kwargs
            ).next_to(box, vect, buff = 0)
            for (height, width), vect in zip(
                heights_and_widths, vects
            )
        ])
        return df_boxes

    def get_df_box_labels(self, df_boxes):
        bottom_box, corner_box, right_box = df_boxes
        result = VGroup()
        quads = [
            (right_box, UP, self.top_func_nudge_label, LEFT),
            (corner_box, RIGHT, self.side_func_nudge_label, ORIGIN),
        ]
        for box, vect, label_tex, aligned_edge in quads:
            brace = Brace(box, vect)
            label = OldTex(label_tex)
            label.next_to(
                brace, vect,
                aligned_edge = aligned_edge,
                buff = SMALL_BUFF
            )
            label.set_color(df_boxes[0].get_color())
            result.add(VGroup(brace, label))
        return result

    def write_df(self):
        deriv = OldTex(
            "df", "=", 
            self.top_func_label, 
            self.side_func_nudge_label,
            "+",
            self.side_func_label,
            self.top_func_nudge_label,
        )
        deriv.scale(0.9)
        deriv.next_to(self.f_def, DOWN, buff = LARGE_BUFF)
        deriv.to_edge(RIGHT)
        for submob, tex in zip(deriv, deriv.expression_parts):
            if tex.startswith("d"):
                submob.set_color(self.df_box_kwargs["fill_color"])
        bottom_box_area = VGroup(*deriv[2:4])
        right_box_area = VGroup(*deriv[5:7])

        bottom_box, corner_box, right_box = self.df_boxes
        plus = OldTex("+").set_fill(opacity = 0)
        df_boxes_copy = VGroup(
            bottom_box.copy(),
            plus,
            right_box.copy(),
            plus.copy(),
            corner_box.copy(),
        )

        self.deriv = deriv
        self.df_boxes_copy = df_boxes_copy
        box, labels = self.box_label_group
        self.full_box_parts = VGroup(*it.chain(
            [box], self.df_boxes, labels, self.df_box_labels
        ))

        self.play(Write(VGroup(*deriv[:2])))
        self.play(
            df_boxes_copy.arrange,
            df_boxes_copy.set_fill, None, self.df_box_kwargs["fill_opacity"],
            df_boxes_copy.next_to, deriv[1]
        )
        deriv.submobjects[4] = df_boxes_copy[1]
        self.wait()

        self.set_color_right_boxes()
        self.set_color_bottom_boxes()
        self.describe_bottom_box(bottom_box_area)
        self.describe_right_box(right_box_area)
        self.ignore_corner()

        # self.add(deriv)

    def set_color_boxes_and_label(self, boxes, label):
        boxes.save_state()
        label.save_state()

        self.play(GrowFromCenter(label))
        self.play(
            boxes.set_color, RED,
            label.set_color, RED,
        )
        self.play(
            label[1].scale, 1.1,
            rate_func = there_and_back
        )
        self.play(boxes.restore, label.restore)
        self.wait()

    def set_color_right_boxes(self):
        self.set_color_boxes_and_label(
            VGroup(*self.df_boxes[1:]),
            self.df_box_labels[0]
        )

    def set_color_bottom_boxes(self):
        self.set_color_boxes_and_label(
            VGroup(*self.df_boxes[:-1]),
            self.df_box_labels[1]
        )

    def describe_bottom_box(self, bottom_box_area):
        bottom_box = self.df_boxes[0]
        bottom_box_copy = self.df_boxes_copy[0]
        other_box_copies = VGroup(*self.df_boxes_copy[1:])
        top_label = self.box_label_group[1][0]
        right_label = self.df_box_labels[1]

        faders = VGroup(*[m for m in self.full_box_parts if m not in [bottom_box, top_label, right_label]])
        faders.save_state()

        self.play(faders.fade, 0.8)
        self.wait()
        self.play(FocusOn(bottom_box_copy))
        self.play(
            ReplacementTransform(bottom_box_copy, bottom_box_area),
            other_box_copies.next_to, bottom_box_area, RIGHT
        )
        self.wait()
        self.play(faders.restore)

    def describe_right_box(self, right_box_area):
        right_box = self.df_boxes[2]
        right_box_copy = self.df_boxes_copy[2]
        right_box_area.next_to(self.df_boxes_copy[1])
        other_box_copies = VGroup(*self.df_boxes_copy[3:])
        top_label = self.df_box_labels[0]
        right_label = self.box_label_group[1][1]

        faders = VGroup(*[m for m in self.full_box_parts if m not in [right_box, top_label, right_label]])
        faders.save_state()

        self.play(faders.fade, 0.8)
        self.wait()
        self.play(FocusOn(right_box_copy))
        self.play(
            ReplacementTransform(right_box_copy, right_box_area),                        
            other_box_copies.next_to, right_box_area, DOWN, 
            MED_SMALL_BUFF, RIGHT,

        )
        self.wait()
        self.play(faders.restore)

    def ignore_corner(self):
        corner = self.df_boxes[1]
        corner.save_state()
        corner_copy = VGroup(*self.df_boxes_copy[-2:])
        words = OldTexText("Ignore")
        words.set_color(RED)
        words.next_to(corner_copy, LEFT, buff = LARGE_BUFF)
        words.shift(MED_SMALL_BUFF*DOWN)
        arrow = Arrow(words, corner_copy, buff = SMALL_BUFF, color = RED)

        self.play(
            corner.set_color, RED,
            corner_copy.set_color, RED,
        )
        self.wait()
        self.play(Write(words), ShowCreation(arrow))
        self.wait()
        self.play(*list(map(FadeOut, [words, arrow, corner_copy])))
        self.wait()
        corner_copy.set_color(BLACK)

    def show_thinner_dx(self):
        self.transition_to_alt_config(dx = self.tiny_dx)

    def expand_derivative(self):
        # self.play(
        #     self.deriv.next_to, self.f_def, DOWN, MED_LARGE_BUFF,
        #     self.deriv.shift_onto_screen
        # )
        # self.wait()

        expanded_deriv = OldTex(
            "df", "=", 
            self.top_func_label, 
            self.side_func_derivative,
            "\\,dx",
            "+", 
            self.side_func_label,
            self.top_func_derivative, 
            "\\,dx"
        )
        final_deriv = OldTex(
            "{df \\over ", "dx}", "=", 
            self.top_func_label, 
            self.side_func_derivative,
            "+", 
            self.side_func_label,
            self.top_func_derivative, 
        )
        color = self.deriv[0].get_color()
        for new_deriv in expanded_deriv, final_deriv:        
            for submob, tex in zip(new_deriv, new_deriv.expression_parts):
                for substr in "df", "dx", self.top_func_derivative, self.side_func_derivative:
                    if substr in tex:
                        submob.set_color(color)
            new_deriv.scale(0.9)
            new_deriv.next_to(self.deriv, DOWN, buff = MED_LARGE_BUFF)
            new_deriv.shift_onto_screen()

        def indicate(mob):
            self.play(
                mob.scale, 1.2,
                mob.set_color, YELLOW,
                rate_func = there_and_back
            )


        for index in 6, 3:
            self.deriv.submobjects.insert(
                index+1, self.deriv[index].copy()
            )
        non_deriv_indices = list(range(len(expanded_deriv)))
        for indices in [(3, 4), (7, 8)]:
            top_part = VGroup()
            bottom_part = VGroup()            
            for i in indices:
                non_deriv_indices.remove(i)
                top_part.add(self.deriv[i].copy())
                bottom_part.add(expanded_deriv[i])
            self.play(top_part.move_to, bottom_part)
            self.wait()
            indicate(top_part)
            self.wait()
            self.play(ReplacementTransform(top_part, bottom_part))
            self.wait()
        top_part = VGroup()
        bottom_part = VGroup()
        for i in non_deriv_indices:
            top_part.add(self.deriv[i].copy())
            bottom_part.add(expanded_deriv[i])
        self.play(ReplacementTransform(
            top_part, bottom_part
        ))

        self.wait()
        self.play(*[
            ReplacementTransform(
                expanded_deriv[i], final_deriv[j],
                path_arc = -np.pi/2
            )
            for i, j in [
                (0, 0),
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 1),
                (5, 5),
                (6, 6),
                (7, 7),
                (8, 1),
            ]
        ])
        self.wait()
        for index in 0, 1, 3, 4, 6, 7:
            indicate(final_deriv[index])
        self.wait()

    def write_derivative_abstractly(self):
        self.transition_to_alt_config(
            return_to_original_configuration = False,
            top_func_label = "g(x)",
            top_func_nudge_label = "dg",
            top_func_derivative = "\\frac{dg}{dx}",
            side_func_label = "h(x)",
            side_func_nudge_label = "dh",
            side_func_derivative = "\\frac{dh}{dx}",
        )
        self.wait()

    def write_mneumonic(self):
        morty = Mortimer()
        morty.scale(0.7)
        morty.to_edge(DOWN)
        morty.shift(2*LEFT)
        words = OldTexText(
            "``Left ", "d(Right) ", "+", " Right ", "d(Left)", "''",
            arg_separator = ""
        )
        VGroup(words[1], words[4]).set_color(self.df_boxes[0].get_color())
        words.scale(0.7)
        words.next_to(morty.get_corner(UP+LEFT), UP)
        words.shift_onto_screen()

        self.play(FadeIn(morty))
        self.play(
            morty.change_mode, "raise_right_hand",
            Write(words)
        )
        self.wait()

    ###############

    def animate_x_change(
        self, target_x, 
        box_label_group = None, 
        x_slider = None,
        **kwargs
        ):
        box_label_group = box_label_group or self.box_label_group
        x_slider = x_slider or self.x_slider
        kwargs["run_time"] = kwargs.get("run_time", 2)
        added_anims = kwargs.get("added_anims", [])

        start_x = x_slider.x_val
        def update_box_label_group(box_label_group, alpha):
            new_x = interpolate(start_x, target_x, alpha)
            new_box_label_group = self.get_box_label_group(new_x)
            Transform(box_label_group, new_box_label_group).update(1)
        
        def update_x_slider(x_slider, alpha):
            new_x = interpolate(start_x, target_x, alpha)
            new_x_slider = self.get_x_slider(new_x)
            Transform(x_slider, new_x_slider).update(1)

        self.play(
            UpdateFromAlphaFunc(
                box_label_group, 
                update_box_label_group
            ),
            UpdateFromAlphaFunc(
                x_slider, 
                update_x_slider
            ),
            *added_anims,
            **kwargs
        )
        x_slider.x_val = target_x

    def get_x_slider(self, x):
        numbers = list(range(int(self.slider_x_max) + 1))
        line = NumberLine(
            x_min = 0,
            x_max = self.slider_x_max,
            unit_size = float(self.slider_width)/self.slider_x_max,
            color = GREY,
            big_tick_numbers = numbers,
            tick_frequency = 0.25,
        )
        line.add_numbers(*numbers)
        line.numbers.next_to(line, UP, buff = SMALL_BUFF)
        for number in line.numbers:
            number.add_background_rectangle()
        line.move_to(self.slider_center)

        triangle = RegularPolygon(
            3, start_angle = np.pi/2,
            fill_color = self.slider_handle_color,
            fill_opacity = 0.8,
            stroke_width = 0,
        )
        triangle.set_height(self.x_slider_handle_height)
        triangle.move_to(line.number_to_point(x), UP)

        x_mob = OldTex("x")
        x_mob.next_to(triangle, DOWN, buff = SMALL_BUFF)

        result = VGroup(line, triangle, x_mob)
        result.x_val = x
        return result

    def get_box_label_group(self, x):
        box = self.get_box(x)
        labels = self.get_box_labels(box)
        return VGroup(box, labels)

    def get_box(self, x):
        box = Rectangle(
            width = self.x_unit_to_space_unit * self.top_func(x),
            height = self.x_unit_to_space_unit * self.side_func(x),
            **self.box_kwargs
        )
        box.move_to(self.box_corner_location, UP+LEFT)
        return box

    def get_box_labels(self, box):
        result = VGroup()
        for label_tex, vect in (self.top_func_label, UP), (self.side_func_label, RIGHT):
            brace = Brace(box, vect, min_num_quads = 5)
            label = OldTex(label_tex)
            label.next_to(brace, vect, buff = SMALL_BUFF)
            result.add(VGroup(brace, label))
        return result
