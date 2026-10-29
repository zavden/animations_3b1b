# ==============================================================================
# Scene:      ParalaxMeasurmentFromEarth
# Source:     videos/_2025/cosmic_distance/paralax.py (lines 164-570)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/cosmic_distance/planets.py
#
# Run from this folder:
#     manimgl ParalaxMeasurmentFromEarth.py ParalaxMeasurmentFromEarth -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#   - Uses MoonTexture/DarkMoonTexture derived from MoonTextureMap.png (the originals are private to Grant).
#   - Uses a procedural starry sky instead of NASA's Hipparcos-Tycho map (hiptyc_2020_8k) and placeholder constellation figures.
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#   - MoonTexture.jpg and DarkMoonTexture.jpg (derived from the lib's real lunar map MoonTextureMap.png; the dark one is the same map dimmed)
#   - hiptyc_2020_8k.jpg (procedural 8192x4096 starry sky with a Milky Way band) and constellation_figures.png (constellation figures between bright stars)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/cosmic_distance/planets.py -----

EARTH_TILT_ANGLE = 23.3 * DEG


# All in Kilometers
EARTH_RADIUS = 6_371


MOON_RADIUS = 1_737.4


MOON_ORBIT_RADIUS = 384_400


SUN_RADIUS = 695_700


MERCURY_ORBIT_RADIUS = 6.805e7


VENUS_ORBIT_RADIUS = 1.082e8


EARTH_ORBIT_RADIUS = 1.473e8


MARS_ORBIT_RADIUS = 2.280e8


JUPITER_ORBIT_RADIUS = 7.613e8


SATURN_ORBIT_RADIUS = 1.439e9


# In days
MERCURY_ORBIT_PERIOD = 87.97


VENUS_ORBIT_PERIOD = 224.7


EARTH_ORBIT_PERIOD = 365.25


MARS_ORBIT_PERIOD = 686.98


JUPITER_ORBIT_PERIOD = 4332.82


SATURN_ORBIT_PERIOD = 10755.7


def get_earth(radius=1.0, day_texture="EarthTextureMap", night_texture="NightEarthTextureMap"):
    sphere = Sphere(radius=radius)
    earth = TexturedSurface(sphere, day_texture, night_texture)
    return earth


def get_moon(radius=1.0, resolution=(101, 51)):
    moon = TexturedSurface(Sphere(radius=radius, resolution=resolution), "MoonTexture", "DarkMoonTexture")
    moon.set_shading(0.25, 0.25, 1)
    return moon


def get_sun(
    radius=1.0,
    near_glow_ratio=2.0,
    near_glow_factor=2,
    big_glow_ratio=4,
    big_glow_factor=1,
    big_glow_opacity=0.35,
):
    sun = TexturedSurface(Sphere(radius=radius), "SunTexture")
    sun.set_shading(0, 0, 0)
    sun.to_edge(LEFT)

    # Glows
    near_glow = GlowDot(radius=near_glow_ratio * radius, glow_factor=near_glow_factor)
    near_glow.move_to(sun)

    big_glow = GlowDot(radius=big_glow_ratio * radius, glow_factor=big_glow_factor, opacity=big_glow_opacity)
    big_glow.move_to(sun)

    return Group(sun, near_glow, big_glow)


def get_celestial_sphere(radius=1000, constellation_opacity=0.1):
    sphere = Group(
        TexturedSurface(Sphere(radius=radius, clockwise=True), "hiptyc_2020_8k"),
        TexturedSurface(Sphere(radius=0.99 * radius, clockwise=True), "constellation_figures"),
    )
    sphere.set_shading(0, 0, 0)
    sphere[1].set_opacity(constellation_opacity)

    sphere.rotate(EARTH_TILT_ANGLE, RIGHT)

    return sphere



# ----- From _2025/cosmic_distance/paralax.py -----

