# ==============================================================================
# Scene:      ShowCreationOfAllOrbits
# Source:     videos/_2025/cosmic_distance/planets.py (lines 2652-2784)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowCreationOfAllOrbits.py ShowCreationOfAllOrbits -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#   - Uses a procedural starry sky instead of NASA's Hipparcos-Tycho map (hiptyc_2020_8k) and placeholder constellation figures.
#   - Uses placeholder Mars textures.
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#   - hiptyc_2020_8k.jpg (procedural 8192x4096 starry sky with a Milky Way band) and constellation_figures.png (constellation figures between bright stars)
#   - MarsTexture.jpg and DarkMarsTexture.jpg (procedural reddish Mars)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *

EARTH_TILT_ANGLE = 23.3 * DEG


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


def get_planet(name, radius=1.0):
    planet = TexturedSurface(Sphere(radius=radius), f"{name}Texture", f"Dark{name}Texture")
    planet.set_shading(0.25, 0.25, 1)
    return planet


def get_celestial_sphere(radius=1000, constellation_opacity=0.1):
    sphere = Group(
        TexturedSurface(Sphere(radius=radius, clockwise=True), "hiptyc_2020_8k"),
        TexturedSurface(Sphere(radius=0.99 * radius, clockwise=True), "constellation_figures"),
    )
    sphere.set_shading(0, 0, 0)
    sphere[1].set_opacity(constellation_opacity)

    sphere.rotate(EARTH_TILT_ANGLE, RIGHT)

    return sphere


