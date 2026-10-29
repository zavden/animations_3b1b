# ==============================================================================
# Scene:      NearbyStars
# Source:     videos/_2025/cosmic_distance/paralax.py (lines 625-917)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/cosmic_distance/planets.py
#
# Run from this folder:
#     manimgl NearbyStars.py NearbyStars -w -m --fps 15
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


# ----- From _2025/cosmic_distance/planets.py -----

EARTH_TILT_ANGLE = 23.3 * DEG


# All in Kilometers
EARTH_RADIUS = 6_371


SUN_RADIUS = 695_700


EARTH_ORBIT_RADIUS = 1.473e8


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

class NearbyStars(InteractiveScene):
    def construct(self):
        # Add sun and earth
        orbit_radius = 3.5
        conversion_factor = orbit_radius / EARTH_ORBIT_RADIUS

        sun = get_sun(radius=conversion_factor * SUN_RADIUS, big_glow_ratio=20)
        sun.center()
        orbit = Circle(radius=orbit_radius)
        orbit.set_stroke(BLUE, (0, 4))
        earth_glow = GlowDot(color=BLUE)
        earth_glow.f_always.move_to(orbit.get_start)

        celestial_sphere = get_celestial_sphere(constellation_opacity=0)
        celestial_sphere[0].set_opacity(1)

        self.add(celestial_sphere, sun, orbit, earth_glow)

        # Show the astronomical unit
        dist_line = Line()
        dist_line.set_stroke(WHITE, 1)
        dist_line.f_always.put_start_and_end_on(sun.get_center, orbit.get_start)

        dist_label = Text("Astronomical\nUnit", font_size=36)
        dist_label.f_always.move_to(
            lambda: dist_line.get_center() + 0.5 * normalize(rotate_vector(dist_line.get_vector(), 90 * DEG))
        )

        self.play(
            FadeIn(dist_line, time_span=(0, 1)),
            FadeIn(dist_label, time_span=(0, 1)),
            Rotate(orbit, TAU, about_point=ORIGIN, rate_func=linear, run_time=10),
        )
        self.wait()

        # Transition to initials
        dist_label.clear_updaters()
        au_label = Text("A.U.", font_size=36)

        def update_au_label(label):
            point = dist_line.get_center()
            direction = normalize(rotate_vector(point, 90 * DEG))
            step = 0.65 * interpolate(label.get_width(), label.get_height(), abs(direction[1]))
            label.move_to(point + step * direction)

        au_label.add_updater(update_au_label)

        self.play(LaggedStart(
            *(
                ReplacementTransform(dist_label[t2][0], au_label[t1][i])
                for t1, t2, i in zip("A.U.", ["A", "stronomical", "U", "nit"], [0, 0, 0, 1])
            ),
            lag_ratio=0.2
        ))
        self.add(au_label)

        # Position to the side
        frame = self.frame
        self.play(
            Rotate(orbit, 90 * DEG),
            frame.animate.reorient(0, 0, 0, 7 * RIGHT, 14),
            run_time=2
        )

        # Zoom into and out of earth real quick
        frame.save_state()
        earth = get_earth(radius=orbit_radius * (EARTH_RADIUS / EARTH_ORBIT_RADIUS))
        earth.move_to(earth_glow)
        earth.rotate(EARTH_TILT_ANGLE, RIGHT)
        frame.move_to(earth)
        frame.set_height(2 * earth.get_height())
        frame.reorient(-74, 79, 0)
        self.camera.light_source.move_to(sun)

        self.remove(earth_glow, orbit, dist_line)
        self.add(earth)
        self.wait()
        srf = squish_rate_func(smooth, 0.7, 1)
        self.play(
            UpdateFromAlphaFunc(frame, lambda m, a: m.reorient(
                *interpolate(np.array([-74, 79, 0]), np.zeros(3), a),
                interpolate(earth.get_center(), 7 * RIGHT, srf(a)),
                np.exp(interpolate(np.log(2 * earth.get_height()), np.log(14), smooth(a))),
            ), run_time=5),
            FadeIn(earth_glow, time_span=(2.5, 4.5)),
            FadeIn(orbit, time_span=(1, 4)),
            FadeIn(dist_line, time_span=(1, 4)),
            FadeIn(au_label, time_span=(4, 5)),
            FadeOut(earth),
            run_time=5,
        )

        # Show observations
        star = Group(
            ImageMobject('StarFourPoints').set_height(0.8).center(),
            GlowDot(color=WHITE).center()
        )
        star[1].add_updater(lambda m: m.set_width(0.4 * ((1 + math.sin(1.5 * self.time)))))
        star.move_to(50 * RIGHT)
        obs_points = Group(
            TrueDot(point, radius=0.1).set_color(GREEN).make_3d()
            for point in [orbit.get_top(), orbit.get_bottom()]
        )
        obs_lines = VGroup(
            self.get_obs_line(obs_point, star)
            for obs_point in obs_points
        )
        obs_lines.set_stroke(WHITE, 2)
        for line, point in zip(obs_lines, obs_points):
            line.start_point = point
            line.star = star
            line.add_updater(lambda m: m.put_start_and_end_on(m.start_point.get_center(), m.star.get_center()))

        obs_labels = VGroup(Text(f"Observation {n}") for n in [1, 2])
        for label, point, vect in zip(obs_labels, obs_points, [UP, DOWN]):
            label.next_to(point, vect, MED_SMALL_BUFF)

        self.add(star)

        self.play(
            ShowCreation(obs_lines[0], suspend_mobject_updating=True),
            FadeIn(obs_labels[0], 0.25 * UP),
            FadeIn(obs_points[0]),
        )
        self.wait()
        self.play(Rotate(orbit, PI), run_time=2)
        self.play(
            ShowCreation(obs_lines[1], suspend_mobject_updating=True),
            FadeIn(obs_labels[1], DOWN),
            FadeIn(obs_points[1]),
        )
        self.wait()

        # Show the angle vary during the orbit
        self.play(
            star.animate.move_to(15 * RIGHT),
            run_time=2
        )
        self.wait()

        obs_lines.suspend_updating()
        sample_obs_line = self.get_obs_line(earth_glow, star)
        self.play(
            FadeIn(sample_obs_line),
            obs_lines.animate.set_stroke(opacity=0.1)
        )
        self.play(Rotate(orbit, PI, run_time=10))
        self.wait()
        self.play(
            FadeOut(sample_obs_line),
            obs_lines.animate.set_stroke(opacity=1),
        )

        # Pull it far away, then back
        curr_center = star.get_center()
        curr_angle = obs_lines[1].get_angle() - obs_lines[0].get_angle()
        orbit_radius / math.tan(curr_angle / 2)

        obs_lines.resume_updating()
        self.play(
            UpdateFromAlphaFunc(star, lambda m, a: m.move_to(
                RIGHT * orbit_radius / math.tan(interpolate(curr_angle, 1e-5, there_and_back_with_pause(a)) / 2)
            )),
            run_time=6,
        )

        # Label the distance and angle
        line_to_star = Line(sun.get_center(), star.get_center())
        line_to_star.set_stroke(RED, 3)
        dist_label = Tex("D", font_size=60)
        dist_label.next_to(line_to_star, UP, buff=2 * SMALL_BUFF)
        dist_label.match_color(line_to_star)

        arc = Arc(PI, -curr_angle / 2, arc_center=star.get_center(), radius=3)
        arc_label = Tex(R"\theta / 2", font_size=60)
        arc_label.next_to(arc, LEFT, buff=SMALL_BUFF)

        self.play(
            ShowCreation(line_to_star),
            obs_lines.animate.set_stroke(width=1),
            FadeIn(dist_label, RIGHT),
        )
        self.wait()
        self.play(
            ShowCreation(arc),
            Write(arc_label),
        )
        self.play(FlashAround(arc_label, run_time=2))
        self.wait()
        self.play(
            Transform(obs_lines[0].copy().clear_updaters(), obs_lines[1].copy(), remover=True),
            run_time=2
        )
        self.wait()

        # Write the tangent equation
        kw = dict(
            t2c={R"\text{A.U.}": BLUE, "D": RED},
            font_size=72
        )
        eq1, eq2 = equations = VGroup(
            Tex(R"\tan\left(\theta / 2\right) = {\text{A.U.} \over D}", **kw),
            Tex(R"\theta = 2 \cdot \tan^{-1}\left({\text{A.U.} \over D}\right)", **kw),
        )
        equations.arrange(DOWN, buff=LARGE_BUFF)
        equations.next_to(frame.get_top(), DOWN, buff=-0.5)
        equations.align_to(dist_label, LEFT)

        self.play(LaggedStart(
            frame.animate.shift(UP),
            Write(eq1[R"\tan\left("]),
            FadeTransform(arc_label.copy(), eq1[R"\theta / 2"][0]),
            Write(eq1[R"\right) = "]),
            FadeTransform(au_label.copy().clear_updaters(), eq1["A.U."][0]),
            Write(eq1[R"\over"]),
            FadeTransform(dist_label.copy(), eq1["D"][0]),
            lag_ratio=0.25,
            run_time=3
        ))
        self.wait()
        self.play(TransformMatchingTex(eq1.copy(), eq2, path_arc=90 * DEG, run_time=2))
        self.wait()

        # Throw in Proxima Centauri numbers
        ac_labels = VGroup(
            Text(text, font_size=60, t2c={"D": RED, "A.U.": BLUE})
            for text in ["Proxima Centauri", "D = 40.17 trillion km", "D = 268,553 A.U."]
        )
        for label in ac_labels:
            label.add_background_rectangle()
        ac_labels.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        ac_labels.next_to(star, DOWN, aligned_edge=LEFT, buff=0).shift(0.5 * LEFT)
        ac_labels[2][0].set_opacity(0)

        for label in ac_labels:
            self.play(Write(label), frame.animate.set_x(8.5), run_time=2)
            self.wait()

        # Plug it in
        shift_value = 2 * LEFT + 2 * UP
        rhs = Tex(R"= 2 \cdot \tan^{-1}\left(1 \over 268{,}553 \right)", font_size=72)
        rhs.next_to(eq2, RIGHT)
        rhs.shift(shift_value)

        answer = Tex(R"=0.000413^\circ", font_size=72)
        answer.next_to(rhs, RIGHT)

        answer_in_arc_seconds = Tex(R"\approx 1.5 \text{ arc-seconds}", font_size=72)
        answer_in_arc_seconds.next_to(answer, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        for tex in [answer, answer_in_arc_seconds]:
            tex.add_background_rectangle()

        self.play(LaggedStart(
            equations.animate.shift(shift_value),
            frame.animate.move_to(11 * RIGHT + 3 * UP).set_height(16),
            *(
                TransformFromCopy(eq2[tex][0], rhs[tex][0])
                for tex in [R"2 \cdot \tan^{-1}\left(", R"\right)"]
            ),
            FadeIn(rhs[R"1 \over"]),
            FadeIn(rhs[R"="]),
            FadeTransform(ac_labels[2]["268,553"].copy(), rhs["268{,}553"].copy()),
            run_time=2,
            lag_ratio=0.1,
        ))
        self.wait()
        self.play(Write(answer))
        self.wait()
        self.play(FadeIn(answer_in_arc_seconds, DOWN))
        self.wait()

        # Fade out and push star away
        self.play(LaggedStartMap(
            FadeOut,
            VGroup(line_to_star, dist_label, arc, arc_label, *ac_labels),
            shift=0.1 * DOWN,
            lag_ratio=0.25
        ))

        obs_lines.resume_updating()
        self.play(
            star.animate.move_to(1000 * RIGHT),
            rate_func=lambda t: t**4,
            run_time=5
        )

    def get_obs_line(self, obj1, obj2, dash_length=0.1, stroke_color=WHITE, stroke_width=2):
        # line = DashedLine(obj1.get_center(), obj2.get_center())
        line = Line(obj1.get_center(), obj2.get_center())
        line.set_stroke(stroke_color, stroke_width)
        line.f_always.put_start_and_end_on(obj1.get_center, obj2.get_center)
        return line
