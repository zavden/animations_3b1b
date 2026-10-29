# ==============================================================================
# Scene:      ExplainSmallAngleApprox
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 761-906)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExplainSmallAngleApprox.py ExplainSmallAngleApprox -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExplainSmallAngleApprox(InteractiveScene):
    def construct(self):
        # Setup
        frame = self.frame
        height = 7.5
        axes = Axes(
            (-2, 2),
            (-2, 2),
            height=height,
            width=height,
            axis_config=dict(include_tip=True)
        )
        axes.shift(-axes.get_origin())
        unit_size = axes.x_axis.get_unit_size()

        circle = Circle(radius=unit_size)
        circle.set_stroke(WHITE, 3)
        point = GlowDot(color=RED)
        point.move_to(circle.get_right())

        radial_line = Line()
        radial_line.set_stroke(BLUE, 3)
        radial_line.f_always.put_start_and_end_on(
            axes.get_origin,
            point.get_center,
        )
        radial_label = Tex(R"1", font_size=36)
        radial_label.add_updater(lambda m: m.move_to(
            radial_line.get_center() + 0.15 * rotate_vector(radial_line.get_vector(), -90 * DEG),
        ))

        self.add(axes)
        self.add(radial_line)
        self.add(radial_label)
        self.play(
            ShowCreation(circle),
            UpdateFromFunc(point, lambda m: m.move_to(circle.get_end())),
            frame.animate.set_height(5),
            run_time=3
        )
        self.wait()

        # Show angle
        theta_color = YELLOW
        x_color = RED
        y_color = GREEN

        h_radial_line = radial_line.copy().clear_updaters()
        radial_label.clear_updaters()
        theta_tracker = ValueTracker(1e-2)
        get_theta = theta_tracker.get_value
        point.add_updater(lambda m: m.move_to(unit_size * rotate_vector(RIGHT, get_theta())))

        arc = always_redraw(lambda: Arc(0, get_theta(), radius=0.5))
        theta_label = Tex(R"\theta", font_size=36)
        theta_label.set_color(theta_color)
        theta_label.f_always.set_height(lambda: clip(arc.get_height(), 1e-2, 0.30))
        theta_label.add_updater(lambda m: m.next_to(arc.pfp(0.65), RIGHT, buff=0.075))

        tan_eq = Tex(
            R"\tan(\theta) = {{y} \over {x}} \approx {\theta \over 1}",
            t2c={R"\theta": theta_color, "{x}": x_color, "{y}": y_color},
        )
        tan_eq.fix_in_frame()
        tan_eq.to_corner(UR).shift(LEFT)

        self.add(h_radial_line)
        self.add(arc)
        self.add(theta_label)
        self.play(
            theta_tracker.animate.set_value(30 * DEG),
            radial_line.animate.set_stroke(WHITE, 3),
            run_time=1
        )
        self.play(
            TransformFromCopy(theta_label.copy().clear_updaters(), tan_eq[R"\theta"][0]),
            Write(tan_eq[R"\tan("]),
            Write(tan_eq[R") ="]),
        )
        self.wait()

        # Show lines
        x_line = Line().set_stroke(x_color, 4)
        y_line = Line().set_stroke(y_color, 4)
        x_line.add_updater(lambda m: m.put_start_and_end_on(
            axes.get_origin(), axes.c2p(math.cos(get_theta()), 0)
        ))
        y_line.add_updater(lambda m: m.put_start_and_end_on(
            axes.c2p(math.cos(get_theta()), 0),
            axes.c2p(math.cos(get_theta()), math.sin(get_theta()))
        ))

        x_label = Tex(R"x", font_size=30).set_color(x_color)
        y_label = Tex(R"y", font_size=30).set_color(y_color)
        VGroup(x_label, y_label).set_backstroke(BLACK, 3)
        x_label.always.next_to(x_line, DOWN, SMALL_BUFF)
        y_label.always.next_to(y_line, RIGHT, buff=0.05)

        self.play(LaggedStart(
            ShowCreation(y_line, suspend_mobject_updating=True),
            VFadeIn(y_label),
            FadeOut(h_radial_line),
            FadeOut(radial_label),
            ShowCreation(x_line, suspend_mobject_updating=True),
            VFadeIn(x_label),
            lag_ratio=0.15
        ))
        self.play(LaggedStart(
            TransformFromCopy(y_label.copy().clear_updaters(), tan_eq["{y}"][0]),
            Write(tan_eq[R"\over"][0]),
            TransformFromCopy(x_label.copy().clear_updaters(), tan_eq["{x}"][0]),
            lag_ratio=0.5
        ))
        self.wait()

        # Shrink down
        self.play(theta_tracker.animate.set_value(0.1), run_time=3)
        self.wait()

        # Analogy
        lil_rect = SurroundingRectangle(tan_eq["{x}"])
        self.play(
            Write(tan_eq[R"\approx"]),
            TransformFromCopy(tan_eq[R"\over"][0], tan_eq[R"\over"][1]),
            ShowCreation(lil_rect),
        )
        self.play(
            TransformFromCopy(tan_eq["{x}"][0], tan_eq["1"][0]),
            lil_rect.animate.surround(tan_eq["1"]),
        )
        self.wait()
        self.play(
            lil_rect.animate.surround(tan_eq["{y}"]),
            y_label.animate.scale(0.5),
            x_label.animate.scale(0.5),
            point.animate.set_radius(0.25 * point.get_radius()),
            frame.animate.reorient(0, 0, 0, (1.46, -0.0, 0.0), 1.87).set_anim_args(run_time=3),
        )
        self.play(
            TransformFromCopy(tan_eq["{y}"][0], tan_eq[R"\theta"][1]),
            lil_rect.animate.surround(tan_eq[R"\theta"][1]),
        )
        self.play(FadeOut(lil_rect))

        # More shrinking!
        self.play(theta_tracker.animate.set_value(1e-2), run_time=8)
