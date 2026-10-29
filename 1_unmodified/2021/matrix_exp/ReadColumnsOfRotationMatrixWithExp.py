# ==============================================================================
# Scene:      ReadColumnsOfRotationMatrixWithExp
# Source:     videos/_2021/matrix_exp.py (lines 4285-4286)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReadColumnsOfRotationMatrixWithExp.py ReadColumnsOfRotationMatrixWithExp -w -m --fps 15
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


class ReadColumnsOfRotationMatrix(Scene):
    show_exponent = False

    def construct(self):
        # Setup
        plane = NumberPlane(faded_line_ratio=0)
        plane.scale(3.0)
        plane.shift(1.5 * DOWN)
        b_plane = plane.copy()
        b_plane.set_color(GREY_B)
        b_plane.set_stroke(opacity=0.5)

        angle = 50 * DEGREES
        plane2 = plane.copy().apply_matrix([
            [math.cos(angle), 0],
            [math.sin(angle), 1],
        ], about_point=plane.get_origin())
        plane3 = plane.copy().apply_matrix([
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ], about_point=plane.get_origin())
        coords = plane.deepcopy().add_coordinate_labels((-2, -1, 1, 2), (-1, 1))
        self.add(b_plane, plane, coords)

        equation = VGroup(
            get_matrix_exponential([[0, -1], [1, 0]]),
            OldTex("="),
            Matrix(
                [["\\cos(t)", "-\\sin(t)"], ["\\sin(t)", "\\cos(t)"]],
                h_buff=2.0
            )
        )
        exp, eq, matrix = equation
        exp[1].set_color(TEAL)
        exp[1].add_background_rectangle()
        matrix.add_background_rectangle()
        equation.arrange(RIGHT)
        equation.set_width(6)
        equation.to_corner(UL)

        if not self.show_exponent:
            equation.remove(*equation[:2])
            equation.set_height(1.5)
            equation.to_corner(UL)

        self.add(equation)

        basis_vectors = VGroup(
            Arrow(plane.get_origin(), plane.c2p(1, 0), buff=0, fill_color=GREEN),
            Arrow(plane.get_origin(), plane.c2p(0, 1), buff=0, fill_color=RED),
        )
        basis_shadows = basis_vectors.copy()
        basis_shadows.set_fill(opacity=0.5)
        self.add(basis_shadows, basis_vectors)

        self.play(FlashAround(matrix.get_columns()[0], color=GREEN))
        self.wait()

        # Show action on basis vectors
        rot_b0, rot_b1 = rot_basis_vectors = basis_vectors.copy()
        for rot_b in rot_basis_vectors:
            rot_b.rotate(angle, about_point=plane.get_origin())

        rbl0, rbl1 = rot_basis_labels = VGroup(
            Matrix([["\\cos(t)"], ["\\sin(t)"]]),
            Matrix([["-\\sin(t)"], ["\\cos(t)"]]),
        )
        for label, color, rot_b, direction in zip(rot_basis_labels, [GREEN, RED], rot_basis_vectors, [UR, LEFT]):
            label.set_color(color)
            label.scale(0.7)
            label.next_to(rot_b.get_end(), direction, SMALL_BUFF)
            label.add_background_rectangle()

        arcs = VGroup(
            Arc(0, angle, arc_center=plane.get_origin(), radius=0.5),
            Arc(PI / 2, angle, arc_center=plane.get_origin(), radius=0.5),
        )
        arcs.set_stroke(WHITE, 2)
        arc_label = OldTexText("$t$", " ")
        arc_label.next_to(arcs[0], RIGHT, SMALL_BUFF)
        arc_label.shift(SMALL_BUFF * UP)

        h_line = DashedLine(plane.get_origin(), plane.c2p(math.cos(angle), 0))
        v_line = DashedLine(plane.c2p(math.cos(angle), 0), plane.c2p(math.cos(angle), math.sin(angle)))
        cos_label = matrix.get_entries()[0].copy().next_to(h_line, DOWN, SMALL_BUFF)
        sin_label = matrix.get_entries()[2].copy().next_to(v_line, RIGHT, SMALL_BUFF)

        self.play(
            TransformFromCopy(matrix[0], rbl0[0]),  # Background rectangles
            TransformFromCopy(matrix.get_brackets(), rbl0.get_brackets()),
            TransformFromCopy(matrix.get_columns()[0], rbl0.get_entries()),
            Transform(plane, plane2, path_arc=angle),
            Transform(basis_vectors[0], rot_b0, path_arc=angle),
            Animation(matrix.get_columns()[1]),
            run_time=2,
        )
        rects = VGroup(*(
            SurroundingRectangle(entry, color=WHITE, stroke_width=2, buff=0.05)
            for entry in rbl0.get_entries()
        ))
        self.play(
            ShowCreation(h_line),
            FadeIn(rects[0]),
            FadeIn(cos_label),
        )
        self.play(
            ShowCreation(v_line),
            FadeOut(rects[0]),
            FadeIn(rects[1]),
            FadeIn(sin_label),
        )
        self.play(FadeOut(rects[1]))
        self.wait()
        self.play(FlashAround(matrix.get_columns()[1], color=RED))
        self.play(
            TransformFromCopy(matrix[0], rbl1[0]),  # Background rectangles
            TransformFromCopy(matrix.get_brackets(), rbl1.get_brackets()),
            TransformFromCopy(matrix.get_columns()[1], rbl1.get_entries()),
            Transform(plane, plane3, path_arc=angle),
            Transform(basis_vectors[1], rot_b1, path_arc=angle),
            Animation(matrix.get_columns()[0]),
            run_time=2,
        )
        self.wait()
        self.play(
            FadeIn(arc_label),
            *map(ShowCreation, arcs),
        )
        self.wait()


class ReadColumnsOfRotationMatrixWithExp(ReadColumnsOfRotationMatrix):
    show_exponent = True
