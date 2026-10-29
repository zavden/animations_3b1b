# ==============================================================================
# Scene:      MultiplicativeGroupOfComplexNumbers
# Source:     videos/_2017/efvgt.py (lines 2030-2330)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MultiplicativeGroupOfComplexNumbers.py MultiplicativeGroupOfComplexNumbers -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The repo stubbed ComplexTransformationScene out; import the ported once_useful_constructs one
#   - Dot.CONFIG does not exist in GL: use DEFAULT_DOT_RADIUS
#   - Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
#   - Cairo animations absorbed unknown kwargs (added_anims); GL raises TypeError: do not forward it
# ==============================================================================

from manim_imports_ext import *

ADDER_COLOR = GREEN


MULTIPLIER_COLOR = YELLOW


# CHANGE: The repo stubbed ComplexTransformationScene out; import the ported once_useful_constructs one
from once_useful_constructs.complex_transformation_scene import ComplexTransformationScene


class AdditiveGroupOfComplexNumbers(ComplexTransformationScene):
    CONFIG = {
        "x_min" : -2*int(FRAME_X_RADIUS),
        "x_max" : 2*int(FRAME_X_RADIUS),
        "y_min" : -FRAME_HEIGHT,
        "y_max" : FRAME_HEIGHT,
        "example_points" : [
            complex(3, 2),
            complex(1, -3),
        ]
    }
    def construct(self):
        self.add_plane()
        self.show_preview_example_slides()
        self.show_vertical_slide()
        self.show_example_point()
        self.show_example_addition()
        self.write_group_name()
        self.show_some_random_slides()

    def add_plane(self):
        self.add_transformable_plane(animate = True)
        zero_dot = Dot(
            self.z_to_point(0),
            color = ADDER_COLOR
        )
        self.play(ShowCreation(zero_dot))
        self.plane.add(zero_dot)
        self.plane.zero_dot = zero_dot
        self.wait()

    def show_preview_example_slides(self):
        example_vect = 2*UP+RIGHT
        for vect in example_vect, -example_vect:
            self.play(self.plane.shift, vect, run_time = 2)
            self.wait()

    def show_vertical_slide(self):
        dots = VGroup(*[
            Dot(self.z_to_point(complex(0, i)))
            for i in range(1, 4)
        ])
        dots.set_color(YELLOW)
        labels = VGroup(*self.imag_labels[-3:])

        arrow = Arrow(ORIGIN, dots[-1].get_center(), buff = 0)
        arrow.set_color(ADDER_COLOR)

        self.plane.save_state()
        for dot, label in zip(dots, labels):
            self.play(
                Indicate(label),
                ShowCreation(dot)
            )
        self.add_foreground_mobjects(dots)
        self.wait()
        Scene.play(self, ShowCreation(arrow))
        self.add_foreground_mobjects(arrow)
        self.play(
            self.plane.shift, dots[-1].get_center(),
            run_time = 2
        )
        self.wait()
        self.play(FadeOut(arrow))
        # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
        self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not arrow]
        self.play(
            self.plane.shift, 6*DOWN,
            run_time = 3,
        )
        self.wait()
        self.play(self.plane.restore, run_time = 2)
        # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
        self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not dots]
        self.play(FadeOut(dots))

    def show_example_point(self):
        z = self.example_points[0]
        point = self.z_to_point(z)
        dot = Dot(point, color = YELLOW)
        arrow = Vector(point, buff = dot.radius)
        arrow.set_color(dot.get_color())
        label = OldTex("%d + %di"%(z.real, z.imag))
        label.next_to(point, UP)
        label.set_color(dot.get_color())
        label.add_background_rectangle()

        real_arrow = Vector(self.z_to_point(z.real))
        imag_arrow = Vector(self.z_to_point(z - z.real))
        VGroup(real_arrow, imag_arrow).set_color(ADDER_COLOR)

        self.play(
            Write(label),
            DrawBorderThenFill(dot)
        )
        self.wait()
        self.play(ShowCreation(arrow))
        self.add_foreground_mobjects(label, dot, arrow)
        self.wait()
        self.slide(z)
        self.wait()
        self.play(FadeOut(self.plane))
        self.plane.restore()
        self.plane.set_stroke(width = 0)
        self.play(self.plane.restore)
        self.play(ShowCreation(real_arrow))
        self.add_foreground_mobjects(real_arrow)
        self.slide(z.real)
        self.wait()
        self.play(ShowCreation(imag_arrow))
        self.wait()
        self.play(imag_arrow.shift, self.z_to_point(z.real))
        self.add_foreground_mobjects(imag_arrow)
        self.slide(z - z.real)
        self.wait()

        # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
        self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not real_arrow]
        # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
        self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not imag_arrow]
        self.play(*list(map(FadeOut, [real_arrow, imag_arrow, self.plane])))
        self.plane.restore()
        self.plane.set_stroke(width = 0)
        self.play(self.plane.restore)

        self.z1 = z
        self.arrow1 = arrow
        self.dot1 = dot
        self.label1 = label

    def show_example_addition(self):
        z1 = self.z1
        arrow1 = self.arrow1
        dot1 = self.dot1
        label1 = self.label1

        z2 = self.example_points[1]
        point2 = self.z_to_point(z2)
        dot2 = Dot(point2, color = TEAL)
        arrow2 = Vector(
            point2, 
            buff = dot2.radius,
            color = dot2.get_color()
        )
        label2 = OldTex(
            "%d %di"%(z2.real, z2.imag)
        )
        label2.next_to(point2, UP+RIGHT)
        label2.set_color(dot2.get_color())
        label2.add_background_rectangle()

        self.play(ShowCreation(arrow2))
        self.play(
            DrawBorderThenFill(dot2),
            Write(label2)
        )
        self.add_foreground_mobjects(arrow2, dot2, label2)
        self.wait()

        self.slide(z1)
        arrow2_copy = arrow2.copy()
        self.play(arrow2_copy.shift, self.z_to_point(z1))
        self.add_foreground_mobjects(arrow2_copy)
        self.slide(z2)
        self.play(FadeOut(arrow2_copy))
        # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
        self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not arrow2_copy]
        self.wait()

        ##Break into components
        real_arrow, imag_arrow = component_arrows = [
            Vector(
                self.z_to_point(z),
                color = ADDER_COLOR
            )
            for z in [
                z1.real+z2.real,
                complex(0, z1.imag+z2.imag),
            ]
        ]
        imag_arrow.shift(real_arrow.get_end())
        plus = OldTex("+").next_to(
            real_arrow.get_center(), UP+RIGHT
        )
        plus.add_background_rectangle()

        rp1, rp2, ip1, ip2 = label_parts = [
            VGroup(label1[1][0].copy()),
            VGroup(label2[1][0].copy()),
            VGroup(*label1[1][2:]).copy(),
            VGroup(*label2[1][1:]).copy(),
        ]
        for part in label_parts:
            part.generate_target()

        rp1.target.next_to(plus, LEFT)
        rp2.target.next_to(plus, RIGHT)
        ip1.target.next_to(imag_arrow.get_center(), RIGHT)
        ip1.target.shift(SMALL_BUFF*DOWN)
        ip2.target.next_to(ip1.target, RIGHT)

        real_background_rect = BackgroundRectangle(
            VGroup(rp1.target, rp2.target)
        )
        imag_background_rect = BackgroundRectangle(
            VGroup(ip1.target, ip2.target)
        )

        self.play(
            ShowCreation(real_arrow),
            ShowCreation(
                real_background_rect,
                rate_func = squish_rate_func(smooth, 0.75, 1),
            ),
            Write(plus),
            *list(map(MoveToTarget, [rp1, rp2]))
        )
        self.wait()
        self.play(
            ShowCreation(imag_arrow),
            ShowCreation(
                imag_background_rect,
                rate_func = squish_rate_func(smooth, 0.75, 1),
            ),
            *list(map(MoveToTarget, [ip1, ip2]))
        )
        self.wait(2)
        to_remove = [
            arrow1, dot1, label1,
            arrow2, dot2, label2,
            real_background_rect,
            imag_background_rect,
            plus,
        ] + label_parts + component_arrows
        for mob in to_remove:
            if mob in self.foreground_mobjects:
                # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
                self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not mob]
        self.play(*list(map(FadeOut, to_remove)))
        self.play(self.plane.restore, run_time = 2)
        self.wait()

    def write_group_name(self):
        title = OldTexText(
            "Additive", "group of", "complex numbers"
        )
        title[0].set_color(ADDER_COLOR)
        title[2].set_color(BLUE)
        title.add_background_rectangle()
        title.to_edge(UP, buff = MED_SMALL_BUFF)

        self.play(Write(title))
        self.add_foreground_mobjects(title)
        self.wait()

    def show_some_random_slides(self):
        example_slides = [
            complex(3),
            complex(0, 2),
            complex(-4, -1),
            complex(-2, -1),
            complex(4, 2),
        ]
        for z in example_slides:
            self.slide(z)
            self.wait()

    #########

    def slide(self, z, *added_anims, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 2)
        self.play(
            ApplyMethod(
                self.plane.shift, self.z_to_point(z),
                **kwargs
            ),
            *added_anims
        )


