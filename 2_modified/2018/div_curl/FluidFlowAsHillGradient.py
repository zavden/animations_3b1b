# ==============================================================================
# Scene:      FluidFlowAsHillGradient
# Source:     videos/_2018/div_curl.py (lines 1385-1429)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FluidFlowAsHillGradient.py FluidFlowAsHillGradient -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - cubic 4-point set_points([LEFT, LEFT, RIGHT, RIGHT]) is invalid for GL quadratic curves; a straight line subdivided into 50 curves stays warpable
# ==============================================================================

from manim_imports_ext import *

# Helper functions
def joukowsky_map(z):
    if z == 0:
        return 0
    return z + fdiv(1, z)


def inverse_joukowsky_map(w):
    u = 1 if w.real >= 0 else -1
    return (w + u * np.sqrt(w**2 - 4)) / 2


def derivative(func, dt=1e-7):
    return lambda z: (func(z + dt) - func(z)) / dt


def negative_gradient(potential_func, dt=1e-7):
    def result(p):
        output = potential_func(p)
        dx = dt * RIGHT
        dy = dt * UP
        dz = dt * OUT
        return -np.array([
            (potential_func(p + dx) - output) / dt,
            (potential_func(p + dy) - output) / dt,
            (potential_func(p + dz) - output) / dt,
        ])
    return result


def cylinder_flow_vector_field(point, R=1, U=1):
    z = R3_to_complex(point)
    # return complex_to_R3(1.0 / derivative(joukowsky_map)(z))
    return complex_to_R3(derivative(joukowsky_map)(z).conjugate())


