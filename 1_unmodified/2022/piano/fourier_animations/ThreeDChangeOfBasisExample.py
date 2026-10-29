# ==============================================================================
# Scene:      ThreeDChangeOfBasisExample
# Source:     videos/_2022/piano/fourier_animations.py (lines 802-931)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDChangeOfBasisExample.py ThreeDChangeOfBasisExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeDChangeOfBasisExample(Scene):
    def construct(self):
        # Add axes and standard basis
        frame = self.camera.frame
        frame.reorient(-20, 75)
        frame.shift(OUT)
        frame.add_updater(lambda m: m.set_theta(
            -20 * math.cos(TAU * self.time / 60) * DEGREES,
        ))

        axes = ThreeDAxes(axis_config=dict(tick_size=0.05))
        axes.set_stroke(width=1)
        plane = NumberPlane(faded_line_ratio=0)
        plane.set_stroke(GREY, 1, 0.5)
        basis_mobs = VGroup(
            Vector(RIGHT, color=RED),
            Vector(UP, color=GREEN),
            Vector(OUT, color=BLUE),
        )

        signal = Vector([-3, 1, 2], color=YELLOW)
        signal.set_opacity(0.75)
        signal_label = Text("Signal")
        signal_label.rotate(90 * DEGREES, RIGHT)
        signal_label.match_color(signal)
        signal_label.add_updater(lambda m: m.next_to(signal.get_end(), OUT))
        coef_label = self.get_coef_label(signal, basis_mobs)

        self.add(axes)
        self.add(plane)
        self.add(basis_mobs)
        self.add(signal)
        self.add(signal_label)
        self.add(coef_label)
        for mob in self.mobjects:
            mob.apply_depth_test()

        # Show components
        components = always_redraw(
            self.get_linear_combination, signal, basis_mobs
        )
        components.suspend_updating()
        self.animate_linear_combination(basis_mobs, components)
        self.wait(2)
        components.resume_updating()
        self.add(components)
        for v in [[-1, 1, 0.5], [1, 1, 0.25], [2, 1, 2]]:
            self.play(
                signal.animate.put_start_and_end_on(ORIGIN, v),
                run_time=3
            )
            self.wait()
        self.wait(5)

        # Change of basis
        rot_matrix = rotation_between_vectors([1, 1, 1], OUT)
        new_basis = rot_matrix.T

        basis_mobs.generate_target()
        for basis_mob, new_vector in zip(basis_mobs.target, new_basis):
            basis_mob.put_start_and_end_on(ORIGIN, new_vector)

        self.play(FadeOut(components))
        self.play(MoveToTarget(basis_mobs, run_time=2))
        self.wait()
        components.update()
        for comp in components:
            self.play(GrowArrow(comp))
        self.add(components)
        for vect in [[1, 0, 2]]:
            self.play(signal.animate.put_start_and_end_on(ORIGIN, vect), run_time=3)
            self.wait()

        frame.suspend_updating()

        self.embed()

    def get_coefficients(self, vect_mob, basis_mobs):
        cob_inv = np.array([
            b.get_vector()
            for b in basis_mobs
        ]).T
        cob = np.linalg.inv(cob_inv)
        return np.dot(cob, vect_mob.get_vector())

    def get_linear_combination(self, vect_mob, basis_mobs):
        coefs = self.get_coefficients(vect_mob, basis_mobs)
        components = VGroup()
        last_point = vect_mob.get_start()
        for coef, basis in zip(coefs, basis_mobs):
            comp = Vector(coef * basis.get_vector())
            comp.match_style(basis)
            comp.set_stroke(opacity=0.5)
            comp.shift(last_point - comp.get_start())
            last_point = comp.get_end()
            components.add(comp)
        return components

    def animate_linear_combination(self, basis_mobs, components):
        for basis, part in zip(basis_mobs, components):
            self.play(TransformFromCopy(basis, part))

    def get_coef_label(self, vect_mob, basis_mobs, lhs_tex="\\vec{\\textbf{s}}"):
        label = VGroup()
        lhs = OldTex(lhs_tex + "=")
        label.numbers = VGroup(*(
            DecimalNumber(include_sign=True)
            for b in basis_mobs
        ))
        label.basis_labels = VGroup(*(
            OldTex("\\vec{\\textbf{v}}_1", color=RED),
            OldTex("\\vec{\\textbf{v}}_2", color=GREEN),
            OldTex("\\vec{\\textbf{v}}_3", color=BLUE),
        ))

        label.add(lhs)
        label.add(*it.chain(*zip(
            label.numbers, label.basis_labels
        )))
        label.fix_in_frame()
        label.arrange(RIGHT, buff=SMALL_BUFF)
        label.to_corner(UL)

        def update_label(label):
            coefs = self.get_coefficients(vect_mob, basis_mobs)
            for coef, number in zip(coefs, label.numbers):
                number.set_value(coef)

        label.add_updater(update_label)
        return label