class KeplersMethod(InteractiveScene):
    def construct(self):
        # Add earth, mars
        frame = self.frame
        frame.set_field_of_view(45 * DEG)
        light_source = self.camera.light_source
        light_source.move_to(ORIGIN)

        orbit_scale_factor = 2.5 / EARTH_ORBIT_RADIUS

        sun = get_sun(radius=0.025, big_glow_ratio=20)
        sun.center()
        earth_orbit = Circle(radius=EARTH_ORBIT_RADIUS * orbit_scale_factor)
        earth_orbit.set_stroke(BLUE, 1)
        earth_orbit.stretch(1.03, 0)

        mars_orbit = Circle(radius=MARS_ORBIT_RADIUS * orbit_scale_factor)
        mars_orbit.set_stroke(RED, 1)
        mars_orbit.stretch(1.03, 0).rotate(50 * DEG)

        earth = get_earth(radius=0.01)
        earth.move_to(earth_orbit.get_start())
        earth_glow = GlowDot(color=BLUE, radius=0.25)
        earth_glow.always.move_to(earth)

        mars = get_planet("Mars", radius=0.01)
        mars_glow = GlowDot(color=RED, radius=0.1)
        mars_glow.always.move_to(mars)
        mars.move_to(mars_orbit.get_start())

        self.add(sun)
        self.add(earth)
        self.add(mars)
        self.add(mars_glow)

        # Add celestial sphere
        celestial_sphere = get_celestial_sphere()
        celestial_sphere.set_z_index(-2)
        celestial_sphere.rotate(170 * DEG)
        self.add(celestial_sphere)

        # Zoom out from earth observing mars, adding an arrow to it
        frame.move_to(earth)
        frame.set_height(6 * earth.get_height())
        frame.reorient(-9, 86, 0)

        line_to_mars = self.get_line_between_bodies(earth, mars, RED)
        line_to_mars.set_z_index(-1)

        symbols = Tex(R"\earth \mars", additional_preamble=R"\usepackage{wasysym}",)
        symbols.scale(0.75)
        earth_symbol, mars_symbol = symbols
        earth_symbol.always.next_to(earth, RIGHT, SMALL_BUFF, aligned_edge=DOWN)
        mars_symbol.always.next_to(mars, UR, buff=0.05)

        self.play(
            frame.animate.to_default_state().set_anim_args(time_span=(1.5, 6)),
            ShowCreation(line_to_mars, suspend_mobject_updating=True),
            mars.animate.scale(5),
            mars_glow.animate.scale(3),
            earth.animate.scale(5).set_anim_args(time_span=(4, 6)),
            FadeIn(earth_glow, time_span=(4, 5)),
            FadeIn(symbols, time_span=(4, 5)),
            run_time=6
        )
        self.wait()

        # Move around the earth and mars
        self.play(
            Rotate(earth, TAU, about_point=earth.get_center() + 0.4 * DOWN),
            MaintainPositionRelativeTo(mars, earth),
            frame.animate.set_height(9),
            run_time=4
        )
        self.play(
            mars.animate.move_to(interpolate(mars.get_center(), earth.get_center(), 0.5)),
            run_time=4,
            rate_func=wiggle,
        )

        # Show the direction the sun
        line_to_sun = self.get_line_between_bodies(earth, sun, YELLOW)
        line_to_sun.set_stroke(width=1)

        self.play(
            ShowCreation(line_to_sun, suspend_mobject_updating=True, run_time=2),
            line_to_mars.animate.set_stroke(width=1)
        )
        self.wait()
        self.play(
            Rotate(earth, TAU, about_point=sun.get_center()),
            Rotate(mars, (EARTH_ORBIT_PERIOD / MARS_ORBIT_PERIOD) * TAU, about_point=sun.get_center()),
            run_time=10
        )

        # Unsure of the distance to the sun
        sun_earth_group = Group(sun[0], earth)
        brace = Brace(Line(sun.get_center(), earth.get_center()), UP)
        q_marks = brace.get_tex("???", buff=SMALL_BUFF)

        brace.f_always.set_width(lambda: get_dist(sun.get_center(), earth.get_center()))
        brace.always.next_to(sun.get_center(), UP, SMALL_BUFF, aligned_edge=LEFT)
        q_marks.always.next_to(brace, UP, SMALL_BUFF)

        self.play(LaggedStart(
            GrowFromPoint(brace, sun.get_center(), suspend_mobject_updating=True),
            FadeIn(q_marks, shift=0.25 * DOWN, suspend_mobject_updating=True),
        ))
        self.play(
            earth.animate.shift(0.5 * LEFT),
            MaintainPositionRelativeTo(mars, earth),
            rate_func=lambda t: wiggle(t, 6),
            run_time=8
        )
        brace.set_fill(border_width=0)
        self.play(FadeOut(brace, suspend_mobject_updating=True), FadeOut(q_marks))

        # Reference both orbits we want to know
        angle = 1.6 * TAU

        earth_annulus = self.get_mystery_orbit(earth_orbit)
        mars_annulus = self.get_mystery_orbit(mars_orbit)

        self.play(
            Rotate(earth, angle, about_point=sun.get_center()),
            Rotate(mars, (EARTH_ORBIT_PERIOD / MARS_ORBIT_PERIOD) * angle, about_point=sun.get_center()),
            FadeIn(earth_annulus, time_span=(3, 5)),
            FadeIn(mars_annulus, time_span=(4, 6)),
            run_time=12
        )

        # Clear the board
        self.play(
            FadeOut(earth_annulus),
            FadeOut(mars_annulus),
            celestial_sphere[0].animate.set_opacity(0.5),
            celestial_sphere[1].animate.set_opacity(0),
        )

        # Fix mars in space
        pin = SVGMobject("push_pin")
        pin.set_height(0.75)
        pin.rotate(40 * DEG, UP)
        pin.set_fill(GREY_E, 1)
        pin.set_shading(0.5, 0.25, 0)
        pin.rotate(10 * DEG)
        pin.move_to(mars.get_center(), DR)

        earth_orbit.set_shape(5.2, 5.0)
        earth_orbit.move_to(0.5 * math.sqrt(earth_orbit.get_width()**2 - earth_orbit.get_height()**2) * LEFT)
        earth_orbit.rotate(angle_of_vector(earth.get_center()) - angle_of_vector(earth_orbit.get_start()), about_point=ORIGIN)
        dens_func = bezier([0, 0.2, 0.8, 1])
        n_samples = 24
        sample_points = [earth_orbit.pfp(dens_func(a)) for a in np.arange(0, 1, 1 / n_samples)]
        earth.move_to(sample_points[0])

        self.play(
            FadeIn(pin, shift=0.5 * DR, rate_func=rush_into),
        )
        self.wait()

        # Show several lines deducing where earth is
        self.remove(line_to_sun, line_to_mars)

        ghost_lines = VGroup()
        ghost_earths = Group()
        self.add(ghost_earths)
        for sample_point in sample_points:
            self.play(
                earth.animate.move_to(sample_point),
                ghost_lines.animate.set_stroke(opacity=0.2),
                run_time=0.5
            )
            new_lines = self.show_earth_location_with_intersection(earth, mars, sun)
            ghost_lines.add(new_lines)
            ghost_earths.add(earth_glow.copy().clear_updaters())

        # Move around fixed mars, see implied ghost locations
        self.play(ghost_lines.animate.set_stroke(opacity=0.2))
        earth.add_updater(lambda m: m.move_to(ghost_earths[-1]))
        pin.add_updater(lambda m: m.move_to(mars.get_center(), DR))
        self.bind_ghost_lines_to_mars(ghost_lines, ghost_earths, mars)

        self.play(
            # Rotate(mars, TAU, about_point=mars.get_center() + 0.2 * LEFT, run_time=5),
            mars.animate.scale(1.2, about_point=ORIGIN),
            rate_func=wiggle,
            run_time=5
        )
        earth.clear_updaters()

        # Unfix mars
        ghost_earths.clear_updaters()
        self.play(
            FadeOut(pin, UL),
            FadeOut(ghost_earths, lag_ratio=0.1, run_time=1),
            FadeOut(ghost_lines, lag_ratio=0.1, run_time=1),
            Rotate(mars, TAU, about_point=sun.get_center(), run_time=8)
        )
        self.wait()

        # Show samples after 5 martian years
        ghost_lines, ghost_earths = self.show_time_series_measurments(earth, mars, sun, earth_glow, 5, 4)
        self.bind_ghost_lines_to_mars(ghost_lines, ghost_earths, mars)

        self.play(*map(FadeOut, [earth, earth_glow, earth_symbol]))
        self.play(Rotate(mars, 5 * DEG, about_point=ORIGIN, run_time=5, rate_func=wiggle))
        self.play(mars.animate.shift(LEFT), run_time=5, rate_func=wiggle)

        earth.move_to(ghost_earths[0])
        mars_copy = mars_glow.copy()
        mars_copy.clear_updaters()
        mars_copy.set_color(PINK)
        self.play(
            FadeOut(ghost_lines),
            ghost_earths.animate.set_color(GREEN),
            FadeIn(mars_copy)
        )

        self.play(
            Rotate(mars, 5 * DEG, about_point=sun.get_center()),
            Rotate(earth, (MARS_ORBIT_PERIOD / EARTH_ORBIT_PERIOD) * 5 * DEG, about_point=sun.get_center()),
            FadeIn(earth_glow),
        )
        self.wait()
        og_ghost_earths = ghost_earths

        # Find a new sample
        ghost_lines, ghost_earths = self.show_time_series_measurments(earth, mars, sun, earth_glow, 5, 2)
        self.bind_ghost_lines_to_mars(ghost_lines, ghost_earths, mars)
        self.play(FadeOut(earth), FadeOut(earth_glow))

        self.play(Rotate(mars, 5 * DEG, about_point=ORIGIN, run_time=5, rate_func=wiggle))
        self.play(mars.animate.shift(LEFT), run_time=5, rate_func=wiggle)

        self.play(*map(FadeOut, [
            ghost_lines, ghost_earths, og_ghost_earths,
            earth_glow, mars_copy,
        ]))

        # Show clusters of five
        step = (MARS_ORBIT_PERIOD / EARTH_ORBIT_PERIOD)
        clusters = Group()
        mars_line_groups = Group()

        last_cluster = Group()
        last_mars_lines = VGroup()
        for n in range(30):
            initial_mars_spot = mars.get_center().copy()
            mars.rotate(5 * DEG, about_point=ORIGIN)

            start = n * (5 / 360)
            alphas = (start + np.arange(5) * step) % 1
            points = [earth_orbit.pfp(dens_func(a)) for a in alphas]
            cluster = Group(GlowDot(point).set_color(BLUE) for point in points)
            mars_lines = VGroup(Line(mars.get_center(), dot.get_center(), buff=0) for dot in cluster)
            mars_lines.set_stroke(RED, 1)
            clusters.add(cluster)

            # Animation
            cluster.set_color(WHITE)
            rigid_group = Group(mars, mars_glow, mars_lines, cluster)
            rigid_group.save_state()
            rigid_group.scale(np.random.uniform(0.9, 1.1), about_point=ORIGIN)
            rigid_group.rotate(np.random.uniform(0, 2 * DEG), about_point=ORIGIN)

            new_mars_spot = mars.get_center().copy()
            mars.move_to(initial_mars_spot)

            self.play(
                FadeOut(last_mars_lines),
                mars.animate.move_to(new_mars_spot)
            )
            self.play(
                ShowIncreasingSubsets(cluster),
                ShowIncreasingSubsets(mars_lines),
                *(dot.animate.set_color(BLUE).set_radius(0.15) for dot in last_cluster)
            )
            self.play(Restore(rigid_group))
            last_cluster = cluster
            last_mars_lines = mars_lines

        earth.move_to(earth_orbit.get_start())
        self.play(
            FadeOut(last_mars_lines),
            FadeOut(last_cluster),
            FadeOut(clusters),
            FadeIn(earth),
            FadeIn(earth_glow),
            FadeIn(earth_symbol),
            ShowCreation(earth_orbit),
        )

        # Show the deduction of Mars' orbit
        mars.set_x(4.8)
        earth_location_tracker = ValueTracker(0)
        earth.add_updater(lambda m: m.move_to(earth_orbit.pfp(dens_func(earth_location_tracker.get_value() % 1))))
        earth_glow.update()
        mars_lines = VGroup()
        earth_copies = Group()
        self.add(mars_lines, earth_copies)
        for n in range(5):
            earth_copy = earth_glow.copy()
            earth_copy.clear_updaters()
            earth_copy.orbit_offset = earth_location_tracker.get_value()
            mars_line = self.get_line_between_bodies(earth_copy, mars, RED, 1, 2)
            mars_line.set_stroke(opacity=0.7)
            mars_line.suspend_updating()

            self.play(
                ShowCreation(mars_line),
                FadeIn(earth_copy)
            )
            mars_lines.add(mars_line)
            earth_copies.add(earth_copy)
            if n == 0:
                self.play(
                    mars.animate.move_to(mars_line.pfp(0.75)).set_anim_args(rate_func=wiggle),
                    frame.animate.set_height(10),
                    run_time=4,
                )
                self.play(
                    mars.animate.set_opacity(0),
                    mars_glow.animate.set_opacity(0),
                    mars_symbol.animate.set_opacity(0),
                )
            if n < 4:
                self.play(
                    Rotate(mars, TAU, about_point=sun.get_center()),
                    earth_location_tracker.animate.increment_value(MARS_ORBIT_PERIOD / EARTH_ORBIT_PERIOD),
                    run_time=2,
                )
            else:
                self.play(
                    mars.animate.set_opacity(1),
                    mars_glow.animate.set_opacity(1),
                    mars_symbol.animate.set_opacity(1),
                )

        # Shift forward a bunch
        self.play(*map(FadeOut, [earth, earth_symbol, earth_glow]))
        earth_location_tracker.set_value(0)
        for dot, mars_line in zip(earth_copies, mars_lines):
            dot.add_updater(lambda m: m.move_to(earth_orbit.pfp(dens_func((earth_location_tracker.get_value() + m.orbit_offset) % 1))))
            mars_line.resume_updating()

        mars_copies = Group()
        self.add(earth_copies, mars_copies)
        for n in range(100):
            d_alpha = 0.01
            mars_copy = mars_glow.copy()
            mars_copy.clear_updaters()
            mars_copy.scale(0.25)
            mars_copies.add(mars_copy)
            mars.rotate(d_alpha * (EARTH_ORBIT_PERIOD / MARS_ORBIT_PERIOD) * TAU, about_point=0.5 * UR)
            earth_location_tracker.increment_value(d_alpha)
            self.wait(0.2)

    def get_line_between_bodies(self, body1, body2, color, stroke_width=2, scale_factor=10):
        line = Line()
        line.set_stroke(color, stroke_width)
        line.f_always.put_start_and_end_on(body1.get_center, body2.get_center)
        line.add_updater(lambda m: m.scale(scale_factor, about_point=m.get_start()))
        return line

    def get_mystery_orbit(self, orbit, opacity=0.25, n_q_marks=12):
        annulus = Annulus(0.9 * orbit.get_radius(), 1.1 * orbit.get_radius())
        annulus.set_fill(orbit.get_color(), opacity=opacity)
        q_marks = VGroup(Tex("?").move_to(orbit.pfp(a)) for a in np.arange(0, 1, 1 / n_q_marks))
        q_marks.set_fill(opacity=0.25)
        return VGroup(annulus, q_marks)

    def show_time_series_measurments(self, earth, mars, sun, earth_glow, n_measurements=5, rotation_time=2):
        ghost_lines = VGroup()
        ghost_earths = Group()
        corner_counter = VGroup(
            Integer(687, include_sign=True, edge_to_fix=RIGHT),
            Text("Days")
        )
        corner_counter.arrange(RIGHT, aligned_edge=UP)
        corner_counter.to_corner(UL, buff=0)

        self.add(ghost_lines)
        self.add(ghost_earths)
        for n in range(n_measurements):
            new_lines = self.show_earth_location_with_intersection(earth, mars, sun)
            ghost_lines.add(new_lines)
            ghost_earths.add(earth_glow.copy().clear_updaters())
            if n < n_measurements - 1:
                corner_counter[0].set_value(0)
                self.add(corner_counter)
                self.play(
                    Rotate(mars, TAU, about_point=sun.get_center()),
                    Rotate(earth, (MARS_ORBIT_PERIOD / EARTH_ORBIT_PERIOD) * TAU, about_point=sun.get_center()),
                    ChangeDecimalToValue(corner_counter[0], 687),
                    ghost_lines.animate.set_stroke(opacity=0.2).set_anim_args(time_span=(0, 1)),
                    run_time=rotation_time
                )
            else:
                self.play(
                    ghost_lines.animate.set_stroke(opacity=0.2),
                    FadeOut(corner_counter)
                )

        return ghost_lines, ghost_earths

    def show_earth_location_with_intersection(self, earth, mars, sun):
        lines = VGroup(
            self.get_line_between_bodies(mars, earth, RED, 1, 2),
            self.get_line_between_bodies(sun, earth, YELLOW, 1, 2),
        )
        lines.clear_updaters()
        lines.set_stroke(width=1)
        self.play(ShowCreation(lines, lag_ratio=0))
        return lines

    def bind_ghost_lines_to_mars(self, ghost_lines, ghost_earths, mars):
        sun_point = ghost_lines[0][1].get_start()
        for pair, dot in zip(ghost_lines, ghost_earths):
            mars_line, sun_line = pair
            mars_line.add_updater(lambda m: m.shift(mars.get_center() - m.get_start()))

            dot.sun_line = sun_line
            dot.mars_line = mars_line
            dot.add_updater(lambda m: m.move_to(find_intersection(
                m.sun_line.get_start(), m.sun_line.get_vector(),
                m.mars_line.get_start(), m.mars_line.get_vector(),
            )))

    def get_rigid_lines_from_mars(self, mars, ghost_earths):
        mars_lines = VGroup(
            self.get_line_between_bodies(mars, dot, RED, 1, 1)
            for dot in ghost_earths
        )
        mars_lines.clear_updaters()
        mars_lines.set_stroke(opacity=0.5)
        return mars_lines


