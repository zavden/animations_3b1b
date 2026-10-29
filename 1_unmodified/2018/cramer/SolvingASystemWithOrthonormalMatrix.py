# ==============================================================================
# Scene:      SolvingASystemWithOrthonormalMatrix
# Source:     videos/_2018/cramer.py (lines 1263-1437)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SolvingASystemWithOrthonormalMatrix.py SolvingASystemWithOrthonormalMatrix -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

X_COLOR = GREEN


Y_COLOR = RED


Z_COLOR = BLUE


OUTPUT_COLOR = YELLOW


INPUT_COLOR = MAROON_B


class LinearSystem(VGroup):
    CONFIG = {
        "matrix_config": {
            "element_to_mobject": Integer,
        },
        "dimensions": 3,
        "min_int": -9,
        "max_int": 10,
        "height": 4,
    }

    def __init__(self, matrix=None, output_vect=None, **kwargs):
        VGroup.__init__(self, **kwargs)
        if matrix is None:
            dim = self.dimensions
            matrix = np.random.randint(
                self.min_int,
                self.max_int,
                size=(dim, dim)
            )
        else:
            dim = len(matrix)
        self.matrix_mobject = Matrix(matrix, **self.matrix_config)
        self.equals = OldTex("=")
        self.equals.scale(1.5)

        colors = [X_COLOR, Y_COLOR, Z_COLOR][:dim]
        chars = ["x", "y", "z"][:dim]
        self.input_vect_mob = Matrix(np.array(chars))
        self.input_vect_mob.elements.set_color_by_gradient(*colors)

        if output_vect is None:
            output_vect = np.random.randint(
                self.min_int, self.max_int, size=(dim, 1))
        self.output_vect_mob = IntegerMatrix(output_vect)
        self.output_vect_mob.elements.set_color(OUTPUT_COLOR)

        for mob in self.matrix_mobject, self.input_vect_mob, self.output_vect_mob:
            mob.set_height(self.height)

        self.add(
            self.matrix_mobject,
            self.input_vect_mob,
            self.equals,
            self.output_vect_mob,
        )
        self.arrange(RIGHT, buff=SMALL_BUFF)


