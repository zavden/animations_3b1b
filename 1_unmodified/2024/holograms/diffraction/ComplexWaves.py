# ==============================================================================
# Scene:      ComplexWaves
# Source:     videos/_2024/holograms/diffraction.py (lines 3793-4089)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexWaves.py ComplexWaves -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ComplexWaves(InteractiveScene):
    def construct(self):
        # Add Amplitude(R + O)^2
        amp_expr = Tex(R"\text{Amplitude}(R + O)^2", font_size=60)
        amp_expr.to_edge(UP)
        RO = amp_expr[R"R + O"][0]
        RO.save_state()
        RO.set_x(0)

        self.play(FadeIn(RO, UP))
        self.wait()
        self.play(
            Write(amp_expr[R"\text{Amplitude}("][0]),
            Write(amp_expr[R")"][0], time_span=(1.5, 2)),
            Restore(RO, time_span=(0.5, 1.5)),
            run_time=2
        )
        self.wait()
        self.play(FadeIn(amp_expr[R"^2"], 0.25 * UP, scale=0.8))
        self.wait()

        # Expand as functions of (x, y, z, t)
        amp_expr.save_state()

        O_func = Tex("O(x, y, z, t)", font_size=60)
        O_func.move_to(UP + LEFT)

        xyz_rect = SurroundingRectangle(O_func["x, y, z"], buff=0.05)
        xyz_rect.set_stroke(YELLOW)
        xyz_rect.stretch(1.3, 1, about_edge=DOWN)
        xyz_rect.round_corners()
        xyz_arrow = Vector(2.2 * UP, thickness=5).next_to(xyz_rect, DOWN)
        xyz_arrow.set_backstroke(BLACK, 4)
        space_words = Text("Point\nin space", font_size=36)
        space_words.next_to(xyz_rect, UP)

        time_rect = SurroundingRectangle(O_func["t"], buff=0.05)
        time_rect.match_height(xyz_rect, stretch=True, about_edge=DOWN)
        time_rect.align_to(xyz_rect, DOWN)
        time_rect.round_corners()
        time_rect.set_stroke(TEAL)
        time_word = Text("Time", font_size=36)  # Make a clock instead?
        time_word.next_to(time_rect, UP)

        self.play(
            amp_expr.animate.scale(0.5).to_corner(UL).set_opacity(0.5),
            TransformFromCopy(amp_expr["O"][0], O_func["O"][0]),
        )
        self.play(Write(O_func[1:], run_time=1, stroke_color=WHITE))
        O_func.set_backstroke(BLACK, 5)
        self.play(
            ShowCreation(xyz_rect),
            GrowArrow(xyz_arrow),
            FadeIn(space_words, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            FadeTransformPieces(space_words, time_word),
            ShowCreation(time_rect),
        )
        self.wait()

        # Show O(x, y, z, t) outputting to a real line
        frequency = 0.25
        amplitude = 1.5
        out_arrow = Vector(RIGHT, thickness=4)
        out_arrow.next_to(O_func, RIGHT)

        real_line = NumberLine((-2, 2, 0.25), width=4, tick_size=0.025, big_tick_spacing=1.0, longer_tick_multiple=3)
        real_line.next_to(out_arrow, RIGHT)
        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            width=4,
            background_line_style=dict(
                stroke_color=GREY_C,
                stroke_width=1,
            ),
            faded_line_style=dict(
                stroke_color=GREY_D,
                stroke_width=0.5,
                stroke_opacity=1,
            )
        )
        plane.move_to(real_line)

        real_line.add_numbers(list(range(-2, 3)), font_size=16)
        plane.add_coordinate_labels(font_size=16)
        plane.set_stroke(behind=True)

        time_tracker = ValueTracker()
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        def get_z():
            return amplitude * np.exp(complex(0, TAU * frequency * time_tracker.get_value()))

        def get_z_point():
            return plane.n2p(get_z())

        real_indicator = Group(GlowDot(radius=0.3), TrueDot().make_3d())

        def update_real_indicator(indicator):
            x = get_z().real
            indicator.move_to(plane.n2p(x))
            if x > 0:
                indicator.set_color(interpolate_color(GREY_D, BLUE, x / amplitude))
            else:
                indicator.set_color(interpolate_color(GREY_D, RED, -x / amplitude))

        real_indicator.add_updater(update_real_indicator)

        self.add(time_tracker)
        self.play(
            GrowArrow(out_arrow),
            FadeIn(real_line),
            xyz_rect.animate.set_stroke(width=1),
            time_rect.animate.set_stroke(width=1),
            FadeOut(time_word),
            FadeIn(real_indicator)
        )
        self.wait(12)

        # Extend to complex plane
        complex_label = Text("Complex Plane")
        complex_label.next_to(plane, UP)
        complex_dot = real_indicator.copy()
        complex_dot.clear_updaters()
        complex_dot.set_color(YELLOW)
        complex_dot.f_always.move_to(get_z_point)

        complex_arrow = Vector(RIGHT)
        complex_arrow.set_color(YELLOW)
        complex_arrow.f_always.put_start_and_end_on(plane.get_origin, get_z_point)

        v_line = Line(UP, DOWN)
        v_line.set_stroke(GREY, 1)
        v_line.f_always.put_start_and_end_on(get_z_point, real_indicator.get_center)

        self.add(plane, real_indicator)
        self.play(
            FadeIn(plane),
            FadeOut(real_line),
            FadeIn(complex_arrow),
            FadeIn(v_line),
        )
        self.play(Write(complex_label))
        self.wait(12)

        # Get into a good position
        time_tracker.resume_updating()
        self.wait_until(lambda: 0.4 < time_tracker.get_value() % 4 < 0.5)
        time_tracker.suspend_updating()

        # Mention amplitude and phase
        angle = complex_arrow.get_angle()
        rot_arrow = complex_arrow.copy()
        rot_arrow.clear_updaters()
        rot_arrow.rotate(-angle, about_point=rot_arrow.get_start())
        rot_arrow.set_opacity(0)
        brace = Brace(rot_arrow, UP, buff=0)
        amp_label = brace.get_text("Amplitude", font_size=30)
        amp_label.set_backstroke(BLACK, 5)
        VGroup(brace, amp_label).rotate(angle, about_point=complex_arrow.get_start())

        arc = Arc(0, angle, radius=0.5, arc_center=plane.get_origin())
        phase_label = Text("Phase", font_size=30)
        phase_label.next_to(arc, RIGHT, SMALL_BUFF)
        phase_label.shift(SMALL_BUFF * UR)

        self.play(
            GrowFromCenter(brace),
            Write(amp_label),
        )
        self.wait()
        self.play(
            ShowCreation(arc),
            TransformFromCopy(rot_arrow, complex_arrow, path_arc=angle),
            Write(phase_label)
        )
        self.wait()

        # Re-emphasize the real component
        self.play(FadeOut(VGroup(brace, amp_label, arc, phase_label)))
        time_tracker.resume_updating()

        plane.save_state()
        self.play(
            plane.animate.fade(0.75),
            FadeIn(real_line),
            complex_arrow.animate.set_fill(opacity=0.25)
        )
        self.wait(8)
        self.play(
            Restore(plane),
            FadeOut(real_line),
            complex_arrow.animate.set_fill(opacity=1.0)
        )
        self.wait(8)
        self.play(
            FadeOut(xyz_rect),
            FadeOut(time_rect),
            FadeOut(xyz_arrow),
            FadeOut(out_arrow),
            FadeOut(real_indicator),
            FadeOut(v_line),
        )

        # Package back into R + O expression
        time_tracker.suspend_updating()

        self.remove(complex_label)
        plane.add(complex_label)
        self.add(plane, complex_arrow)
        self.play(
            Transform(O_func, amp_expr.saved_state[-3], remover=True),
            Restore(amp_expr),
            plane.animate.move_to(DOWN),
            run_time=2
        )

        # Add R arrow
        O_arrow = complex_arrow
        O_arrow.clear_updaters()
        R_arrow = Vector().set_color(TEAL)
        comb_arrow = Vector().set_color(GREY_B)

        R_phase_tracker = ValueTracker(30 * DEGREES)
        O_phase_tracker = ValueTracker(complex_arrow.get_angle())
        R_amp = math.sqrt(2)
        O_amp = 1.5

        def get_R():
            return R_amp * np.exp(complex(0, R_phase_tracker.get_value()))

        def get_O():
            return O_amp * np.exp(complex(0, O_phase_tracker.get_value()))

        R_arrow.put_start_and_end_on(plane.get_origin(), plane.n2p(get_R()))
        comb_arrow.put_start_and_end_on(plane.get_origin(), plane.n2p(get_R() + get_O()))

        R_label = self.get_arrow_label(R_arrow, "R")
        O_label = self.get_arrow_label(O_arrow, "O")
        comb_label = self.get_arrow_label(comb_arrow, "R + O", buff=-0.5)

        self.play(
            GrowArrow(R_arrow),
            O_arrow.animate.shift(R_arrow.get_vector()),
            FadeIn(R_label),
            FadeIn(O_label),
        )
        self.play(
            FadeIn(comb_arrow),
            FadeIn(comb_label),
        )
        self.wait()

        R_arrow.add_updater(lambda m: m.put_start_and_end_on(
            plane.get_origin(), plane.n2p(get_R())
        ))
        O_arrow.add_updater(lambda m: m.put_start_and_end_on(
            plane.n2p(get_R()), plane.n2p(get_R() + get_O()),
        ))
        comb_arrow.add_updater(lambda m: m.put_start_and_end_on(
            plane.get_origin(), plane.n2p(get_R() + get_O()),
        ))

        # Write |R + O|^2
        lhs = Text("Film opacity = ")
        lhs.move_to(amp_expr, LEFT)
        lhs.set_color(GREY_B)
        new_amp_expr = Tex(R"c|R + O|^2")
        new_amp_expr.next_to(lhs, RIGHT)

        self.play(
            ReplacementTransform(amp_expr["(R + O)^2"][0], new_amp_expr),
            FadeOut(amp_expr["Amplitude"][0]),
        )
        self.play(FadeIn(lhs, lag_ratio=0.1))
        self.wait()

        # Change R and O values
        self.play(
            R_phase_tracker.animate.set_value(-45 * DEGREES),
            O_phase_tracker.animate.set_value(-45 * DEGREES), run_time=2
        )
        self.wait()
        self.play(
            O_phase_tracker.animate.set_value(-125 * DEGREES),
            R_phase_tracker.animate.set_value(45 * DEGREES),
            run_time=3
        )
        self.wait()

    def get_arrow_label(self, arrow, symbol, font_size=24, buff=0.25):
        result = Tex(symbol, font_size=font_size)
        result.match_color(arrow)
        result.add_updater(lambda m: m.move_to(arrow.get_center() + buff * normalize(rotate_vector(arrow.get_vector(), PI / 2))))
        return result