class ShowCreationOfAllOrbits(KeplersMethod):
    def construct(self):
        # Add all orbits (Copied largely from NearestPlanets)
        frame = self.frame
        sun = get_sun(radius=0.02, big_glow_ratio=20).center()
        celestial_sphere = get_celestial_sphere(constellation_opacity=0.01)

        self.add(celestial_sphere)
        self.add(sun)

        # Add orbits
        radius_conversion = 2.0 / EARTH_ORBIT_RADIUS
        seconds_per_day = MERCURY_ORBIT_PERIOD

        radii = radius_conversion * np.array([
            MERCURY_ORBIT_RADIUS,
            VENUS_ORBIT_RADIUS,
            EARTH_ORBIT_RADIUS,
            MARS_ORBIT_RADIUS,
            JUPITER_ORBIT_RADIUS,
            SATURN_ORBIT_RADIUS,
        ])
        periods = [
            MERCURY_ORBIT_PERIOD,
            VENUS_ORBIT_PERIOD,
            EARTH_ORBIT_PERIOD,
            MARS_ORBIT_PERIOD,
            JUPITER_ORBIT_PERIOD,
            SATURN_ORBIT_PERIOD,
        ]
        eccentricities = [
            0.206,
            0,
            0.017,
            0.093,
            0.048,
            0.056
        ]
        colors = [GREY_C, TEAL, BLUE, RED, ORANGE, GREY_BROWN]

        orbits = VGroup()
        for radius, period, color, ecc in zip(radii, periods, colors, eccentricities):
            orbit = Circle(radius=radius)
            orbit.set_stroke(color, width=2)
            orbit.stretch(math.sqrt(1 - ecc**2), 1)
            orbit.shift(0.5 * radius * ecc * RIGHT)
            orbit.rotate(random.random() * TAU, about_point=ORIGIN)
            orbit.set_anti_alias_width(5)
            orbit.period = period
            orbits.add(orbit)

        # Add planet dots
        symbol_texs = [R"\mercury", R"\venus", R"\earth", R"\mars", R"\jupiter", R"\saturn"]
        symbols = Tex(
            "".join(symbol_texs),
            additional_preamble=R"\usepackage{wasysym}",
            font_size=32
        )
        planet_dots = Group()
        symbols[-2:].scale(3)
        for orbit, symbol in zip(orbits, symbols):
            dot = GlowDot(color=orbit.get_color())
            dot.move_to(orbit.get_start())
            orbit.dot = dot
            orbit.symbol = symbol
            symbol.buff_factor = (orbit.get_radius() + 0.6 * symbol.get_height()) / orbit.get_radius()
            symbol.dot = dot
            symbol.add_updater(lambda m: m.move_to(m.buff_factor * m.dot.get_center()))
            planet_dots.add(dot)

        # Draw the orbits
        earth_orbit = orbits[2]
        earth_orbit.set_stroke(width=1)

        frame.set_phi(70 * DEG)
        frame.add_updater(lambda m, dt: m.set_phi(m.get_phi() * (1 - 0.03 * dt)))
        frame.set_height(3)
        growth_rate_tracker = ValueTracker(0.1)
        frame.add_updater(lambda m, dt: m.set_height(m.get_height() + growth_rate_tracker.get_value() * dt))

        self.add(earth_orbit)
        self.draw_orbit(earth_orbit, orbits[3], MARS_ORBIT_PERIOD, 5)
        self.draw_orbit(earth_orbit, orbits[0], MERCURY_ORBIT_PERIOD, 7)
        self.draw_orbit(earth_orbit, orbits[1], VENUS_ORBIT_PERIOD, 6)
        self.draw_orbit(
            earth_orbit, orbits[4], JUPITER_ORBIT_PERIOD, 2, run_time=10,
            added_anims=[frame.animate.set_height(18)],
        )
        growth_rate_tracker.set_value(0.4)
        self.play(FadeIn(orbits[5]))

        # Just linger
        self.wait(9)

    def draw_orbit(self, earth_orbit, orbit, period, n_samples=3, run_time=4, added_anims=[]):
        orbit.set_stroke(width=2)
        earth_year_tracker = ValueTracker()
        get_earth_time = earth_year_tracker.get_value

        def get_earth_orbit_point(offset):
            return earth_orbit.pfp((offset + earth_year_tracker.get_value()) % 1)

        earth_dots = Group()
        lines = VGroup()
        for n in range(n_samples):
            dot = GlowDot(color=earth_orbit.get_color(), radius=0.1)
            dot.offset = n * (period / EARTH_ORBIT_PERIOD)
            dot.add_updater(lambda m: m.move_to(get_earth_orbit_point(m.offset)))
            earth_dots.add(dot)

            line = self.get_line_between_bodies(dot, orbit.dot, orbit.get_color(), 1, 1.1)
            lines.add(line),

        self.play(
            FadeIn(earth_dots),
            ShowCreation(lines, lag_ratio=0.1, suspend_mobject_updating=True),
            FadeIn(orbit.dot),
            FadeIn(orbit.symbol),
        )
        self.play(
            ShowCreation(orbit),
            UpdateFromFunc(orbit.dot, lambda m: m.move_to(orbit.get_end())),
            earth_year_tracker.animate.set_value(period / EARTH_ORBIT_PERIOD),
            *added_anims,
            run_time=run_time,
        )
        self.play(
            FadeOut(lines),
            FadeOut(earth_dots),
            FadeOut(orbit.dot),
            FadeOut(orbit.symbol),
            orbit.animate.set_stroke(width=1)
        )
