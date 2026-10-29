# ==============================================================================
# Scene:      ElectricField
# Source:     videos/_2018/div_curl.py (lines 679-864)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ElectricField.py ElectricField -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - cubic 4-point set_points([LEFT, LEFT, RIGHT, RIGHT]) is invalid for GL quadratic curves; a straight line subdivided into 50 curves stays warpable
#   - original bug: set_value received the function instead of its value (formatting a function fails in any manim version)
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


def cylinder_flow_vector_field(point, R=1, U=1):
    z = R3_to_complex(point)
    # return complex_to_R3(1.0 / derivative(joukowsky_map)(z))
    return complex_to_R3(derivative(joukowsky_map)(z).conjugate())


def get_charged_particles(color, sign, radius=0.1):
    result = Circle(
        stroke_color=WHITE,
        stroke_width=0.5,
        fill_color=color,
        fill_opacity=0.8,
        radius=radius
    )
    sign = OldTex(sign)
    sign.set_stroke(WHITE, 1)
    sign.set_width(0.5 * result.get_width())
    sign.move_to(result)
    result.add(sign)
    return result


def get_proton(radius=0.1):
    return get_charged_particles(RED, "+", radius)


def get_electron(radius=0.05):
    return get_charged_particles(BLUE, "-", radius)


# TODO, this is untested after turning it from a
# ContinualAnimation into a VGroup
class JigglingSubmobjects(VGroup):
    CONFIG = {
        "amplitude": 0.05,
        "jiggles_per_second": 1,
    }

    def __init__(self, group, **kwargs):
        VGroup.__init__(self, **kwargs)
        for submob in group.submobjects:
            submob.jiggling_direction = rotate_vector(
                RIGHT, np.random.random() * TAU,
            )
            submob.jiggling_phase = np.random.random() * TAU
            self.add(submob)
        self.add_updater(lambda m, dt: m.update(dt))

    def update(self, dt):
        for submob in self.submobjects:
            submob.jiggling_phase += dt * self.jiggles_per_second * TAU
            submob.shift(
                self.amplitude *
                submob.jiggling_direction *
                np.sin(submob.jiggling_phase) * dt
            )


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