class CylinderModel(Scene):
    CONFIG = {
        "production_quality_flow": True,
        "vector_field_func": cylinder_flow_vector_field,
    }

    def construct(self):
        self.add_plane()
        self.add_title()
        self.show_numbers()
        self.show_contour_lines()
        self.show_flow()
        self.apply_joukowsky_map()

    def add_plane(self):
        self.plane = ComplexPlane()
        self.plane.add_coordinates()
        self.plane.coordinate_labels.submobjects.pop(-1)
        self.add(self.plane)

    def add_title(self):
        title = OldTexText("Complex Plane")
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.add_background_rectangle()
        self.title = title
        self.add(title)

    def show_numbers(self):
        run_time = 5

        unit_circle = self.unit_circle = Circle(
            radius=self.plane.unit_size,
            fill_color=BLACK,
            fill_opacity=0,
            stroke_color=YELLOW
        )
        dot = Dot()
        dot_update = UpdateFromFunc(
            dot, lambda d: d.move_to(unit_circle.point_from_proportion(1))
        )
        exp_tex = OldTex("e^{", "0.00", "i}")
        zero = exp_tex.get_part_by_tex("0.00")
        zero.fade(1)
        exp_tex_update = UpdateFromFunc(
            exp_tex, lambda et: et.next_to(dot, UR, SMALL_BUFF)
        )
        exp_decimal = DecimalNumber(
            0, num_decimal_places=2,
            include_background_rectangle=True,
            color=YELLOW
        )
        exp_decimal.replace(zero)
        exp_decimal_update = ChangeDecimalToValue(
            exp_decimal, TAU,
            position_update_func=lambda mob: mob.move_to(zero),
            run_time=run_time,
        )

        sample_numbers = [
            complex(-5, 2),
            complex(2, 2),
            complex(3, 1),
            complex(-5, -2),
            complex(-4, 1),
        ]
        sample_labels = VGroup()
        for z in sample_numbers:
            sample_dot = Dot(self.plane.number_to_point(z))
            sample_label = DecimalNumber(
                z,
                num_decimal_places=0,
                include_background_rectangle=True,
            )
            sample_label.next_to(sample_dot, UR, SMALL_BUFF)
            sample_labels.add(VGroup(sample_dot, sample_label))

        self.play(
            ShowCreation(unit_circle, run_time=run_time),
            VFadeIn(exp_tex),
            UpdateFromAlphaFunc(
                exp_decimal,
                lambda ed, a: ed.set_fill(opacity=a)
            ),
            dot_update,
            exp_tex_update,
            exp_decimal_update,
            LaggedStartMap(
                FadeIn, sample_labels,
                remover=True,
                rate_func=there_and_back,
                run_time=run_time,
            )
        )
        self.play(
            FadeOut(exp_tex),
            FadeOut(exp_decimal),
            FadeOut(dot),
            unit_circle.set_fill, BLACK, {"opacity": 1},
        )
        self.wait()

    def show_contour_lines(self):
        warped_grid = self.warped_grid = self.get_warpable_grid()
        h_line = Line(3 * LEFT, 3 * RIGHT, color=WHITE)  # Hack
        func_label = self.get_func_label()

        self.remove(self.plane)
        self.add_foreground_mobjects(self.unit_circle, self.title)
        self.play(
            warped_grid.apply_complex_function, inverse_joukowsky_map,
            Animation(h_line, remover=True)
        )
        self.play(Write(func_label))
        self.add_foreground_mobjects(func_label)
        self.wait()

    def show_flow(self):
        stream_lines = self.get_stream_lines()
        stream_lines_copy = stream_lines.copy()
        stream_lines_copy.set_stroke(YELLOW, 1)
        stream_lines_animation = self.get_stream_lines_animation(
            stream_lines
        )

        tiny_buff = 0.0001
        v_lines = VGroup(*[
            Line(
                UP, ORIGIN,
                path_arc=0,
                n_arc_anchors=20,
            ).shift(x * RIGHT)
            for x in np.linspace(0, 1, 5)
        ])
        v_lines.match_background_image_file(stream_lines)
        fast_lines, slow_lines = [
            VGroup(*[
                v_lines.copy().next_to(point, vect, tiny_buff)
                for point, vect in it.product(h_points, [UP, DOWN])
            ])
            for h_points in [
                [0.5 * LEFT, 0.5 * RIGHT],
                [2 * LEFT, 2 * RIGHT],
            ]
        ]
        for lines in fast_lines, slow_lines:
            lines.apply_complex_function(inverse_joukowsky_map)

        self.add(stream_lines_animation)
        self.wait(7)
        self.play(
            ShowCreationThenDestruction(
                stream_lines_copy,
                lag_ratio=0,
                run_time=3,
            )
        )
        self.wait()
        self.play(ShowCreation(fast_lines))
        self.wait(2)
        self.play(ReplacementTransform(fast_lines, slow_lines))
        self.wait(3)
        self.play(
            FadeOut(slow_lines),
            VFadeOut(stream_lines_animation.mobject)
        )
        self.remove(stream_lines_animation)

    def apply_joukowsky_map(self):
        shift_val = 0.1 * LEFT + 0.2 * UP
        scale_factor = get_norm(RIGHT - shift_val)
        movers = VGroup(self.warped_grid, self.unit_circle)
        self.unit_circle.insert_n_curves(50)

        stream_lines = self.get_stream_lines()
        stream_lines.scale(scale_factor)
        stream_lines.shift(shift_val)
        stream_lines.apply_complex_function(joukowsky_map)

        self.play(
            movers.scale, scale_factor,
            movers.shift, shift_val,
        )
        self.wait()
        self.play(
            movers.apply_complex_function, joukowsky_map,
            ShowCreationThenFadeAround(self.func_label),
            run_time=2
        )
        self.add(self.get_stream_lines_animation(stream_lines))
        self.wait(20)

    # Helpers

    def get_func_label(self):
        func_label = self.func_label = OldTex("f(z) = z + 1 / z")
        func_label.add_background_rectangle()
        func_label.next_to(self.title, DOWN, MED_SMALL_BUFF)
        return func_label

    def get_warpable_grid(self):
        top_grid = NumberPlane()
        top_grid.prepare_for_nonlinear_transform()
        bottom_grid = top_grid.copy()
        tiny_buff = 0.0001
        top_grid.next_to(ORIGIN, UP, buff=tiny_buff)
        bottom_grid.next_to(ORIGIN, DOWN, buff=tiny_buff)
        result = VGroup(top_grid, bottom_grid)
        result.add(*[
            Line(
                ORIGIN, FRAME_WIDTH * RIGHT / 2,
                color=WHITE,
                path_arc=0,
                n_arc_anchors=100,
            ).next_to(ORIGIN, vect, buff=2)
            for vect in (LEFT, RIGHT)
        ])
        # This line is a bit of a hack
        h_line = Line(LEFT, RIGHT, color=WHITE)
        # CHANGE: cubic 4-point set_points([LEFT, LEFT, RIGHT, RIGHT]) is invalid for GL quadratic curves; a straight line subdivided into 50 curves stays warpable
        h_line.insert_n_curves(50)
        h_line.scale(2)
        result.add(h_line)
        return result

    def get_stream_lines(self):
        func = self.vector_field_func
        if self.production_quality_flow:
            delta_x = 0.5
            delta_y = 0.1
        else:
            delta_x = 1
            # delta_y = 1
            delta_y = 0.1
        return StreamLines(
            func,
            start_points_generator_config={
                "x_min": -8,
                "x_max": -7,
                "y_min": -4,
                "y_max": 4,
                "delta_x": delta_x,
                "delta_y": delta_y,
                "n_repeats": 1,
                "noise_factor": 0.1,
            },
            stroke_width=2,
            virtual_time=15,
        )

    def get_stream_lines_animation(self, stream_lines):
        if self.production_quality_flow:
            line_anim_class = ShowPassingFlashWithThinningStrokeWidth
        else:
            line_anim_class = ShowPassingFlash
        return AnimatedStreamLines(
            stream_lines,
            line_anim_class=line_anim_class,
        )


# TODO: Revisit this
class FluidFlowAsHillGradient(CylinderModel, ThreeDScene):
    CONFIG = {
        "production_quality_flow": False,
    }

    def construct(self):
        def potential(point):
            x, y = point[:2]
            result = 2 - 0.01 * op.mul(
                ((x - 4)**2 + y**2),
                ((x + 4)**2 + y**2)
            )
            return max(-10, result)

        vector_field_func = negative_gradient(potential)

        stream_lines = StreamLines(
            vector_field_func,
            virtual_time=3,
            color_lines_by_magnitude=False,
            start_points_generator_config={
                "delta_x": 0.2,
                "delta_y": 0.2,
            }
        )
        for line in stream_lines:
            line.get_points()[:, 2] = np.apply_along_axis(
                potential, 1, line.get_points()
            )
        stream_lines_animation = self.get_stream_lines_animation(
            stream_lines
        )

        plane = NumberPlane()

        self.add(plane)
        self.add(stream_lines_animation)
        self.wait(3)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.move_camera(
            phi=70 * DEGREES,
            run_time=2
        )
        self.wait(5)
