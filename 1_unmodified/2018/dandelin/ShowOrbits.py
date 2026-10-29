# ==============================================================================
# Scene:      ShowOrbits
# Source:     videos/_2018/dandelin.py (lines 445-515)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/lost_lecture.py
#
# Run from this folder:
#     manimgl ShowOrbits.py ShowOrbits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


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



# ----- From _2018/dandelin.py -----

class ShowArrayOfEccentricities(Scene):
    def construct(self):
        eccentricities = np.linspace(0, 0.99, 6)
        eccentricity_labels = VGroup(*list(map(
            DecimalNumber, eccentricities
        )))
        ellipses = self.get_ellipse_row(eccentricities)
        ellipses.set_color_by_gradient(BLUE, YELLOW)
        ellipses.move_to(DOWN)

        for label, ellipse in zip(eccentricity_labels, ellipses):
            label.next_to(ellipse, UP)

        name = OldTexText("Eccentricity")
        name.scale(1.5)
        name.to_edge(UP)
        alt_name = OldTexText("(read ``squishification'')")
        alt_name.set_color(YELLOW)
        alt_name.next_to(name, RIGHT)
        alt_name.shift_onto_screen()
        name.generate_target()
        name.target.next_to(alt_name, LEFT)

        arrows = VGroup(*[
            Arrow(name.get_bottom(), label.get_top())
            for label in eccentricity_labels
        ])
        arrows.set_color_by_gradient(BLUE, YELLOW)

        for label, arrow in zip(eccentricity_labels, arrows):
            label.save_state()
            label.fade(1)
            label.scale(0.1)
            label.move_to(arrow.get_start())

        morty = Mortimer(height=2)
        morty.next_to(alt_name, DOWN)

        self.add(ellipses[0])
        for e1, e2 in zip(ellipses[:-1], ellipses[1:]):
            self.play(ReplacementTransform(
                e1.copy(), e2,
                path_arc=10 * DEGREES
            ))
        self.wait()

        self.play(
            Write(name),
            LaggedStartMap(GrowArrow, arrows),
            LaggedStartMap(Restore, eccentricity_labels)
        )
        self.wait()
        self.play(
            Write(alt_name),
            MoveToTarget(name),
            morty.change, "hooray", alt_name,
            VFadeIn(morty),
        )
        self.play(Blink(morty))
        self.play(morty.change, "thinking", ellipses)
        self.wait()
        self.play(Blink(morty))

        for i in 0, -1:
            e_copy = ellipses[i].copy()
            e_copy.set_color(RED)
            self.play(ShowCreation(e_copy))
            self.play(
                ShowCreationThenFadeAround(
                    eccentricity_labels[i],
                ),
                FadeOut(e_copy)
            )
        self.wait()

        circle = ellipses[0]
        group = VGroup(*it.chain(
            eccentricity_labels,
            ellipses[1:],
            arrows,
            name,
            alt_name,
            [morty]
        ))
        self.play(
            LaggedStartMap(FadeOutAndShiftDown, group),
            circle.set_height, 5,
            circle.center,
        )

    def get_ellipse(self, eccentricity, width=2):
        result = Circle(color=WHITE)
        result.set_width(width)
        a = width / 2.0
        c = eccentricity * a
        b = np.sqrt(a**2 - c**2)
        result.stretch(b / a, 1)
        result.shift(c * LEFT)

        result.eccentricity = eccentricity
        return result

    def get_ellipse_row(self, eccentricities, buff=MED_SMALL_BUFF, **kwargs):
        result = VGroup(*[
            self.get_ellipse(e, **kwargs)
            for e in eccentricities
        ])
        result.arrange(RIGHT, buff=buff)
        return result

    def get_eccentricity(self, ellipse):
        """
        Assumes that it's major/minor axes line up
        with x and y axes
        """
        a = ellipse.get_width()
        b = ellipse.get_height()
        if b > a:
            a, b = b, a
        c = np.sqrt(a**2 - b**2)
        return fdiv(c, a)


class ShowOrbits(ShowArrayOfEccentricities):
    CONFIG = {"camera_config": {"background_opacity": 1}}

    def construct(self):
        earth_eccentricity = 0.0167
        comet_eccentricity = 0.9671
        earth_orbit = self.get_ellipse(eccentricity=earth_eccentricity)
        comet_orbit = self.get_ellipse(eccentricity=comet_eccentricity)
        earth_orbit.set_height(5)
        comet_orbit.set_width(
            0.7 * FRAME_WIDTH,
            about_point=ORIGIN,
        )

        sun = ImageMobject("Sun")
        earth = ImageMobject("Earth")
        comet = ImageMobject("Comet")
        sun.set_height(1)
        earth.set_height(0.5)
        comet.set_height(0.1)

        earth_parts = VGroup(sun, earth_orbit, earth)

        eccentricity_label = DecimalNumber(
            earth_eccentricity,
            num_decimal_places=4
        )
        eccentricity_equals = OldTexText(
            "Eccentricity = "
        )
        earth_orbit_words = OldTexText("Earth's orbit")
        earth_orbit_words.set_color(BLUE)
        full_label = VGroup(
            earth_orbit_words,
            eccentricity_equals, eccentricity_label
        )
        full_label.arrange(RIGHT, SMALL_BUFF)
        earth_orbit_words.shift(0.5 * SMALL_BUFF * UL)
        full_label.to_edge(UP)

        comet_orbit_words = OldTexText("Halley's comet orbit")
        comet_orbit_words.set_color(GREY_B)
        comet_orbit_words.move_to(earth_orbit_words, RIGHT)

        orbiting_earth = Orbiting(earth, sun, earth_orbit)
        orbiting_comet = Orbiting(comet, sun, comet_orbit)

        self.add(full_label, earth_orbit_words)
        self.add(sun, earth_orbit, orbiting_earth)
        self.wait(10)
        orbiting_earth.rate = 1.5
        orbiting_comet.rate = 1.5
        self.play(
            earth_parts.set_height,
            comet_orbit.get_height() / 4.53,
            earth_parts.shift, 3 * RIGHT
        )
        comet_orbit.shift(3 * RIGHT)
        comet_orbit.save_state()
        Transform(comet_orbit, earth_orbit).update(1)
        self.play(
            Restore(comet_orbit, run_time=2),
            ChangingDecimal(
                eccentricity_label,
                lambda a: self.get_eccentricity(comet_orbit)
            ),
            FadeOut(earth_orbit_words, UP),
            FadeInFromDown(comet_orbit_words)
        )
        self.add(orbiting_comet)
        self.wait(10)
