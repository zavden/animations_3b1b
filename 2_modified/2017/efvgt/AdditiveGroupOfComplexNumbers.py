# ==============================================================================
# Scene:      AdditiveGroupOfComplexNumbers
# Source:     videos/_2017/efvgt.py (lines 1432-1703)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AdditiveGroupOfComplexNumbers.py AdditiveGroupOfComplexNumbers -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The repo stubbed ComplexTransformationScene out; import the ported once_useful_constructs one
#   - Scene.remove already drops a mobject from the foreground list (CL18 shim), so list.remove raised ValueError: filter it instead
# ==============================================================================

from manim_imports_ext import *

ADDER_COLOR = GREEN


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
