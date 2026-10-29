# ==============================================================================
# Scene:      ComplexComponents
# Source:     videos/_2025/grover/state_vectors.py (lines 2941-3186)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexComponents.py ComplexComponents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BitString(VGroup):
    def __init__(self, value, length=4, buff=SMALL_BUFF):
        self.length = length
        bit_mob = Integer(0)
        super().__init__(bit_mob.copy() for n in range(length))
        self.arrange(RIGHT, buff=buff)
        self.set_value(value)

    def set_value(self, value):
        bits = bin(value)[2:].zfill(self.length)
        for mob, bit in zip(self, bits):
            mob.set_value(int(bit))


class ComplexComponents(InteractiveScene):
    def construct(self):
        # Set up vectors
        state = normalize(np.random.uniform(-1, 1, 4))
        dec_vect = DecimalMatrix(state.reshape(-1, 1), decimal_config=dict(include_sign=True))
        dec_vect.move_to(3 * LEFT)

        indices = VGroup(BitString(n, 2) for n in range(4))
        for index, elem in zip(indices, dec_vect.elements):
            index.set_color(GREY_B)
            index.match_height(elem)
            index.next_to(dec_vect, LEFT)
            index.match_y(elem)

        x_vect, z_vect = var_vects = [
            TexMatrix(np.array([f"{char}_{n}" for n in range(4)]).reshape(-1, 1))
            for char in "xz"
        ]
        for vect in var_vects:
            vect.match_height(dec_vect)
            vect.move_to(dec_vect, LEFT)

        self.add(dec_vect, indices)
        self.wait()

        # Real number lines and complex planes
        number_lines = VGroup(
            NumberLine(
                (-1, 1, 0.1),
                big_tick_spacing=1,
                width=3,
                tick_size=0.05,
                stroke_color=GREY_C,
            )
            for n in range(4)
        )
        number_lines.arrange(DOWN, buff=1.0)
        number_lines.next_to(dec_vect, RIGHT, buff=1.0)

        complex_planes = VGroup(
            ComplexPlane((-1, 1), (-1, 1)).replace(number_line, 0)
            for number_line in number_lines
        )

        for number_line in number_lines:
            number_line.add_numbers([-1, 0, 1], font_size=24, buff=0.15)
        for plane in complex_planes:
            plane.add_coordinate_labels(font_size=16)

        complex_planes.generate_target()
        complex_planes.target.arrange(DOWN, buff=1.0)
        complex_planes.target.set_height(7)
        complex_planes.target.next_to(x_vect, RIGHT, buff=2.0)
        complex_planes.set_opacity(0)

        R_labels, C_labels = [
            VGroup(
                Tex(Rf"\mathds{{{char}}}", font_size=36).next_to(mob.get_right(), RIGHT)
                for mob in group
            )
            for char, group in zip("RC", [number_lines, complex_planes.target])
        ]

        # Set up dots
        state_tracker = ComplexValueTracker(state)

        dots = GlowDot(color=YELLOW).replicate(len(state))

        def update_dots(dots):
            for dot, value, plane in zip(dots, state_tracker.get_value(), complex_planes):
                dot.move_to(plane.n2p(value))

        dots.add_updater(update_dots)

        dot_lines = VGroup(Line() for dot in dots)
        dot_lines.set_stroke(YELLOW, 2, 0.5)

        def update_dot_lines(lines):
            for line, x, dot in zip(lines, x_vect.elements, dots):
                line.put_start_and_end_on(
                    x.get_right() + 0.05 * RIGHT,
                    dot.get_center()
                )

        update_dot_lines(dot_lines)

        self.play(
            LaggedStartMap(FadeIn, number_lines, lag_ratio=0.25),
            LaggedStartMap(FadeIn, R_labels, lag_ratio=0.25),
            LaggedStart(
                # (FadeInFromPoint(dot, elem.get_center())
                (FadeTransform(elem, dot)
                for elem, dot in zip(dec_vect.elements, dots)),
                lag_ratio=0.05,
                group_type=Group
            ),
            LaggedStart(
                (FadeTransform(elem.copy(), x)
                for elem, x in zip(dec_vect.elements, x_vect.elements)),
                lag_ratio=0.05,
            ),
            LaggedStartMap(ShowCreation, dot_lines),
            ReplacementTransform(dec_vect.get_brackets(), x_vect.get_brackets(), time_span=(1, 2)),
            run_time=2
        )
        self.add(dots, dot_lines)
        dot_lines.add_updater(update_dot_lines)

        self.play(
            state_tracker.animate.set_value(normalize(np.random.uniform(-1, 1, 4))),
            run_time=4
        )

        # Transition to complex plane
        number_lines.generate_target()
        for line, plane in zip(number_lines.target, complex_planes.target):
            line.replace(plane, 0)
            line.set_opacity(0)

        self.play(
            MoveToTarget(complex_planes),
            MoveToTarget(number_lines, remover=True),
            *(FadeTransform(R, C) for R, C in zip(R_labels, C_labels)),
            ReplacementTransform(x_vect, z_vect)
        )
        self.wait()

        for n in range(4):
            self.random_state_change(state_tracker, pump_index=(0 if n == 3 else None))

        # Zoom in on one value
        frame = self.frame

        plane = complex_planes[0]
        c_dot = GlowDot(color=YELLOW, radius=0.05)
        c_dot.move_to(dots[0])

        self.play(
            frame.animate.set_height(1.6).move_to(plane),
            FadeIn(c_dot),
            FadeOut(dots),
            FadeOut(dot_lines),
            run_time=2
        )

        # Show magnitude
        c_line = Line(plane.c2p(0), c_dot.get_center())
        c_line.set_stroke(YELLOW, 2)
        big_brace_width = 3
        brace = Brace(Line(LEFT, RIGHT).set_width(big_brace_width), DOWN)
        brace.scale(c_line.get_length() / big_brace_width, about_point=ORIGIN)
        brace.rotate(c_line.get_angle() + PI, about_point=ORIGIN)
        brace.shift(c_line.get_center())

        mag_label = Tex(R"|z_0|", font_size=12)
        mag_label.next_to(brace.get_center(), DR, buff=0.05),

        self.play(
            ShowCreation(c_line),
            GrowFromCenter(brace),
            FadeIn(mag_label),
        )

        # Show phase
        arc = always_redraw(lambda: Arc(
            0, c_line.get_angle() % TAU, radius=0.1, arc_center=plane.c2p(0),
            stroke_color=MAROON_B
        ))
        arc.update()
        arc.suspend_updating()

        phi_label = Tex(R"\varphi", font_size=12)
        phi_label.set_color(MAROON_B)
        phi_label.add_updater(
            lambda m: m.move_to(arc.pfp(0.5)).shift(0.5 * (arc.pfp(0.5) - plane.c2p(0)))
        )

        self.play(ShowCreation(arc), FadeIn(phi_label))
        self.wait()

        # Show prob
        prob_eq = Tex(R"\text{Prob} = |z_0|^2", font_size=12)
        prob_eq.move_to(mag_label)
        prob_eq.align_to(C_labels[0], RIGHT).shift(0.2 * RIGHT)

        self.play(
            TransformFromCopy(mag_label, prob_eq["|z_0|"][0], path_arc=45 * DEG),
            Write(prob_eq[R"\text{Prob} ="][0]),
            Write(prob_eq["2"][0]),
        )
        self.wait()

        # Change phase
        c_dot.add_updater(lambda m: m.move_to(c_line.get_end()))
        ghost_line = c_line.copy().set_stroke(opacity=0.5)

        self.add(ghost_line)
        arc.resume_updating()
        phi = c_line.get_angle() % TAU
        for angle in [-(1 - 1e-5) * phi, PI, phi - PI]:
            self.play(
                Rotate(c_line, angle, about_point=plane.n2p(0), run_time=6),
            )
            self.wait()

        # Zoom back out
        fader = Group(prob_eq, mag_label, brace, c_line, c_dot, arc, phi_label, ghost_line)
        fader.clear_updaters()
        dot_lines.set_stroke(opacity=0.25)
        self.play(
            frame.animate.to_default_state(),
            FadeOut(fader),
            FadeIn(dots),
            FadeIn(dot_lines),
            run_time=4
        )

        # More random motion
        self.random_state_change(state_tracker)

        dots.suspend_updating()
        self.play(
            *(
                Rotate(
                    dot,
                    random.random() * 2 * TAU,
                    about_point=plane.c2p(0),
                    run_time=10,
                    rate_func=there_and_back,
                )
                for dot, plane in zip(dots, complex_planes)
            )
        )
        dots.resume_updating()

        for n in range(4):
            self.random_state_change(state_tracker)

    def random_state_change(self, state_tracker, pump_index=None, run_time=2):
        rands = np.random.uniform(-1, 1, 4)
        if pump_index is not None:
            rands[pump_index] = 4
        mags = normalize(rands)
        phases = np.exp(TAU * np.random.random(4) * 1j)
        new_state = mags * phases
        self.play(state_tracker.animate.set_value(new_state), run_time=2)
