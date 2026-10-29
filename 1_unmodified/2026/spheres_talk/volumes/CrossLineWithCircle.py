# ==============================================================================
# Scene:      CrossLineWithCircle
# Source:     videos/_2026/spheres_talk/volumes.py (lines 997-1213)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CrossLineWithCircle.py CrossLineWithCircle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CrossLineWithCircle(InteractiveScene):
    def construct(self):
        # Equation
        self.frame.set_field_of_view(5 * DEG)
        line = Line(DOWN, UP)
        line.set_stroke(GREEN_E, 8)
        circle = Circle()
        circle.set_stroke(RED, 3)
        pure_sphere = Sphere()
        pure_sphere.set_color(BLUE_E, 1)
        sphere = Group(pure_sphere, SurfaceMesh(pure_sphere))
        sphere.match_height(circle)
        sphere.rotate(75 * DEG, LEFT)

        group = Group(
            sphere,
            Tex(R"=", font_size=120),
            line,
            Tex(R"\times", font_size=120),
            circle,
        )
        group.arrange(RIGHT, buff=LARGE_BUFF)

        self.add(group)

        # Formulas
        sphere_3d_form = Tex(R"x^2 + y^2 + z^2 = 1")
        sphere_3d_form.next_to(group[0], DOWN, buff=MED_LARGE_BUFF)

        line_form = Tex(R"z^2 \le 1")
        line_form.match_x(line).match_y(sphere_3d_form)

        circle_form = Tex(R"x^2 + y^2 = 1 - z^2")
        circle_form.match_x(circle).match_y(sphere_3d_form)

        self.play(FadeIn(sphere_3d_form, DOWN))
        self.wait()
        self.play(TransformFromCopy(sphere_3d_form["z^2 = 1"], line_form))
        self.wait()
        self.play(
            TransformMatchingTex(sphere_3d_form.copy(), circle_form, path_arc=45 * DEG)
        )
        self.wait()

        # Show dependence
        interval = NumberLine((-1, 1))
        interval.put_start_and_end_on(line.get_start(), line.get_end())

        z_dot = Group(GlowDot(radius=0.5), TrueDot(radius=0.1).make_3d())
        z_dot.set_color(GREEN)
        z_tracker = ValueTracker(0)
        get_z = z_tracker.get_value
        z_dot.add_updater(lambda m: m.move_to(interval.n2p(get_z())))

        circle_width = circle.get_width()
        circle_center = circle.get_center().copy()
        circle.add_updater(lambda m: m.set_width(circle_width * math.sqrt(1 - get_z()**2)).move_to(circle_center))

        self.play(
            FadeIn(z_dot),
            FadeIn(interval),
        )
        self.play(z_tracker.animate.set_value(0.95), run_time=4)
        self.play(z_tracker.animate.set_value(-0.95), run_time=8)
        self.play(z_tracker.animate.set_value(0), run_time=4)
        circle.clear_updaters()

        # Repalce with final form
        rect = SurroundingRectangle(circle_form)
        self.play(ShowCreation(rect))
        self.play(
            FadeOut(circle_form[-3:]),
            circle_form[:-3].animate.shift(0.5 * RIGHT),
        )
        self.wait()
        self.play(
            FadeOut(rect),
            FadeOut(z_dot),
            FadeOut(interval),
        )

        # Label it as boundary of B^3
        fade_rects = VGroup(
            BackgroundRectangle(mob, buff=SMALL_BUFF, fill_opacity=0.5)
            for mob in group[0::2]
        )
        sphere_labels = self.get_sphere_labels(3, fade_rects)

        for label, rect in zip(sphere_labels, fade_rects):
            self.play(FadeIn(rect), FadeIn(label))
        self.wait()

        # Transition to 4D case
        disk = circle.copy()
        disk.match_style(line)
        disk.set_fill(GREEN, 0.5)
        disk.move_to(line)
        hyper_sphere_labels = self.get_sphere_labels(4, group[0::2])
        db4_label, b2_label, db2_label = hyper_sphere_labels
        db4_label.shift(SMALL_BUFF * UP)
        for label in hyper_sphere_labels[1:]:
            label.scale(0.8)

        self.play(
            LaggedStartMap(FadeOut, sphere_labels, shift=0.5 * UP, lag_ratio=0.5, run_time=1),
            FadeIn(db4_label, shift=0.5 * UP),
            FadeOut(group[0], LEFT),
            group[1].animate.move_to(midpoint(db4_label.get_right(), disk.get_left())),
            group[3].animate.move_to(VGroup(disk, circle)),
            ReplacementTransform(line, disk),
            FadeOut(VGroup(sphere_3d_form, circle_form, line_form)),
            *map(FadeOut, fade_rects),
        )

        # Add labels
        labels4d = VGroup(
            Tex(R"x^2 + y^2 + z^2 + w^2 = 1").next_to(db4_label, DOWN),
            Tex(R"z^2 + w^2 \le 1").next_to(disk, DOWN),
            Tex(R"x^2 + y^2 = 1 - z^2 - w^2").next_to(circle, DOWN),
            Tex(R"x^2 + y^2 = 1").next_to(circle, DOWN),
        )
        for label in labels4d:
            label.align_to(labels4d, DOWN)

        labels4d[0].shift(0.5 * LEFT)
        labels4d[2].to_edge(RIGHT, buff=SMALL_BUFF)

        self.play(FadeIn(labels4d[0], DOWN))
        self.wait()
        self.play(TransformFromCopy(labels4d[0]["z^2 + w^2 = 1"][0], labels4d[1], path_arc=30 * DEG))
        self.wait()
        self.play(TransformFromCopy(labels4d[0], labels4d[2], path_arc=30 * DEG))
        self.wait()

        # Manipuliate z and w, let circle change size
        axes = Axes((-1, 1, 0.25), (-1, 1, 0.25), axis_config=dict(tick_size=0.025))
        axes.replace(disk)
        z_dot.clear_updaters()
        z_dot[1].set_radius(0.07)
        z_dot.move_to(axes.c2p(0, 0))

        def get_radius():
            z, w = axes.p2c(z_dot.get_center())
            return math.sqrt(1 - z**2 - w**2)

        circle_center = circle.get_center()
        circle.add_updater(lambda m: m.set_width(circle_width * get_radius()).move_to(circle_center))

        self.play(
            FadeIn(axes),
            FadeIn(z_dot),
        )
        self.play(z_dot.animate.shift(0.7 * UR), run_time=4)
        self.wait()
        self.play(z_dot.animate.shift(1.0 * DOWN), run_time=4)
        self.wait()
        self.play(z_dot.animate.move_to(axes.get_origin()), run_time=5)
        circle.clear_updaters()
        self.play(FadeOut(z_dot), FadeOut(axes))

        # Simplify circle formula
        rect = SurroundingRectangle(labels4d[2])
        self.play(ShowCreation(rect))
        self.play(
            TransformMatchingTex(labels4d[2], labels4d[3]),
            rect.animate.surround(labels4d[3]),
            run_time=2
        )
        self.wait()
        self.play(FadeOut(rect))

        # Go up to five dimensions
        db5_label = Tex(R"\partial B^5", font_size=120)
        db5_label.move_to(db4_label)
        sphere = pure_sphere
        sphere.replace(disk)

        self.play(LaggedStart(
            FadeOut(labels4d[:2]),
            FadeOut(labels4d[3]),
            FadeOut(disk, 0.5 * UP),
            FadeIn(sphere, 0.5 * UP),
            FadeOut(db4_label, 0.5 * UP),
            FadeIn(db5_label, 0.5 * UP),
        ))
        self.wait()

        # Show the labels
        labels5d = VGroup(
            Tex(R"x^2 + y^2 + z^2 + w^2 + v^2 = 1").next_to(db5_label, DOWN),
            Tex(R"z^2 + w^2 + v^2 \le 1").next_to(sphere, DOWN),
            Tex(R"x^2 + y^2 = 1").next_to(circle, DOWN),
        )
        for label in labels5d:
            label.scale(0.8, about_edge=DOWN)
            label.align_to(labels5d, DOWN)

        labels5d[0].shift(LEFT)

        self.play(FadeIn(labels5d[0], DOWN))
        self.wait()
        self.play(TransformFromCopy(labels5d[0]["z^2 + w^2 + v^2 = 1"][0], labels5d[1], path_arc=30 * DEG))
        self.wait()
        self.play(
            TransformFromCopy(labels5d[0]["x^2 + y^2"][0], labels5d[2]["x^2 + y^2"][0], path_arc=30 * DEG),
            TransformFromCopy(labels5d[0]["= 1"][0], labels5d[2]["= 1"][0], path_arc=30 * DEG),
        )
        self.wait()

    def get_sphere_labels(self, n, group):
        labels = VGroup(
            Tex(tex, font_size=120)
            for tex in [fR"\partial B^{n}", f"B^{n - 2}", fR"\partial B^2"]
        )
        for label, mob in zip(labels, group):
            label.move_to(mob)
        return labels
