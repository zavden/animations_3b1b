# ==============================================================================
# Scene:      FrequencyVsAngularFrequency
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 739-896)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FrequencyVsAngularFrequency.py FrequencyVsAngularFrequency -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FrequencyVsAngularFrequency(TeacherStudentsScene):
    def construct(self):
        # Correction
        morty = self.teacher
        stds = self.students

        rf_words = Text("Resonant frequency")
        raf_words = Text("Resonant angular frequency")
        omega = Tex(R"\omega_r", font_size=72)
        omega.set_color(PINK)
        omega.move_to(self.hold_up_spot, DOWN)
        for words in rf_words, raf_words:
            words.next_to(omega, UP)

        cross = Cross(rf_words)
        self.add(rf_words, omega)
        morty.change_mode("raise_right_hand")
        self.play(
            ShowCreation(cross),
            self.change_students("sassy", "hesitant", "angry")
        )
        rf_words.add(cross)
        rf_words.target = rf_words.generate_target()
        rf_words.target.next_to(raf_words, UP, LARGE_BUFF)
        rf_words.target.set_fill(opacity=0.5)
        rf_words.target[-1].set_opacity(0)

        self.wait()
        self.play(
            MoveToTarget(rf_words),
            TransformMatchingStrings(
                rf_words.copy(), raf_words,
                run_time=1,
            ),
            self.change_students("pondering", "hesitant", "hesitant")
        )

        # Show cycles
        plane = ComplexPlane(
            (-1, 1), (-1, 1),
            background_line_style=dict(stroke_width=1, stroke_color=BLUE),
            faded_line_style=dict(stroke_width=0.5, stroke_opacity=0.5, stroke_color=BLUE),
        )
        plane.set_height(4)
        plane.to_edge(DOWN)
        circle = Circle(radius=plane.x_axis.get_unit_size())
        circle.set_stroke(TEAL, 2)
        circle.move_to(plane.get_origin())

        f_words = Text("Frequency", font_size=60)
        af_words = Text("Angular Frequency", font_size=60)
        for words, x in [(f_words, -1), (af_words, 1)]:
            words.set_x(x * FRAME_WIDTH  / 4)
            words.to_edge(UP, buff=MED_SMALL_BUFF)

        t2c = {R"\omega": PINK, "f": TEAL}
        f_eq = Tex(R"f = {\text{Cycles} \over \text{Seconds}}", t2c=t2c)
        f_eq.next_to(f_words, DOWN, MED_LARGE_BUFF)
        f_eq["f"].set_color(YELLOW)
        af_eq = Tex(R"\omega = {\text{Radians} \over \text{Seconds}}", t2c=t2c)
        af_eq.next_to(af_words, DOWN, MED_LARGE_BUFF)
        af_eq[R"\omega"].set_color(PINK)

        angle_tracker = ValueTracker()
        angle_tracker.add_updater(lambda m, dt: m.increment_value(0.25 * dt * TAU))
        vect = Vector(RIGHT).set_color(YELLOW)
        vect.add_updater(lambda m: m.put_start_and_end_on(
            plane.n2p(0),
            plane.n2p(np.exp(complex(0, angle_tracker.get_value())))
        ))

        self.add(angle_tracker)
        self.play(
            FadeOut(self.background),
            LaggedStartMap(FadeOut, self.pi_creatures, shift=DOWN),
            ShowCreation(plane, lag_ratio=0.1),
            FadeIn(circle),
            TransformMatchingStrings(rf_words, f_words),
            TransformMatchingStrings(raf_words, af_words),
            FadeTransform(omega, af_eq[R"\omega"]),
            FadeIn(af_eq[1:]),
            FadeIn(f_eq),
            VFadeIn(vect)
        )
        self.wait(4)

        # Show specific value
        f_value_eq = Tex("f = 0.25", t2c=t2c)
        af_value_eq = Tex(R"\omega = 2\pi f = 1.57", t2c=t2c)
        values = VGroup(f_value_eq, af_value_eq)
        values.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        values.next_to(plane, LEFT, MED_LARGE_BUFF)

        self.play(FadeIn(f_value_eq))
        self.wait(8)
        self.play(FadeIn(af_value_eq))

        # Show angle label
        arc_angle_tracker = ValueTracker()
        get_arc_angle = arc_angle_tracker.get_value 
        arc = always_redraw(lambda: Arc(
            0, get_arc_angle(),
            arc_center=plane.n2p(0),
            radius=0.5,
        ))
        arc_angle_label = DecimalNumber(0, unit=R"\text{ Radians}")
        arc_angle_label.add_updater(lambda m: m.set_value(get_arc_angle()))
        arc_angle_label.add_updater(lambda m: m.next_to(arc.get_center(), UR))
        arc_angle_label.add_updater(lambda m: m[4:].shift(SMALL_BUFF * RIGHT))


        self.add(arc)
        self.play(
            arc_angle_tracker.animate.set_value(TAU / 4),
            VFadeIn(arc_angle_label),
        )
        arc.clear_updaters()
        self.wait(10)
        self.play(
            VFadeOut(arc),
            VFadeOut(arc_angle_label),
            FadeOut(values),
        )

        # Show cosine
        plane.add(circle)
        plane.generate_target()
        plane.target.to_edge(LEFT)
        axes = Axes((0, 16), (-1, 1), width=9, height=0.75 * plane.get_height())
        axes.next_to(plane.target, RIGHT)
        graph = axes.get_graph(lambda x: np.cos(TAU * 0.25 * x))
        graph.set_stroke(YELLOW, 2)

        cos_eq = Tex(R"\cos(\omega t) = \cos(2\pi f t)", t2c=t2c)
        cos_eq.next_to(graph, UP)
        omega_arrow = Vector(0.5 * DOWN).set_color(PINK)
        omega_arrow.next_to(cos_eq[R"\omega"], UP, SMALL_BUFF)

        dot = GlowDot()
        dot.add_updater(lambda m: m.move_to(plane.n2p(math.cos(angle_tracker.get_value()))))
        line = Line(UP, DOWN)
        line.set_stroke(YELLOW, 1)
        line.add_updater(lambda m: m.put_start_and_end_on(
            vect.get_end(), dot.get_center()
        ))

        self.play(
            MoveToTarget(plane),
            FadeIn(axes, 2 * LEFT)
        )
        self.wait(4 * (1 - (angle_tracker.get_value() / TAU) % 1))
        self.add(dot, line)
        self.play(
            ShowCreation(graph, rate_func=linear),
            FadeIn(cos_eq, time_span=(0, 1)),
            ShowCreation(omega_arrow, time_span=(4, 5)),
            run_time=16
        )
