# ==============================================================================
# Scene:      ComplexExtension
# Source:     videos/_2025/laplace/main_equations.py (lines 1497-1657)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexExtension.py ComplexExtension -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexExtension(InteractiveScene):
    def construct(self):
        # Set up input and output planes
        input_plane, output_plane = planes = VGroup(
            ComplexPlane((-3, 3), (-3, 3))
            for n in range(2)
        )
        planes.set_height(5)
        planes.arrange(RIGHT, buff=1.5)
        for plane in planes:
            plane.axes.set_stroke(WHITE, 1, 1)
            plane.background_lines.set_stroke(BLUE, 1, 0.5)
            plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)

        self.add(planes)

        # Set up limited domain
        domain = self.get_rect_group(2, 1, input_plane, 0.2 + 0.2j)
        domain.set_z_index(2)
        self.add(domain)

        # Show a mapping
        def func(z):
            return -0.05j * z**3

        def point_func(points):
            return np.array([
                output_plane.n2p(func(input_plane.p2n(p)))
                for p in points
            ])

        mapped_domain = domain.copy().apply_points_function(point_func, about_edge=None)
        mapped_domain.set_z_index(2)

        arrow = Arrow(
            domain.get_top(),
            mapped_domain.get_top(),
            path_arc=-90 * DEG,
            fill_color=TEAL,
            thickness=5
        )
        arrow.set_z_index(1)
        func_label = Tex(R"f(z)")
        func_label.next_to(arrow, UP, SMALL_BUFF)
        func_label.set_backstroke()

        self.play(
            Write(arrow, time_span=(0, 1)),
            Write(func_label, time_span=(0.5, 1.5)),
            ReplacementTransform(
                domain.copy().set_fill(opacity=0),
                mapped_domain,
                path_arc=-90 * DEG,
                run_time=3
            )
        )

        # Show the extension
        dark_red = interpolate_color(RED_E, BLACK, 0.5)
        extension = self.get_extended_domain(input_plane, domain, 4, 2, corner_value=-1, color=dark_red)
        mapped_extension = extension.copy().apply_points_function(point_func, about_edge=None)

        self.play(Write(extension, run_time=1, lag_ratio=1e-2))
        self.wait()
        self.play(
            TransformFromCopy(extension.copy().set_fill(opacity=0), mapped_extension, path_arc=-90 * DEG),
            run_time=3
        )
        self.wait()

        # Two possibilities
        frame = self.frame
        possibilities = VGroup(
            Text("1) There is no such extension", font_size=72),
            Text("2) There is only one extension", font_size=72),
        )
        possibilities.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        possibilities.next_to(planes, UP, buff=LARGE_BUFF)
        only_one = possibilities[1]["only one"][0]
        underline = Underline(only_one, buff=-SMALL_BUFF).set_stroke(YELLOW)

        self.play(
            Write(possibilities[0][:2]),
            Write(possibilities[1][:2]),
            frame.animate.reorient(0, 0, 0, (0, 1.5, 0.0), 9).set_anim_args(time_span=(0, 1)),
            run_time=2
        )
        self.wait()
        self.play(FadeIn(possibilities[0][2:], lag_ratio=0.1))
        self.wait()
        self.play(FadeIn(possibilities[1][2:], lag_ratio=0.1))
        self.play(
            ShowCreation(underline),
            only_one.animate.set_fill(YELLOW)
        )
        self.wait()

        # Analytic continuation
        ac_words = Text("Analytic Continuation", font_size=72)
        ac_words.next_to(output_plane, UP, MED_LARGE_BUFF)

        darkest_red = interpolate_color(RED_E, BLACK, 0.9)
        big_domain = self.get_extended_domain(input_plane, extension, 6, 6, corner_value=-3 - 3j, color=darkest_red)
        big_domain.set_stroke(WHITE, 0.5, 0.1)
        big_domain.set_fill(dark_red, 0.5)
        mapped_big_domain = big_domain.copy().apply_points_function(point_func, about_edge=None)

        self.play(
            FadeOut(possibilities, lag_ratio=0.05),
            FadeOut(underline),
            Write(ac_words, time_span=(0.5, 2.)),
        )
        self.play(
            Write(mapped_big_domain, lag_ratio=5e-2, stroke_color=RED, stroke_width=0.5),
            Write(big_domain, lag_ratio=5e-2, stroke_color=RED, stroke_width=0.5),
            run_time=8
        )
        self.wait()

    def get_extended_domain(self, plane, domain, width, height, corner_value, color=RED_E):
        extension = self.get_rect_group(width, height, plane, corner_value=corner_value, color=color)

        min_x = domain.get_x(LEFT)
        max_x = domain.get_x(RIGHT)
        min_y = domain.get_y(DOWN)
        max_y = domain.get_y(UP)
        to_remove = list()
        for square in extension:
            if (min_x < square.get_x() < max_x) and (min_y < square.get_y() < max_y):
                to_remove.append(square)
        extension.remove(*to_remove)
        extension.sort(lambda p: get_norm(p - domain.get_center()))
        return extension

    def get_rect_group(self, width, height, plane, corner_value=0, square_density=5, color=BLUE_E):
        square = Square(side_length=plane.x_axis.get_unit_size() / square_density)
        square.set_stroke(WHITE, 0.5)
        square.set_fill(color, 1)
        square.insert_n_curves(20)
        grid = square.get_grid(square_density * height, square_density * width, buff=0)
        grid.move_to(plane.n2p(corner_value), DL)
        return grid

        rect = Rectangle(width, height)
        rect.set_width(width * plane.x_axis.get_unit_size())
        rect.move_to(plane.n2p(corner_value), DL)
        rect.set_stroke(color, 2)
        rect.set_fill(color, 1)
        rect.insert_n_curves(200)

        rect_lines = VGroup(
            Line(DOWN, UP).get_grid(1, width * line_density + 1, buff=SMALL_BUFF),
            Line(LEFT, RIGHT).get_grid(height * line_density + 1, 1, buff=SMALL_BUFF),
        )
        for group in rect_lines:
            group.replace(rect, stretch=True)
            group.set_stroke(WHITE, 1, 0.5)
            for line in group:
                line.insert_n_curves(20)

        return VGroup(rect, rect_lines)