class SolvingASystemWithOrthonormalMatrix(LinearTransformationScene):
    CONFIG = {
        "array_scale_factor": 0.6,
    }

    def construct(self):
        # Setup system
        angle = TAU / 12
        matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        output_vect = [1, 2]
        symbolic_matrix = [
            ["\\cos(30^\\circ)", "-\\sin(30^\\circ)"],
            ["\\sin(30^\\circ)", "\\cos(30^\\circ)"],
        ]
        system = LinearSystem(
            matrix=symbolic_matrix,
            output_vect=output_vect,
            matrix_config={
                "h_buff": 2.5,
                "element_to_mobject": Tex,
            },
            height=1.25,
        )
        system.to_corner(UL)
        system.matrix_mobject.set_column_colors(X_COLOR, Y_COLOR)
        system.input_vect_mob.elements.set_color(WHITE)
        system_rect = BackgroundRectangle(system, buff=MED_SMALL_BUFF)

        matrix_brace = Brace(system.matrix_mobject, DOWN, buff=SMALL_BUFF)
        orthonomal_label = OldTexText("Orthonormal")
        orthonomal_label.set_color(WHITE)
        orthonomal_label.next_to(matrix_brace, DOWN, SMALL_BUFF)
        orthonomal_label.add_background_rectangle()

        # Input and output vectors
        output_vect_mob = self.get_vector(output_vect, color=OUTPUT_COLOR)
        output_vect_label = system.output_vect_mob.copy()
        output_vect_label.add_background_rectangle()
        output_vect_label.scale(self.array_scale_factor)
        output_vect_label.next_to(
            output_vect_mob.get_end(), RIGHT, buff=SMALL_BUFF)

        input_vect = np.dot(np.linalg.inv(matrix), output_vect)
        input_vect_mob = self.get_vector(input_vect, color=INPUT_COLOR)
        input_vect_label = OldTexText("Mystery input vector")
        input_vect_label.add_background_rectangle()
        input_vect_label.next_to(input_vect_mob.get_end(), RIGHT, SMALL_BUFF)
        input_vect_label.match_color(input_vect_mob)

        # Column arrays
        column_mobs = VGroup()
        for i, vect in zip(list(range(2)), [DR, DL]):
            elements = system.matrix_mobject.deepcopy().mob_matrix[:, i]
            column_mob = MobjectMatrix(elements)
            column_mob.add_background_rectangle()
            column_mob.scale(self.array_scale_factor)
            column_mob.next_to(
                self.get_vector(matrix[:, i]).get_end(), vect,
                buff=SMALL_BUFF
            )
            column_mobs.add(column_mob)
        column_mobs[1].shift(SMALL_BUFF * UP)

        # Dot product lines
        x_point = self.plane.coords_to_point(input_vect[0], 0)
        y_point = self.plane.coords_to_point(0, input_vect[1])
        input_dashed_lines = VGroup(
            DashedLine(input_vect_mob.get_end(), x_point),
            DashedLine(input_vect_mob.get_end(), y_point),
        )
        output_dashed_lines = input_dashed_lines.copy()
        output_dashed_lines.apply_matrix(matrix)

        self.add_foreground_mobjects(system_rect, system)
        self.add_foreground_mobjects(matrix_brace, orthonomal_label)
        self.add_foreground_mobjects(output_vect_mob, output_vect_label)
        self.plane.set_stroke(width=2)

        self.apply_matrix(matrix)
        self.wait()
        self.play(LaggedStartMap(ShowCreation, output_dashed_lines))
        self.play(*self.get_column_animations(system.matrix_mobject, column_mobs))
        self.wait()
        self.remove(*output_dashed_lines)
        self.apply_inverse(matrix, added_anims=[
            FadeOut(column_mobs),
            ReplacementTransform(output_vect_mob.copy(), input_vect_mob),
            ReplacementTransform(
                output_dashed_lines.copy(), input_dashed_lines),
            FadeIn(input_vect_label),
        ])
        self.wait()
        self.remove(input_dashed_lines, input_vect_mob)
        self.apply_matrix(matrix, added_anims=[
            FadeOut(input_vect_label),
            ReplacementTransform(input_vect_mob.copy(), output_vect_mob),
            ReplacementTransform(input_dashed_lines.copy(),
                                 output_dashed_lines),
            FadeIn(column_mobs),
        ])

        # Write dot product equations
        equations = VGroup()
        for i in 0, 1:
            moving_output_vect_label = output_vect_label.copy()
            moving_column_mob = column_mobs[i].copy()
            moving_var = system.input_vect_mob.elements[i].copy()
            equation = VGroup(
                moving_var.generate_target(),
                OldTex("="),
                moving_output_vect_label.generate_target(),
                OldTex("\\cdot"),
                moving_column_mob.generate_target(use_deepcopy=True)
            )
            equation.movers = VGroup(
                moving_var, moving_output_vect_label, moving_column_mob
            )
            for element in moving_column_mob.target.get_family():
                if not isinstance(element, Tex):
                    continue
                tex_string = element.get_tex()
                if "sin" in tex_string or "cos" in tex_string:
                    element.set_stroke(width=1)
                    element.scale(1.25)
            equation.to_write = equation[1::2]
            equation[2].match_height(equation[4])
            equation.arrange(RIGHT, buff=SMALL_BUFF)
            equation.background_rectangle = BackgroundRectangle(equation)
            equation.add_to_back(equation.background_rectangle)
            equations.add(equation)
        equations.arrange(DOWN, buff=MED_LARGE_BUFF)
        equations.scale(1.25)
        equations.to_corner(UR, buff=MED_SMALL_BUFF)
        equations_rect = BackgroundRectangle(equations, buff=MED_LARGE_BUFF)
        equations_rect.set_fill(opacity=0.9)

        for i, equation in enumerate(equations):
            anims = [
                FadeIn(equation.background_rectangle),
                Write(equation.to_write),
                LaggedStartMap(
                    MoveToTarget, equation.movers,
                    path_arc=60 * DEGREES
                )
            ]
            if i == 0:
                anims.insert(0, FadeIn(equations_rect))
            self.play(*anims)
            self.wait()

    def get_column_animations(self, matrix_mobject, column_mobs):
        def get_kwargs(i):
            return {
                "rate_func": squish_rate_func(smooth, 0.4 * i, 0.6 + 0.4 * i),
                "run_time": 2,
            }
        return list(it.chain(*[
            [
                FadeIn(cm[0], **get_kwargs(i)),
                ReplacementTransform(
                    matrix_mobject.brackets.copy(),
                    cm.brackets,
                    **get_kwargs(i)
                ),
                ReplacementTransform(
                    VGroup(*matrix_mobject.mob_matrix[:, i]).copy(),
                    cm.elements,
                    **get_kwargs(i)
                ),
            ]
            for i, cm in enumerate(column_mobs)
        ]))
