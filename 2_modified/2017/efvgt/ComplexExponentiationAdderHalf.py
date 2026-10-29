# ==============================================================================
# Scene:      ComplexExponentiationAdderHalf
# Source:     videos/_2017/efvgt.py (lines 2922-3045)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ComplexExponentiationAdderHalf.py ComplexExponentiationAdderHalf -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The repo stubbed ComplexTransformationScene out; import the ported once_useful_constructs one
#   - CONFIG of a plain (non-Scene) mixin is not turned into attributes: use class attributes
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


# CHANGE: CONFIG of a plain (non-Scene) mixin is not turned into attributes: use class attributes
class ComplexExponentiationAbstract():
    # CONFIG of a plain mixin is not digested by GL: plain class attributes
    start_base = 2
    new_base = 5
    group_type = None
    color = None
    vect = None
    def construct(self):
        self.base = self.start_base
        example_inputs = [2, -3, 1]
        self.add_vertical_line()
        self.add_plane_unanimated()
        self.add_title()
        self.add_arrow()
        self.show_example(complex(1, 1))
        self.draw_real_line()
        self.show_real_actions(*example_inputs)
        self.show_pure_imaginary_actions(*example_inputs)
        self.set_color_vertical_line()
        self.set_color_unit_circle()
        self.show_pure_imaginary_actions(*example_inputs)
        self.walk_input_up_vertical()
        self.change_base(self.new_base, str(self.new_base))
        self.walk_input_up_vertical()
        self.change_base(np.exp(1), "e")
        self.take_steps_for_e()
        self.write_eulers_formula()
        self.show_pure_imaginary_actions(-np.pi, np.pi)
        self.wait()

    def add_vertical_line(self):
        line = Line(FRAME_Y_RADIUS*UP, FRAME_Y_RADIUS*DOWN)
        line.set_stroke(color = self.color, width = 10)
        line.shift(-FRAME_X_RADIUS*self.vect/2)
        self.add(line)
        self.add_foreground_mobjects(line)

    def add_plane_unanimated(self):
        should_skip_animations = self.skip_animations
        self.skip_animations = True
        self.add_plane()
        self.skip_animations = should_skip_animations

    def add_title(self):
        title = OldTexText(self.group_type, "group")
        title.scale(0.8)
        title[0].set_color(self.color)
        title.add_background_rectangle()
        title.to_edge(UP, buff = MED_SMALL_BUFF)
        self.add_foreground_mobjects(title)

    def add_arrow(self):
        arrow = Arrow(LEFT, RIGHT, color = WHITE)
        arrow.move_to(-FRAME_X_RADIUS*self.vect/2 + 2*UP)
        arrow.set_stroke(width = 6),
        func_mob = OldTex("2^x")    
        func_mob.next_to(arrow, UP, aligned_edge = LEFT)
        func_mob.add_background_rectangle()

        self.add_foreground_mobjects(arrow, func_mob)
        self.wait()
        self.func_mob = func_mob

    def show_example(self, z):
        self.apply_action(
            z,
            run_time = 5,
            rate_func = there_and_back
        )

    def draw_real_line(self):
        line = VGroup(Line(ORIGIN, FRAME_X_RADIUS*RIGHT))
        if self.vect[0] < 0:
            line.add(Line(ORIGIN, FRAME_X_RADIUS*LEFT))
        line.set_color(RED)

        self.play(*list(map(ShowCreation, line)), run_time = 3)
        self.add_foreground_mobjects(line)

        self.real_line = line

    def show_real_actions(self, *example_inputs):
        for x in example_inputs:
            self.apply_action(x)
            self.wait()

    def show_pure_imaginary_actions(self, *example_input_imag_parts):
        for y in example_input_imag_parts:
            self.apply_action(complex(0, y), run_time = 3)
            self.wait()

    def change_base(self, new_base, new_base_tex):
        new_func_mob = OldTex(new_base_tex + "^x")
        new_func_mob.add_background_rectangle()
        new_func_mob.move_to(self.func_mob)

        self.play(FocusOn(self.func_mob))
        self.play(Transform(self.func_mob, new_func_mob))
        self.wait()
        self.base = new_base

    def write_eulers_formula(self):
        formula = OldTex("e^", "{\\pi", "i}", "=", "-1")
        VGroup(*formula[1:3]).set_color(ADDER_COLOR)
        formula[-1].set_color(MULTIPLIER_COLOR)
        formula.scale(1.5)
        formula.next_to(ORIGIN, UP)
        formula.shift(-FRAME_X_RADIUS*self.vect/2)
        for part in formula:
            part.add_to_back(BackgroundRectangle(part))

        Scene.play(self, Write(formula))
        self.add_foreground_mobjects(formula)
        self.wait(2)


