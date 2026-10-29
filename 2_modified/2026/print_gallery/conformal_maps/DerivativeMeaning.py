# ==============================================================================
# Scene:      DerivativeMeaning
# Source:     videos/_2026/print_gallery/conformal_maps.py (lines 807-1277)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DerivativeMeaning.py DerivativeMeaning -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Axes.add_axis_labels does not exist in this ManimGL: axes.add(axes.get_axis_labels(...)) is used (also for localAxes)
#   - FadeOut(input_space) together with ReplacementTransform(input_space.numbers, ...) failed (ValueError on data shapes); the numbers are separated from the axes before animating
# ==============================================================================

from manim_imports_ext import *
import math

class DerivativeMeaning(InteractiveScene):
    def construct(self):
        # Plot a function
        x_range = (-3, 3)
        y_range = (-3, 3)
        axes = Axes(
            x_range=x_range,
            y_range=y_range
        ).set_stroke(width=5, color=GREY)
        # CHANGE: Axes.add_axis_labels does not exist in this ManimGL; get_axis_labels creates the labels (and stores them in axes.axis_labels), then they are added to the axes.
        axes.add(axes.get_axis_labels("x", "f(x)"))
        axes.add_coordinate_labels(font_size=18, excluding=[])
        axes.coordinate_labels[0][x_range[1]].set_opacity(0)
        axes.coordinate_labels[1][y_range[1]].set_opacity(0)
        self.add(axes)
        self.wait(1)

        def func(x):
            return x**3 + 3 * x**2 - x - 3

        curve = ParametricCurve(
            lambda t: (axes.c2p(t, func(t))), (-3.5, x_range[1], 0.1)
        ).set_stroke(width=8, color=BLUE, opacity=0.7)
        f_of_x = Tex(
            r"f(x) = x^3 + 3x^2 - x - 4",
            font_size=40
        ).set_color(BLUE).to_corner(UR, buff=0.5).fix_in_frame()
        self.play(Write(f_of_x, run_time=2), ShowCreation(curve, run_time=4))
        self.wait(1)

        # Draw a set of local axes labeled dx and dy
        points = curve.get_points()
        points_index = 20
        localAxes = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5)
        )
        # CHANGE: same as above, get_axis_labels is used instead of add_axis_labels.
        localAxes.add(localAxes.get_axis_labels("dx", "df(x)"))
        localAxes.axis_labels.set_opacity(0)
        localAxes.set_stroke(width=3, color=GREY).scale(0.1).move_to(points[points_index]).shift(RIGHT * 0.014)
        self.bring_to_back(localAxes)
        self.play(FadeIn(localAxes))

        # Zoom in on part of the graph
        self.camera.frame.save_state()
        self.play(
            FadeOut(f_of_x),
            self.camera.frame.animate(run_time=7).scale(0.008).move_to(points[points_index] + DOWN * 0.01),
            localAxes.animate(run_time=7).set_stroke(width=5)
        )

        # Show small changes in x and y
        brace_x = Brace(Line(ORIGIN, RIGHT), DOWN).set_color(YELLOW).scale(0.011).align_to(localAxes.c2p(0, 0), UL)
        delta_x = Tex(r"\Delta x", font_size=0.5).set_color(YELLOW).next_to(brace_x, DOWN, buff=0.002)
        self.play(GrowFromEdge(brace_x, UP), Write(delta_x))
        brace_f_of_x = Brace(Line(ORIGIN, UP * 2.8), RIGHT).set_color(PINK).scale(0.011).align_to(brace_x.get_corner(UR), DL)
        delta_f_of_x = Tex(r"\Delta f(x)", font_size=0.5).set_color(PINK).next_to(brace_f_of_x, RIGHT, buff=0.002)
        self.play(GrowFromEdge(brace_f_of_x, LEFT), Write(delta_f_of_x))

        # Show that delta f(x) = delta x*c
        equation = Tex(
            r"\Delta f(x)", r"\ \approx\ ", r"\Delta x", r"\ \cdot\ {c}", r"\text{(at a small scale)}",
            tex_to_color_map={r"\Delta f(x)": PINK, r"\Delta x": YELLOW, "{c}": GREEN},
        )
        equation[r"\text{(at a small scale)}"].scale(0.85).next_to(equation[:-15], DOWN)

        smallScaleOpacityTracker = ValueTracker(0)

        def update_equation(m):
            m.set_height(
                0.46 * self.camera.frame.get_height() / FRAME_HEIGHT
            ).align_to(
                self.camera.frame, UL
            ).shift(
                DR * 0.5 * self.camera.frame.get_width() / FRAME_WIDTH
            )
            m[-15:].set_opacity(smallScaleOpacityTracker.get_value())
        equation.add_updater(update_equation)
        delta_f_of_x_copy = delta_f_of_x.copy()
        delta_x_copy = delta_x.copy()
        equation_copy = equation.copy()
        self.play(
            AnimationGroup(
                ReplacementTransform(delta_f_of_x_copy, equation_copy[r"\Delta f(x)"], path_arc=PI * 0.2),
                Write(equation_copy[r"\approx"]),
                ReplacementTransform(delta_x_copy, equation_copy[r"\Delta x"], path_arc=PI * 0.2),
                Write(equation_copy[r"\ \cdot\ {c}"]), lag_ratio=0.4), run_time=2.5)
        self.remove(delta_x_copy, delta_f_of_x_copy, equation_copy)
        self.add(equation)
        self.wait(2)
        rect = SurroundingRectangle(equation[:-15], buff=0.002, fill_opacity=0, stroke_width=4, stroke_color=TEAL)
        self.play(ShowCreation(rect, run_time=2))
        self.play(FadeOut(rect))
        self.wait(1)

        # Zoom back out to see the graph
        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(VGroup(localAxes, brace_x, brace_f_of_x, delta_x, delta_f_of_x)),
                    smallScaleOpacityTracker.animate(run_time=4).set_value(1),
                    self.camera.frame.animate(run_time=7).restore()
                ),
                FadeIn(f_of_x), lag_ratio=0.8)
        )
        self.wait(0.5)

        # View the function as a transformation
        self.play(FadeOut(VGroup(axes.get_y_axis(), curve)), axes.coordinate_labels[0][x_range[1]].animate.set_opacity(1))
        input_space = axes.get_x_axis()
        input_space[1].set_color(YELLOW)
        n = 250
        x_min = 0
        x_max = 3
        dots = VGroup(*[
            Dot(radius=0.001).set_stroke(width=10).set_color(
                interpolate_color(YELLOW_E, YELLOW_A, i / n)
            ).move_to(
                input_space.n2p(x_min + (i / (n - 1)) * (x_max - x_min))
            )
            for i in range(n)
        ])
        self.play(AnimationGroup(*[FadeIn(dot, shift=DOWN) for dot in dots], lag_ratio=0.003))
        input_space_group = Group(input_space, Point(), dots)
        input_space_group.generate_target()
        output_space = input_space.copy()
        f_of_x_label = Tex("f(x)").set_color(PINK)
        f_of_x_label.set_height(
            input_space[1].get_height() / f_of_x_label[1].get_height()
        ).match_y(
            output_space[1]
        ).align_to(
            output_space[1], LEFT
        )
        output_space[1].become(f_of_x_label)
        Group(input_space_group.target, output_space).arrange(buff=0.7).set_width(FRAME_WIDTH * 0.98)

        input_space_text = TexText("Input Space", font_size=60).next_to(input_space_group.target[0], DOWN, buff=0.5).set_color(YELLOW)
        output_space_text = TexText("Output Space", font_size=60).next_to(output_space, DOWN, buff=0.5).set_color(PINK)
        equation.clear_updaters()
        equation.generate_target()
        equation.target.set_x(0).to_edge(DOWN, buff=0.7)
        equation.target[-15:].next_to(equation.target[:-15], RIGHT, buff=0.25)
        self.play(
            f_of_x.animate.match_x(output_space).set_color(WHITE).set_color_by_tex_to_color_map({"f": PINK, "x": YELLOW}),
            MoveToTarget(equation, run_time=2),
            AnimationGroup(
                MoveToTarget(input_space_group),
                FadeIn(output_space, shift=LEFT * 0.5),
                FadeIn(VGroup(input_space_text, output_space_text), shift=UP * 0.4), lag_ratio=0.5),
        )
        equationRect = BackgroundRectangle(equation, buff=0.1)
        equationGroup = VGroup(equationRect, equation)
        self.add(equationGroup)
        equationGroup.fix_in_frame()
        input_dots = dots.copy()
        self.play(
            AnimationGroup(*[
                dots[i].animate(
                    path_arc=-PI * 0.5
                ).move_to(
                    output_space.n2p(func(input_space.p2n(dots[i].get_center())))
                ).set_opacity(
                    0 if func(input_space.p2n(dots[i].get_center())) < x_range[0]
                    or func(input_space.p2n(dots[i].get_center())) > x_range[1]
                    else 1
                ).set_color(
                    interpolate_color(PINK, PURPLE_A, min(1, 2.5 * i / n))
                )
                for i in range(len(dots))
            ], lag_ratio=0.01), run_time=3)

        # Look at the spacing between the dots
        output_dot_index = 50
        self.play(FadeOut(f_of_x), self.camera.frame.animate(run_time=4).move_to(dots[output_dot_index]).scale(0.1))
        humps = VGroup(*[
            ArcBetweenPoints(
                dots[i].get_center(), dots[i + 1].get_center(), angle=PI * 0.9
            ).set_stroke(
                width=5, color=TEAL
            )
            for i in range(len(dots) - 1)
            # if output_space.p2n(dots[i].get_center()) > x_range[0] + 0.01
            # and output_space.p2n(dots[i].get_center()) < x_range[1] - 0.01
        ])
        self.play(AnimationGroup(*[GrowArrow(hump) for hump in humps], lag_ratio=0.025))
        self.wait(3)

        # Zoom in on a particular output
        patch_output = dots[output_dot_index - 3: output_dot_index + 4]
        self.play(self.camera.frame.animate.move_to(patch_output).scale(0.22), run_time=4)
        self.wait(2)

        # Find the corresponding input
        self.add(input_dots)
        camera_width = self.camera.frame.get_width()
        self.play(self.camera.frame.animate.restore(), run_time=1.5)
        patch_input = input_dots[output_dot_index - 3: output_dot_index + 4].copy()
        self.play(self.camera.frame.animate.set_width(camera_width).move_to(patch_input), run_time=2.5)

        # Find a patch from the input space
        self.play(patch_input.animate.shift(UP * 0.01))

        # Show delta xs
        input_patch_humps = VGroup(*[
            ArcBetweenPoints(
                patch_input[i].get_center(), patch_input[i + 1].get_center(), angle=-PI * 0.9
            ).set_stroke(
                width=5, color=TEAL
            )
            for i in range(len(patch_input) - 1)
        ])
        delta_xs = VGroup(*[
            Tex(r"\Delta x", font_size=0.6).set_color(YELLOW).next_to(
                input_patch_humps[i], UP, buff=0.004
            )
            for i in range(6)
        ])
        self.play(AnimationGroup(*[GrowArrow(hump) for hump in input_patch_humps], lag_ratio=0.025))
        self.play(AnimationGroup(*[FadeIn(delta_x, shift=UP * 0.005) for delta_x in delta_xs], lag_ratio=0.15))

        # Move the patch over to the output space
        self.camera.frame.add_updater(lambda m: m.match_x(patch_input).match_z(patch_input))
        self.play(
            VGroup(input_patch_humps, delta_xs, patch_input).animate(
                path_arc=-PI * 0.4,
                path_arc_axis=OUT * 0.1 + DOWN * 2
            ).shift(
                RIGHT * (patch_output[3].get_x() - patch_input[3].get_x())
            ), run_time=3)
        self.wait(1)

        # Show delta f(x)s
        delta_f_of_xs = VGroup(*[
            Tex(r"\Delta f(x)", font_size=1).set_color(PINK).next_to(
                humps[output_dot_index - 3 + i], DOWN, buff=0.01
            )
            for i in range(6)
        ])
        self.play(AnimationGroup(*[FadeIn(delta_f_of_x, shift=DOWN * 0.01) for delta_f_of_x in delta_f_of_xs], lag_ratio=0.15))

        # Line up the dots
        patch_input.generate_target()
        delta_x_value = patch_input[4].get_x() - patch_input[3].get_x()
        delta_f_of_x_value = (patch_output[-1].get_x() - patch_output[0].get_x()) / (len(patch_output) - 1)
        c = delta_f_of_x_value / delta_x_value
        for i in range(len(patch_input)):
            patch_input.target[i].set_x(patch_input[3].get_x() + c * delta_x_value * (i - 3))
        scaled_humps = VGroup(*[
            ArcBetweenPoints(
                patch_input.target[i].get_center(), patch_input.target[i + 1].get_center(), angle=-PI * 0.9
            ).set_stroke(
                width=5, color=TEAL
            )
            for i in range(len(patch_input) - 1)
        ])

        delta_x_times_cs = VGroup(*[
            Tex(r"\Delta x \cdot c", tex_to_color_map={"f": PINK, r"\Delta x": YELLOW, "c": GREEN}, font_size=1).next_to(
                scaled_humps[i], UP, buff=0.01
            )
            for i in range(6)
        ])
        self.play(
            MoveToTarget(patch_input),
            ReplacementTransform(input_patch_humps, scaled_humps),
            AnimationGroup(*[
                ReplacementTransform(delta_xs[i], delta_x_times_cs[i])
                for i in range(len(delta_xs))
            ]),
            self.camera.frame.animate.shift(DOWN * 0.02),
            equationGroup.animate.scale(1.08).shift(UP * 0.35), run_time=2)
        # equation = Tex(
        #     r"\Delta f(x)", r"\ \approx\ ", r"\Delta x", r"\ \cdot\ c",
        #     tex_to_color_map = {r"\Delta f(x)": PINK, r"\Delta x": YELLOW, "c": PINK},
        #     font_size = 1.6
        # ).next_to(delta_x_times_cs, UP, buff = 0.02)
        # self.play(Write(equation), run_time = 2)
        self.wait(2)

        # Zoom back out
        self.camera.frame.clear_updaters()
        self.remove(input_space_text, output_space_text)
        f_of_x.clear_updaters().set_opacity(0)
        self.add(f_of_x)
        self.play(
            self.camera.frame.animate(run_time=3).restore().scale(1.15).shift(UP * 0.6),
            FadeOut(VGroup(equation, delta_x_times_cs, scaled_humps, patch_input, input_dots, dots, humps, delta_f_of_xs)),
            f_of_x.animate.set_opacity(1).next_to(output_space, UP, buff=2.6).shift(LEFT * 0.7 + DOWN * 0.2)
        )

        # Turn the number lines into complex planes
        x_max = x_range[1]
        in_plane, out_plane = planes = VGroup(
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
        )
        in_plane.match_width(input_space[0])
        in_plane.move_to(input_space.ticks[3])
        out_plane.match_width(output_space[0])
        out_plane.move_to(output_space.ticks[3])
        in_plane.add_coordinate_labels(
            list(range(-x_max, x_max + 1)) + [x * 1j for x in list(range(-x_max, x_max + 1)) if x != 0],
            font_size=16
        )
        out_plane.add_coordinate_labels(
            list(range(-x_max, x_max + 1)) + [x * 1j for x in list(range(-x_max, x_max + 1)) if x != 0],
            font_size=16
        )

        in_plane.set_stroke(GREY_D, 1)
        out_plane.set_stroke(GREY_D, 1)

        f_of_z = Tex(
            "f(z) = z^3 + 3z^2 - z - 4",
            font_size=50,
            tex_to_color_map={"f": PINK, "z": YELLOW}
        ).set_stroke(
            width=10, color=BLACK, behind=True
        ).next_to(
            out_plane, UP, buff=0.5
        ).set_x(
            out_plane.c2p(0)[0]
        )
        # CHANGE: FadeOut(input_space) and ReplacementTransform(input_space.numbers, ...) animate the same
        # numbers at once and in this ManimGL the FadeOut fails (ValueError: different data sizes after
        # aligning the points); the numbers are separated from the axes and left as independent mobjects.
        input_numbers = input_space.numbers
        output_numbers = output_space.numbers
        input_space.remove(input_numbers)
        output_space.remove(output_numbers)
        self.add(input_numbers, output_numbers)
        self.play(
            AnimationGroup(
                FadeOut(input_space),
                ReplacementTransform(input_numbers, in_plane.coordinate_labels[:x_max * 2 + 1]),
                FadeIn(VGroup(in_plane[:4], in_plane.coordinate_labels[x_max * 2 + 1:]), shift=UP * 0.5)
            ),
            AnimationGroup(
                FadeOut(output_space),
                ReplacementTransform(output_numbers, out_plane.coordinate_labels[:x_max * 2 + 1]),
                FadeIn(VGroup(out_plane[:4], out_plane.coordinate_labels[x_max * 2 + 1:]), shift=UP * 0.5)
            ),
            FadeOut(f_of_x),
            FadeIn(f_of_z)
        )

        # Show the transformation
        grid_size = 3
        squares = Square().get_grid(grid_size, grid_size, buff=0)
        squares.replace(in_plane)
        squares.set_stroke(WHITE, 1, 0.5)
        squares.set_width(0.07).move_to(in_plane.n2p(-0.8 + 0.2j))

        moving_plane = squares.copy()
        input_patch = moving_plane.copy().set_fill(color=BLACK, opacity=0.3)
        moving_plane.insert_n_curves(10)
        moving_plane.target = moving_plane.generate_target()
        moving_plane.target.apply_function(lambda p: out_plane.n2p(func(in_plane.p2n(p))))
        moving_plane.target.set_color(PINK)

        square_index = 895
        self.add(in_plane, out_plane, moving_plane, Point(), f_of_z)
        self.camera.frame.save_state()
        destination = out_plane.n2p(func(in_plane.p2n(input_patch.get_center())))
        self.play(
            AnimationGroup(
                self.camera.frame.animate.scale(0.04, about_point=moving_plane.get_center()),
                FadeIn(moving_plane), lag_ratio=0.4), run_time=2)
        self.play(self.camera.frame.animate.move_to(destination).scale(3), MoveToTarget(moving_plane), run_time=6)
        self.wait(2)

        # Find the tiny patch of squares
        self.play(self.camera.frame.animate.restore(), run_time=1.5)
        self.play(self.camera.frame.animate.scale(0.01).move_to(input_patch), FadeIn(input_patch), run_time=3)

        # Show delta zs
        delta_z_arrows = VGroup(*[
            Arrow(
                input_patch[grid_size * grid_size // 2].get_center(),
                input_patch[i].get_center(),
                buff=0,
                thickness=0.06
            ).set_color(
                YELLOW
            ).scale(
                math.sqrt(0.5) if i in [0, 2, 6, 8] else 1,
                about_point=input_patch[grid_size * grid_size // 2].get_center()
            )
            for i in range(len(input_patch)) if i != grid_size * grid_size // 2
        ])
        delta_zs = VGroup(*[
            Tex(r"\Delta z", font_size=0.5).set_color(YELLOW).next_to(arrow.get_end(), arrow.get_end() - arrow.get_start(), buff=0.1)
            for arrow in delta_z_arrows
        ])
        delta_zs[1].shift(LEFT * 0.0025)
        # delta_zs[3].shift(UP*0.001)
        # delta_zs[4].shift(UP*0.002)
        delta_zs[6].shift(LEFT * 0.0025)
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    GrowArrow(delta_z_arrows[i]),
                    FadeIn(delta_zs[i]), lag_ratio=0.6)
                for i in range(len(delta_z_arrows))
            ], lag_ratio=0.1)
        )

        # Move the patch over to the output space
        self.camera.frame.add_updater(lambda m: m.move_to(input_patch))
        self.play(
            VGroup(input_patch, delta_z_arrows, delta_zs).animate(
                path_arc=-PI * 0.01
            ).move_to(
                destination
            ),
            self.camera.frame.animate.scale(3.8), run_time=3)
        self.wait(1)

        # Show delta f(z)s
        delta_f_of_z_arrows = VGroup(*[
            Arrow(
                moving_plane.target[grid_size * grid_size // 2].get_center(),
                moving_plane.target[i].get_center(),
                buff=0,
                thickness=0.12
            ).set_color(
                PINK
            ).scale(
                math.sqrt(0.5) if i in [0, 2, 6, 8] else 1,
                about_point=moving_plane.target[grid_size * grid_size // 2].get_center()
            )
            for i in range(len(moving_plane.target)) if i != grid_size * grid_size // 2
        ])
        delta_f_of_zs = VGroup(*[
            Tex(r"\Delta f(z)", font_size=1.5).set_color(PINK).next_to(arrow.get_end(), arrow.get_end() - arrow.get_start(), buff=0.04)
            for arrow in delta_f_of_z_arrows
        ])
        delta_f_of_zs[1].shift(RIGHT * 0.015)
        delta_f_of_zs[3].shift(UP * 0.003)
        delta_f_of_zs[4].shift(DOWN * 0.004)
        delta_f_of_zs[6].shift(LEFT * 0.02)
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    GrowArrow(delta_f_of_z_arrows[i]),
                    FadeIn(delta_f_of_zs[i]), lag_ratio=0.6)
                for i in range(len(delta_f_of_z_arrows))
            ], lag_ratio=0.1),
            VGroup(input_patch, delta_z_arrows, delta_zs).animate.shift(0)
        )

        # Write delta f(z) = delta z * c
        equation = Tex(
            r"\Delta f(z)", r"\ \approx\ ", r"\Delta z", r"\ \cdot\ c",
            tex_to_color_map={r"\Delta f(z)": PINK, r"\Delta z": YELLOW, "c": GREEN},
            font_size=3
        ).next_to(moving_plane.target, LEFT, buff=0.02)
        self.camera.frame.clear_updaters()
        self.play(self.camera.frame.animate.shift(LEFT * 0.1))
        self.play(Write(equation), run_time=1)

        # Line up the grids
        delta_z_times_cs = VGroup(*[
            Tex(r"\Delta z \cdot c", font_size=1.5, tex_to_color_map={r"\Delta z": YELLOW, "c": GREEN}).next_to(arrow.get_end(), arrow.get_end() - arrow.get_start(), buff=0.04)
            for arrow in delta_f_of_z_arrows
        ])
        delta_z_times_cs[1].shift(RIGHT * 0.015)
        delta_z_times_cs[3].shift(UP * 0.003)
        delta_z_times_cs[4].shift(DOWN * 0.004)
        delta_z_times_cs[6].shift(LEFT * 0.02)
        input_patch_group = VGroup(input_patch, delta_z_arrows)
        input_patch_group.generate_target()
        input_patch_group.target.scale(4).rotate(-PI * 0.019).set_opacity(1)
        input_patch_group.target[1].set_color(PINK)
        self.play(
            MoveToTarget(input_patch_group),
            AnimationGroup(*[ReplacementTransform(delta_zs[::-1][i], delta_z_times_cs[i]) for i in range(len(delta_zs))]), run_time=2)

        self.wait(3)
