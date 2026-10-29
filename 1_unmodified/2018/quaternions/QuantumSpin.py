# ==============================================================================
# Scene:      QuantumSpin
# Source:     videos/_2018/quaternions.py (lines 1049-1113)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuantumSpin.py QuantumSpin -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuantumSpin(Scene):
    def construct(self):
        title = Title("Two-state system")

        electron = Dot(color=BLUE)
        electron.set_height(1)
        electron.set_sheen(0.3, UL)
        electron.set_fill(opacity=0.8)
        kwargs = {
            "path_arc": PI,
        }
        curved_arrows = VGroup(
            Arrow(RIGHT, LEFT, **kwargs),
            Arrow(LEFT, RIGHT, **kwargs),
        )
        curved_arrows.set_color(GREY_B)
        curved_arrows.set_stroke(width=2)

        y_arrow = Vector(UP)
        y_arrow.set_color(RED)

        y_ca = curved_arrows.copy()
        y_ca.rotate(70 * DEGREES, LEFT)
        y_group = VGroup(y_ca[0], y_arrow, electron.copy(), y_ca[1])

        x_arrow = y_arrow.copy().rotate(90 * DEGREES, IN, about_point=ORIGIN)
        x_arrow.set_color(GREEN)
        x_ca = curved_arrows.copy()
        x_ca.rotate(70 * DEGREES, UP)
        x_group = VGroup(x_ca[0], x_arrow, electron.copy(), x_ca[1])

        z_ca = curved_arrows.copy()
        z_group = VGroup(electron.copy(), z_ca, Dot(color=BLUE))

        groups = VGroup(x_group, y_group, z_group)
        groups.arrange(RIGHT, buff=1.5)
        groups.move_to(UP)

        y_ca.rotation = Rotating(
            y_ca, axis=rotate_vector(OUT, 70 * DEGREES, LEFT)
        )
        x_ca.rotation = Rotating(
            x_ca, axis=rotate_vector(OUT, 70 * DEGREES, UP)
        )
        z_ca.rotation = Rotating(z_ca, axis=OUT)
        rotations = [ca.rotation for ca in [x_ca, y_ca, z_ca]]

        matrices = VGroup(
            Matrix([["0", "1"], ["1", "0"]]),
            Matrix([["0", "-i"], ["i", "0"]]),
            Matrix([["1", "0"], ["0", "-1"]]),
        )
        for matrix, group in zip(matrices, groups):
            matrix.next_to(group, DOWN)
        for matrix in matrices[1:]:
            matrix.align_to(matrices[0], DOWN)

        self.add(title, groups)
        self.play()
        self.play(
            LaggedStartMap(FadeInFromDown, matrices, run_time=3),
            *rotations
        )
        for x in range(2):
            self.play(*rotations)
