# ==============================================================================
# Scene:      FromODEToVectorField
# Source:     videos/_2019/diffyq/part1/staging.py (lines 2170-2207)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl FromODEToVectorField.py FromODEToVectorField -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_vector_symbol(*texs, **kwargs):
    config = {
        "include_background_rectangle": True,
        "bracket_h_buff": SMALL_BUFF,
        "bracket_v_buff": SMALL_BUFF,
        "element_alignment_corner": ORIGIN,
    }
    config.update(kwargs)
    array = [[tex] for tex in texs]
    return Matrix(array, **config)



# ----- From _2019/diffyq/part1/staging.py -----

class FromODEToVectorField(Scene):
    def construct(self):
        matrix_config = {
            "bracket_v_buff": 2 * SMALL_BUFF,
            "element_to_mobject_config": {
                "tex_to_color_map": {
                    "x": GREEN,
                    "y": RED,
                    "z": BLUE,
                },
            }
        }
        vect = get_vector_symbol(
            "x(t)", "y(t)", "z(t)",
            **matrix_config,
        )
        d_vect = get_vector_symbol(
            "\\sigma\\big(y(t) - x(t)\\big)",
            "x(t)\\big(\\rho - z(t)\\big) - y(t)",
            "x(t)y(t) - \\beta z(t)",
            **matrix_config
        )
        equation = VGroup(
            OldTex("d \\over dt").scale(1.5),
            vect,
            OldTex("="),
            d_vect
        )
        equation.scale(0.8)
        equation.arrange(RIGHT)
        equation.to_edge(UP)

        arrow = Vector(DOWN, color=YELLOW)
        arrow.next_to(equation, DOWN)

        self.add(equation)
        self.play(ShowCreation(arrow))
        self.wait()
