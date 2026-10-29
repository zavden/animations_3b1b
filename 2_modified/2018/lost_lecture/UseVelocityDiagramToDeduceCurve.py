# ==============================================================================
# Scene:      UseVelocityDiagramToDeduceCurve
# Source:     videos/_2018/lost_lecture.py (lines 3619-4136)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl UseVelocityDiagramToDeduceCurve.py UseVelocityDiagramToDeduceCurve -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject has no pixel_array in ManimGL; scaling the RGBA pixels by a is the same as set_opacity(a)
#   - SunAnimation was turned from a ContinualAnimation into a Group (see the TODO in the source): it has no .mobject, the group itself is the foreground mobject
#   - Python 2 integer division: the value is a list index
#   - curr_v_perp is already a scalar norm; GL's norm() cannot take a scalar
#   - Python 2 integer division: the value is a list index
#   - Python 2 integer division: the value is a list index
#   - GrowArrow on an arrow whose updater rescales it changes the point count mid-interpolation ('could not broadcast'); suspend the updater during the growth
#   - Transform(...).update(1) built a new animation (and copies) every frame; frame time and memory grew without bound (SIGKILL at 5 GB). become() gives the same final state
#   - GL's Scene.add/remove ungroup a group when one of its family members is added on its own: the comet is inside the Orbiting group, so adding the comet as foreground destroyed the group (its update never ran, the orbit froze and the wait-until-proportion loop never ended); use the whole orbit group as the foreground mobject
#   - same: comet is a member of the Orbiting group, so use the group as foreground (the loop below waits for orbit.proportion to advance)
# ==============================================================================

from manim_imports_ext import *

COBALT = "#0047AB"


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


