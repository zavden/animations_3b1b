# ==============================================================================
# Scene:      EllipticFunctions
# Source:     videos/_2026/print_gallery/misc_scenes.py (lines 4-108)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EllipticFunctions.py EllipticFunctions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EllipticFunctions(InteractiveScene):
    def construct(self):
        # Create two planes
        x_max = 15
        in_plane, out_plane = planes = VGroup(
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
        )
        in_plane.set_width(5.5)
        out_plane.set_width(5.5)
        in_plane.add_coordinate_labels(
            list(range(-x_max, x_max + 1, 5)) + [x * 1j for x in list(range(-x_max, x_max + 1, 5)) if x != 0],
            font_size=10
        )
        out_plane.add_coordinate_labels(
            list(range(-x_max, x_max + 1, 5)) + [x * 1j for x in list(range(-x_max, x_max + 1, 5)) if x != 0],
            font_size=10
        )
        in_plane.coordinate_labels.shift(UR * 0.06)
        out_plane.coordinate_labels.shift(UR * 0.06)
        in_plane.set_stroke(GREY_D, 1)
        out_plane.set_stroke(GREY_D, 1)
        VGroup(in_plane, out_plane).arrange(buff=0.75).to_edge(DOWN, buff=0.5)
        self.add(in_plane, out_plane)
        self.add(Dot(radius=0.04).set_color(WHITE).set_stroke(width=4, color=BLACK).move_to(in_plane.n2p(0)))

        z = Tex("z", font_size=70).set_color(YELLOW).next_to(in_plane, UP, buff=0.2).set_x(in_plane.c2p(0)[0])
        f_of_z = Tex(
            r"""
                \wp(z)=\frac{1}{z^2}+\sum_{\lambda \in \left\{k_1 \omega_1+k_2 \omega_2\right\}}
                \left(\frac{1}{(z-\lambda)^2}-\frac{1}{\lambda^2}\right)
            """,
            font_size=28,
            tex_to_color_map={r"\wp": PINK, "z": YELLOW, r"\lambda": BLUE, r"\omega_1": GREEN, r"\omega_2": RED}
        ).next_to(
            out_plane, UP, buff=0.2
        ).set_x(
            out_plane.c2p(0)[0]
        )
        self.add(z, f_of_z)

        # Add lattice points
        omega1 = 1 + 1j
        omega2 = 2 - 3j
        omega1_dot = GlowDot().set_color(GREEN).move_to(in_plane.n2p(omega1))
        omega2_dot = omega1_dot.copy().set_color(RED).move_to(in_plane.n2p(omega2))
        omega1_label = Tex(
            r"\omega_1", font_size=30
        ).set_color(
            GREEN
        ).set_stroke(
            width=7, color=BLACK, behind=True
        ).next_to(
            omega1_dot, UR, buff=-0.1
        )
        omega2_label = Tex(
            r"\omega_2", font_size=30
        ).set_color(
            RED
        ).set_stroke(
            width=7, color=BLACK, behind=True
        ).next_to(
            omega2_dot, UR, buff=-0.1
        )

        lattice = VGroup()
        lambdas = []
        for k1 in range(-20, 20):
            for k2 in range(-10, 10):
                lamb = k1 * omega1 + k2 * omega2
                if lamb != 0 and lamb.real >= -x_max and lamb.real <= x_max and lamb.imag >= -x_max and lamb.imag <= x_max:
                    lambdas.append(lamb)
                    dot = Dot(radius=0.04).set_color(BLUE).set_opacity(0.9).move_to(in_plane.n2p(lamb))
                    lattice.add(dot)
        self.add(lattice, omega1_dot, omega1_label, omega2_dot, omega2_label)

        # Add z dot
        offset = -0.3 * omega1 + 0.9 * omega2
        z_init = offset
        z_dot = GlowDot().set_color(YELLOW).move_to(in_plane.n2p(z_init))
        z_label = Tex("z", font_size=35).set_color(YELLOW).set_stroke(width=7, color=BLACK, behind=True)
        z_label.add_updater(lambda m: m.next_to(z_dot, UL, buff=-0.1))
        # z_tail = TracingTail(z_dot, stroke_color = YELLOW, time_traced = 6)
        self.add(z_dot, z_label)

        # Add p(z) dot
        def p(z):
            return 1 / z**2 + sum([1 / (z - lamb)**2 - 1 / lamb**2 for lamb in lambdas])

        p_z_dot = GlowDot().set_color(PINK)
        p_z_dot.add_updater(lambda m: m.move_to(out_plane.n2p(p(in_plane.p2n(z_dot.get_center())))))
        p_z_label = Tex(
            r"\wp(z)", font_size=35, tex_to_color_map={r"\wp": PINK, "z": YELLOW}
        ).set_stroke(width=7, color=BLACK, behind=True)
        p_z_label.add_updater(lambda m: m.next_to(p_z_dot, UR, buff=-0.1))
        p_z_tail = TracingTail(p_z_dot, stroke_color=PINK, time_traced=6)
        self.add(p_z_dot, p_z_label, p_z_tail)

        # Move z around
        # choices = [omega1, omega2, -omega1, -omega2, omega1 + omega2, omega1 - omega2, -omega1 + omega2, -omega1 -omega2]
        choices = [omega1, omega2, -omega1, -omega2]
        for _ in range(10):
            next_point = in_plane.p2n(z_dot.get_center()) + random.choice(choices)
            self.play(z_dot.animate.move_to(in_plane.n2p(next_point)), run_time=3)
            self.wait(0.6)
