# ==============================================================================
# Scene:      SnellsLaw
# Source:     videos/_2023/optics_puzzles/bending_waves.py (lines 84-263)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SnellsLaw.py SnellsLaw -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - tank.svg is missing (private): placeholder tank silhouette; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/tank.svg (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SnellsLaw(InteractiveScene):
    # index = 1.5
    index = 1.0

    def construct(self):
        # Setup key objects
        medium = FullScreenRectangle()
        medium.set_fill(BLUE, 0.3).set_stroke(width=0)
        medium.stretch(0.5, 1, about_edge=DOWN)

        hit_point = medium.get_top()
        angle_tracker = ValueTracker(40 * DEGREES)
        beam = self.get_beam(angle_tracker, hit_point)

        glow = GlowDot(color=YELLOW)

        self.add(medium)

        # Shine in
        anim_kw = dict(run_time=3, rate_func=linear)
        self.play(
            ShowCreation(beam, **anim_kw),
            UpdateFromFunc(glow, lambda m: m.move_to(beam.get_end()))
        )
        self.wait()

        # Add angle labels
        normal_line = Line(2 * UP, 2 * DOWN)
        normal_line.move_to(hit_point)
        normal_line.set_stroke(WHITE, 1)

        def get_theta1():
            return angle_tracker.get_value()

        def get_theta2():
            return np.arcsin(np.sin(get_theta1()) / self.index)

        arc_kw = dict(radius=0.8, stroke_width=1)
        arc1 = always_redraw(lambda: Arc(90 * DEGREES, get_theta1(), **arc_kw))
        arc2 = always_redraw(lambda: Arc(-90 * DEGREES, get_theta2(), **arc_kw))
        theta1_label = Tex(R"\theta_1")
        theta1_label.arc = arc1
        theta2_label = Tex(R"\theta_2")
        theta2_label.arc = arc2

        def update_theta_label(label):
            point = label.arc.pfp(0.2)
            vect = normalize(point - hit_point)
            label.set_height(min(0.4, max(1.0 * label.arc.get_width(), 1e-2)))
            label.next_to(point, vect, buff=SMALL_BUFF)

        theta1_label.add_updater(update_theta_label)
        theta2_label.add_updater(update_theta_label)

        ineq = Tex(R"\theta_1 > \theta_2")
        ineq.move_to(FRAME_WIDTH * RIGHT / 4 + 3 * UP)

        self.play(
            LaggedStart(
                ShowCreation(normal_line),
                ShowCreation(arc1),
                ShowCreation(arc2),
                Write(theta1_label),
                Write(theta2_label),
                lag_ratio=0.1,
                run_time=1
            ),
            FadeIn(ineq, UP)
        )
        self.wait()

        angle_labels = VGroup(normal_line, arc1, arc2, theta1_label, theta2_label)

        # Vary the angle for a bit
        self.remove(arc2, theta2_label, ineq)

        beam.set_stroke(opacity=1, width=2)
        for width in np.linspace(2, 10.0, 40):
            beam_copy = beam.copy()
            beam_copy.set_stroke(width=width, opacity=0.2 / (width)**1.4)
            self.add(beam_copy)

        for angle in [70 * DEGREES, -50 * DEGREES, 40 * DEGREES]:
            self.play(angle_tracker.animate.set_value(angle), run_time=5)

        # Tank analogy
        tank = SVGMobject("tank")
        tank.set_fill(WHITE)
        tank.rotate(-16 * DEGREES)
        tank.set_height(1)
        tank.move_to(beam.pfp(0.25))

        self.play(FadeOut(angle_labels))
        self.frame.set_height(4)
        self.play(
            tank.animate.move_to(beam.pfp(0.49)).set_anim_args(rate_func=linear, run_time=6),
            VFadeIn(tank),
            self.frame.animate.set_height(4).set_anim_args(time_span=(4, 6))
        )
        self.play(
            tank.animate.rotate(get_theta2() - get_theta1()).move_to(hit_point + 0.3 * UP + 0.1 * LEFT),
            rate_func=linear,
            run_time=1.5,
        )
        self.play(
            tank.animate.move_to(beam.pfp(0.65)).set_anim_args(rate_func=linear, run_time=8),
            VFadeOut(tank, time_span=(7, 8)),
            self.frame.animate.set_height(8).set_anim_args(time_span=(6, 8))
        )
        self.wait()

        # Write Snell's law
        law = Tex(R"{\sin(\theta_1) \over v_1} = {\sin(\theta_2) \over v_2}", font_size=52)
        title = TexText("Snell's Law", font_size=60)
        group = VGroup(title, law)
        group.arrange(DOWN, buff=0.75)
        group.to_corner(UR)

        self.play(FadeIn(angle_labels))
        self.play(
            Write(title),
            FlashUnder(title, run_time=2),
            FadeOut(ineq[">"]),
            Transform(ineq[R"\theta_1"], law[R"\theta_1"]),
            Transform(ineq[R"\theta_2"], law[R"\theta_2"]),
        )
        self.play(FadeIn(law))
        self.wait()
        tl1_copy = theta1_label.copy()
        tl2_copy = theta2_label.copy()
        self.play(LaggedStart(
            Transform(tl1_copy, law[R"\theta_1"]),
            Transform(tl2_copy, law[R"\theta_2"]),
            lag_ratio=0.5
        ))
        self.play(FadeIn(law, lag_ratio=0.1, run_time=2))
        self.remove(tl1_copy, tl2_copy)
        self.wait()

        # Vary the angle again
        for angle in [70 * DEGREES, 20 * DEGREES, 40 * DEGREES]:
            self.play(angle_tracker.animate.set_value(angle), run_time=3)

        # Show speeds
        in_beam = Line(beam.get_start(), hit_point)
        out_beam = Line(hit_point, beam.get_end())
        in_beam.set_length(8, about_point=hit_point)

        def get_dot_anim():
            dot = GlowDot()
            return Succession(
                MoveAlongPath(dot, in_beam, rate_func=linear, run_time=3),
                MoveAlongPath(dot, out_beam, rate_func=linear, run_time=3),
                remover=True,
            )

        self.play(LaggedStart(
            *(
                get_dot_anim()
                for x in range(50)
            ),
            lag_ratio=0.02,
            run_time=20,
        ))

    def get_beam(self, angle_tracker, hit_point, stroke_color=YELLOW, stroke_width=3):
        result = Line()
        result.set_stroke(stroke_color, stroke_width)

        def update_beam(beam):
            theta1 = angle_tracker.get_value()
            theta2 = np.arcsin(np.sin(theta1) / self.index)
            beam.set_points_as_corners([
                hit_point + 0.6 * FRAME_HEIGHT * rotate_vector(UP, theta1) / math.cos(theta1),
                hit_point,
                hit_point + 0.6 * FRAME_HEIGHT * rotate_vector(DOWN, theta2) / math.cos(theta2),
            ])

        result.add_updater(update_beam)
        return result
