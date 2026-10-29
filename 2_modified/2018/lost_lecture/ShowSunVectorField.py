# ==============================================================================
# Scene:      ShowSunVectorField
# Source:     videos/_2018/lost_lecture.py (lines 4139-4160)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/div_curl.py
#
# Run from this folder:
#     manimgl ShowSunVectorField.py ShowSunVectorField -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject has no pixel_array in ManimGL; scaling the RGBA pixels by a is the same as set_opacity(a)
#   - SunAnimation was turned from a ContinualAnimation into a Group (see the TODO in the source): it has no .mobject, the group itself is the foreground mobject
#   - curr_v_perp is already a scalar norm; GL's norm() cannot take a scalar
#   - Transform(...).update(1) built a new animation (and copies) every frame; frame time and memory grew without bound (SIGKILL at 5 GB). become() gives the same final state
#   - GL's Scene.add/remove ungroup a group when one of its family members is added on its own: the comet is inside the Orbiting group, so adding the comet as foreground destroyed the group (its update never ran, the orbit froze and the wait-until-proportion loop never ended); use the whole orbit group as the foreground mobject
# ==============================================================================

from manim_imports_ext import *


# ----- From _2018/div_curl.py -----

def get_force_field_func(*point_strength_pairs, **kwargs):
    radius = kwargs.get("radius", 0.5)

    def func(point):
        result = np.array(ORIGIN)
        for center, strength in point_strength_pairs:
            to_center = center - point
            norm = get_norm(to_center)
            if norm == 0:
                continue
            elif norm < radius:
                to_center /= radius**3
            elif norm >= radius:
                to_center /= norm**3
            to_center *= -strength
            result += to_center
        return result
    return func



# ----- From _2018/lost_lecture.py -----

