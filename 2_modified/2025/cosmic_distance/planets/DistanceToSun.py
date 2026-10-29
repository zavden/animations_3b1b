# ==============================================================================
# Scene:      DistanceToSun
# Source:     videos/_2025/cosmic_distance/planets.py (lines 1123-1701)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DistanceToSun.py DistanceToSun -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#   - Uses MoonTexture/DarkMoonTexture derived from MoonTextureMap.png (the originals are private to Grant).
#   - Removed the line moon.target.data['d_normal_point'] = ...: that field no longer exists in this manimgl.
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#   - MoonTexture.jpg and DarkMoonTexture.jpg (derived from the lib's real lunar map MoonTextureMap.png; the dark one is the same map dimmed)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *

EARTH_TILT_ANGLE = 23.3 * DEG


# All in Kilometers
EARTH_RADIUS = 6_371


MOON_ORBIT_RADIUS = 384_400


SUN_RADIUS = 695_700


EARTH_ORBIT_RADIUS = 1.473e8


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


class DistanceToSun(InteractiveScene):
    def construct(self):
        # Show sun and the earth
        frame = self.frame
        frame.set_field_of_view(15 * DEG)
        light_source = self.camera.light_source

        earth = get_earth(radius=0.1)
        earth.rotate(90 * DEG)
        earth.rotate(-EARTH_TILT_ANGLE, UP)
        earth.to_edge(LEFT, buff=1.0)

        sun = get_sun(radius=1.0)
        sun.move_to((0.5 * FRAME_WIDTH - 2) * RIGHT)
        sun.rotate(90 * DEG, LEFT)

        light_source.f_always.move_to(sun[0].get_center)
        self.add(light_source)

        self.add(earth, sun)
        frame.reorient(0, 0, 0, earth.get_center(), 2 * earth.get_height())
        self.play(frame.animate.to_default_state(), run_time=5)

        # Show distance and radius
        sun_brace = Brace(sun[0], RIGHT)
        sun_brace.stretch(0.5, 1, about_edge=UP)
        sun_brace.move_to(sun.get_center(), DL).shift(SMALL_BUFF * RIGHT)
        sun_radius_label = sun_brace.get_tex("R_S", buff=0.05)
        VGroup(sun_brace, sun_radius_label).set_color(BLACK)

        dist_line = Line(earth.get_center(), sun.get_center())
        dist_line.insert_n_curves(10)
        dist_line.set_stroke(WHITE, width=(0, *5 * [2], 0))
        dist_label = Tex(R"D_S")
        dist_label.next_to(dist_line, UP, SMALL_BUFF)

        self.play(
            GrowFromCenter(sun_brace),
            Write(sun_radius_label),
        )
        self.wait()
        self.play(
            ShowCreation(dist_line),
            Write(dist_label),
        )
        self.wait()

        # Show ratio
        ratio = Tex(R"{R_S \over D_S}")
        ratio.to_corner(UL)
        ratio.set_color(YELLOW)

        self.play(
            TransformFromCopy(sun_radius_label, ratio["R_S"][0]),
            TransformFromCopy(dist_label, ratio["D_S"][0]),
            Write(ratio[R"\over"][0])
        )
        self.wait()

        # Zoom into the moon
        orbit_radius = 2
        orbit = Circle(radius=orbit_radius, n_components=100)
        orbit.move_to(earth)
        orbit.set_stroke(GREY, (0, 2))

        scaled_moon_radius = 0.5 * (sun[0].get_height() / get_dist(earth.get_center(), sun.get_center())) * orbit_radius
        small_moon_radius = (1.0 / 4) * earth.get_height()
        moon = get_moon(radius=small_moon_radius)
        moon.move_to(orbit.get_end())

        self.add(orbit, moon)
        self.play(
            FadeIn(orbit),
            FadeIn(moon),
            dist_line.animate.set_stroke(opacity=0),
            frame.animate.reorient(0, 0, 0, (-4.94, 0.05, 0.0), 1.83),
            run_time=4,
        )
        self.wait()

        # Show the moon sizes and ratio
        moon_brace = sun_brace.copy().set_color(WHITE)
        moon_brace.set_height(moon.get_height())
        moon_brace.next_to(moon, RIGHT, buff=0, aligned_edge=UP)
        moon_brace.stretch(0.5, 1, about_edge=UP)
        moon_radius_label = moon_brace.get_tex("R_M", font_size=8, buff=0.01)
        moon_radius_label.align_to(moon_brace, DOWN)

        moon_dist_line = Line(earth.get_center(), moon.get_center())
        moon_dist_line.insert_n_curves(20)
        moon_dist_line.set_stroke(TEAL_A, (0, 2, 2, 2, 0))
        moon_dist_label = Tex("D_M", font_size=8)
        moon_dist_label.next_to(moon_dist_line, UP, buff=0.01)

        moon_ratio = Tex(R"{R_M \over D_M}", font_size=10)
        moon_ratio.set_color(GREY_B)
        moon_ratio.next_to(frame.get_corner(UL), DR, buff=SMALL_BUFF)

        self.play(FadeIn(moon_ratio))
        self.play(
            GrowFromCenter(moon_brace),
            TransformFromCopy(moon_ratio["R_M"][0], moon_radius_label),
        )
        self.play(
            ShowCreation(moon_dist_line),
            TransformFromCopy(moon_ratio["D_M"][0], moon_dist_label),
        )
        self.wait()

        # Compare ratios
        equals = Tex("=")
        equals.next_to(ratio, RIGHT, 2 * SMALL_BUFF)

        sun_point = Point(sun.get_center())
        size_ratio = moon.get_height() / get_dist(moon.get_center(), earth.get_center())
        sun[0].add_updater(lambda m: m.move_to(sun_point).set_height(size_ratio * get_dist(sun_point.get_center(), earth.get_center())))
        sun[1].add_updater(lambda m: m.move_to(sun[0]).set_height(1.2 * sun[0].get_height()))
        sun[2].add_updater(lambda m: m.move_to(sun[0]))

        VGroup(sun_brace, sun_radius_label).set_color(WHITE)
        sun_brace.f_always.set_height(lambda: 0.5 * sun[0].get_height(), stretch=lambda: True)
        sun_brace.always.next_to(sun[0], RIGHT, buff=0, aligned_edge=UP)
        sun_radius_label.always.next_to(sun_brace, buff=0.05)

        self.remove(sun_brace, sun_radius_label, dist_line, dist_label, ratio)

        self.play(
            frame.animate.reorient(-87.85, 89.126, 0, [-5.6279674 ,-0.0808167, 0.00590339], 0.03),
            sun[2].animate.set_opacity(0.15),
            *map(FadeOut, [moon_ratio, moon_dist_line, moon_dist_label, moon_brace, moon_radius_label, orbit]),
            run_time=5,
        )
        self.wait()
        self.play(
            frame.animate.to_default_state(),
            FadeIn(orbit),
            run_time=3
        )

        VGroup(sun_radius_label, dist_label).set_color(YELLOW)
        self.play(
            GrowFromCenter(sun_brace),
            GrowFromCenter(sun_radius_label),
        )
        dist_line.set_stroke(opacity=1),
        self.play(
            FadeIn(dist_line),
            FadeIn(dist_label, shift=0.25 * UP),
        )
        self.wait()

        # Wiggle the orbit
        self.play(
            orbit.animate.stretch(0.8, 0).stretch(1.2, 1),
            UpdateFromFunc(Group(moon), lambda m: m.move_to(orbit.get_end())),
            rate_func=wiggle,
            run_time=4
        )
        self.wait()

        # Fade Out labels
        self.play(
            LaggedStartMap(
                FadeOut,
                VGroup(dist_line, dist_label, sun_brace, sun_radius_label),
                scale=0.5,
            ),
        )

        # Shift sun scale around
        sun.clear_updaters()
        to_moon = moon.get_center() - earth.get_center()
        true_sun_center = earth.get_center() + to_moon * (EARTH_ORBIT_RADIUS / MOON_ORBIT_RADIUS)
        true_sun_height = earth.get_height() * (SUN_RADIUS / EARTH_RADIUS)
        sun.save_state()
        sun.target = sun.generate_target()
        sun.target.scale(true_sun_height / sun[0].get_height())
        sun.target.move_to(true_sun_center)
        sun.target[1].set_radius(1.2 * true_sun_height)
        sun.target[2].set_radius(10 * true_sun_height)

        self.play(
            MoveToTarget(sun),
            frame.animate.reorient(0, 0, 0, (365.67, 14.24, 0.0), 485.35),
            run_time=5
        )

        sun.target[0].set_height(2 * moon.get_height())
        sun.target[1].set_height(1.2 * 2 * moon.get_height())
        sun.target[2].set_height(50 * 2 * moon.get_height())
        sun.target[2].set_opacity(0.35)
        sun.target.move_to(earth.get_center() + 2 * to_moon)

        self.play(
            MoveToTarget(sun, time_span=(0, 2)),
            frame.animate.reorient(0, 0, 0, (-3.89, 0.03, 0.0), 4.73),
            run_time=4
        )

        # Show being twice as big
        dist_brace = Brace(Line(earth.get_top(), moon.get_top()), UP, buff=0.1)
        dist_brace2 = dist_brace.copy().shift(dist_brace.get_width() * RIGHT)

        side_brace = Brace(moon, RIGHT, buff=0)
        side_brace.stretch(0.25, 0, about_edge=LEFT)
        side_brace_pair = side_brace.get_grid(2, 1, buff=0)
        side_brace_pair.next_to(sun[0], RIGHT, buff=0)

        self.play(GrowFromPoint(dist_brace, dist_brace.get_left()))
        self.play(TransformFromCopy(dist_brace, dist_brace2))

        self.play(GrowFromCenter(side_brace))
        self.play(TransformFromCopy(VGroup(side_brace), side_brace_pair))
        self.wait()

        self.play(LaggedStartMap(FadeOut, VGroup(dist_brace, dist_brace2, side_brace, side_brace_pair)))
        self.wait()

        # Show one moon orbit (with the intention of showing phases in the corner)
        orbit_group = Group(orbit, moon)

        self.play(Rotate(orbit_group, TAU, about_point=earth.get_center(), rate_func=linear, run_time=10))
        self.play(Rotate(orbit_group, TAU / 8, about_point=earth.get_center(), rate_func=linear, run_time=1.25))

        # Sun highlights half, we see half
        words1 = Text("Sun illuminates half")
        words2 = Text("We see half")
        sub_words = Text("(a different half)", font_size=36)

        words1.move_to(4 * RIGHT + 2 * UP)
        words2.move_to(4 * LEFT + 2 * DOWN)
        sub_words.next_to(words2, DOWN)

        arrow1 = Arrow(words1.get_bottom(), 0.75 * RIGHT, path_arc=-60 * DEG)
        arrow2 = Arrow(words2.get_top(), 0.75 * LEFT, path_arc=-60 * DEG)

        VGroup(words1, words2, sub_words, arrow1, arrow2).scale(0.6 / FRAME_HEIGHT, about_point=ORIGIN).shift(moon.get_center())
        VGroup(words2, sub_words, arrow2).set_color(BLUE_D)

        our_half = Sphere(radius=0.51 * moon.get_height())
        our_half.set_color(BLUE, 0.35)
        our_half.always_sort_to_camera(self.camera)
        our_half.rotate(90 * DEG, UP)
        our_half.rotate(45 * DEG)
        our_half.move_to(moon)
        our_half.pointwise_become_partial(our_half, 0, 0.5)

        self.play(
            frame.animate.reorient(0, 0, 0, moon.get_center(), 0.6),
            run_time=2
        )
        self.play(
            FadeIn(words1, lag_ratio=0.1),
            Write(arrow1),
        )
        self.wait()
        self.play(
            FadeIn(words2, lag_ratio=0.1),
            Write(arrow2),
            ShowCreation(our_half)
        )
        self.wait()
        self.play(FadeIn(sub_words, 0.03 * DOWN))
        self.play(
            FadeOut(VGroup(words1, arrow1, words2, arrow2, sub_words)),
            frame.animate.reorient(0, 0, 0, (-6.23, 0.02, 0.0), 4.73).set_anim_args(run_time=2),
        )

        # Transition to a different phase
        orbit_group.add(our_half)
        self.play(Rotate(orbit_group, TAU / 4, about_point=earth.get_center(), run_time=5))
        self.play(our_half.animate.set_opacity(0))

        # Flat moon
        moon.save_state()
        moon.target = moon.generate_target()
        moon.target.rotate(45 * DEG)
        moon.target.stretch(0.01, 0)
        moon.target.rotate(-45 * DEG)
        # CHANGE: this manimgl no longer has the d_normal_point field (normals are computed in the shader from the mesh); the
        # line that forced the moon's normal is removed.

        self.play(MoveToTarget(moon))
        self.play(
            frame.animate.reorient(3, 63, 0, (-6.08, 1.44, -0.78), 2.88),
            run_time=3
        )
        self.play(
            Rotate(orbit_group, -TAU / 4, about_point=earth.get_center(), run_time=8, rate_func=there_and_back),
        )
        self.play(
            Restore(moon, time_span=(0, 1)),
            frame.animate.reorient(0, 0, 0, (-4.8, 0, 0.0), 4.22),
            run_time=2
        )

        # Show full and new moons
        self.play(Rotate(orbit_group, TAU / 8, about_point=earth.get_center(), run_time=2))
        full_moon = moon.copy()
        full_moon_label = Text("Full moon", font_size=15)
        full_moon_label.next_to(full_moon, UR, buff=0.025)
        self.play(Write(full_moon_label))
        self.wait()

        self.add(full_moon)
        self.play(Rotate(orbit_group, TAU / 2, about_point=earth.get_center(), run_time=2))

        new_moon = moon.copy()
        new_moon_label = Text("New moon", font_size=15)
        new_moon_label.next_to(new_moon, UL, buff=0.025)
        self.play(Write(new_moon_label))
        self.wait()
        self.add(new_moon)

        # Ask about half moon
        question = Text("When is the\nhalf moon?", font_size=15)
        question.set_color(RED)
        question.always.next_to(moon, DL, buff=0.025)

        self.play(
            Rotate(orbit_group, 3 * TAU / 8, about_point=earth.get_center(), run_time=8),
            VFadeIn(question, time_span=(1, 3))
        )
        self.play(Rotate(orbit_group, -TAU / 8, about_point=earth.get_center(), run_time=8))
        self.wait()

        # Show incorrect right angle
        not_here = Text("Not here!", font_size=15)
        not_here.next_to(moon, DL, buff=0.05)
        not_here.set_color(RED)
        half_moon_label = Text("Half moon", font_size=15)

        def get_half_moon_angle():
            orbit_radius = orbit.get_width() / 2
            sun_dist = get_dist(sun[0].get_center(), earth.get_center())
            return math.acos(orbit_radius / sun_dist)

        def get_half_moon_point():
            theta = get_half_moon_angle()
            return earth.get_center() + rotate_vector(RIGHT, theta) * orbit.get_width() / 2

        half_moon_point = get_half_moon_point()

        lines1 = VGroup(
            Line(sun[0].get_center(), earth.get_center()),
            Line(earth.get_center(), orbit.get_top()),
        )
        lines2 = VGroup(
            Line(sun[0].get_center(), half_moon_point),
            Line(half_moon_point, earth.get_center())
        )
        VGroup(lines1, lines2).set_stroke(WHITE, 2)

        elbow1 = Elbow(width=0.15).shift(earth.get_center())
        elbow2 = Elbow(width=0.15, angle=get_half_moon_angle() - PI).shift(half_moon_point)

        self.play(
            FadeOut(question),
            FadeIn(not_here, scale=0.75),
            FadeIn(lines1),
            FadeIn(elbow1),
        )
        self.wait()
        self.play(
            ReplacementTransform(lines1, lines2, time_span=(2, 3)),
            ReplacementTransform(elbow1, elbow2, time_span=(2, 3)),
            Rotate(orbit_group, get_half_moon_angle() - 90 * DEG, about_point=earth.get_center()),
            FadeOut(not_here, time_span=(0, 1)),
            run_time=3
        )

        half_moon_label.always.next_to(moon, UR, buff=0.025)
        self.play(FadeIn(half_moon_label))
        self.wait()

        # Zoom in
        self.play(
            frame.animate.reorient(-30, 87, 0, (-5.02, 1.67, 0.0), 0.35),
            # elbow2.animate.scale(0.1, about_point=half_moon_point),
            FadeOut(lines2),
            FadeOut(elbow2),
            FadeOut(half_moon_label),
            run_time=3,
        )
        self.wait()
        self.play(
            frame.animate.reorient(3, 0, 0, (-5.02, 1.71, 0.01), 0.36),
            our_half.animate.set_opacity(0.35),
            run_time=2
        )
        self.wait()

        lit_half = our_half.copy().set_opacity(0)
        lit_half.shift(1e-2 * OUT)
        self.play(
            Transform(
                lit_half,
                lit_half.copy().rotate(90 * DEG, about_point=half_moon_point).set_color(YELLOW, 0.35),
                path_arc=90 * DEG,
            ),
            run_time=1
        )
        self.wait()
        self.play(
            FadeOut(lit_half),
            our_half.animate.set_opacity(0),
            FadeIn(half_moon_label),
            frame.animate.reorient(0, 0, 0, (-2.89, 0.13, 0.0), 6.83),
            FadeIn(elbow2),
            FadeIn(lines2),
            run_time=5,
        )

        # Move sun away
        def get_lunar_angle():
            return angle_of_vector(moon.get_center() - earth.get_center())

        def get_implied_sun_location():
            return earth.get_center() + RIGHT * (orbit.get_width() / 2) / math.cos(get_lunar_angle())

        sun.f_always.move_to(get_implied_sun_location)

        sun_line, moon_line = lines2
        orbit_group.add(moon_line, elbow2)

        sun_line.add_updater(lambda m: m.put_start_and_end_on(moon.get_center(), sun.get_center()))

        self.remove(lines2)
        self.add(orbit_group, sun_line)
        self.play(Rotate(orbit_group, 25 * DEG, about_point=earth.get_center()), run_time=5)
        self.play(Rotate(orbit_group, -35 * DEG, about_point=earth.get_center()), run_time=5)
        self.play(Rotate(orbit_group, 25 * DEG, about_point=earth.get_center()), run_time=10)

        # Add angle label
        v_line = DashedLine(earth.get_center(), earth.get_center() + orbit.get_width() * UP)
        v_line.set_stroke(WHITE, 1)

        def get_diff_arc(radius=0.75, color=WHITE, stroke_width=3):
            return Arc(
                90 * DEG,
                get_half_moon_angle() - 90 * DEG,
                radius=radius,
                arc_center=earth.get_center()
            ).set_stroke(color, stroke_width)

        arc = always_redraw(get_diff_arc)
        theta_label = Tex(R"\theta", font_size=24)
        theta_label.add_updater(lambda m: m.set_width(min(0.15, 0.5 * arc.get_width())))
        theta_label.add_updater(lambda m: m.next_to(arc.pfp(0.6), UP, SMALL_BUFF))

        self.play(
            ShowCreation(v_line),
            FadeIn(arc),
            FadeIn(theta_label),
        )
        self.wait()
        self.play(
            Rotate(orbit_group, 10 * DEG, about_point=earth.get_center()),
            run_time=8
        )

        # Equation
        dist_eq = Tex(R"D_S = {D_M \over \sin(\theta)}", t2c={"D_S": YELLOW, "D_M": GREY_B})
        dist_eq.to_edge(UP)
        dist_eq.fix_in_frame()

        dist_line = Line(earth.get_center(), sun[0].get_center())
        dist_line.set_stroke(YELLOW, 2)
        dist_label = Tex(R"D_S", font_size=72)
        dist_label.next_to(dist_line, DOWN)

        self.play(
            frame.animate.reorient(0, 0, 0, (4.7, 0.17, 0.0), 14.93),
            ShowCreation(dist_line, time_span=(3, 5)),
            FadeIn(dist_label, RIGHT, time_span=(3, 5)),
            FadeIn(dist_eq, time_span=(3, 5)),
            run_time=5
        )
        self.wait()

        # Zoom in on discrpency
        self.play(
            FadeOut(dist_eq, time_span=(0, 2)),
            frame.animate.reorient(0, 0, 0, (-6.0, 1.05, 0.0), 2.52),
            run_time=5,
        )

        # Comment on discrepency
        disc_arc = get_diff_arc(radius=orbit_radius, color=BLUE, stroke_width=5)
        est_words = Text("Aristarchus estimated\n6 hours", font_size=15)
        est_words.next_to(frame.get_corner(UL), DR, SMALL_BUFF)
        est_words.set_color(BLUE)

        question = Text("How much time\nis this?", font_size=15)
        question.move_to(est_words, UP)
        question.set_color(BLUE)

        arrow = Arrow(
            est_words["6 hours"].get_bottom() + 0.05 * DOWN,
            disc_arc.get_center(),
            buff=0.025,
            path_arc=90 * DEG,
            thickness=1.5
        )
        arrow.set_fill(BLUE)

        self.play(
            FadeIn(question),
            FadeIn(arrow),
            ShowCreation(disc_arc)
        )
        self.wait()
        self.play(
            FadeOut(question, 0.25 * UP),
            FadeIn(est_words, 0.25 * UP),
        )
        self.wait()

        # Show true answer
        true_answer = TexText(R"True answer: $\sim30$ minutes", font_size=15)
        true_answer.set_color(TEAL)
        true_answer.move_to(est_words, DL)

        self.play(
            FadeOut(est_words, 0.25 * LEFT, time_span=(1, 2)),
            FadeIn(true_answer, 0.25 * LEFT, time_span=(1.25, 2.25)),
            Rotate(orbit_group, 4 * DEG, about_point=earth.get_center()),
            UpdateFromAlphaFunc(disc_arc, lambda m, a: m.become(
                get_diff_arc(
                    radius=orbit_radius,
                    color=interpolate_color(BLUE, TEAL, a),
                    stroke_width=5
                )
            )),
            arrow.animate.set_color(TEAL).shift(0.05 * LEFT),
            run_time=3,
        )
        self.wait()

        # Show false distance to the Sun
        brace = Brace(Line(earth.get_bottom(), new_moon.get_bottom()), buff=0)
        brace_copies = brace.get_grid(1, 20, buff=0)
        brace_copies.move_to(brace, LEFT)

        v_line_copies = VGroup(
            v_line.copy().align_to(brace_copy, RIGHT)
            for brace_copy in brace_copies
        )
        v_line_copies.stretch(0.5, 1, about_edge=DOWN)

        self.play(
            FadeOut(true_answer),
            FadeOut(arrow),
            FadeOut(disc_arc),
            FadeOut(dist_line),
            FadeOut(dist_label),
            Rotate(orbit_group, 1 * DEG - math.asin(1 / 20), about_point=earth.get_center())
        )
        self.play(
            frame.animate.reorient(0, 0, 0, (13.31, -0.69, 0.0), 26.92),
            FadeIn(brace, time_span=(0, 1)),
            LaggedStart(
                (TransformFromCopy(brace, brace2, path_arc=45 * DEG)
                for brace2 in brace_copies),
                lag_ratio=0.1,
                time_span=(1, 5)
            ),
            LaggedStartMap(FadeIn, v_line_copies, lag_ratio=0.1, time_span=(1.5, 5)),
            sun[2].animate.set_radius(50).set_glow_factor(2),
            run_time=5,
        )
        self.wait()

        # True distance
        self.play(
            Rotate(orbit_group, math.asin(1 / 20) - math.asin(1 / 383), about_point=earth.get_center()),
            frame.animate.reorient(0, 0, 0, (364.45, -1.75, 0.0), 480.47),
            run_time=6
        )
        self.wait()