class MultiplicativeGroupOfComplexNumbers(AdditiveGroupOfComplexNumbers):
    CONFIG = {
        # CHANGE: Dot.CONFIG does not exist in GL: use DEFAULT_DOT_RADIUS
        "dot_radius" : DEFAULT_DOT_RADIUS,
        "y_min" : -3*FRAME_Y_RADIUS,
        "y_max" : 3*FRAME_Y_RADIUS,
    }
    def construct(self):
        self.add_plane()
        self.add_title()
        self.fix_zero_and_move_one()
        self.show_example_actions()
        self.show_action_at_i()
        self.show_action_at_i_again()
        self.show_i_squared_is_negative_one()
        self.talk_through_specific_example()
        self.show_break_down()
        self.example_actions_broken_down()

    def add_plane(self):
        AdditiveGroupOfComplexNumbers.add_plane(self)
        one_dot = Dot(
            self.z_to_point(1), 
            color = MULTIPLIER_COLOR,
            radius = self.dot_radius,
        )
        self.plane.add(one_dot)
        self.plane.one_dot = one_dot
        self.plane.save_state()
        self.add(self.plane)

    def add_title(self):
        title = OldTexText(
            "Multiplicative", "group of", 
            "complex numbers"
        )
        title.to_edge(UP)
        title[0].set_color(MULTIPLIER_COLOR)
        title[2].set_color(BLUE)
        title.add_background_rectangle()

        self.play(Write(title, run_time = 2))
        self.wait()
        self.add_foreground_mobjects(title)

    def fix_zero_and_move_one(self):
        zero_arrow = Arrow(
            UP+1.25*LEFT, ORIGIN, 
            buff = 2*self.dot_radius
        )
        zero_arrow.set_color(ADDER_COLOR)
        zero_words = OldTexText("Fix zero")
        zero_words.set_color(ADDER_COLOR)
        zero_words.add_background_rectangle()
        zero_words.next_to(zero_arrow.get_start(), UP)

        one_point = self.z_to_point(1)
        one_arrow = Arrow(
            one_point+UP+1.25*RIGHT, one_point, 
            buff = 2*self.dot_radius,
            color = MULTIPLIER_COLOR,
        )
        one_words = OldTexText("Drag one")
        one_words.set_color(MULTIPLIER_COLOR)
        one_words.add_background_rectangle()
        one_words.next_to(one_arrow.get_start(), UP)

        self.play(
            Write(zero_words, run_time = 2),
            ShowCreation(zero_arrow),
            Indicate(self.plane.zero_dot, color = RED),
        )
        self.play(
            Write(one_words, run_time = 2),
            ShowCreation(one_arrow),
            Indicate(self.plane.one_dot, color = RED),
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [
            zero_words, zero_arrow,
            one_words, one_arrow,
        ])))

    def show_example_actions(self):
        z_list = [
            complex(2),
            complex(0.5),
            complex(2, 1),
            complex(-2, 2),
        ]
        for last_z, z in zip([1] + z_list, z_list):
            self.multiply_by_z(z/last_z)
            self.wait()
        self.reset_plane()
        self.wait()

    def show_action_at_i(self):
        i_point = self.z_to_point(complex(0, 1))
        i_dot = Dot(i_point)
        i_dot.set_color(RED)
        i_arrow = Arrow(i_point+UP+LEFT, i_point)
        i_arrow.set_color(i_dot.get_color())

        arc = Arc(
            start_angle = np.pi/24,
            angle = 10*np.pi/24,
            radius = self.z_to_point(1)[0],
            num_anchors = 20,
        )
        arc.add_tip(tip_length = 0.15)
        arc.set_color(YELLOW)

        self.play(
            ShowCreation(i_arrow),
            DrawBorderThenFill(i_dot)
        )
        self.wait()
        self.play(
            FadeOut(i_arrow),
            ShowCreation(arc)
        )
        self.add_foreground_mobjects(arc)
        self.wait(2)
        self.multiply_by_z(complex(0, 1), run_time = 3)
        self.remove(i_dot)
        self.wait()

        self.turn_arrow = arc

    def show_action_at_i_again(self):
        neg_one_label = [m for m in self.real_labels if m.get_tex() == "-1"][0]
        half_turn_arc = Arc(
            start_angle = np.pi/12,
            angle = 10*np.pi/12,
            color = self.turn_arrow.get_color()
        )
        half_turn_arc.add_tip(tip_length = 0.15)

        self.multiply_by_z(complex(0, 1), run_time = 3)
        self.wait()
        self.play(Transform(
            self.turn_arrow, half_turn_arc,
            path_arc = np.pi/2
        ))
        self.wait()        
        self.play(Indicate(neg_one_label, run_time = 2))
        self.wait()
        # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
        self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not self.turn_arrow]
        self.reset_plane(FadeOut(self.turn_arrow))

    def show_i_squared_is_negative_one(self):
        equation = OldTex("i", "\\cdot", "i", "=", "-1")
        terms = equation[::2]
        equation.add_background_rectangle()
        equation.next_to(ORIGIN, RIGHT)
        equation.shift(1.5*UP)
        equation.set_color(MULTIPLIER_COLOR)

        self.play(Write(equation, run_time = 2))
        self.wait()
        for term in terms[:2]:
            self.multiply_by_z(
                complex(0, 1),
                added_anims = [
                    Animation(equation),
                    Indicate(term, color = RED, run_time = 2)
                ]
            )
            self.wait()
        self.play(Indicate(terms[-1], color = RED, run_time = 2))
        self.wait()
        self.reset_plane(FadeOut(equation))

    def talk_through_specific_example(self):
        z = complex(2, 1)
        angle = np.angle(z)
        point = self.z_to_point(z)
        dot = Dot(point, color = WHITE)
        label = OldTex("%d + %di"%(z.real, z.imag))
        label.add_background_rectangle()
        label.next_to(dot, UP+RIGHT, buff = 0)

        brace = Brace(
            Line(ORIGIN, self.z_to_point(np.sqrt(5))),
            UP
        )
        brace_text = brace.get_text("$\\sqrt{5}$")
        brace_text.add_background_rectangle()
        brace_text.scale(0.7, about_point = brace.get_top())
        brace.rotate(angle)
        brace_text.rotate(angle).rotate(-angle)
        VGroup(brace, brace_text).set_color(MAROON_B)
        arc = Arc(angle, color = WHITE, radius = 0.5)
        angle_label = OldTex("30^\\circ")
        angle_label.scale(0.7)
        angle_label.next_to(
            arc, RIGHT, 
            buff = SMALL_BUFF, aligned_edge = DOWN
        )
        angle_label.set_color(MULTIPLIER_COLOR)

        self.play(
            Write(label),
            DrawBorderThenFill(dot)
        )
        self.add_foreground_mobjects(label, dot)
        self.wait()
        self.multiply_by_z(z, run_time = 3)
        self.wait()
        self.reset_plane()
        self.multiply_by_z(
            np.exp(complex(0, 1)*angle),
            added_anims = [
                ShowCreation(arc, run_time = 2),
                Write(angle_label)
            ]
        )
        self.add_foreground_mobjects(arc, angle_label)
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.add_foreground_mobjects(brace, brace_text)
        self.multiply_by_z(np.sqrt(5), run_time = 3)
        self.wait(2)
        to_remove = [
            label, dot,
            brace, brace_text, 
            arc, angle_label,
        ]
        for mob in to_remove:
            # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
            self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not mob]
        self.reset_plane(*list(map(FadeOut, to_remove)))
        self.wait()

    def show_break_down(self):
        positive_reals = Line(ORIGIN, FRAME_X_RADIUS*RIGHT)
        positive_reals.set_color(MAROON_B)
        circle = Circle(
            radius = self.z_to_point(1)[0],
            color = MULTIPLIER_COLOR
        )
        real_actions = [3, 0.5, 1]
        rotation_actions = [
            np.exp(complex(0, angle))
            for angle in np.linspace(0, 2*np.pi, 4)[1:]
        ]

        self.play(ShowCreation(positive_reals))
        self.add_foreground_mobjects(positive_reals)
        for last_z, z in zip([1]+real_actions, real_actions):
            self.multiply_by_z(z/last_z)
        self.wait()
        self.play(ShowCreation(circle))
        self.add_foreground_mobjects(circle)
        for last_z, z in zip([1]+rotation_actions, rotation_actions):
            self.multiply_by_z(z/last_z, run_time = 3)
        self.wait()

    def example_actions_broken_down(self):
        z_list = [
            complex(2, -1),
            complex(-2, -3),
            complex(0.5, 0.5),
        ]
        for z in z_list:
            dot = Dot(self.z_to_point(z))
            dot.set_color(WHITE)
            dot.save_state()
            dot.move_to(self.plane.one_dot)
            dot.set_fill(opacity = 1)

            norm = np.abs(z)
            angle = np.angle(z)
            rot_z = np.exp(complex(0, angle))

            self.play(dot.restore)
            self.multiply_by_z(norm)
            self.wait()
            self.multiply_by_z(rot_z)
            self.wait()
            self.reset_plane(FadeOut(dot))

    ##

    def multiply_by_z(self, z, run_time = 2, **kwargs):
        target = self.plane.copy()
        target.apply_complex_function(lambda w : z*w)
        for dot in target.zero_dot, target.one_dot:
            dot.set_width(2*self.dot_radius)
        angle = np.angle(z)
        kwargs["path_arc"] = kwargs.get("path_arc", angle)
        self.play(
            # CHANGE: Cairo animations absorbed unknown kwargs (added_anims); GL raises TypeError: do not forward it
            Transform(self.plane, target, run_time = run_time, **{k: v for k, v in kwargs.items() if k != "added_anims"}),
            *kwargs.get("added_anims", [])
        )

    def reset_plane(self, *added_anims):
        self.play(FadeOut(self.plane), *added_anims)
        self.plane.restore()
        self.play(FadeIn(self.plane))