class ComplexExponentiationAdderHalf(
    ComplexExponentiationAbstract, 
    AdditiveGroupOfComplexNumbers
    ):
    CONFIG = {
        "group_type" : "Additive",
        "color" : GREEN_B,
        "vect" : LEFT,
    }
    def construct(self):
        ComplexExponentiationAbstract.construct(self)

    def apply_action(self, z, run_time = 2, **kwargs):
        kwargs["run_time"] = run_time
        self.play(
            # CHANGE: Cairo animations absorbed unknown kwargs (added_anims); GL raises TypeError: do not forward it
            ApplyMethod(
                self.plane.shift, self.z_to_point(z),
                **{k: v for k, v in kwargs.items() if k != "added_anims"}
            ),
            *kwargs.get("added_anims", [])
        )

    def set_color_vertical_line(self):
        line = VGroup(
            Line(ORIGIN, FRAME_Y_RADIUS*UP),
            Line(ORIGIN, FRAME_Y_RADIUS*DOWN),
        )
        line.set_color(YELLOW)

        self.play(
            FadeOut(self.real_line),
            *list(map(ShowCreation, line))
        )
        # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
        self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not self.real_line]
        self.play(
            line.rotate, np.pi/24,
            rate_func = wiggle,
        )
        self.wait()

        self.foreground_mobjects = [line] + self.foreground_mobjects
        self.vertical_line = line

    def set_color_unit_circle(self):
        line = VGroup(
            Line(ORIGIN, FRAME_Y_RADIUS*UP),
            Line(ORIGIN, FRAME_Y_RADIUS*DOWN),
        )
        line.set_color(YELLOW)
        for submob in line:
            submob.insert_n_curves(10)
            submob.make_smooth()
        circle = VGroup(
            Circle(),
            Circle().flip(RIGHT),
        )
        circle.set_color(YELLOW)
        circle.shift(FRAME_X_RADIUS*RIGHT)

        self.play(ReplacementTransform(
            line, circle, run_time = 3
        ))
        self.remove(circle)
        self.wait()

    def walk_input_up_vertical(self):
        arrow = Arrow(ORIGIN, UP, buff = 0, tip_length = 0.15)
        arrow.set_color(GREEN)
        brace = Brace(arrow, RIGHT, buff = SMALL_BUFF)
        brace_text = brace.get_text("1 unit")
        brace_text.add_background_rectangle()

        Scene.play(self, ShowCreation(arrow))
        self.add_foreground_mobjects(arrow)
        self.play(
            GrowFromCenter(brace),
            Write(brace_text, run_time = 1)
        )
        self.add_foreground_mobjects(brace, brace_text)        
        self.wait()
        self.apply_action(complex(0, 1))
        self.wait(7)##Line up with MultiplierHalf

        to_remove = arrow, brace, brace_text
        for mob in to_remove:
            # CHANGE: Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
            self.foreground_mobjects = [m for m in self.foreground_mobjects if m is not mob]
        self.play(*list(map(FadeOut, to_remove)))
        self.apply_action(complex(0, -1))

    def take_steps_for_e(self):
        slide_values = [1, 1, 1, np.pi-3]
        braces = [
            Brace(Line(ORIGIN, x*UP), RIGHT, buff = SMALL_BUFF)
            for x in np.cumsum(slide_values)
        ]
        labels = list(map(TexText, [
            "1 unit",
            "2 units",
            "3 units",
            "$\\pi$ units",
        ]))
        for label, brace in zip(labels, braces):
            label.add_background_rectangle()
            label.next_to(brace, RIGHT, buff = SMALL_BUFF)

        curr_brace = None
        curr_label = None
        for slide_value, label, brace in zip(slide_values, labels, braces):
            self.apply_action(complex(0, slide_value))
            if curr_brace is None:
                curr_brace = brace
                curr_label = label
                self.play(
                    GrowFromCenter(curr_brace),
                    Write(curr_label)
                )
                self.add_foreground_mobjects(brace, label)
            else:
                self.play(
                    Transform(curr_brace, brace),
                    Transform(curr_label, label),
                )
            self.wait()
            self.wait(4) ##Line up with multiplier half