class ParalaxMeasurmentFromEarth(InteractiveScene):
    def construct(self):
        # Add earth
        self.camera.light_source.move_to(500 * RIGHT)

        radius = 3
        earth = Circle(radius=radius)
        earth.set_fill(BLUE_B, 0.5)
        earth.set_stroke(WHITE, 3)
        earth.to_edge(LEFT)
        earth_back = earth.copy()
        earth_back.set_fill(BLACK, 1).set_stroke(width=0)

        earth_pattern = SVGMobject("earth")
        earth_pattern.replace(earth)
        earth_pattern.set_fill(Color(hsl=(0.23, 0.5, 0.2)), 1)

        self.add(earth_back, earth, earth_pattern)

        # Add two observers
        pi_height = 0.25
        randy, morty = pis = VGroup(
            Randolph(height=2, mode="hesitant").look_at(10 * RIGHT),
            Mortimer(height=2, mode="pondering").look_at(10 * RIGHT),
        )
        angles = [45 * DEG, -55 * DEG]
        labels = VGroup(
            Text("Observer 1", font_size=36),
            Text("Observer 2", font_size=36),
        )
        pis.arrange(DOWN, buff=1.0)
        pis.move_to(3 * RIGHT)

        obs_points = []
        obs_dots = Group()

        for pi, label, angle in zip(pis, labels, angles):
            label.next_to(pi, DOWN, SMALL_BUFF)
            target_point = earth.pfp((angle / TAU) % 1)

            pi.target = pi.generate_target()
            pi.target.set_height(pi_height)
            pi.target.next_to(target_point, UP, buff=0)
            pi.target.rotate(angle - 90 * DEG, about_point=target_point)

            label.target = label.generate_target()
            label.target.scale(0.5)
            # label.target.next_to(pi.target, rotate_vector(RIGHT, angle), buff=SMALL_BUFF)
            label.target.next_to(pi.target, UP * np.sign(angle), buff=SMALL_BUFF, aligned_edge=LEFT)

            obs_dots.add(TrueDot(target_point, color=pi.get_color()).make_3d())
            obs_points.append(target_point)

        self.play(
            LaggedStartMap(FadeIn, pis, shift=0.5 * UP, lag_ratio=0.5),
            LaggedStartMap(FadeIn, labels, shift=0.25 * UP, lag_ratio=0.5),

        )
        self.play(LaggedStartMap(Blink, pis, lag_ratio=0.25))
        self.play(
            LaggedStartMap(MoveToTarget, pis, lag_ratio=0.7),
            LaggedStartMap(MoveToTarget, labels, lag_ratio=0.7),
            FadeIn(obs_dots, time_span=(0.75, 1.25)),
        )
        self.wait()

        # Show lines to object
        frame = self.frame
        obj = GlowDot(12 * RIGHT, color=TEAL)

        obs_lines = VGroup(
            DashedLine(obs_points[0], obj.get_center()),
            DashedLine(obs_points[1], obj.get_center()),
        )
        obs_lines.set_stroke(WHITE, 2)

        self.play(
            frame.animate.set_width(20, about_edge=LEFT),
            *map(ShowCreation, obs_lines),
            FadeIn(obj),
            run_time=2
        )
        self.wait()

        # Analogy with eyeballs
        eyes = Randolph().eyes
        eyes.set_height(1)
        eyes.set_z_index(-1)

        def look_at(eye, object, midpoint):
            direction = normalize(object.get_center() - midpoint)
            eye.pupil.move_to(midpoint + 0.8 * eye.pupil.get_width() * direction)

        for eye, point, angle in zip(eyes, obs_points, angles):
            eye.next_to(ORIGIN, UP, buff=-0.35)
            eye.rotate(angle - 90 * DEG, about_point=ORIGIN)
            eye.shift(point)
            eye.point = point
            eye.add_updater(lambda m: look_at(m, obj, m.point))

        for line, dot in zip(obs_lines, obs_dots):
            line.dot = dot
            line.add_updater(lambda m: m.put_start_and_end_on(m.dot.get_center(), obj.get_center()))

        self.play(
            FadeIn(eyes),
            FadeOut(pis),
            FadeOut(labels),
        )

        obj.save_state()
        for vect in [6 * LEFT, 4 * UP, 4 * DOWN + 20 * RIGHT]:
            self.play(obj.animate.shift(vect), run_time=3)
        self.play(Restore(obj, run_time=3))
        self.play(
            FadeOut(eyes),
            FadeIn(pis),
            FadeIn(labels),
        )

        # Add stars
        conversion_factor = radius / EARTH_RADIUS
        celestial_sphere = get_celestial_sphere(radius=JUPITER_ORBIT_RADIUS * conversion_factor, constellation_opacity=0.0)
        celestial_sphere.set_z_index(-2)
        low_obs_group = VGroup(obs_lines[1], pis[1], labels[1])
        low_obs_group.save_state()
        frame.save_state()
        self.play(
            FadeIn(celestial_sphere),
            low_obs_group.animate.fade(0.75),
            frame.animate.set_height(20, about_edge=LEFT).shift(2 * RIGHT),
        )

        # Show moving observer
        self.play(
            Rotate(Group(pis[0], obs_dots[0]), angles[1] - angles[0], about_point=earth.get_center()),
            MaintainPositionRelativeTo(labels[0], pis[0]),
            run_time=8,
            rate_func=there_and_back,
        )
        self.play(
            Restore(low_obs_group),
            Restore(frame),
        )

        # Show line between
        line_between = Line(*obs_points)
        line_between.set_stroke(YELLOW, 3)
        brace_between = LineBrace(line_between, DOWN)

        self.play(
            ShowCreation(line_between),
            earth.animate.set_fill(opacity=0.35).set_stroke(width=2, opacity=1),
            earth_pattern.animate.set_fill(opacity=0.75),
        )
        self.wait()
        self.play(GrowFromCenter(brace_between))
        self.wait()
        self.play(FadeOut(brace_between))
        self.wait()

        # Move dot around
        self.play(low_obs_group.animate.fade(0.9))
        self.play(obj.animate.shift(3 * UP), rate_func=wiggle, run_time=5)
        self.play(Restore(low_obs_group))

        # Add angle labels
        colors = [BLUE, RED]
        angle_labels = self.get_angle_labels(obs_lines, obs_points, line_between, arc_props=[0.75, 0.5], colors=colors)

        for angle_label in angle_labels:
            self.play(Write(angle_label))
            self.wait()

        # Show remaining angle
        tip_arc = Arc(
            obs_lines[0].get_angle() + PI,
            obs_lines[1].get_angle() - obs_lines[0].get_angle(),
            arc_center=obj.get_center(),
            radius=1
        )
        tip_arc_label = Tex(
            R"180^\circ - \alpha - \beta",
            t2c={R"\alpha": colors[0], R"\beta": colors[1]}
        )
        tip_arc_label.next_to(tip_arc, LEFT, MED_SMALL_BUFF)

        self.play(LaggedStart(
            ShowCreation(tip_arc),
            FadeTransform(angle_labels[0][1].copy(), tip_arc_label[R"\alpha"][0]),
            FadeTransform(angle_labels[1][1].copy(), tip_arc_label[R"\beta"][0]),
            Write(tip_arc_label[R"180^\circ"]),
            Write(tip_arc_label[R"-"]),
            run_time=2
        ))
        self.wait()

        # Emphasize one distance
        obs1_brace = LineBrace(obs_lines[0])

        self.play(GrowFromCenter(brace_between))
        self.wait()
        self.play(Transform(brace_between, obs1_brace))
        self.wait()
        self.play(FadeOut(brace_between))

        # Replace with true earth
        frame.set_field_of_view(20 * DEG)
        true_earth = get_earth(radius=radius)
        true_earth.move_to(earth)
        true_earth.set_z_index(-1)
        true_earth.rotate(90 * DEG, LEFT)
        true_earth.rotate(140 * DEG, UP)
        true_earth.rotate(-EARTH_TILT_ANGLE, OUT)

        new_obs_lines = VGroup(
            Line(ol.get_start(), ol.get_end())
            for ol in obs_lines
        )
        new_obs_lines.match_style(obs_lines)

        self.play(
            FadeIn(true_earth),
            FadeOut(earth_back),
            FadeOut(earth),
            FadeOut(earth_pattern),
            FadeOut(tip_arc_label),
            FadeOut(tip_arc),
            FadeOut(obs_lines),
            FadeIn(new_obs_lines),
        )
        self.wait()

        obs_lines = new_obs_lines

        # Drag point very far away, show orbitss
        self.set_floor_plane("xz")

        for line, dot in zip(obs_lines, obs_dots):
            line.dot = dot
            line.add_updater(lambda m: m.put_start_and_end_on(m.dot.get_center(), obj.get_center()))

        angle_labels.add_updater(
            lambda m: m.become(
                self.get_angle_labels(
                    obs_lines,
                    obs_points=[obs_dots[0].get_center(), obs_dots[1].get_center()],
                    line_between=line_between,
                    arc_props=[0.75, 0.5]
                )
            )
        )

        moon_orbit = Circle(radius=MOON_ORBIT_RADIUS * conversion_factor)
        moon_orbit.set_stroke(GREY_B, width=(0, 3))
        moon_orbit.move_to(earth)
        moon_orbit.rotate(90 * DEG, LEFT)
        moon = get_moon(radius=conversion_factor * MOON_RADIUS)
        moon.move_to(moon_orbit.get_right())

        frame.add_updater(lambda m, dt: m.set_phi(interpolate(m.get_phi(), -90 * DEG, 0.025 * dt)))

        self.add(moon_orbit, moon)
        self.play(
            obj.animate.move_to(moon),
            frame.animate.set_height(1.5 * moon_orbit.get_width()).move_to(moon_orbit.get_right()).set_field_of_view(35 * DEG),
            FadeIn(moon_orbit),
            run_time=5
        )
        self.wait(5)

        # Show Venus
        sun = get_sun(SUN_RADIUS * conversion_factor, big_glow_ratio=20)
        sun.move_to(earth.get_center() + EARTH_ORBIT_RADIUS * conversion_factor * RIGHT)

        earth_orbit = Circle(radius=EARTH_ORBIT_RADIUS * conversion_factor)
        venus_orbit = Circle(radius=VENUS_ORBIT_RADIUS * conversion_factor)
        for orbit, color in zip([earth_orbit, venus_orbit], [BLUE, TEAL]):
            orbit.rotate(PI)
            orbit.set_stroke(color, width=(0, 3))
            orbit.move_to(sun)
            orbit.rotate(90 * DEG, LEFT)

        self.add(sun)
        self.play(
            frame.animate.set_height(0.4 * earth_orbit.get_width()).move_to(interpolate(venus_orbit.get_left(), sun.get_center(), 0.25)),
            FadeIn(earth_orbit, time_span=(2, 4)),
            FadeIn(venus_orbit, time_span=(2, 4)),
            obj.animate.move_to(venus_orbit.get_left()),
            run_time=8,
        )
        self.wait(4)
        frame.save_state()

        # Zoom back in
        frame.clear_updaters()
        if False:
            # This is for the transition to transit of Venus scene
            frame.clear_updaters()
            obs_lines.apply_depth_test()
            self.remove(line_between, angle_labels, pis, labels)
            # self.remove(obs_lines[1])
            self.play(
                frame.animate.reorient(-62, -2, 0, (4.64, 1.98, 2.86), 15.80),
                FadeOut(moon_orbit, time_span=(3, 4)),
                FadeOut(moon, time_span=(3, 4)),
                FadeOut(earth_orbit, time_span=(3, 4)),
                run_time=5,
                rate_func=lambda t: smooth(rush_from(t)),
            )
            self.play(frame.animate.reorient(0, 0, 0, (5.93, 0.25, 0.0), 15.86), run_time=5)
            self.wait()

            self.play(obs_dots[0].animate.move_to(obs_dots[1]), run_time=2)
            self.wait()

        self.play(
            frame.animate.reorient(0, 1, 0, (3.02, 0.82, -0.03), 15.80),
            FadeOut(moon_orbit, time_span=(3, 4)),
            FadeOut(moon, time_span=(3, 4)),
            FadeOut(earth_orbit, time_span=(3, 4)),
            run_time=4,
        )
        self.wait()
        self.add(angle_labels, obs_lines)
        self.play(
            Rotate(Group(pis[0], obs_dots[0]), 90 * DEG - angles[0], about_point=earth.get_center()),
            Rotate(Group(pis[1], obs_dots[1]), -90 * DEG - angles[1], about_point=earth.get_center()),
            MaintainPositionRelativeTo(labels[0], pis[0]),
            MaintainPositionRelativeTo(labels[1], pis[1]),
            UpdateFromFunc(line_between, lambda m: m.put_start_and_end_on(obs_dots[0].get_center(), obs_dots[1].get_center())),
            run_time=3
        )
        self.wait()

        # Slow zoom out
        self.play(
            frame.animate.reorient(-33, -9, 0, (20739.48, 3596.8, 5435.71), 33171.78),
            FadeIn(earth_orbit, time_span=(10, 12)),
            run_time=30,
            rate_func=lambda t: smooth(smooth(t))
        )

        # Zoom out to more of the solar system
        # frame.restore()

        new_orbits = VGroup(
            Circle(radius=r * conversion_factor)
            for r in [MERCURY_ORBIT_RADIUS, MARS_ORBIT_RADIUS, JUPITER_ORBIT_RADIUS, SATURN_ORBIT_RADIUS]
        )

        for orbit, color in zip(new_orbits, [GREY_B, RED, ORANGE, GREY_BROWN]):
            orbit.set_stroke(color, (0, 3))
            orbit.rotate(random.random() * TAU)
            orbit.rotate(90 * DEG, LEFT)
            orbit.move_to(sun)

        all_orbits = VGroup(new_orbits[0], venus_orbit, earth_orbit, *new_orbits[1:])
        periods = [
            MERCURY_ORBIT_PERIOD,
            VENUS_ORBIT_PERIOD,
            EARTH_ORBIT_PERIOD,
            MARS_ORBIT_PERIOD,
            JUPITER_ORBIT_PERIOD,
            SATURN_ORBIT_PERIOD,
        ]
        for orbit, period in zip(all_orbits, periods):
            orbit.period = period
            orbit.clear_updaters()
            orbit.add_updater(lambda m, dt: m.rotate(20 * dt / m.period, axis=UP))

        self.play(
            FadeIn(new_orbits, time_span=(0, 3)),
            frame.animate.reorient(-29, -41, 0, ORIGIN, 753807.38),
            celestial_sphere.animate.set_width(20 * JUPITER_ORBIT_RADIUS * conversion_factor),
            run_time=20
        )

    def get_angle_labels(
        self,
        obs_lines,
        obs_points,
        line_between,
        arc_props=[0.5, 0.5],
        arc_radius=0.5,
        colors=[BLUE, RED],
        backstroke_width=4,
    ):
        arc_radius = 0.5
        angle_syms = Tex(R"\alpha \beta")
        angle_syms.set_backstroke(BLACK, backstroke_width)
        colors = [BLUE, RED]
        angle_labels = VGroup()
        for obs_line, obs_point, angle_sym, arc_prop, color in zip(obs_lines, obs_points, angle_syms, arc_props, colors):
            obs_angle = obs_line.get_angle()
            line_angle = line_between.get_angle() + (PI if obs_angle > 0 else 0)
            arc = Arc(obs_angle, line_angle - obs_angle, arc_center=obs_point, radius=arc_radius)
            arc.set_stroke(color, 3)

            angle_sym.next_to(arc.pfp(arc_prop), arc.pfp(arc_prop) - obs_point)
            angle_sym.set_fill(color, border_width=1)

            angle_labels.add(VGroup(arc, angle_sym))

        angle_labels.set_stroke(behind=True)

        return angle_labels
