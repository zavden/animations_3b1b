# ==============================================================================
# Scene:      HighlightEarthOrbit
# Source:     videos/_2025/cosmic_distance/planets.py (lines 2201-2202)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HighlightEarthOrbit.py HighlightEarthOrbit -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#   - Uses a procedural starry sky instead of NASA's Hipparcos-Tycho map (hiptyc_2020_8k) and placeholder constellation figures.
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#   - hiptyc_2020_8k.jpg (procedural 8192x4096 starry sky with a Milky Way band) and constellation_figures.png (constellation figures between bright stars)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *

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


class NearestPlanets(InteractiveScene):
    random_seed = 2
    highlighted_orbit = None
    linger = False

    def construct(self):
        # Frame
        frame = self.frame

        # Add sun
        sun = get_sun(radius=0.01, big_glow_ratio=20)
        sun.center()

        # Add celestial sphere
        celestial_sphere = TexturedSurface(Sphere(radius=200), "hiptyc_2020_8k")
        celestial_sphere.set_shading(0, 0, 0)
        celestial_sphere.set_opacity(0.75)
        self.add(celestial_sphere)
        self.add(sun)

        # Add orbits
        radius_conversion = 1.0 / EARTH_ORBIT_RADIUS
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
        colors = [GREY_C, TEAL, BLUE, RED, ORANGE, GREY_BROWN]

        orbits = VGroup()
        for radius, period, color in zip(radii, periods, colors):
            orbit = Circle(radius=radius)
            orbit.set_stroke(color, width=(0, 3 * radius**0.25))
            orbit.rotate(random.random() * TAU, about_point=ORIGIN)
            orbit.set_anti_alias_width(5)
            orbit.period = period
            orbit.add_updater(lambda m, dt: m.rotate(0.5 * (seconds_per_day / m.period) * TAU * dt))
            orbits.add(orbit)

        self.add(*orbits)

        # Add symbols
        symbol_texs = [R"\mercury", R"\venus", R"\earth", R"\mars", R"\jupiter", R"\saturn"]
        symbols = Tex(
            "".join(symbol_texs),
            additional_preamble=R"\usepackage{wasysym}",
            font_size=16
        )
        for symbol, orbit in zip(symbols, orbits):
            radius = orbit.get_width() / 2
            symbol.orbit = orbit
            symbol.scale(radius**0.5)
            buff = symbol.get_height()
            symbol.factor = (radius - buff) / radius
            symbol.add_updater(lambda m: m.move_to(m.orbit.get_start() * m.factor))

        symbols.update()
        self.add(*symbols)

        # Highlight
        if self.highlighted_orbit is not None:
            orbits.set_stroke(opacity=0.25)
            symbols.set_fill(opacity=0.25)
            orbits[self.highlighted_orbit].set_stroke(opacity=1)
            symbols[self.highlighted_orbit].set_fill(opacity=1)

        # Zoom out
        frame = self.frame

        frame.reorient(0, 56, 0, (-0.11, 0.08, -0.37), 2.76)
        self.play(
            frame.animate.reorient(0, 0, 0, ORIGIN, 15),
            run_time=30,
        )

        if self.linger:
            self.wait(30)

        # Ask about relative sizes
        braces = VGroup()
        for orbit, symbol_tex, angle in zip(orbits, symbol_texs, np.linspace(90 * DEG, 0, len(symbol_texs))):
            brace = Brace(Line(ORIGIN, orbit.get_width()**0.5 * RIGHT), UP, buff=0)
            brace.set_width(orbit.get_width() / 2, about_edge=LEFT)
            sym = Tex(Rf"R{symbol_tex}", additional_preamble=R"\usepackage{wasysym}", font_size=24)
            sym[1].scale(0.5)
            sym[1].next_to(sym[0].get_corner(DR), RIGHT, buff=0)
            sym.match_height(brace)
            sym.set_backstroke(BLACK, 5)
            sym.next_to(brace, UP, buff=0.05)
            brace.add(sym)
            brace.rotate(angle, RIGHT, about_edge=DOWN)
            braces.add(brace)
        braces.reverse_submobjects()

        main_brace = braces[0].copy()
        self.play(
            Succession(
                GrowFromCenter(main_brace),
                *(Transform(main_brace, b, rate_func=lambda t: smooth(clip(1.5 * t, 0, 1))) for b in braces[1:]),
            ),
            frame.animate.reorient(0, 61, 0, ORIGIN, 2.5).set_field_of_view(20 * DEG),
            run_time=6
        )
        self.wait()
        self.play(FadeOut(main_brace))

        # Prepare nested spheres
        spheres = Group(
            self.get_open_sphere(orbit.get_radius())
            for orbit in orbits
        )
        for sphere in spheres:
            sphere.clip_tracker.set_value(1.3)
            sphere[0].set_opacity(0.25)

        # Show platonic solids
        solids = self.get_platonic_solids()
        for solid in solids:
            solid.add_updater(lambda m, dt: m.rotate(10 * DEG * dt * math.cos(self.time), axis=OUT))

        box = SurroundingRectangle(solids)
        solids.next_to(
            rotate_vector(frame.get_corner(UL), frame.get_phi(), RIGHT),
            IN + RIGHT,
            buff=SMALL_BUFF
        )

        self.play(
            LaggedStartMap(FadeIn, solids, shift=0.25 * OUT, run_time=2, lag_ratio=0.25),
            FadeOut(symbols),
        )
        self.wait(3)

        # Show the nesting
        orbits.apply_depth_test()
        spheres.set_color(GREY_D, 1)
        spheres.set_shading(0.25, 0.25, 0.2)
        self.camera.light_source.move_to(20 * LEFT)

        octo, icos, dodec, tetra, cube = solids
        target_solids = self.get_platonic_solids()
        factors = [1.5, 1.15, 1.2, 2.0, 1.0]
        for target_solid, sphere, factor in zip(target_solids, spheres, factors):
            target_solid.set_width(factor * sphere.get_width())
            target_solid.shift(-target_solid.get_all_points().mean(0))
        target_solids[4].center()

        def drop_sphere(index, run_time=1.5):
            self.add(spheres[index])
            self.play(
                FadeIn(spheres[index], scale=0.7),
                run_time=run_time
            )
            self.add(solids[index:])

        self.add(spheres[0], solids[0])
        self.play(  # Octohedron
            FadeIn(spheres[0]),
            ReplacementTransform(solids[0], target_solids[0]),
            frame.animate.reorient(-8, 72, 0, (0.0, 0.0, 0.0), 2.50),
            run_time=2
        )
        drop_sphere(1, run_time=2)
        self.wait(2)
        self.play(  # Dodecahedron
            target_solids[0].animate.set_stroke(opacity=0.25),
            ReplacementTransform(solids[1], target_solids[1]),
            frame.animate.reorient(-2, 69, 0, ORIGIN, 2.92),
            solids[2:].animate.shift(LEFT + 0.1 * OUT),
            run_time=2
        )
        drop_sphere(2)
        self.play(  # Dodec
            target_solids[1].animate.set_stroke(opacity=0.25),
            ReplacementTransform(solids[2], target_solids[2]),
            frame.animate.reorient(-16, 69, 0, ORIGIN, 4),
            solids[3:].animate.shift(LEFT + 0.5 * OUT),
            run_time=2
        )
        drop_sphere(3)
        self.play(  # Tetra
            target_solids[2].animate.set_stroke(opacity=0.25),
            ReplacementTransform(solids[3], target_solids[3]),
            frame.animate.reorient(-31, 68, 0, ORIGIN, 9),
            solids[4:].animate.scale(5).shift(3 * LEFT + 2 * OUT),
            run_time=2
        )
        drop_sphere(4)
        self.play(  # Cube
            target_solids[3].animate.set_stroke(opacity=0.25),
            ReplacementTransform(solids[4], target_solids[4]),
            frame.animate.reorient(-9, 69, 0, ORIGIN, 15),
            run_time=2
        )
        drop_sphere(5)
        self.play(frame.animate.reorient(-19, 72, 0, ORIGIN, 20), run_time=3)

        # Ambient panning
        frame.clear_updaters()
        frame.add_ambient_rotation(3 * DEG)
        self.play(
            LaggedStart(*(sphere.clip_tracker.animate.set_value(0) for sphere in spheres[::-1]), lag_ratio=0.25, run_time=6)
        )
        last_solid = target_solids[-1]
        for solid in (*target_solids, *target_solids, *target_solids):
            self.play(
                solid.animate.set_stroke(WHITE, 2, 1),
                last_solid.animate.set_stroke(WHITE, 1, 0.25),
            )
            last_solid = solid

        # Show difficulty in making the theory fit
        frame.clear_updaters()
        orbits.suspend_updating()

        self.add(*spheres)
        self.play(*(
            mob.animate.scale(1.1).set_anim_args(rate_func=lambda t: wiggle(t, 5), time_span=(random.random(), 4 + random.random()))
            for mob in (*spheres, *orbits, *target_solids)
        ))

        # Trouble with orbits
        self.play(
            frame.animate.reorient(0, 0, 0, ORIGIN, 12),
            target_solids.animate.set_stroke(opacity=0.2),
            FadeOut(spheres),
            run_time=2
        )

        factors = np.random.uniform(0.8, 1.2, len(orbits))
        angles = np.random.uniform(0, TAU, len(orbits))
        self.play(
            *(
                orbit.animate.rotate(angle).stretch(factor, 0).stretch(1 / factor, 1).rotate(-angle).set_anim_args(
                    rate_func=lambda t: wiggle(t, 7),
                    time_span=(random.random(), 6 + random.random())
                )
                for orbit, factor, angle in zip(orbits, factors, angles)
            ),
            FadeOut(target_solids),
        )

        # Get rid of circles, add planets
        self.camera.light_source.move_to(ORIGIN)

        small_radius = 0.01
        planets = Group(
            Sphere(radius=small_radius * math.sqrt(orbit.get_radius()), color=orbit.get_color()).set_shading(0.25, 0.25, 1)
            for orbit in orbits
        )
        planets.replace_submobject(2, get_earth(radius=small_radius))
        for planet, orbit, symbol in zip(planets, orbits, symbols):
            planet.f_always.move_to(orbit.get_start)
            symbol.clear_updaters()
            symbol.always.next_to(planet, UR, buff=0.025)

        fading_orbits = orbits.copy()
        orbits.set_stroke(opacity=0)

        self.play(
            FadeOut(fading_orbits, shift=2 * LEFT, lag_ratio=0.2),
            FadeIn(planets),
            FadeIn(symbols),
            celestial_sphere.animate.set_opacity(0.25),
            frame.animate.set_height(4),
            run_time=3,
        )
        orbits.resume_updating()

        # Add observation lines
        lines = VGroup()
        non_earth_planets = [*planets[:2], *planets[3:]]
        for planet in non_earth_planets:
            # line = Line().set_stroke(colors[list(planets).index(planet)], 1)
            line = Line().set_stroke(planet.get_color(), 2, opacity=0.75)
            line.f_always.put_start_and_end_on(planets[2].get_center, planet.get_center)
            lines.add(line)
        lines.apply_depth_test()

        self.play(
            frame.animate.set_height(6).move_to(DOWN),
            FadeIn(lines, time_span=(0, 1)),
            run_time=12
        )

        # Change perspective
        orbits.suspend_updating()
        earth = planets[2]
        self.play(
            frame.animate.reorient(82, 87, 0, earth.get_center(), 0.05),
            FadeOut(symbols),
            *(planet.animate.scale(0.1) for planet in non_earth_planets),
            celestial_sphere.animate.set_opacity(1),
            run_time=3
        )
        self.wait()

    def get_open_sphere(self, radius, color=GREY_C, opacity=0.5):
        sphere = Sphere(radius=radius)
        sphere.set_color(color, opacity)
        sphere.always_sort_to_camera(self.camera)

        mesh = SurfaceMesh(sphere, normal_nudge=0, resolution=(51, 25))
        mesh.set_stroke(WHITE, 0.5, 0.1)
        mesh.set_anti_alias_width(1)
        mesh.deactivate_depth_test()

        result = Group(sphere, mesh)
        result.clip_tracker = ValueTracker(0)

        sphere.add_updater(lambda m: m.set_clip_plane(IN, result.clip_tracker.get_value() * radius))
        mesh.add_updater(lambda m: m.set_clip_plane(OUT, result.clip_tracker.get_value() * radius))

        return result

    def get_platonic_solids(self):
        # Platonic solid test
        dodec = Dodecahedron()
        cube = VCube()

        icos_verts = np.array([pent.get_vertices().mean(0) for pent in dodec])
        octo_verts = np.array([square.get_vertices().mean(0) for square in cube])
        tetra_verts = vertices = np.array([
            [0, 0, 1],
            [np.sqrt(8 / 9), 0, -1 / 3],
            [-np.sqrt(2 / 9), np.sqrt(2 / 3), -1 / 3],
            [-np.sqrt(2 / 9), -np.sqrt(2 / 3), -1 / 3],
        ])

        octo = self.wireframe_from_points(octo_verts, 4)
        icos = self.wireframe_from_points(icos_verts, 5)
        tetra = self.wireframe_from_points(tetra_verts, 3)

        solids = VGroup(octo, icos, dodec, tetra, cube)
        for solid in solids:
            solid.set_height(0.25)
            solid.set_stroke(WHITE, 1)
            solid.set_fill(opacity=0)
            solid.set_stroke(flat=False)
            solid.apply_depth_test()
        solids.arrange(RIGHT, buff=0.25)

        return solids

    def wireframe_from_points(self, points, n_neighbors):
        lines = VGroup()
        for point in points:
            norms = np.linalg.norm(points - point, axis=1)
            indices = np.argsort(norms)
            lines.add(*(
                Line(point, points[index])
                for index in indices[1:1 + n_neighbors]
            ))

        return lines


class HighlightEarthOrbit(NearestPlanets):
    highlighted_orbit = 2