# TODO, this is untested after turning it from a
# ContinualAnimation into a VGroup
class Orbiting(VGroup):
    CONFIG = {
        "rate": 7.5,
    }

    def __init__(self, planet, star, ellipse, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.add(planet)
        self.planet = planet
        self.star = star
        self.ellipse = ellipse
        # Proportion of the way around the ellipse
        self.proportion = 0
        planet.move_to(ellipse.point_from_proportion(0))

        self.add_updater(lambda m, dt: m.update(dt))

    def update(self, dt):
        # time = self.internal_time

        planet = self.planet
        star = self.star
        ellipse = self.ellipse

        rate = self.rate
        radius_vector = planet.get_center() - star.get_center()
        rate *= 1.0 / get_norm(radius_vector)

        prop = self.proportion
        d_prop = 0.001
        ds = get_norm(op.add(
            ellipse.point_from_proportion((prop + d_prop) % 1),
            -ellipse.point_from_proportion(prop),
        ))

        delta_prop = (d_prop / ds) * rate * dt

        self.proportion = (self.proportion + delta_prop) % 1
        planet.move_to(
            ellipse.point_from_proportion(self.proportion)
        )


# TODO, this is untested after turning it from a
# ContinualAnimation into a Group
class SunAnimation(Group):
    CONFIG = {
        "rate": 0.2,
        "angle": 60 * DEGREES,
    }

    def __init__(self, sun, **kwargs):
        Group.__init__(self, **kwargs)
        self.sun = sun
        self.rotated_sun = sun.deepcopy()
        self.rotated_sun.rotate(60 * DEGREES)
        self.time = 0

        self.add(self.sun, self.rotated_sun)
        self.add_updater(lambda m, dt: m.update(dt))

    def update(self, dt):
        time = self.time
        self.time += dt
        a = (np.sin(self.rate * time * TAU) + 1) / 2.0
        self.rotated_sun.rotate(-self.angle)
        self.rotated_sun.move_to(self.sun)
        self.rotated_sun.rotate(self.angle)
        # CHANGE: ImageMobject has no pixel_array in ManimGL; scaling the RGBA pixels by a is the same as set_opacity(a)
        self.rotated_sun.set_opacity(a)


class TheMotionOfPlanets(Scene):
    CONFIG = {
        "camera_config": {"background_opacity": 1},
        "random_seed": 2,
    }

    def construct(self):
        self.add_title()
        self.setup_orbits()

    def add_title(self):
        title = OldTexText("``The motion of planets around the sun''")
        title.set_color(YELLOW)
        title.to_edge(UP)
        title.add_to_back(title.copy().set_stroke(BLACK, 5))
        self.add(title)
        self.title = title

    def setup_orbits(self):
        sun = ImageMobject("sun")
        sun.set_height(0.7)
        planets, ellipses, orbits = self.get_planets_ellipses_and_orbits(sun)

        archivist_words = OldTexText(
            "Judith Goodstein (Caltech archivist)"
        )
        archivist_words.to_corner(UL)
        archivist_words.shift(1.5 * DOWN)
        archivist_words.add_background_rectangle()
        alt_name = OldTexText("David Goodstein (Caltech physicist)")
        alt_name.next_to(archivist_words, DOWN, aligned_edge=LEFT)
        alt_name.add_background_rectangle()

        book = ImageMobject("Lost_Lecture_cover")
        book.set_height(4)
        book.next_to(alt_name, DOWN)

        self.add(SunAnimation(sun))
        self.add(ellipses, planets)
        self.add(self.title)
        self.add(*orbits)
        self.add_foreground_mobjects(planets)
        self.wait(10)
        self.play(
            VGroup(ellipses, sun).shift, 3 * RIGHT,
            FadeInFromDown(archivist_words),
            Animation(self.title)
        )
        self.add_foreground_mobjects(archivist_words)
        self.wait(3)
        self.play(FadeInFromDown(alt_name))
        self.add_foreground_mobjects(alt_name)
        self.wait()
        self.play(FadeInFromDown(book))
        self.wait(15)

    def get_planets_ellipses_and_orbits(self, sun):
        planets = VGroup(
            ImageMobject("mercury"),
            ImageMobject("venus"),
            ImageMobject("earth"),
            ImageMobject("mars"),
            ImageMobject("comet")
        )
        sizes = [0.383, 0.95, 1.0, 0.532, 0.3]
        orbit_radii = [0.254, 0.475, 0.656, 1.0, 3.0]
        orbit_eccentricies = [0.206, 0.006, 0.0167, 0.0934, 0.967]

        for planet, size in zip(planets, sizes):
            planet.set_height(0.5)
            planet.scale(size)

        ellipses = VGroup(*[
            Circle(radius=r, color=WHITE, stroke_width=1)
            for r in orbit_radii
        ])
        for circle, ec in zip(ellipses, orbit_eccentricies):
            a = circle.get_height() / 2
            c = ec * a
            b = np.sqrt(a**2 - c**2)
            circle.stretch(b / a, 1)
            c = np.sqrt(a**2 - b**2)
            circle.shift(c * RIGHT)
        for circle in ellipses:
            circle.rotate(
                TAU * np.random.random(),
                about_point=ORIGIN
            )

        ellipses.scale(3.5, about_point=ORIGIN)

        orbits = [
            Orbiting(
                planet, sun, circle,
                rate=0.25 * r**(2 / 3)
            )
            for planet, circle, r in zip(planets, ellipses, orbit_radii)
        ]
        orbits[-1].proportion = 0.15
        orbits[-1].rate = 0.5

        return planets, ellipses, orbits


class AskAboutEllipses(TheMotionOfPlanets):
    CONFIG = {
        "camera_config": {"background_opacity": 1},
        "sun_height": 0.5,
        "sun_center": ORIGIN,
        "animate_sun": True,
        "a": 3.5,
        "b": 2.0,
        "ellipse_color": WHITE,
        "ellipse_stroke_width": 1,
        "comet_height": 0.2,
    }

    def construct(self):
        self.add_title()
        self.add_sun()
        self.add_orbit()
        self.add_focus_lines()
        self.add_force_labels()
        self.comment_on_imperfections()
        self.set_up_differential_equations()

    def add_title(self):
        title = Title("Why are orbits ellipses?")
        self.add(title)
        self.title = title

    def add_sun(self):
        sun = ImageMobject("sun", height=self.sun_height)
        sun.move_to(self.sun_center)
        self.sun = sun
        self.add(sun)
        if self.animate_sun:
            sun_animation = SunAnimation(sun)
            self.add(sun_animation)
            # CHANGE: SunAnimation was turned from a ContinualAnimation into a Group (see the TODO in the source): it has no .mobject, the group itself is the foreground mobject
            self.add_foreground_mobjects(sun_animation)
        else:
            self.add_foreground_mobjects(sun)

    def add_orbit(self):
        sun = self.sun
        comet = self.get_comet()
        ellipse = self.get_ellipse()
        orbit = Orbiting(comet, sun, ellipse)

        self.add(ellipse)
        self.add(orbit)

        self.ellipse = ellipse
        self.comet = comet
        self.orbit = orbit

    def add_focus_lines(self):
        f1, f2 = self.focus_points
        comet = self.comet
        lines = VGroup(Line(LEFT, RIGHT), Line(LEFT, RIGHT))
        lines.set_stroke(GREY_B, 1)

        def update_lines(lines):
            l1, l2 = lines
            P = comet.get_center()
            l1.put_start_and_end_on(f1, P)
            l2.put_start_and_end_on(f2, P)
            return lines

        animation = Mobject.add_updater(
            lines, update_lines
        )
        self.add(animation)
        self.wait(8)

        self.focus_lines = lines
        self.focus_lines_animation = animation

    def add_force_labels(self):
        radial_line = self.focus_lines[0]

        # Radial line measurement
        radius_measurement_kwargs = {
            "num_decimal_places": 3,
            "color": BLUE,
        }
        radius_measurement = DecimalNumber(1, **radius_measurement_kwargs)

        def update_radial_measurement(measurement):
            angle = -radial_line.get_angle() + np.pi
            radial_line.rotate(angle, about_point=ORIGIN)
            new_decimal = DecimalNumber(
                radial_line.get_length(),
                **radius_measurement_kwargs
            )
            max_width = 0.6 * radial_line.get_width()
            if new_decimal.get_width() > max_width:
                new_decimal.set_width(max_width)
            new_decimal.next_to(radial_line, UP, SMALL_BUFF)
            VGroup(new_decimal, radial_line).rotate(
                -angle, about_point=ORIGIN
            )
            # CHANGE: Transform(...).update(1) built a new animation (and copies) every frame; frame time and memory grew without bound (SIGKILL at 5 GB). become() gives the same final state
            measurement.become(new_decimal)

        radius_measurement_animation = Mobject.add_updater(
            radius_measurement, update_radial_measurement
        )

        # Force equation
        force_equation = OldTex(
            "F = {GMm \\over (0.000)^2}",
            tex_to_color_map={
                "F": YELLOW,
                "0.000": BLACK,
            }
        )
        force_equation.next_to(self.title, DOWN)
        force_equation.to_edge(RIGHT)
        radius_in_denominator_ref = force_equation.get_part_by_tex("0.000")
        radius_in_denominator = DecimalNumber(
            0, **radius_measurement_kwargs
        )
        radius_in_denominator.scale(0.95)
        update_radius_in_denominator = ContinualChangingDecimal(
            radius_in_denominator,
            lambda a: radial_line.get_length(),
            position_update_func=lambda mob: mob.move_to(
                radius_in_denominator_ref, LEFT
            )
        )

        # Force arrow
        force_arrow, force_arrow_animation = self.get_force_arrow_and_update(
            self.comet
        )

        inverse_square_law_words = OldTexText(
            "``Inverse square law''"
        )
        inverse_square_law_words.next_to(force_equation, DOWN, MED_LARGE_BUFF)
        inverse_square_law_words.to_edge(RIGHT)
        force_equation.next_to(inverse_square_law_words, UP, MED_LARGE_BUFF)

        def v_fade_in(mobject):
            return UpdateFromAlphaFunc(
                mobject,
                lambda mob, alpha: mob.set_fill(opacity=alpha)
            )

        self.add(update_radius_in_denominator)
        self.add(radius_measurement_animation)
        self.play(
            FadeIn(force_equation),
            v_fade_in(radius_in_denominator),
            v_fade_in(radius_measurement)
        )
        self.add(force_arrow_animation)
        self.play(v_fade_in(force_arrow))
        self.wait(8)
        self.play(Write(inverse_square_law_words))
        self.wait(9)

        self.force_equation = force_equation
        self.inverse_square_law_words = inverse_square_law_words
        self.force_arrow = force_arrow
        self.radius_measurement = radius_measurement

    def comment_on_imperfections(self):
        planets, ellipses, orbits = self.get_planets_ellipses_and_orbits(self.sun)
        orbits.pop(-1)
        ellipses.submobjects.pop(-1)
        planets.submobjects.pop(-1)

        scale_factor = 20
        center = self.sun.get_center()
        ellipses.save_state()
        ellipses.scale(scale_factor, about_point=center)

        self.add(*orbits)
        self.play(ellipses.restore, Animation(planets))
        self.wait(7)
        self.play(
            ellipses.scale, scale_factor, {"about_point": center},
            Animation(planets)
        )
        self.remove(*orbits)
        self.remove(planets, ellipses)
        self.wait(2)

    def set_up_differential_equations(self):
        d_dt = OldTex("{d \\over dt}")
        in_vect = Matrix(np.array([
            "x(t)",
            "y(t)",
            "\\dot{x}(t)",
            "\\dot{y}(t)",
        ]))
        equals = OldTex("=")
        out_vect = Matrix(np.array([
            "\\dot{x}(t)",
            "\\dot{y}(t)",
            "-x(t) / (x(t)^2 + y(t)^2)^{3/2}",
            "-y(t) / (x(t)^2 + y(t)^2)^{3/2}",
        ]), element_alignment_corner=ORIGIN)

        equation = VGroup(d_dt, in_vect, equals, out_vect)
        equation.arrange(RIGHT, buff=SMALL_BUFF)
        equation.set_width(6)

        equation.to_corner(DR, buff=MED_LARGE_BUFF)
        cross = Cross(equation)

        self.play(Write(equation))
        self.wait(6)
        self.play(ShowCreation(cross))
        self.wait(6)

    # Helpers
    def get_comet(self):
        comet = ImageMobject("comet")
        comet.set_height(self.comet_height)
        return comet

    def get_ellipse(self):
        a = self.a
        b = self.b
        c = np.sqrt(a**2 - b**2)
        ellipse = Circle(radius=a)
        ellipse.set_stroke(
            self.ellipse_color,
            self.ellipse_stroke_width,
        )
        ellipse.stretch(fdiv(b, a), dim=1)
        ellipse.move_to(
            self.sun.get_center() + c * LEFT,
        )
        self.focus_points = [
            self.sun.get_center(),
            self.sun.get_center() + 2 * c * LEFT,
        ]
        return ellipse

    def get_force_arrow_and_update(self, comet, scale_factor=1):
        force_arrow = Arrow(LEFT, RIGHT, color=YELLOW)
        sun = self.sun

        def update_force_arrow(arrow):
            radial_line = Line(
                sun.get_center(), comet.get_center()
            )
            radius = radial_line.get_length()
            # target_length = 1 / radius**2
            target_length = scale_factor / radius  # Lies!
            arrow.scale(
                target_length / arrow.get_length()
            )
            arrow.rotate(
                np.pi + radial_line.get_angle() - arrow.get_angle()
            )
            arrow.shift(
                radial_line.get_end() - arrow.get_start()
            )
        force_arrow_animation = Mobject.add_updater(
            force_arrow, update_force_arrow
        )

        return force_arrow, force_arrow_animation

    def get_radial_line_and_update(self, comet):
        line = Line(LEFT, RIGHT)
        line.set_stroke(GREY_B, 1)
        line_update = Mobject.add_updater(
            line, lambda l: l.put_start_and_end_on(
                self.sun.get_center(),
                comet.get_center(),
            )
        )
        return line, line_update


class IntroduceShapeOfVelocities(AskAboutEllipses, MovingCameraScene):
    CONFIG = {
        "animate_sun": True,
        "sun_center": 2 * RIGHT,
        "a": 4.0,
        "b": 3.5,
        "num_vectors": 25,
    }

    def construct(self):
        self.setup_orbit()
        self.warp_orbit()
        self.reference_inverse_square_law()
        self.show_velocity_vectors()
        self.collect_velocity_vectors()

    def setup_orbit(self):
        self.add_sun()
        self.add_orbit()
        # CHANGE: GL's Scene.add/remove ungroup a group when one of its family members is added on its own: the comet is inside the Orbiting group, so adding the comet as foreground destroyed the group (its update never ran, the orbit froze and the wait-until-proportion loop never ended); use the whole orbit group as the foreground mobject
        self.add_foreground_mobjects(self.orbit)

    def warp_orbit(self):
        def func(z, c=3.5):
            return 1 * (np.exp((1.0 / c) * (z) + 1) - np.exp(1))

        ellipse = self.ellipse
        ellipse.save_state()
        ellipse.generate_target()
        ellipse.target.stretch(0.7, 1)
        ellipse.target.apply_complex_function(func)
        ellipse.target.replace(ellipse, dim_to_match=1)

        self.wait(5)
        self.play(MoveToTarget(ellipse, run_time=2))
        self.wait(5)

    def reference_inverse_square_law(self):
        ellipse = self.ellipse
        force_equation = OldTex(
            "F", "=", "{G", "M", "m", "\\over", "R^2}"
        )
        force_equation.move_to(ellipse)
        force_equation.set_color_by_tex("F", YELLOW)

        force_arrow, force_arrow_update = self.get_force_arrow_and_update(
            self.comet, scale_factor=3,
        )
        radial_line, radial_line_update = self.get_radial_line_and_update(
            self.comet
        )

        self.add(radial_line_update)
        self.add(force_arrow_update)
        self.play(
            Restore(ellipse),
            Write(force_equation),
            UpdateFromAlphaFunc(
                force_arrow,
                lambda m, a: m.set_fill(opacity=a)
            ),
            UpdateFromAlphaFunc(
                radial_line,
                lambda m, a: m.set_stroke(width=a)
            ),
        )
        self.wait(10)

    def show_velocity_vectors(self):
        alphas = np.linspace(0, 1, self.num_vectors, endpoint=False)
        vectors = VGroup(*[
            self.get_velocity_vector(alpha)
            for alpha in alphas
        ])

        moving_vector, moving_vector_animation = self.get_velocity_vector_and_update()

        self.play(LaggedStartMap(
            ShowCreation, vectors,
            lag_ratio=0.2,
            run_time=3,
        ))
        self.wait(5)

        self.add(moving_vector_animation)
        self.play(
            FadeOut(vectors),
            VFadeIn(moving_vector)
        )
        self.wait(10)
        vectors.set_fill(opacity=0.5)
        self.play(
            LaggedStartMap(ShowCreation, vectors),
            Animation(moving_vector)
        )
        self.wait(5)

        self.velocity_vectors = vectors
        self.moving_vector = moving_vector

    def collect_velocity_vectors(self):
        vectors = self.velocity_vectors.copy()
        frame = self.camera_frame
        ellipse = self.ellipse

        frame_shift = 2.5 * LEFT
        root_point = ellipse.get_left() + 3 * LEFT + 1 * UP
        vector_targets = VGroup()
        for vector in vectors:
            vector.target = Arrow(
                root_point,
                root_point + vector.get_vector(),
                buff=0,
                rectangular_stem_width=0.025,
                tip_length=0.2,
                color=vector.get_color(),
            )
            vector.target.add_to_back(
                vector.target.copy().set_stroke(BLACK, 5)
            )
            vector_targets.add(vector.target)

        circle = Circle(color=YELLOW)
        circle.replace(vector_targets)
        circle.scale(1.04)

        velocity_space = OldTexText("Velocity space")
        velocity_space.next_to(circle, UP)

        rect = SurroundingRectangle(
            VGroup(circle, velocity_space),
            buff=MED_LARGE_BUFF,
            color=WHITE,
        )

        self.play(
            ApplyMethod(
                frame.shift, frame_shift,
                run_time=2,
            ),
            LaggedStartMap(
                MoveToTarget, vectors,
                run_time=4,
            ),
            FadeInFromDown(velocity_space),
            FadeInFromDown(rect),
        )
        self.wait(2)
        self.play(
            ShowCreation(circle),
            Animation(vectors)
        )
        self.wait(24)

    # Helpers
    def get_velocity_vector(self, alpha, d_alpha=0.01, scalar=3.0):
        norm = get_norm
        ellipse = self.ellipse
        sun_center = self.sun.get_center()

        min_length = 0.1 * scalar
        max_length = 0.5 * scalar

        p1, p2 = [
            ellipse.point_from_proportion(a)
            for a in (alpha, alpha + d_alpha)
        ]
        vector = Arrow(
            p1, p2, buff=0
        )
        radius_vector = p1 - sun_center
        curr_v_perp = norm(np.cross(
            vector.get_vector(),
            radius_vector / norm(radius_vector)
        ))
        vector.scale(
            # CHANGE: curr_v_perp is already a scalar norm; GL's norm() cannot take a scalar
            scalar / (curr_v_perp * norm(radius_vector)),
            about_point=vector.get_start()
        )
        vector.set_color(
            interpolate_color(
                BLUE, RED, inverse_interpolate(
                    min_length, max_length,
                    vector.get_length()
                )
            )
        )
        vector.add_to_back(
            vector.copy().set_stroke(BLACK, 5)
        )
        return vector

    def get_velocity_vector_and_update(self):
        moving_vector = self.get_velocity_vector(0)

        def update_moving_vector(vector):
            new_vector = self.get_velocity_vector(
                self.orbit.proportion,
            )
            Transform(vector, new_vector).update(1)

        moving_vector_animation = Mobject.add_updater(
            moving_vector, update_moving_vector
        )
        return moving_vector, moving_vector_animation


class ShowSunVectorField(Scene):
    def construct(self):
        sun_center = IntroduceShapeOfVelocities.CONFIG["sun_center"]
        vector_field = VectorField(
            get_force_field_func((sun_center, -1))
        )
        vector_field.set_fill(opacity=0.8)
        vector_field.sort(
            lambda p: -get_norm(p - sun_center)
        )

        for vector in vector_field:
            vector.generate_target()
            vector.target.set_fill(opacity=1)
            vector.target.set_stroke(YELLOW, 0.5)

        for x in range(3):
            self.play(LaggedStartMap(
                MoveToTarget, vector_field,
                rate_func=there_and_back,
                lag_ratio=0.5,
            ))
