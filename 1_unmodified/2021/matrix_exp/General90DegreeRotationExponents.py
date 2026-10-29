# ==============================================================================
# Scene:      General90DegreeRotationExponents
# Source:     videos/_2021/matrix_exp.py (lines 4922-4974)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl General90DegreeRotationExponents.py General90DegreeRotationExponents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_matrix_exponential(matrix, height=1.5, scalar_tex="t", **matrix_config):
    elem = matrix[0][0]
    if isinstance(elem, str):
        mat_class = Matrix
    elif isinstance(elem, int) or isinstance(elem, np.int64):
        mat_class = IntegerMatrix
    else:
        mat_class = DecimalMatrix

    matrix = mat_class(matrix, **matrix_config)
    base = OldTex("e")
    base.set_height(0.4 * height)
    matrix.set_height(0.6 * height)
    matrix.move_to(base.get_corner(UR), DL)
    result = VGroup(base, matrix)
    if scalar_tex:
        scalar = OldTex(scalar_tex)
        scalar.set_height(0.7 * base.get_height())
        scalar.next_to(matrix, RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        result.add(scalar)
    return result


class General90DegreeRotationExponents(Scene):
    def construct(self):
        # Setup
        exps = VGroup(
            get_matrix_exponential([["0", "-1"], ["1", "0"]]),
            OldTex("e^{it}", tex_to_color_map={"i": RED}),
            OldTex(
                "e^{(ai + bj + ck)t}",
                tex_to_color_map={
                    "i": RED,
                    "j": GREEN,
                    "k": BLUE,
                }
            ),
            OldTex(
                "e^{i \\sigma_x t}, \\quad ",
                "e^{i \\sigma_y t}, \\quad ",
                "e^{i \\sigma_z t}",
                tex_to_color_map={
                    "\\sigma_x": RED,
                    "\\sigma_y": GREEN,
                    "\\sigma_z": BLUE,
                }
            ),
        )
        exps[0][1].set_color(TEAL)
        exps[0].scale(0.5)

        exps.arrange(DOWN, buff=1.5, aligned_edge=LEFT)

        labels = VGroup(
            OldTexText("$90^\\circ$ rotation matrix"),
            OldTexText("Imaginary numbers"),
            OldTexText("Quaternions"),
            OldTexText("Pauli matrices"),
        )
        for label, exp in zip(labels, exps):
            label.scale(0.75)
            label.next_to(exp, LEFT, LARGE_BUFF, aligned_edge=DOWN)
            label.align_to(labels[0], LEFT)

        VGroup(exps, labels).to_edge(LEFT)

        quat_note = OldTex("(a^2 + b^2 + c^2 = 1)", font_size=24)
        quat_note.next_to(exps[2], DOWN, aligned_edge=LEFT)
        exps[2].add(quat_note)

        for exp, label in zip(exps, labels):
            self.play(
                FadeIn(exp),
                FadeIn(label),
            )
        self.wait()