class ShowEqualAngleSlices(IntroduceShapeOfVelocities):
    CONFIG = {
        "animate_sun": True,
        "theta": 30 * DEGREES,
    }

    def construct(self):
        self.setup_orbit()
        self.show_equal_angle_slices()
        self.ask_about_time_per_slice()
        self.areas_are_proportional_to_radius_squared()
        self.show_inverse_square_law()
        self.directly_compare_velocity_vectors()

    def setup_orbit(self):
        IntroduceShapeOfVelocities.setup_orbit(self)
        self.remove(self.orbit)
        self.add(self.comet)

    def show_equal_angle_slices(self):
        sun_center = self.sun.get_center()
        ellipse = self.ellipse

        def get_cos_angle_diff(v1, v2):
            return np.dot(
                v1 / get_norm(v1),
                v2 / get_norm(v2),
            )

        lines = VGroup()
        angle_arcs = VGroup()
        thetas = VGroup()
        angles = np.arange(0, TAU, self.theta)
        for angle in angles:
            prop = angle / TAU
            vect = rotate_vector(RIGHT, angle)
            end_point = ellipse.point_from_proportion(prop)
            curr_cos = get_cos_angle_diff(
                end_point - sun_center, vect
            )
            coss_diff = (1 - curr_cos)
            while abs(coss_diff) > 0.00001:
                d_prop = 0.001
                alt_end = ellipse.point_from_proportion(
                    (prop + d_prop) % 1
                )
                alt_cos = get_cos_angle_diff(alt_end - sun_center, vect)
                d_cos = (alt_cos - curr_cos)

                delta_prop = (coss_diff / d_cos) * d_prop
                prop += delta_prop
                end_point = ellipse.point_from_proportion(prop)
                curr_cos = get_cos_angle_diff(end_point - sun_center, vect)
                coss_diff = 1 - curr_cos

            line = Line(sun_center, end_point)
            line.prop = prop
            lines.add(line)

            angle_arc = AnnularSector(
                angle=self.theta,
                inner_radius=1,
                outer_radius=1.05,
            )
            angle_arc.rotate(angle, about_point=ORIGIN)
            angle_arc.scale(0.5, about_point=ORIGIN)
            angle_arc.shift(sun_center)
            angle_arc.mid_angle = angle + self.theta / 2
            angle_arcs.add(angle_arc)

            theta = OldTex("\\theta")
            theta.scale(0.6)
            vect = rotate_vector(RIGHT, angle_arc.mid_angle)
            theta.move_to(
                angle_arc.get_center() + 0.2 * vect
            )
            thetas.add(theta)

        arcs = VGroup()
        wedges = VGroup()
        for l1, l2 in adjacent_pairs(lines):
            arc = VMobject()
            arc.pointwise_become_partial(
                ellipse, l1.prop, (l2.prop or 1.0)
            )
            arcs.add(arc)

            wedge = VMobject()
            wedge.append_vectorized_mobject(
                Line(sun_center, arc.get_points()[0])
            )
            wedge.append_vectorized_mobject(arc)
            wedge.append_vectorized_mobject(
                Line(arc.get_points()[-1], sun_center)
            )
            wedges.add(wedge)

        lines.set_stroke(GREY_B, 2)
        angle_arcs.set_color_by_gradient(
            YELLOW, BLUE, RED, PINK, YELLOW
        )
        arcs.set_color_by_gradient(BLUE, YELLOW)
        wedges.set_stroke(width=0)
        wedges.set_fill(opacity=1)
        wedges.set_color_by_gradient(BLUE, COBALT, BLUE_E, BLUE)

        kwargs = {
            "run_time": 6,
            "lag_ratio": 0.2,
            "rate_func": there_and_back,
        }
        faders = VGroup(wedges, angle_arcs, thetas)
        faders.set_fill(opacity=0.4)
        thetas.set_fill(opacity=0)

        self.play(
            FadeIn(faders),
            *list(map(ShowCreation, lines))
        )
        self.play(*[
            LaggedStartMap(
                ApplyMethod, fader,
                lambda m: (m.set_fill, {"opacity": 1}),
                **kwargs
            )
            for fader in faders
        ] + [Animation(lines)])
        self.wait()

        self.lines = lines
        self.wedges = wedges
        self.arcs = arcs
        self.angle_arcs = angle_arcs
        self.thetas = thetas

    def ask_about_time_per_slice(self):
        wedge1 = self.wedges[0]
        # CHANGE: Python 2 integer division: the value is a list index
        wedge2 = self.wedges[len(self.wedges) // 2]
        arc1 = self.arcs[0]
        # CHANGE: Python 2 integer division: the value is a list index
        arc2 = self.arcs[len(self.arcs) // 2]
        comet = self.comet
        frame = self.camera_frame

        words1 = OldTexText(
            "Time spent \\\\ traversing \\\\ this slice?"
        )
        words2 = OldTexText("How about \\\\ this one?")

        words1.to_corner(UR)
        words2.next_to(wedge2, LEFT, MED_LARGE_BUFF)

        arrow1 = Arrow(
            words1.get_bottom(),
            wedge1.get_center() + wedge1.get_height() * DOWN / 2,
            color=WHITE,
        )
        arrow2 = Arrow(
            words2.get_right(),
            wedge2.get_center() + wedge2.get_height() * UL / 4,
            color=WHITE
        )

        foreground = VGroup(
            self.ellipse, self.angle_arcs,
            self.lines, comet,
        )
        self.play(
            Write(words1),
            wedge1.set_fill, {"opacity": 1},
            GrowArrow(arrow1),
            Animation(foreground),
            frame.scale, 1.2,
        )
        self.play(MoveAlongPath(comet, arc1, rate_func=linear))
        self.play(
            Write(words2),
            wedge2.set_fill, {"opacity": 1},
            Write(arrow2),
            Animation(foreground),
        )
        self.play(MoveAlongPath(comet, arc2, rate_func=linear, run_time=3))
        self.wait()

        self.area_questions = VGroup(words1, words2)
        self.area_question_arrows = VGroup(arrow1, arrow2)
        self.highlighted_wedges = VGroup(wedge1, wedge2)

    def areas_are_proportional_to_radius_squared(self):
        wedges = self.highlighted_wedges
        wedge = wedges[1]
        frame = self.camera_frame
        ellipse = self.ellipse
        sun_center = self.sun.get_center()

        # CHANGE: Python 2 integer division: the value is a list index
        line = self.lines[len(self.lines) // 2]
        thick_line = line.copy().set_stroke(PINK, 4)
        radius_word = OldTexText("Radius")
        radius_word.next_to(thick_line, UP, SMALL_BUFF)
        radius_word.match_color(thick_line)

        # CHANGE: Python 2 integer division: the value is a list index
        arc = self.arcs[len(self.arcs) // 2]
        thick_arc = arc.copy().set_stroke(RED, 4)

        scaling_group = VGroup(
            wedge, thick_line, radius_word, thick_arc
        )

        expression = OldTexText(
            "Time", "$\\propto$",
            "Area", "$\\propto$", "$(\\text{Radius})^2$"
        )
        expression.next_to(ellipse, UP, LARGE_BUFF)

        prop_to_brace = Brace(expression[1], DOWN, buff=SMALL_BUFF)
        prop_to_words = OldTexText("(proportional to)")
        prop_to_words.scale(0.7)
        prop_to_words.next_to(prop_to_brace, DOWN, SMALL_BUFF)
        VGroup(prop_to_words, prop_to_brace).set_color(GREEN)

        self.play(
            Write(expression[:3]),
            frame.shift, 0.5 * UP,
            FadeInFromDown(prop_to_words),
            GrowFromCenter(prop_to_brace),
        )
        self.wait(2)
        self.play(
            ShowCreation(thick_line),
            FadeInFromDown(radius_word)
        )
        self.wait()
        self.play(ShowCreationThenDestruction(thick_arc))
        self.play(ShowCreation(thick_arc))
        self.wait()
        self.play(Write(expression[3:]))
        self.play(
            scaling_group.scale, 0.5,
            {"about_point": sun_center},
            Animation(self.area_question_arrows),
            Animation(self.comet),
            rate_func=there_and_back,
            run_time=4,
        )
        self.wait()

        expression.add(prop_to_brace, prop_to_words)
        self.proportionality_expression = expression

    def show_inverse_square_law(self):
        prop_exp = self.proportionality_expression
        comet = self.comet
        frame = self.camera_frame
        ellipse = self.ellipse
        orbit = self.orbit
        # CHANGE: Python 2 integer division: the value is a list index
        next_line = self.lines[(len(self.lines) // 2) + 1]

        # CHANGE: Python 2 integer division: the value is a list index
        arc = self.arcs[len(self.arcs) // 2]

        force_expression = OldTex(
            "ma", "=", "\\text{Force}",
            "\\propto", "\\frac{1}{(\\text{Radius})^2}"
        )
        force_expression.next_to(ellipse, LEFT, MED_LARGE_BUFF)
        force_expression.align_to(prop_exp, UP)
        force_expression.set_color_by_tex("Force", YELLOW)

        acceleration_expression = OldTex(
            "a", "=", "{\\Delta v",
            "\\over", "\\Delta t}",
            "\\propto", "{1 \\over (\\text{Radius})^2}"
        )
        acceleration_expression.next_to(
            force_expression, DOWN, buff=0.75,
            aligned_edge=LEFT
        )

        delta_v_expression = OldTex(
            "\\Delta v}", "\\propto",
            "{\\Delta t", "\\over", "(\\text{Radius})^2}"
        )
        delta_v_expression.next_to(
            acceleration_expression, DOWN, buff=0.75,
            aligned_edge=LEFT
        )
        delta_t_numerator = delta_v_expression.get_part_by_tex(
            "\\Delta t"
        )
        moving_R_squared = prop_exp.get_part_by_tex("Radius").copy()
        moving_R_squared.generate_target()
        moving_R_squared.target.move_to(delta_t_numerator, DOWN)
        moving_R_squared.target.set_color(GREEN)

        randy = Randolph()
        randy.next_to(force_expression, DOWN, LARGE_BUFF)

        force_vector, force_vector_update = self.get_force_arrow_and_update(
            comet, scale_factor=3,
        )
        moving_vector, moving_vector_animation = self.get_velocity_vector_and_update()

        self.play(
            FadeOut(self.area_questions),
            FadeOut(self.area_question_arrows),
            FadeInFromDown(force_expression),
            frame.shift, 2 * LEFT,
        )
        self.remove(*self.area_questions)
        self.play(
            randy.change, "confused", force_expression,
            VFadeIn(randy)
        )
        self.wait(2)
        self.play(
            randy.change, "pondering", force_expression[0],
            ShowPassingFlashAround(force_expression[:2]),
        )
        self.play(Blink(randy))
        self.play(
            FadeInFromDown(acceleration_expression),
            randy.change, "hooray", force_expression,
            randy.shift, 2 * DOWN,
        )
        self.wait(2)
        self.play(Blink(randy))
        self.play(randy.change, "thinking")
        self.wait()

        self.play(
            comet.move_to, arc.get_points()[0],
            path_arc=90 * DEGREES
        )
        force_vector_update.update(0)
        # CHANGE: GrowArrow on an arrow whose updater rescales it changes the point count mid-interpolation ('could not broadcast'); suspend the updater during the growth
        force_vector.suspend_updating()
        self.play(
            Blink(randy),
            GrowArrow(force_vector)
        )
        force_vector.resume_updating()
        self.add(force_vector_update)
        # CHANGE: same: comet is a member of the Orbiting group, so use the group as foreground (the loop below waits for orbit.proportion to advance)
        self.add_foreground_mobjects(orbit)
        # Slightly hacky orbit treatment here...
        orbit.proportion = 0.5
        moving_vector_animation.update(0)
        start_velocity_vector = moving_vector.copy()
        self.play(
            GrowArrow(start_velocity_vector),
            randy.look_at, moving_vector
        )
        self.add(moving_vector_animation)
        self.add(orbit)
        while orbit.proportion < next_line.prop:
            self.wait(self.frame_duration)
        self.remove(orbit)
        self.add_foreground_mobjects(comet)
        self.wait(2)
        self.play(
            randy.change, "pondering", force_expression,
            randy.shift, 2 * DOWN,
            FadeInFromDown(delta_v_expression)
        )
        self.play(Blink(randy))
        self.wait(2)
        self.play(
            delta_t_numerator.scale, 1.5, {"about_edge": DOWN},
            delta_t_numerator.set_color, YELLOW
        )
        self.play(ShowCreationThenFadeAround(prop_exp[:-2]))
        self.play(
            delta_t_numerator.fade, 1,
            MoveToTarget(moving_R_squared),
            randy.change, "happy", delta_v_expression
        )
        delta_v_expression.add(moving_R_squared)
        self.wait()
        self.play(FadeOut(randy))

        self.start_velocity_vector = start_velocity_vector
        self.end_velocity_vector = moving_vector.copy()
        self.moving_vector = moving_vector
        self.force_expressions = VGroup(
            force_expression,
            acceleration_expression,
            delta_v_expression,
        )

    def directly_compare_velocity_vectors(self):
        ellipse = self.ellipse
        lines = self.lines
        expressions = self.force_expressions
        vectors = VGroup(*[
            self.get_velocity_vector(line.prop)
            for line in lines
        ])
        # CHANGE: Python 2 integer division: the value is a list index
        index = len(vectors) // 2
        v1 = vectors[index]
        v2 = vectors[index + 1]

        root_point = ellipse.get_left() + 3 * LEFT + DOWN
        root_dot = Dot(root_point)

        for vector in vectors:
            vector.save_state()
            vector.target = Arrow(
                *vector.get_start_and_end(),
                color=vector.get_color(),
                buff=0
            )
            vector.target.scale(2)
            vector.target.shift(
                root_point - vector.target.get_start()
            )
            vector.target.add_to_back(
                vector.target.copy().set_stroke(BLACK, 5)
            )

        difference_vectors = VGroup()
        external_angle_lines = VGroup()
        external_angle_arcs = VGroup()
        for vect1, vect2 in adjacent_pairs(vectors):
            diff_vect = Arrow(
                vect1.target.get_end(),
                vect2.target.get_end(),
                buff=0,
                color=YELLOW,
                rectangular_stem_width=0.025,
                tip_length=0.15
            )
            diff_vect.add_to_back(
                diff_vect.copy().set_stroke(BLACK, 2)
            )
            difference_vectors.add(diff_vect)

            line = Line(
                diff_vect.get_start(),
                diff_vect.get_start() + 2 * diff_vect.get_vector(),
            )
            external_angle_lines.add(line)

            arc = Arc(self.theta, stroke_width=2)
            arc.rotate(line.get_angle(), about_point=ORIGIN)
            arc.scale(0.4, about_point=ORIGIN)
            arc.shift(line.get_center())
            external_angle_arcs.add(arc)
        external_angle_lines.set_stroke(GREY_B, 2)
        diff_vect = difference_vectors[index]

        polygon = Polygon(*[
            vect.target.get_end()
            for vect in vectors
        ])
        polygon.set_fill(BLUE_E, opacity=0.8)
        polygon.set_stroke(WHITE, 3)

        self.play(ShowCreationThenFadeAround(v1))
        self.play(
            MoveToTarget(v1),
            GrowFromCenter(root_dot),
            expressions.scale, 0.5, {"about_edge": UL}
        )
        self.wait()
        self.play(
            ReplacementTransform(
                v1.saved_state.copy(), v2.saved_state,
                path_arc=self.theta
            )
        )
        self.play(MoveToTarget(v2), Animation(root_dot))
        self.wait()
        self.play(GrowArrow(diff_vect))
        self.wait()

        n = len(vectors)
        for i in range(n - 1):
            v1 = vectors[(i + index + 1) % n]
            v2 = vectors[(i + index + 2) % n]
            diff_vect = difference_vectors[(i + index + 1) % n]
            # TODO, v2.saved_state is on screen untracked
            self.play(ReplacementTransform(
                v1.saved_state.copy(), v2.saved_state,
                path_arc=self.theta
            ))
            self.play(
                MoveToTarget(v2),
                GrowArrow(diff_vect)
            )
        self.add(self.orbit)
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, external_angle_lines),
            LaggedStartMap(ShowCreation, external_angle_arcs),
            Animation(difference_vectors),
        )
        self.add_foreground_mobjects(difference_vectors)
        self.wait(2)
        self.play(FadeIn(polygon))
        self.wait(5)
        self.play(FadeOut(polygon))
        self.wait(15)
        self.play(FadeIn(polygon))


class UseVelocityDiagramToDeduceCurve(ShowEqualAngleSlices):
    CONFIG = {
        "animate_sun": True,
        "theta": 15 * DEGREES,
        "index": 6,
    }

    def construct(self):
        self.setup_orbit()
        self.setup_velocity_diagram()
        self.show_theta_degrees()
        self.match_velocity_vector_to_tangency()
        self.replace_vectors_with_lines()
        self.not_that_velocity_vector_is_theta()
        self.ask_about_curve()
        self.show_90_degree_rotation()
        self.show_geometry_of_rotated_diagram()

    def setup_orbit(self):
        ShowEqualAngleSlices.setup_orbit(self)
        self.force_skipping()
        self.show_equal_angle_slices()
        self.revert_to_original_skipping_status()

        orbit_word = self.orbit_word = OldTexText("Orbit")
        orbit_word.scale(1.5)
        orbit_word.next_to(self.ellipse, UP, LARGE_BUFF)
        self.add(orbit_word)

    def setup_velocity_diagram(self):
        ellipse = self.ellipse
        root_point = ellipse.get_left() + 4 * LEFT + DOWN
        frame = self.camera_frame

        root_dot = Dot(root_point)
        vectors = VGroup()
        original_vectors = VGroup()
        for line in self.lines:
            vector = self.get_velocity_vector(line.prop)
            vector.save_state()
            original_vectors.add(vector.copy())
            vector.target = self.get_velocity_vector(
                line.prop, scalar=8.0
            )
            vector.target.shift(
                root_point - vector.target.get_start()
            )

            vectors.add(vector)

        circle = Circle()
        circle.rotate(92 * DEGREES)
        circle.replace(VGroup(*[v.target for v in vectors]))
        circle.set_stroke(WHITE, 2)
        circle.shift(
            (root_point[0] - circle.get_center()[0]) * RIGHT
        )
        circle.shift(0.035 * LEFT)  # ?!?

        velocities_word = OldTexText("Velocities")
        velocities_word.scale(1.5)
        velocities_word.next_to(circle, UP)
        velocities_word.align_to(self.orbit_word, DOWN)

        frame.scale(1.2)
        frame.shift(3 * LEFT + 0.5 * UP)

        self.play(ApplyWave(ellipse))
        self.play(*list(map(GrowArrow, vectors)))
        self.play(
            LaggedStartMap(
                MoveToTarget, vectors,
                lag_ratio=1,
                run_time=2
            ),
            GrowFromCenter(root_dot),
            FadeInFromDown(velocities_word),
        )
        self.add_foreground_mobjects(root_dot)
        self.play(
            ShowCreation(circle),
            Animation(vectors),
        )
        self.wait()

        self.vectors = vectors
        self.original_vectors = original_vectors
        self.velocity_circle = circle
        self.root_dot = root_dot
        self.circle = circle

    def show_theta_degrees(self):
        lines = self.lines
        ellipse = self.ellipse
        circle = self.circle
        vectors = self.vectors
        comet = self.comet
        sun_center = self.sun.get_center()

        index = self.index
        angle = fdiv(index, len(lines)) * TAU
        thick_line = lines[index].copy()
        thick_line.set_stroke(RED, 3)
        horizontal = lines[0].copy()
        horizontal.set_stroke(WHITE, 3)

        ellipse_arc = VMobject()
        ellipse_arc.pointwise_become_partial(
            ellipse, 0, thick_line.prop
        )
        ellipse_arc.set_stroke(YELLOW, 3)

        ellipse_wedge = self.get_wedge(ellipse_arc, sun_center)
        ellipse_wedge_start = self.get_wedge(
            VectorizedPoint(ellipse.get_right()), sun_center
        )

        ellipse_angle_arc = Arc(
            self.theta * index,
            radius=0.5
        )
        ellipse_angle_arc.shift(sun_center)
        ellipse_theta = OldTex("\\theta")
        ellipse_theta.next_to(ellipse_angle_arc, RIGHT, MED_SMALL_BUFF)
        ellipse_theta.shift(2 * SMALL_BUFF * UL)

        vector = vectors[index].deepcopy()
        vector.set_fill(YELLOW)
        vector.save_state()
        Transform(vector, vectors[0]).update(1)
        vector.set_fill(YELLOW)
        circle_arc = VMobject()
        circle_arc.pointwise_become_partial(
            circle, 0, fdiv(index, len(vectors))
        )
        circle_arc.set_stroke(RED, 4)
        circle_theta = OldTex("\\theta")
        circle_theta.scale(1.5)
        circle_theta.next_to(circle_arc, UP, SMALL_BUFF)
        circle_theta.shift(SMALL_BUFF * DL)

        circle_wedge = self.get_wedge(circle_arc, circle.get_center())
        circle_wedge.set_fill(PINK)
        circle_wedge_start = self.get_wedge(
            Line(circle.get_top(), circle.get_top()),
            circle.get_center()
        ).match_style(circle_wedge)

        circle_center_dot = Dot(circle.get_center())
        # circle_center_dot.set_color(BLUE)

        self.play(FocusOn(comet))
        self.play(
            ReplacementTransform(
                ellipse_wedge_start, ellipse_wedge,
                path_arc=angle,
            ),
            FadeIn(ellipse_arc),
            ShowCreation(ellipse_angle_arc),
            Write(ellipse_theta),
            ReplacementTransform(
                lines[0].copy(), thick_line,
                path_arc=angle
            ),
            MoveAlongPath(comet, ellipse_arc),
            run_time=2
        )
        self.wait()
        self.play(
            ReplacementTransform(
                circle_wedge_start, circle_wedge,
                path_arc=angle
            ),
            ShowCreation(circle_arc),
            Write(circle_theta),
            Restore(vector, path_arc=angle),
            GrowFromCenter(circle_center_dot),
            FadeIn(horizontal),
            run_time=2
        )
        self.wait()

        self.set_variables_as_attrs(
            index,
            ellipse_wedge, ellipse_arc,
            ellipse_angle_arc, ellipse_theta,
            thick_line, horizontal,
            circle_wedge, circle_arc,
            circle_theta, circle_center_dot,
            highlighted_vector=vector
        )

    def match_velocity_vector_to_tangency(self):
        vector = self.highlighted_vector
        comet = self.comet
        original_vector = self.original_vectors[self.index].copy()
        original_vector.set_fill(YELLOW)

        tangent_line = Line(
            *original_vector.get_start_and_end()
        )
        tangent_line.set_stroke(GREY_B, 3)
        tangent_line.scale(5)
        tangent_line.move_to(comet)

        self.play(
            ReplacementTransform(
                vector.copy(), original_vector,
                run_time=2
            ),
            Animation(comet),
        )
        self.wait()
        self.play(
            ShowCreation(tangent_line),
            Animation(original_vector),
            Animation(comet),
        )
        self.wait()

        self.set_variables_as_attrs(
            example_tangent_line=tangent_line,
            example_tangent_vector=original_vector,
        )

    def replace_vectors_with_lines(self):
        vectors = self.vectors
        original_vectors = self.original_vectors
        root_dot = self.root_dot
        highlighted_vector = self.highlighted_vector

        lines = VGroup()
        tangent_lines = VGroup()
        for vect, o_vect in zip(vectors, original_vectors):
            line = Line(*vect.get_start_and_end())
            t_line = Line(*o_vect.get_start_and_end())
            t_line.scale(5)
            t_line.move_to(o_vect.get_start())

            lines.add(line)
            tangent_lines.add(t_line)

            vect.generate_target()
            vect.target.scale(0, about_point=root_dot.get_center())

        lines.set_stroke(GREEN, 2)
        tangent_lines.set_stroke(GREEN, 2)

        highlighted_line = Line(
            *highlighted_vector.get_start_and_end(),
            stroke_color=YELLOW,
            stroke_width=4
        )

        self.play(
            LaggedStartMap(MoveToTarget, vectors),
            highlighted_vector.scale, 0,
            {"about_point": root_dot.get_center()},
            Animation(highlighted_vector),
            Animation(self.circle_wedge),
            Animation(self.circle_arc),
            Animation(self.circle),
            Animation(self.circle_center_dot),
        )
        self.remove(vectors, highlighted_vector)
        self.play(
            LaggedStartMap(ShowCreation, lines),
            ShowCreation(highlighted_line),
            Animation(highlighted_vector),
        )
        self.wait()
        self.play(
            ReplacementTransform(
                lines.copy(),
                tangent_lines,
                run_time=3,
            )
        )
        self.wait()
        self.play(FadeOut(tangent_lines))

        self.eccentric_lines = lines
        self.highlighted_line = highlighted_line

    def not_that_velocity_vector_is_theta(self):
        vector = self.example_tangent_vector
        v_line = Line(DOWN, UP)
        v_line.move_to(vector.get_start(), DOWN)
        angle = vector.get_angle() - 90 * DEGREES
        arc = Arc(angle, radius=0.5)
        arc.rotate(90 * DEGREES, about_point=ORIGIN)
        arc.shift(vector.get_start())

        theta_q = OldTex("\\theta ?")
        theta_q.next_to(arc, UP)
        theta_q.shift(SMALL_BUFF * LEFT)
        cross = Cross(theta_q)

        self.play(ShowCreation(v_line))
        self.play(
            ShowCreation(arc),
            FadeInFromDown(theta_q),
        )
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()
        self.play(*list(map(FadeOut, [v_line, arc, theta_q, cross])))
        self.wait()
        self.play(
            ReplacementTransform(
                self.ellipse_theta.copy(), self.circle_theta,
            ),
            ReplacementTransform(
                self.ellipse_angle_arc.copy(), self.circle_arc,
            ),
            run_time=2,
        )
        self.wait()
        self.play(
            ReplacementTransform(
                self.circle.copy(),
                self.circle_center_dot,
            )
        )
        self.wait()

    def ask_about_curve(self):
        ellipse = self.ellipse
        circle = self.circle
        line = self.highlighted_line.copy()
        vector = self.example_tangent_vector

        morty = Mortimer(height=2.5)
        morty.move_to(ellipse.get_corner(UL))
        morty.shift(MED_SMALL_BUFF * LEFT)

        self.play(FadeIn(morty))
        self.play(
            morty.change, "confused", ellipse,
            ShowCreationThenDestruction(
                ellipse.copy().set_stroke(BLUE, 3),
                run_time=2
            )
        )
        self.play(
            Blink(morty),
            ApplyWave(ellipse),
        )
        self.play(morty.look_at, circle)
        self.play(morty.change, "pondering", circle)
        self.play(Blink(morty))
        self.play(morty.look_at, ellipse)
        self.play(morty.change, "maybe", ellipse)
        self.play(
            line.move_to, vector, run_time=2
        )
        self.play(FadeOut(line))
        self.wait()
        self.play(morty.look_at, circle)
        self.wait()
        self.play(FadeOut(morty))

    def show_90_degree_rotation(self):
        circle = self.circle
        circle_setup = VGroup(
            circle, self.eccentric_lines,
            self.circle_wedge,
            self.circle_arc,
            self.highlighted_line,
            self.circle_center_dot,
            self.root_dot,
            self.circle_theta,
        )
        circle_setup.generate_target()
        angle = -90 * DEGREES
        circle_setup.target.rotate(
            angle,
            about_point=circle.get_center()
        )
        circle_setup.target[-1].rotate(-angle)
        circle_setup.target[2].set_fill(opacity=0)
        circle_setup.target[2].set_stroke(WHITE, 4)

        self.play(MoveToTarget(circle_setup, path_arc=angle))
        self.wait()

        lines = self.eccentric_lines
        highlighted_line = self.highlighted_line
        ghost_lines = lines.copy()
        ghost_lines.set_stroke(width=1)
        ghost_lines[self.index].set_stroke(YELLOW, 4)
        for mob in list(lines) + [highlighted_line]:
            mob.generate_target()
            mob.save_state()
            mob.target.rotate(-angle)

        foci = [
            self.root_dot.get_center(),
            circle.get_center(),
        ]
        a = circle.get_width() / 4
        c = get_norm(foci[1] - foci[0]) / 2
        b = np.sqrt(a**2 - c**2)
        little_ellipse = Circle(radius=a)
        little_ellipse.stretch(b / a, 1)
        little_ellipse.move_to(center_of_mass(foci))
        little_ellipse.set_stroke(PINK, 4)

        self.add(ghost_lines)
        self.play(
            LaggedStartMap(
                MoveToTarget, lines,
                lag_ratio=0.1,
                run_time=8,
            ),
            MoveToTarget(highlighted_line),
            path_arc=-angle,
        )
        self.play(ShowCreation(little_ellipse))
        self.wait(2)
        self.play(
            little_ellipse.replace, self.ellipse,
            run_time=4,
            rate_func=there_and_back_with_pause
        )
        self.wait(2)

        self.play(*[
            Restore(
                mob,
                path_arc=angle,
                run_time=4,
                rate_func=there_and_back_with_pause
            )
            for mob in list(lines) + [highlighted_line]
        ] + [Animation(little_ellipse)])

        self.ghost_lines = ghost_lines
        self.little_ellipse = little_ellipse

    def show_geometry_of_rotated_diagram(self):
        ellipse = self.ellipse
        little_ellipse = self.little_ellipse
        circle = self.circle
        perp_line = self.highlighted_line.copy()
        perp_line.rotate(PI)
        circle_arc = self.circle_arc
        arc_copy = circle_arc.copy()
        center = circle.get_center()
        velocity_vector = self.example_tangent_vector

        e_line = perp_line.copy().rotate(90 * DEGREES)
        c_line = Line(center, e_line.get_end())
        c_line.set_stroke(WHITE, 4)

        # lines = [c_line, e_line, perp_line]

        tangency_point = line_intersection(
            perp_line.get_start_and_end(),
            c_line.get_start_and_end(),
        )
        tangency_point_dot = Dot(tangency_point)
        tangency_point_dot.set_color(BLUE)
        tangency_point_dot.save_state()
        tangency_point_dot.scale(5)
        tangency_point_dot.set_fill(opacity=0)

        def indicate(line):
            red_copy = line.copy().set_stroke(RED, 5)
            return ShowPassingFlash(red_copy, run_time=2)

        self.play(
            self.ghost_lines.set_stroke, {"width": 0.5},
            self.eccentric_lines.set_stroke, {"width": 0.5},
            *list(map(WiggleOutThenIn, [e_line, c_line]))
        )
        for x in range(3):
            self.play(
                indicate(e_line),
                indicate(c_line),
            )
        self.play(WiggleOutThenIn(perp_line))
        for x in range(2):
            self.play(indicate(perp_line))
        self.play(Restore(tangency_point_dot))
        self.add_foreground_mobjects(tangency_point_dot)
        self.wait(2)
        self.play(
            arc_copy.scale, 0.15, {"about_point": center},
            run_time=2
        )
        self.wait(2)
        self.play(
            perp_line.move_to, velocity_vector,
            run_time=4,
            rate_func=there_and_back_with_pause
        )
        self.wait()
        self.play(
            little_ellipse.replace, ellipse,
            run_time=4,
            rate_func=there_and_back_with_pause
        )
        self.wait()

    # Helpers
    def get_wedge(self, arc, center_point, opacity=0.8):
        wedge = VMobject()
        wedge.append_vectorized_mobject(
            Line(center_point, arc.get_points()[0])
        )
        wedge.append_vectorized_mobject(arc)
        wedge.append_vectorized_mobject(
            Line(arc.get_points()[-1], center_point)
        )
        wedge.set_stroke(width=0)
        wedge.set_fill(COBALT, opacity=opacity)
        return wedge
