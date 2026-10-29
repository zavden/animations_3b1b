# ==============================================================================
# Scene:      AskAboutEllipses
# Source:     videos/_2018/lost_lecture.py (lines 700-975)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AskAboutEllipses.py AskAboutEllipses -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject has no pixel_array in ManimGL; scaling the RGBA pixels by a is the same as set_opacity(a)
#   - SunAnimation was turned from a ContinualAnimation into a Group (see the TODO in the source): it has no .mobject, the group itself is the foreground mobject
#   - Transform(...).update(1) built a new animation (and copies) every frame; frame time and memory grew without bound (SIGKILL at 5 GB). become() gives the same final state
# ==============================================================================

from manim_imports_ext import *

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
