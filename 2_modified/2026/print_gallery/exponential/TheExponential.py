# ==============================================================================
# Scene:      TheExponential
# Source:     videos/_2026/print_gallery/exponential.py (lines 429-1250)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TheExponential.py TheExponential -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Typo in the original: frame.animate.reorient.reorient(...) -> frame.animate.reorient(...)
# ==============================================================================

from manim_imports_ext import *

def apply_func_between_planes(mob, func, src_plane, trg_plane):
    mob.shift(-src_plane.get_origin())
    mob.scale(1.0 / src_plane.get_unit_size(), about_point=ORIGIN)
    mob.apply_complex_function(func)
    mob.scale(trg_plane.get_unit_size(), about_point=ORIGIN)
    mob.shift(trg_plane.get_origin())
    return mob


class TheExponential(InteractiveScene):
    def construct(self):
        # Set up input and output space, top an bottom
        in_line = NumberLine((-5, 5), unit_size=1.5)
        in_line.move_to(2 * UP)
        in_line.add_numbers(font_size=20)

        out_line = NumberLine((-21, 21), unit_size=1.5)
        out_line.move_to(2 * DOWN)
        out_line.add_numbers(font_size=20)

        arrow_buff = 0.75
        func_arrow = Arrow(in_line.n2p(0), out_line.n2p(1), buff=arrow_buff, thickness=6)
        func_label = Tex(R"e^{x}", font_size=72)
        func_label.next_to(func_arrow.get_center(), UR, buff=MED_SMALL_BUFF)
        og_func_arrow = func_arrow.copy()

        self.add(in_line, out_line)

        # Show example dots
        sample_xs = np.arange(-4, 4.25, 0.25)
        in_dots = Group(*[TrueDot(in_line.n2p(x)) for x in sample_xs])
        out_dots = Group(*[TrueDot(out_line.n2p(np.exp(x))) for x in sample_xs])
        all_dots = Group(in_dots, out_dots)
        for dots in all_dots:
            for dot in dots:
                dot.set_radius(0.1)
                dot.make_3d()
                dot.deactivate_depth_test()
                dot.set_glow_factor(0.15)
            dots.set_submobject_colors_by_gradient(YELLOW, BLUE, interp_by_hsl=True)

        self.play(LaggedStartMap(FadeIn, in_dots, lag_ratio=0.1, run_time=1))
        self.play(
            GrowArrow(func_arrow),
            FadeIn(func_label, 0.25 * func_arrow.get_vector()),
            TransformFromCopy(in_dots, out_dots, lag_ratio=0.01, run_time=2),
        )
        self.wait()

        # Show a few real-valued inputs
        frame = self.frame
        x_tracker = ValueTracker(0)
        get_x = x_tracker.get_value

        def get_y():
            return np.exp(get_x())

        in_dot = in_dots[-1].copy()
        out_dot = out_dots[0].copy()
        in_dot.add_updater(lambda m: m.move_to(in_line.n2p(get_x())))
        out_dot.add_updater(lambda m: m.move_to(out_line.n2p(get_y())))

        active_func_arrow = func_arrow.copy()
        active_func_arrow.add_updater(lambda m: m.set_points_by_ends(
            in_line.n2p(get_x()),
            out_line.n2p(get_y()),
            buff=0.5
        ))

        active_func_label = Tex(R"e^{+0.00} = 1.000")
        active_func_label.make_number_changeable("+0.00", include_sign=True).f_always.set_value(get_x)
        active_func_label.make_number_changeable("1.000").f_always.set_value(get_y)
        active_func_label.always.next_to(active_func_arrow.get_center(), UR, MED_SMALL_BUFF)

        output_labels = VGroup(
            Tex(Rf"e^{{{n}}}", font_size=36).next_to(out_line.n2p(np.exp(n)), UP, MED_SMALL_BUFF)
            for n in range(4)
        )

        all_dots.target = all_dots.generate_target()
        all_dots.target.set_opacity(0.25)
        for dot, opacity in zip(all_dots.target[1][:12], np.linspace(0, 0.25, 12)):
            dot.set_opacity(opacity)

        self.play(
            MoveToTarget(all_dots),
            ReplacementTransform(func_arrow, active_func_arrow),
            FadeTransformPieces(func_label, active_func_label),
            FadeIn(in_dot),
            FadeIn(out_dot),
        )
        self.wait()
        self.play(FlashAround(in_dot))
        self.play(TransformFromCopy(in_dot, out_dot, suspend_mobject_updating=True, path_arc=30 * DEG))
        self.add(output_labels[0])
        self.play(FlashAround(out_dot))
        self.wait()
        self.play(
            x_tracker.animate.set_value(1),
            frame.animate.set_x(5),
            run_time=5
        )
        self.add(output_labels[1])
        self.wait()
        self.play(
            x_tracker.animate.set_value(2),
            frame.animate.set_x(5),
        )
        self.add(output_labels[2])
        self.wait()
        self.play(
            x_tracker.animate.set_value(3),
            frame.animate.set_height(16).set_x(17),
            run_time=2
        )
        self.add(output_labels[3])
        self.wait()

        # Show negative inputs
        self.play(
            x_tracker.animate.set_value(-1),
            frame.animate.set_height(8).move_to(ORIGIN),
            run_time=8
        )
        self.play(x_tracker.animate.set_value(-4), run_time=6)
        self.wait()
        self.play(FadeOut(Group(in_dots, out_dots, in_dot, out_dot, active_func_label, output_labels)))

        # Transition to a side-by-side view
        x_max = 7
        in_plane, out_plane = [
            ComplexPlane(
                (-x_max, x_max),
                (-x_max, x_max),
                unit_size=0.4,
                faded_line_ratio=0,
                background_line_style=dict(stroke_color=BLUE_D, stroke_width=1),
                axis_config=dict(stroke_color=GREY_A, stroke_width=1),
            )
            for _ in range(2)
        ]
        in_plane.to_edge(LEFT)
        out_plane.to_edge(RIGHT)
        func_arrow.set_points_by_ends(in_plane.get_right(), out_plane.get_left(), buff=0.25)
        func_label = Tex(R"e^{z}")
        func_label.next_to(func_arrow, DOWN, SMALL_BUFF)

        for line, plane, in [(in_line, in_plane), (out_line, out_plane)]:
            line.target = line.generate_target()
            scale_factor = plane.x_axis.get_unit_size() / line.get_unit_size()
            shift_vect = plane.n2p(0) - line.n2p(0)
            line.target.scale(scale_factor)
            line.target.shift(shift_vect)
            line.target.set_opacity(0)
            plane.add_coordinate_labels(font_size=12, buff=0.05)
            plane.save_state()
            plane.scale(1.0 / scale_factor)
            plane.shift(-shift_vect)
            plane.set_opacity(0)

        active_func_arrow.clear_updaters()
        self.play(
            LaggedStart(
                AnimationGroup(MoveToTarget(in_line), Restore(in_plane)),
                AnimationGroup(MoveToTarget(out_line), Restore(out_plane)),
                lag_ratio=0.3
            ),
            ReplacementTransform(active_func_arrow, func_arrow),
            FadeIn(func_label, time_span=(1.5, 2)),
            run_time=2
        )
        self.wait()

        # Add input and output dots
        z_tracker = ComplexValueTracker(0)
        get_z = z_tracker.get_value

        def get_w():
            return np.exp(get_z())

        in_dot.clear_updaters()
        out_dot.clear_updaters()

        in_dot.set_radius(0.06)
        out_dot.set_radius(0.06)
        in_dot.add_updater(lambda m: m.move_to(in_plane.n2p(get_z())))
        out_dot.add_updater(lambda m: m.move_to(out_plane.n2p(get_w())))

        z_label = VGroup(Tex(R"z = "), DecimalNumber(complex(1, 1)))
        z_label.arrange(RIGHT)
        z_label.set_height(0.2)
        z_label[1].shift(0.05 * UP)
        z_label.set_backstroke(BLACK, 3)
        z_label.set_z_index(1)
        z_label[1].f_always.set_value(get_z)
        z_label.always.next_to(in_dot, UR, buff=0.05)

        self.play(
            FadeIn(in_dot),
            FadeIn(out_dot),
            FadeIn(z_label),
            in_plane.background_lines.animate.set_stroke(opacity=0.5),
            out_plane.background_lines.animate.set_stroke(opacity=0.5),
        )

        # Walk up the imaginary line
        def apply_exp_to_input_shape(mob):
            mob.apply_points_function(lambda ps: np.array([
                out_plane.n2p(np.exp(in_plane.p2n(p)))
                for p in ps
            ]), about_point=ORIGIN)
            return mob

        def get_line_circle_pair(x, line_color=BLUE, circle_color=YELLOW, stroke_width=2):
            v_line = Line(in_plane.n2p(x), in_plane.n2p(complex(x, TAU)))
            v_line.set_stroke(line_color, stroke_width)
            out_circle = apply_exp_to_input_shape(v_line.copy().insert_n_curves(100).set_stroke(circle_color))
            return v_line, out_circle

        v_lines = VGroup()
        out_circles = VGroup()
        x_values = [0, 1, 2, -1, -2]
        for x in x_values:
            v_line, out_circle = get_line_circle_pair(x)

            self.play(z_tracker.animate.set_value(x))
            self.play(
                z_tracker.animate.increment_value(complex(0, TAU)),
                ShowCreation(v_line),
                ShowCreation(out_circle),
                run_time=6
            )
            self.wait()
            self.play(z_tracker.animate.set_value(x), run_time=2)

            v_lines.add(v_line)
            out_circles.add(out_circle)

        self.play(z_tracker.animate.set_value(2), run_time=2)
        self.wait()

        # Show one unit to one radian
        z_tracker.set_value(complex(2, TAU))
        z_unit = in_plane.get_unit_size()
        left_rect = Rectangle(2 * z_unit, z_unit)
        left_rect.move_to(in_plane.n2p(0), DL)
        left_rect.insert_n_curves(100)
        left_rect.set_stroke(TEAL, 2)
        left_rect.set_fill(TEAL, 0.3)
        brace = Brace(left_rect, RIGHT, SMALL_BUFF)
        brace.stretch(0.5, 0, about_edge=LEFT)
        brace_label = brace.get_tex("+i", font_size=30)
        left_rect.save_state()
        left_rect.stretch(1e-2, 1, about_edge=DOWN)

        rad_label = Text("+1 Radian", font_size=30)
        rad_label.add_updater(lambda m: m.move_to(
            out_plane.n2p(np.exp(z_tracker.get_value() - 0.5j - 0.3))
        ))
        rad_label.set_backstroke(BLACK, 3)

        sector = always_redraw(
            lambda: apply_func_between_planes(left_rect.copy(), np.exp, in_plane, out_plane)
        )

        two_pi_brace = Brace(v_lines, RIGHT, SMALL_BUFF)
        two_pi_label = two_pi_brace.get_tex(R"+2\pi i")

        self.play(
            z_tracker.animate.set_value(2),
            frame.animate.reorient(0, 0, 0, (-2.7, 0.42, 0.0), 2.48),
            run_time=1,
        )
        self.play(
            Restore(left_rect),
            GrowFromPoint(brace, brace.get_bottom()),
            FadeIn(brace_label, 0.1 * UP),
            z_tracker.animate.increment_value(1j),
            run_time=2
        )
        self.wait()
        sector.update()
        rad_label.update()
        rad_label.suspend_updating()
        self.play(
            TransformFromCopy(left_rect, sector),
            FadeTransformPieces(brace_label, rad_label),
            frame.animate.reorient(0, 0, 0, (5.8, 1.11, 0.0), 3.22),
            run_time=3
        )
        self.wait()
        rad_label.resume_updating()
        left_group = VGroup(left_rect, brace, brace_label)
        for n in range(5):
            self.play(
                frame.animate.to_default_state(),
                z_tracker.animate.increment_value(1j),
                left_group.animate.shift(z_unit * UP),
                run_time=1,
            )
            self.wait()
        self.play(
            z_tracker.animate.increment_value((TAU - 6) * 1j),
            FadeOut(left_rect),
            FadeOut(sector),
            FadeOut(rad_label),
            ReplacementTransform(brace, two_pi_brace),
            FadeTransform(brace_label, two_pi_label),
        )
        self.wait()
        self.play(
            FadeOut(two_pi_brace),
            FadeOut(two_pi_label),
        )

        # Note the height of the lines
        brace = Brace(v_lines, LEFT, buff=SMALL_BUFF)
        brace_label = brace.get_tex(R"2\pi")

        self.play(
            GrowFromCenter(brace),
            Write(brace_label),
        )
        self.wait()

        # Map lines to circles
        v_lines.sort(lambda p: p[0])
        out_circles.submobjects.sort(key=lambda m: m.get_width())
        out_circles.note_changed_family(only_changed_order=True)
        circle_ghosts = out_circles.copy()
        circle_ghosts.set_stroke(opacity=0.25)

        self.add(circle_ghosts)
        self.play(
            FadeOut(out_circles),
            LaggedStartMap(ShowCreation, v_lines, lag_ratio=0.1),
            run_time=2
        )
        self.play(LaggedStart(
            (TransformFromCopy(line, circle, path_arc=(0, 0.3 * PI))
            for line, circle in zip(v_lines, out_circles)),
            lag_ratio=0.25,
            run_time=5
        ))
        self.wait()

        # Emphasize spacing by 1
        top_arrows = VGroup(
            Arrow(vl1.get_top(), vl2.get_top(), path_arc=-180 * DEG, thickness=2, buff=0.1, fill_color=TEAL)
            for vl1, vl2 in zip(v_lines, v_lines[1:])
        )
        top_labels = VGroup(
            Tex(R"+1", font_size=20).next_to(arrow, UP, buff=0.05)
            for arrow in top_arrows
        )

        self.play(
            LaggedStartMap(Write, top_arrows, lag_ratio=0.25),
            LaggedStartMap(FadeIn, top_labels, shift=0.1 * UP, lag_ratio=0.25),
        )
        self.wait()

        # Emphasize scale factor of e
        out_arrows = VGroup()
        scale_labels = VGroup()
        for c1, c2 in zip(out_circles[2:], out_circles[3:]):
            arrows = VGroup(
                Arrow(c1.pfp(a), c2.pfp(a), buff=0.1 * c1.get_width(), thickness=3)
                for a in np.arange(0, 1, 1.0 / 8)
            )
            arrows.set_fill(YELLOW_E)
            arrows.set_backstroke(BLACK, 3)
            out_arrows.add(arrows)
            scale_label = Tex(R"\times e")
            scale_label.set_max_width(0.8 * arrows[0].get_width())
            scale_label.next_to(arrows[0], UP, SMALL_BUFF)
            scale_labels.add(scale_label)

        circle_ghosts.set_stroke(opacity=0.5)
        v_line_ghosts = v_lines.copy().set_stroke(opacity=0.5)

        self.add(circle_ghosts, v_line_ghosts)
        self.play(
            FadeOut(out_circles[:2]),
            FadeOut(out_circles[3:]),
            FadeOut(v_lines[:2]),
            FadeOut(v_lines[3:]),
            z_tracker.animate.set_value(0),
        )
        self.wait()
        for n in [0, 1]:
            self.play(
                LaggedStartMap(GrowArrow, out_arrows[n], lag_ratio=1e-2),
                FadeIn(scale_labels[n], shift=0.1 * RIGHT, scale=2),
                TransformFromCopy(out_circles[n + 2], out_circles[n + 3]),
                TransformFromCopy(v_lines[n + 2], v_lines[n + 3]),
                z_tracker.animate.set_value(n + 1),
                run_time=3
            )
            self.wait()

        # Clean up the board
        self.play(
            FadeOut(VGroup(out_arrows, scale_labels, brace, brace_label, top_arrows, top_labels), lag_ratio=0.02),
            FadeOut(Group(in_dot, out_dot, z_label), lag_ratio=0.1),
            FadeOut(v_line_ghosts),
            FadeOut(circle_ghosts),
            v_lines.animate.set_stroke(opacity=1),
            out_circles.animate.set_stroke(opacity=1),
        )

        # Show an example grid from where the v-lines have been drawn
        grid_density = 4
        grid_width = (len(v_lines) - 1) * grid_density
        in_grid = Square().get_grid(int(TAU * grid_density), grid_width, buff=0)
        in_grid.sort(lambda p: np.dot(p, (0.1, 1, 0)))
        in_grid.match_width(v_lines)
        in_grid.move_to(v_lines, DOWN)
        in_grid.set_stroke(width=1)
        in_grid.set_submobject_colors_by_gradient(BLUE, YELLOW, interp_by_hsl=True)
        in_grid_ghost = in_grid.copy()
        in_grid_ghost.set_stroke(width=1, opacity=0.5)

        out_grid = apply_exp_to_input_shape(in_grid.copy().insert_n_curves(10))

        self.play(
            Write(in_grid),
            out_circles.animate.set_stroke(WHITE, 1),
            v_lines.animate.set_stroke(WHITE, 1),
        )
        self.wait()
        self.remove(in_grid)
        self.add(in_grid_ghost)
        self.play(
            out_plane.background_lines.animate.set_stroke(opacity=0.25),
            *(
                ReplacementTransform(in_square.copy(), out_square, path_arc=0.35 * z.imag + 0.05 * (z.real + 2))
                for in_square, out_square in zip(in_grid, out_grid)
                for z in [in_plane.p2n(in_square.get_center())]
            ),
            run_time=3
        )
        self.wait()

        # Cycle through squares
        solid_in_grid = in_grid.copy()
        solid_in_grid.sort(lambda p: np.dot(p, (1, 0.01, 0)))
        for square in solid_in_grid:
            square.set_fill(square.get_stroke_color(), 0.5)
            square.set_stroke(width=2)
        solid_out_grid = apply_exp_to_input_shape(solid_in_grid.copy().insert_n_curves(10))

        self.play(
            ShowSubmobjectsOneByOne(solid_in_grid),
            ShowSubmobjectsOneByOne(solid_out_grid),
            run_time=10,
            rate_func=lambda a: (0.5 + 0.5 * a),
        )
        self.remove(solid_in_grid, solid_out_grid)
        self.wait()

        # Re-emphasize the lines
        v_lines.set_stroke(BLUE, 3)
        out_circles.set_stroke(YELLOW, 3)

        self.play(
            *(
                LaggedStartMap(ShowCreation, group, lag_ratio=0.5, run_time=3)
                for group in [v_lines, out_circles]
            ),
            in_grid_ghost.animate.set_stroke(opacity=0.25),
            out_grid.animate.set_stroke(opacity=0.25),
        )
        self.play(LaggedStart(
            (TransformFromCopy(line, circle, path_arc=(0, 0.25 * PI))
            for line, circle in zip(v_lines, out_circles)),
            lag_ratio=0.1,
            run_time=3
        ))
        self.wait()

        # Full grid
        full_grid = Square3D(resolution=(10, 10)).get_grid(4 * x_max, 4 * x_max, buff=0)
        full_grid.match_width(in_plane)
        full_grid.move_to(in_plane)
        full_grid.set_shading(0, 0, 0)
        for n, square in enumerate(full_grid):
            row = n // (4 * x_max)
            col = n % (4 * x_max)
            parity = (row + col) % 2
            square.set_color([GREY_C, GREY_E][parity], 1)
        full_grid.sort(lambda p: np.dot(p, (0.01, 1, 0)))

        full_v_lines = VGroup(
            Line(in_plane.c2p(x, -x_max), in_plane.c2p(x, x_max)).insert_n_curves(100)
            for x in range(-x_max, x_max + 1)
        )
        full_v_lines.set_stroke(RED, 3)
        full_v_lines.set_submobject_colors_by_gradient(YELLOW, RED)
        full_v_lines.apply_depth_test()

        self.play(
            *map(FadeOut, [in_grid_ghost, v_lines, out_grid, out_circles]),
            ShowCreation(full_v_lines, lag_ratio=0.25, run_time=5),
        )
        self.wait()
        self.play(FadeIn(full_grid, lag_ratio=1e-3, run_time=1))
        self.wait()

        # Roll up into a cylinder
        def cylinder_func(points, threshold=0):
            xs = in_plane.x_axis.p2n(points)
            ys = in_plane.y_axis.p2n(points)
            theta = threshold - ys
            scale_factor = np.exp(0.01 * ys)
            spiral_points = np.array([xs.T, threshold - scale_factor * np.sin(theta), 1 - scale_factor * np.cos(theta)]).T
            result = np.array([xs, ys, np.zeros_like(xs)]).T
            curved_indices = (ys < threshold)
            result[curved_indices] = spiral_points[curved_indices]
            return result

        threshold_tracker = ValueTracker(-x_max)

        def update_rolled_cylinder(rolled_cylinder):
            for sm1, sm2 in zip(rolled_cylinder, rolled_cylinder.saved_state):
                sm1.match_points(sm2)
                sm1.match_color(sm2)
            threshold = threshold_tracker.get_value()
            rolled_cylinder.apply_points_function(lambda ps: cylinder_func(ps, threshold))
            rolled_cylinder.match_width(full_grid)
            rolled_cylinder.shift(full_grid[-1].get_end() - rolled_cylinder[-1].get_end())
            return rolled_cylinder

        rolled_cylinder = full_grid.copy()
        rolled_cylinder.save_state()
        rolled_v_lines = full_v_lines.copy()
        rolled_v_lines.save_state()

        self.remove(full_grid, full_v_lines)
        self.add(rolled_cylinder)
        self.play(
            frame.animate.reorient(58, 70, 0, (-1.74, 2.71, 0.02), 6.40),
            UpdateFromFunc(rolled_cylinder, update_rolled_cylinder),
            UpdateFromFunc(rolled_v_lines, update_rolled_cylinder),
            threshold_tracker.animate.set_value(x_max).set_anim_args(time_span=(2, 7)),
            run_time=8,
        )
        self.wait()

        # Show circle circumference
        circle = Circle(radius=in_plane.x_axis.get_unit_size())
        circle.set_color(RED)
        circle.flip(RIGHT)
        circle.rotate(90 * DEG, UP)
        circle.move_to(rolled_cylinder, RIGHT)
        circle.set_stroke(WHITE, 5)

        circle_center = circle.get_center()
        circum_dec = DecimalNumber(0, font_size=24)
        circum_dec.save_state()
        circum_tracker = ValueTracker(0)

        def update_circum_dec(circum_dec):
            circum_dec.restore()
            if circum_tracker.get_value() >= TAU - 1e-5:
                circum_dec.become(Tex(R"2\pi", font_size=36))
            else:
                circum_dec.set_value(circum_tracker.get_value())
            circum_dec.rotate(90 * DEG, RIGHT).rotate(90 * DEG, OUT)
            circum_dec.move_to(circle_center + 1.5 * (circle.get_end() - circle_center))

        circum_dec.add_updater(update_circum_dec)

        self.add(circum_dec)
        self.play(
            ShowCreation(circle),
            circum_tracker.animate.set_value(TAU),
            run_time=3
        )
        circum_dec.update()
        circum_dec.clear_updaters()
        self.wait()
        self.play(FadeOut(circle), FadeOut(circum_dec))
        self.wait()

        # Squish the cylinder
        cylinder = Group(rolled_cylinder, rolled_v_lines)
        cylinder.apply_depth_test()

        cylinder.target = cylinder.generate_target()
        cylinder.target.rotate(90 * DEG, DOWN)
        cylinder.target.next_to(out_plane, OUT, buff=1)

        def squish(points):
            xs, ys, zs = points.T
            xs, ys = normalize_along_axis(np.array([xs, ys]).T, 1).T
            radius = np.exp(zs)
            return np.array([radius * xs, radius * ys, np.zeros_like(xs)]).T

        central_cylinder = cylinder.target.copy()
        central_cylinder.set_width(2)
        central_cylinder.center()

        for mob in [cylinder.target, central_cylinder]:
            sorted_pieces = list(mob.family_members_with_points())
            sorted_pieces.sort(key=lambda m: m.get_z())
            for piece in sorted_pieces[int(0.82 * len(sorted_pieces)):]:
                piece.fade(1)

        central_cylinder.apply_points_function(squish, about_point=ORIGIN)
        central_cylinder.scale(out_plane.x_axis.get_unit_size(), about_point=ORIGIN)
        central_cylinder.shift(out_plane.get_center())

        self.play(
            MoveToTarget(cylinder),
            frame.animate.reorient(-1, 72, 0, (3.42, 0.82, 1.64), 11.83),
            run_time=8
        )
        central_cylinder.deactivate_depth_test()
        cylinder.deactivate_depth_test()

        self.play(Transform(cylinder, central_cylinder, run_time=3))
        self.wait()

        # Show input and output space again
        cylinder.set_clip_plane(RIGHT, 20)
        out_plane.background_lines.set_stroke(BLUE, 1, 1)
        in_plane.background_lines.set_stroke(BLUE, 1, 1)
        full_grid.set_opacity(0.5)
        v_lines.deactivate_depth_test()

        self.add(full_grid, out_plane, in_plane, full_v_lines)
        self.play(
            frame.animate.to_default_state(),
            cylinder.animate.set_clip_plane(RIGHT, -1).set_anim_args(time_span=(0, 1.5)),
            FadeIn(out_plane),
            FadeIn(full_grid, time_span=(2, 3)),
            FadeIn(full_v_lines, time_span=(2, 3)),
            FadeIn(in_plane),
            run_time=3
        )
        self.wait()
        self.play(
            ShowCreation(full_v_lines, lag_ratio=0.1),
            ShowCreation(rolled_v_lines, lag_ratio=0.1),
            run_time=3
        )
        self.wait()

        # Clear the board
        self.play(
            FadeOut(Group(full_grid, full_v_lines, cylinder)),
            in_plane.background_lines.animate.set_stroke(BLUE, 1, 0.5),
            out_plane.background_lines.animate.set_stroke(BLUE, 1, 0.5),
        )
        self.wait()

        # Show three points colliding
        z_range = [-TAU * 1j, 0, TAU * 1j] + [
            unit * n * TAU * 1j
            for n in range(2, int(200 / TAU))
            for unit in [-1, 1]
        ]
        input_dots = VGroup(
            Dot(in_plane.n2p(z))
            for z in z_range
        )
        in_dot_labels = VGroup(Tex(R"-2\pi i"), Tex(R"0"), Tex(R"2 \pi i"))
        for dot, label, vect in zip(input_dots, in_dot_labels, [LEFT, 0.5 * UL, LEFT]):
            label.next_to(dot, vect, SMALL_BUFF)

        out_dot_one = Dot(out_plane.n2p(1))
        out_dot_label = Tex(R"1")
        out_dot_label.next_to(out_dot_one, UR, SMALL_BUFF)

        in_plane_label = Tex(R"z").next_to(in_plane, UP)
        out_plane_label = Tex(R"e^{z}").next_to(out_plane, UP)

        dot_arrows = VGroup(
            Arrow(input_dot, out_dot_one, thickness=4, fill_color=RED, fill_opacity=0.75)
            for input_dot in input_dots
        )
        dot_arrows.set_fill(opacity=0.75)

        self.play(
            LaggedStartMap(FadeIn, input_dots),
            LaggedStartMap(FadeIn, in_dot_labels),
            in_plane.coordinate_labels[14:].animate.set_opacity(0),
            ReplacementTransform(func_label, out_plane_label),
            TransformFromCopy(func_label[1], in_plane_label[0]),
            func_arrow.animate.match_y(out_plane_label),
        )
        self.wait()
        self.play(
            LaggedStartMap(GrowArrow, dot_arrows[:3], lag_ratio=0.25),
            LaggedStart(
                (TransformFromCopy(input_dot, out_dot_one)
                for input_dot in input_dots[:3]),
                lag_ratio=0.25,
            )
        )
        self.wait()

        # Flip arrows
        self.play(
            *(
                Transform(
                    arrow,
                    arrow.copy().rotate(PI),
                    rate_func=there_and_back_with_pause,
                    run_time=3,
                    path_arc=45 * DEG,
                )
                for arrow in [*dot_arrows[:3], func_arrow]
            )
        )
        self.wait()

        # Equations
        equations = VGroup(
            Tex(R"e^{-2\pi i} = 1"),
            Tex(R"e^{0} = 1"),
            Tex(R"e^{2\pi i} = 1"),
        )
        z_tracker.set_value(0)
        for equation, y in zip(equations, [-2, 0.35, 2]):
            equation.move_to(y * UP)

        self.play(
            FadeIn(equations[1]),
            FadeIn(in_dot),
            FadeIn(out_dot),
            dot_arrows[0].animate.set_opacity(0.1),
            dot_arrows[2].animate.set_opacity(0.1),
        )
        self.wait()
        self.play(
            z_tracker.animate.set_value(complex(0, TAU)),
            LaggedStart(
                FadeIn(equations[2], UP),
                FadeOut(equations[1], UP),
                lag_ratio=0.1,
            ),
            dot_arrows[1].animate.set_opacity(0.1),
            dot_arrows[2].animate.set_opacity(1),
            run_time=2
        )
        self.wait()
        self.play(
            z_tracker.animate.set_value(complex(0, -TAU)),
            LaggedStart(
                FadeIn(equations[0], DOWN),
                FadeOut(equations[2], DOWN),
                lag_ratio=0.1,
            ),
            dot_arrows[2].animate.set_opacity(0.1),
            dot_arrows[0].animate.set_opacity(1),
        )
        self.wait()

        # Show infinite sequence
        big_in_plane = ComplexPlane((-x_max, x_max), (-10, 200), faded_line_ratio=0)
        big_in_plane.axes.match_style(in_plane.axes)
        big_in_plane.background_lines.match_style(in_plane.background_lines)
        big_in_plane.replace(in_plane, dim_to_match=0)
        big_in_plane.x_axis.add_numbers(range(-x_max + 1, x_max), font_size=12, buff=0.05)

        new_in_dot_labels = VGroup(
            Tex(Rf"{n} \pi i").next_to(dot, LEFT)
            for dot, n in zip(input_dots[4::2], range(4, 30, 2))
        )

        dot_arrows[3:].set_opacity(0)

        corner_eq = Tex(R"e^{2\pi i n} = 1", font_size=60)
        corner_eq.fix_in_frame()
        corner_eq.to_corner(UR)

        self.play(
            dot_arrows.animate.set_opacity(0.5).set_anim_args(lag_ratio=0.01, run_time=3),
            FadeIn(new_in_dot_labels, lag_ratio=0.1, time_span=(1, 3)),
            FadeIn(corner_eq),
            FadeOut(equations[0]),
            FadeIn(big_in_plane),
            FadeOut(in_plane_label),
            FadeOut(func_arrow),
            FadeOut(in_plane, time_span=(0.5, 1)),
            frame.animate.reorient(6, 62, 0, (-0.01, -0.01, -0.01), 8.00).set_anim_args(run_time=3)
        )
        self.wait()
        for _ in range(10):
            self.play(
                z_tracker.animate.increment_value(TAU * 1j),
                dot_arrows.animate.set_opacity(0.2),
                run_time=2,
            )
        self.play(FadeOut(corner_eq))

        # Flip the arrows
        exp_arrow = Arrow(in_plane, out_plane, thickness=6)
        exp_label = Tex(R"e^{z}", font_size=72, t2c={"z": BLUE})
        log_label = Tex(R"\ln(w)", font_size=72, t2c={"w": PINK})
        exp_label.next_to(exp_arrow, UP, SMALL_BUFF)
        log_label.next_to(exp_arrow, DOWN, SMALL_BUFF)

        self.add(exp_arrow)
        self.add(exp_label)

        z_tracker.set_value(-4 * TAU * 1j)
        z_tracker.clear_updaters()
        z_tracker.add_updater(lambda m, dt: m.increment_value(complex(0, PI * dt)))
        self.add(z_tracker)

        frame.reorient(5, 60, 0, (-0.38, -0.12, -0.11), 8.22)
        self.wait(5)
        self.play(
            Rotate(exp_arrow, PI, time_span=(1, 2)),
            ReplacementTransform(exp_label, log_label, path_arc=PI, time_span=(1, 2)),
            LaggedStart(
                (arrow.animate.rotate(PI).set_opacity(0.4).set_anim_args(path_arc=30 * DEG)
                for arrow in dot_arrows),
                lag_ratio=(1.0 / len(dot_arrows)),
            ),
            frame.animate.reorient(0, 51, 0, (-0.01, -0.01, -0.01)),
            run_time=3
        )
        self.play(
            # CHANGE: typo in the original ("reorient.reorient"); .animate.reorient(...) is the correct call.
            frame.animate.reorient(0, 62, 0, (-0.01, -0.01, -0.01), 8.22),
            run_time=12
        )
        self.wait(12)
