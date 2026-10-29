# ==============================================================================
# Scene:      SizeOfEarthRenewed
# Source:     videos/_2025/cosmic_distance/planets.py (lines 260-534)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SizeOfEarthRenewed.py SizeOfEarthRenewed -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed the line earth.data['d_normal_point'] = ...: that field no longer exists in this manimgl (normals come from the mesh in the shader).
# ==============================================================================

from manim_imports_ext import *

EARTH_TILT_ANGLE = 23.3 * DEG


def get_earth(radius=1.0, day_texture="EarthTextureMap", night_texture="NightEarthTextureMap"):
    sphere = Sphere(radius=radius)
    earth = TexturedSurface(sphere, day_texture, night_texture)
    return earth


def get_sphere_mesh(radius=1.0):
    sphere = Sphere(radius=radius)
    mesh = SurfaceMesh(sphere)
    mesh.set_stroke(WHITE, 0.5, 0.5)
    return mesh


class SizeOfEarthRenewed(InteractiveScene):
    radius = 3.0

    def construct(self):
        # Setup
        self.set_floor_plane("xz")
        frame = self.frame
        frame.set_field_of_view(15 * DEG)

        light = self.camera.light_source
        light.move_to(20 * RIGHT)

        # Add earth
        sphere = Sphere(radius=self.radius)
        earth = get_earth(radius=self.radius)
        mesh = get_sphere_mesh(radius=self.radius)
        mesh.rotate(-2 * DEG)
        transparent_earth = earth.copy()
        transparent_earth.set_opacity(0.25)

        inner_shell = sphere.copy()
        inner_shell.set_color(GREY_E)
        inner_shell.set_height(0.99 * 2 * self.radius)

        earth_group = Group(inner_shell, earth, mesh, transparent_earth)
        earth_group.rotate(90 * DEG, LEFT)

        slice_tracker = ValueTracker(self.radius + SMALL_BUFF)
        earth.add_updater(lambda m: m.set_clip_plane(OUT, slice_tracker.get_value()))
        inner_shell.add_updater(lambda m: m.set_clip_plane(OUT, slice_tracker.get_value()))
        mesh.add_updater(lambda m: m.set_clip_plane(IN, -slice_tracker.get_value()))
        transparent_earth.add_updater(lambda m: m.set_clip_plane(IN, -slice_tracker.get_value()))

        circle = Circle(radius=self.radius)

        earth_axis = rotate_vector(UP, -EARTH_TILT_ANGLE)

        axis_line = Line(DOWN, UP).set_height(8)
        axis_line.set_stroke(WHITE, 1)

        earth_group.rotate(147 * DEG, UP)
        earth_group.rotate(-EARTH_TILT_ANGLE, OUT)

        self.add(earth)

        # Unflatten earth
        earth.save_state()
        earth.stretch(1e-3, 0)
        # CHANGE: this manimgl no longer has the d_normal_point field (normals are computed in the shader from the mesh), so
        # forcing the flattened Earth's normal is no longer needed; the line is removed.

        frame.reorient(5, 0, -90, 2 * RIGHT)

        self.play(
            frame.animate.reorient(0, 0, -90, RIGHT),
            Restore(earth),
            run_time=3,
        )

        # Add rays from the sun
        sun = GlowDot(100 * RIGHT, radius=1)
        n_rays = 25
        rays = Line(LEFT, RIGHT).replicate(n_rays)
        rays.set_stroke(YELLOW, 1)

        def update_rays(rays):
            ys = np.linspace(earth.get_y(UP), earth.get_y(DOWN), len(rays))
            for ray, y in zip(rays, ys):
                ray.put_start_and_end_on(
                    sun.get_center(),
                    [math.sqrt(abs(self.radius**2 - y**2)), y, 0],
                )

        rays.add_updater(update_rays)
        rays.set_z_index(-1)

        self.play(
            FadeIn(rays, shift=0.5 * LEFT, lag_ratio=0.02),
            run_time=2
        )
        self.play(
            frame.animate.reorient(-67, -7, 0, (0.92, 2.13, 3.94), 20.25),
            sun.animate.move_to(50 * RIGHT),
            run_time=3,
        )
        self.play(
            sun.animate.move_to(1000 * RIGHT).set_anim_args(time_span=(0, 3)),
            frame.animate.reorient(-130, -14, 0, (2.66, 0.14, -0.69), 8.18).set_anim_args(time_span=(2, 7)),
            run_time=7,
        )

        # Show line through Syene
        center_dot = GlowDot(color=RED)
        slice_tracker.set_value(self.radius + SMALL_BUFF)
        angle = 7 * DEG

        h_line = Line(ORIGIN, 20 * RIGHT)
        h_line.set_stroke(YELLOW, 2)

        self.add(earth_group)
        self.play(
            slice_tracker.animate.set_value(0),
            FadeIn(center_dot, scale=0.25),
            run_time=2
        )
        self.play(
            ShowCreation(h_line, rate_func=rush_into, run_time=2),
            FadeOut(rays, run_time=2),
            frame.animate.reorient(-205, -11, 0, (3.0, -0.0, 0.0), 6.50).set_anim_args(run_time=10),
        )

        # Rotate the earth about a bit
        earth_group.save_state()
        self.play(Rotate(earth_group, 40 * DEG, axis=OUT, run_time=3))
        self.play(Rotate(earth_group, 40 * DEG, axis=UP, run_time=3, rate_func=there_and_back))
        self.play(Rotate(earth_group, -40 * DEG, axis=OUT, run_time=3))

        # Emphasize the tilt of the earth's axis
        axis_line = Line(-1.25 * self.radius * earth_axis, 1.25 * self.radius * earth_axis)
        axis_line.set_stroke(WHITE, 2)
        self.play(
            Rotate(earth_group, 2 * TAU, axis=earth_axis),
            FadeIn(axis_line, time_span=(0, 1)),
            FadeIn(rays, remover=True, time_span=(4, 15), rate_func=lambda t: there_and_back_with_pause(t, 9 / 11)),
            frame.animate.reorient(-91, -36, 0, (4.91, -1.44, 0.39), 11.01).set_anim_args(time_span=(4, 15), rate_func=lambda t: there_and_back_with_pause(t, 0.2)),
            run_time=15,
        )

        # Show tropic of cancer
        def get_lat_line(angle):
            result = Circle(radius=self.radius)
            result.rotate(90 * DEG, LEFT).rotate(EARTH_TILT_ANGLE, axis=IN)
            result.set_stroke(TEAL, 2)
            result.apply_depth_test()
            result.scale(math.cos(angle))
            result.shift(math.sin(angle) * earth_axis * self.radius)
            return result

        equator_label = Text("Equator")
        equator_label.flip().rotate(EARTH_TILT_ANGLE, IN)
        equator_label.move_to(self.radius * IN + 0.15 * earth_axis)
        equator_label.set_backstroke()

        cancer_label = Text("Tropic of Cancer")
        cancer_label.flip().rotate(EARTH_TILT_ANGLE, IN)
        cancer_label.move_to(op.add(
            math.cos(EARTH_TILT_ANGLE) * self.radius * IN,
            (math.sin(EARTH_TILT_ANGLE) * self.radius + 0.15) * earth_axis,
        ))

        tropic_of_cancer = get_lat_line(EARTH_TILT_ANGLE)

        d_line = h_line.copy().rotate(angle, about_point=ORIGIN)
        d_line.set_stroke(PINK)

        alex_point = earth.get_center() + self.radius * normalize(d_line.get_vector())
        alex_name = Text("Alexandria", font_size=36).flip()
        alex_name.next_to(alex_point, UR, buff=SMALL_BUFF).shift(0.45 * UP)
        alex_arrow = Arrow(alex_name.get_bottom() + 0.35 * LEFT, alex_point, buff=SMALL_BUFF, thickness=2)

        syene_point = earth.get_right()
        syene_name = Text("Syene", font_size=36).flip()
        syene_name.next_to(syene_point, DR, buff=MED_SMALL_BUFF).shift(0.25 * DOWN)
        syene_arrow = Arrow(syene_name.get_top(), syene_point, buff=SMALL_BUFF, thickness=2)

        self.play(
            Rotate(earth_group, TAU, axis=earth_axis),
            ShowCreation(tropic_of_cancer),
            axis_line.animate.set_stroke(opacity=0.5).set_anim_args(time_span=(0, 1)),
            run_time=12,
        )

        self.play(
            frame.animate.reorient(-172, 0, 0, (3.05, -0.01, -0.01), 6.69),
            Write(cancer_label, time_span=(1, 3)),
            run_time=3
        )
        self.wait()
        self.play(
            Write(syene_name),
            GrowArrow(syene_arrow),
        )
        self.play(
            frame.animate.reorient(-225, -8, 0, (3.05, -0.01, -0.01), 6.69),
            FadeOut(cancer_label, time_span=(0, 2)),
            run_time=4
        )
        self.wait()

        # Show line through Alexandria
        self.play(
            ShowCreation(d_line),
            frame.animate.reorient(-189, 6, 0, (3.05, -0.01, -0.01), 6.69),
            run_time=3,
        )
        self.play(
            Write(alex_name),
            GrowArrow(alex_arrow),
        )
        self.wait()

        # Show the angle
        earth_point = circle.pfp(angle / TAU)
        upper_ray = Line(earth_point, earth_point + 20 * RIGHT)
        upper_ray.match_style(h_line)

        arc = Arc(0, 2 * angle, radius=3, arc_center=earth_point)
        arc.scale(1 / 2, about_edge=DOWN)
        arc_labels = VGroup()
        for tex in [R"\theta", R"7^{\circ}"]:
            arc_label = Tex(tex, font_size=36)
            arc_label.flip()
            arc_label.next_to(arc, RIGHT, SMALL_BUFF)
            arc_labels.add(arc_label)

        arc_label = arc_labels[0]

        self.play(
            FadeIn(upper_ray),
            ShowCreation(arc),
            FadeIn(arc_label),
        )
        self.wait()
        self.play(Transform(arc_label, arc_labels[1]))
        self.wait()
        self.play(
            arc.animate.shift(earth_point - arc.get_end()).shift(0.01 * LEFT).set_stroke(RED),
            arc_label.animate.next_to(earth_point, DR, buff=0.05),
            upper_ray.animate.set_stroke(width=1, opacity=0.5),
            run_time=2
        )
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(alex_name, alex_arrow, syene_name, syene_arrow)))

        # Show full circumference
        self.play(
            frame.animate.reorient(-173, 0, 0, (2.91, 0.1, -0.01), 7.20),
            ShowCreation(circle),
            run_time=4,
        )

        # Ambient panning
        circle.apply_depth_test()
        self.play(
            FadeOut(arc_label, time_span=(3, 5)),
            frame.animate.reorient(110 - 360, -10, 0, (-0.41, -0.16, 3.6), 7.86),
            run_time=24,
        )

    def old_material(self):
        # Tilt earth
        v_line = axis_line.copy()
        d_line = axis_line.copy()

        arc = Arc(90 * DEG, -EARTH_TILT_ANGLE, radius=1.75)
        arc.set_stroke(WHITE, 2)
        arc_label = Tex(R"23.5^\circ", font_size=36)
        arc_label.next_to(arc.pfp(0.65), UP, buff=0.15)

        self.play(
            Rotate(earth_group, -EARTH_TILT_ANGLE, axis=OUT),
            Rotate(axis_line, -EARTH_TILT_ANGLE, axis=OUT),
            Rotate(d_line, -EARTH_TILT_ANGLE, axis=OUT),
            FadeIn(v_line),
            VFadeIn(d_line),
            ShowCreation(arc),
            Write(arc_label),
            run_time=2
        )
        self.wait()
        self.add(rays, axis_line, earth_group)
        self.play(
            FadeOut(VGroup(v_line, d_line, arc, arc_label), time_span=(0, 1)),
            frame.animate.reorient(-138, -25, 0, (4.72, -0.66, -0.11), 10.77),
            run_time=12
        )
