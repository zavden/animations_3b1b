# ==============================================================================
# Scene:      IntroduceThreeDNumbers
# Source:     videos/_2018/quaternions.py (lines 3062-3258)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceThreeDNumbers.py IntroduceThreeDNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceThreeDNumbers(SpecialThreeDScene):
    CONFIG = {
        "camera_config": {
            "exponential_projection": False,
        }
    }

    def construct(self):
        self.add_third_axis()
        self.reorient_axes()
        self.show_example_number()

    def add_third_axis(self):
        plane = ComplexPlane(
            y_radius=FRAME_WIDTH / 4,
            unit_size=2,
            secondary_line_ratio=1,
        )
        plane.add_coordinates()
        title = OldTexText("Complex Plane")
        title.scale(1.8)
        title.add_background_rectangle()
        title.to_corner(UL, buff=MED_SMALL_BUFF)

        real_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        imag_line = Line(DOWN, UP).set_height(FRAME_HEIGHT)
        real_line.set_color(YELLOW)
        imag_line.set_color(RED)

        for label in plane.coordinate_labels:
            label.remove(label.background_rectangle)
            label.shift(SMALL_BUFF * IN)
            self.add_fixed_orientation_mobjects(label)
        reals = plane.coordinate_labels[:7]
        imags = plane.coordinate_labels[7:]

        self.add(plane, title)
        for line, group in (real_line, reals), (imag_line, imags):
            line.set_stroke(width=5)
            self.play(
                ShowCreationThenDestruction(line),
                LaggedStartMap(
                    Indicate, group,
                    rate_func=there_and_back,
                    color=line.get_color(),
                ),
                run_time=2,
            )

        self.plane = plane
        self.title = title

    def reorient_axes(self):
        z_axis = NumberLine(unit_size=2)
        z_axis.rotate(90 * DEGREES, axis=DOWN)
        z_axis.rotate(90 * DEGREES, axis=OUT)
        z_axis.set_color(WHITE)
        z_axis_top = Line(
            z_axis.number_to_point(0),
            z_axis.get_end(),
        )
        z_axis_top.match_style(z_axis)

        z_unit_line = Line(
            z_axis.number_to_point(0),
            z_axis.number_to_point(1),
            color=RED,
            stroke_width=5
        )

        j_labels = VGroup(
            OldTex("-2j"),
            OldTex("-j"),
            OldTex("j"),
            OldTex("2j"),
        )
        for label, num in zip(j_labels, [-2, -1, 1, 2]):
            label.next_to(z_axis.number_to_point(num), RIGHT, MED_SMALL_BUFF)
            self.add_fixed_orientation_mobjects(label)

        plane = self.plane

        colored_ = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        y_line = Line(DOWN, UP).set_height(FRAME_WIDTH)
        z_line = Line(IN, OUT).set_depth(FRAME_WIDTH)
        colored_.set_stroke(GREEN, 5)
        y_line.set_stroke(RED, 5)
        z_line.set_stroke(YELLOW, 5)
        colored_coord_lines = VGroup(colored_, y_line, z_line)

        coord_lines = VGroup(
            plane.axes[0], plane.axes[1], z_axis,
        )
        for i1, i2 in [(0, 2), (1, 0), (2, 1)]:
            coord_lines[i1].target = coord_lines[i2].copy()

        new_title = OldTexText("Imaginary plane")
        new_title.replace(self.title)
        new_title.move_to(self.title)

        self.add(z_axis, plane, z_axis_top)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-80 * DEGREES,
            added_anims=[
                plane.set_stroke, {"opacity": 0.5},
            ],
            run_time=2,
        )
        self.begin_ambient_camera_rotation(rate=0.02)
        self.wait()
        self.play(FadeIn(j_labels, IN))
        z_axis.add(j_labels)
        self.play(
            ShowCreationThenDestruction(z_unit_line),
            run_time=2
        )
        self.wait(4)

        group = VGroup(*it.chain(plane.coordinate_labels, j_labels))
        for label in group:
            label.generate_target()
            axis = np.ones(3)
            label.target.rotate_about_origin(-120 * DEGREES, axis=axis)
            label.target.rotate(120 * DEGREES, axis=axis)
        for y, label in zip([-2, -1, 1, 2], j_labels):
            label.target.scale(0.65)
            label.target.next_to(
                2 * y * UP, RIGHT, 2 * SMALL_BUFF
            )
        self.remove(z_axis_top)
        self.play(
            LaggedStartMap(MoveToTarget, group, lag_ratio=0.8),
            LaggedStartMap(MoveToTarget, coord_lines, lag_ratio=0.8),
            FadeOut(self.title),
            FadeIn(new_title),
            run_time=3
        )
        self.add(z_axis_top)
        self.wait(3)
        for line, wait in zip(colored_coord_lines, [False, True, True]):
            self.play(
                ShowCreationThenDestruction(line),
                run_time=2
            )
            if wait:
                self.wait()

    def show_example_number(self):
        x, y, z = coords = 2 * np.array([1.5, -1, 1.25])
        dot = Sphere(radius=0.05)
        dot.set_fill(GREY_B)
        dot.move_to(coords)
        point_line = Line(ORIGIN, coords)
        point_line.set_stroke(WHITE, 1)

        z_line = Line(ORIGIN, z * OUT)
        x_line = Line(z_line.get_end(), z_line.get_end() + x * RIGHT)
        y_line = Line(x_line.get_end(), x_line.get_end() + y * UP)

        x_line.set_stroke(GREEN, 5)
        y_line.set_stroke(RED, 5)
        z_line.set_stroke(YELLOW, 5)
        lines = VGroup(z_line, x_line, y_line)

        number_label = OldTex(
            str(z / 2), "+", str(x / 2), "i", "+", str(y / 2), "j",
            tex_to_color_map={
                str(z / 2): YELLOW,
                str(x / 2): GREEN,
                str(y / 2): RED,
            }
        )
        number_label.next_to(ORIGIN, RIGHT, LARGE_BUFF)
        number_label.to_edge(UP)

        self.add_fixed_in_frame_mobjects(number_label)
        self.play(
            ShowCreation(point_line),
            FadeIn(dot, -coords),
            FadeInFromDown(number_label)
        )
        self.wait()
        for num, line in zip([z, x, y], lines):
            tex = number_label.get_part_by_tex(str(num / 2))
            rect = SurroundingRectangle(tex)
            rect.set_color(WHITE)

            self.add_fixed_in_frame_mobjects(rect)
            self.play(
                ShowCreation(line),
                ShowCreationThenDestruction(rect),
                run_time=2
            )
            self.remove_fixed_in_frame_mobjects(rect)
            self.wait()
        self.wait(15)