class ElectricField(CylinderModel, MovingCameraScene):
    def construct(self):
        self.add_plane()
        self.add_title()
        self.setup_warped_grid()
        self.show_uniform_field()
        self.show_moving_charges()
        self.show_field_lines()

    def setup_warped_grid(self):
        warped_grid = self.warped_grid = self.get_warpable_grid()
        warped_grid.save_state()
        func_label = self.get_func_label()
        unit_circle = self.unit_circle = Circle(
            radius=self.plane.unit_size,
            stroke_color=YELLOW,
            fill_color=BLACK,
            fill_opacity=1
        )

        self.add_foreground_mobjects(self.title, func_label, unit_circle)
        self.remove(self.plane)
        self.play(
            warped_grid.apply_complex_function, inverse_joukowsky_map,
        )
        self.wait()

    def show_uniform_field(self):
        vector_field = self.vector_field = VectorField(
            lambda p: UP,
            colors=[BLUE_E, WHITE, RED]
        )
        protons, electrons = groups = [
            VGroup(*[method(radius=0.2) for x in range(20)])
            for method in (get_proton, get_electron)
        ]
        for group in groups:
            group.arrange(RIGHT, buff=MED_SMALL_BUFF)
            random.shuffle(group.submobjects)
        protons.next_to(FRAME_HEIGHT * DOWN / 2, DOWN)
        electrons.next_to(FRAME_HEIGHT * UP / 2, UP)

        self.play(
            self.warped_grid.restore,
            FadeOut(self.unit_circle),
            FadeOut(self.title),
            FadeOut(self.func_label),
            LaggedStartMap(GrowArrow, vector_field)
        )
        self.remove_foreground_mobjects(self.title, self.func_label)
        self.wait()
        for group, vect in (protons, UP), (electrons, DOWN):
            self.play(LaggedStartMap(
                ApplyMethod, group,
                lambda m: (m.shift, (FRAME_HEIGHT + 1) * vect),
                run_time=3,
                rate_func=rush_into
            ))

    def show_moving_charges(self):
        unit_circle = self.unit_circle

        protons = VGroup(*[
            get_proton().move_to(
                rotate_vector(0.275 * n * RIGHT, angle)
            )
            for n in range(4)
            for angle in np.arange(
                0, TAU, TAU / (6 * n) if n > 0 else TAU
            )
        ])
        jiggling_protons = JigglingSubmobjects(protons)
        electrons = VGroup(*[
            get_electron().move_to(
                proton.get_center() +
                proton.radius * rotate_vector(RIGHT, angle)
            )
            for proton in protons
            for angle in [np.random.random() * TAU]
        ])
        jiggling_electrons = JigglingSubmobjects(electrons)
        electrons.generate_target()
        for electron in electrons.target:
            y_part = electron.get_center()[1]
            if y_part > 0:
                electron.shift(2 * y_part * DOWN)

        # New vector field
        def new_electric_field(point):
            if get_norm(point) < 1:
                return ORIGIN
            vect = cylinder_flow_vector_field(point)
            return rotate_vector(vect, 90 * DEGREES)
        new_vector_field = VectorField(
            new_electric_field,
            colors=self.vector_field.colors
        )

        warped_grid = self.warped_grid

        self.play(GrowFromCenter(unit_circle))
        self.add(jiggling_protons, jiggling_electrons)
        self.add_foreground_mobjects(
            self.vector_field, unit_circle, protons, electrons
        )
        self.play(
            LaggedStartMap(VFadeIn, protons),
            LaggedStartMap(VFadeIn, electrons),
        )
        self.play(
            self.camera.frame.scale, 0.7,
            run_time=3
        )
        self.play(
            MoveToTarget(electrons),  # More indication?
            warped_grid.apply_complex_function, inverse_joukowsky_map,
            Transform(
                self.vector_field,
                new_vector_field
            ),
            run_time=3
        )
        self.wait(5)

    def show_field_lines(self):
        h_lines = VGroup(*[
            Line(
                5 * LEFT, 5 * RIGHT,
                path_arc=0,
                n_arc_anchors=50,
                stroke_color=GREY_B,
                stroke_width=2,
            ).shift(y * UP)
            for y in np.arange(-3, 3.25, 0.25)
            if y != 0
        ])
        h_lines.apply_complex_function(inverse_joukowsky_map)
        for h_line in h_lines:
            h_line.save_state()

        voltage = DecimalNumber(
            10, num_decimal_places=1,
            unit="\\, V",
            color=YELLOW,
            include_background_rectangle=True,
        )
        vp_prop = 0.1
        voltage_point = VectorizedPoint(
            h_lines[4].point_from_proportion(vp_prop)
        )

        def get_voltage(dummy_arg):
            y = voltage_point.get_center()[1]
            return 10 - y

        voltage_update = voltage.add_updater(
            # CHANGE: original bug: set_value received the function instead of its value (formatting a function fails in any manim version)
            lambda d: d.set_value(get_voltage(None)),
        )
        voltage.add_updater(
            lambda d: d.next_to(
                voltage_point, UP, SMALL_BUFF
            )
        )

        self.play(ShowCreation(
            h_lines,
            run_time=2,
            lag_ratio=0
        ))
        self.add(voltage_update)
        self.add_foreground_mobjects(voltage)
        self.play(
            UpdateFromAlphaFunc(
                voltage, lambda m, a: m.set_fill(opacity=a)
            ),
            h_lines[4].set_stroke, YELLOW, 4,
        )
        for hl1, hl2 in zip(h_lines[4:], h_lines[5:]):
            self.play(
                voltage_point.move_to,
                hl2.point_from_proportion(vp_prop),
                hl1.restore,
                hl2.set_stroke, YELLOW, 3,
                run_time=0.5
            )
            self.wait(0.5)
