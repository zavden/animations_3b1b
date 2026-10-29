# ==============================================================================
# Scene:      ExponentialsMoreBroadly
# Source:     videos/_2019/diffyq/part4/staging.py (lines 2199-2317)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExponentialsMoreBroadly.py ExponentialsMoreBroadly -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo vector field as a group of arrows, with delta_x/delta_y and get_vector, instead of the current GL API.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import CairoVectorField as VectorField

class ExponentialsMoreBroadly(Scene):
    def construct(self):
        self.write_fourier_series()
        self.pull_out_complex_exponent()
        self.show_matrix_exponent()

    def write_fourier_series(self):
        formula = OldTex(
            "f({t}) = "
            "\\sum_{n = -\\infty}^\\infty",
            "c_{n}", "e^{{n} \\cdot 2\\pi i {t}}"
            "",
            tex_to_color_map={
                "{t}": LIGHT_PINK,
                "{n}": YELLOW
            }
        )
        formula[2][4].set_color(YELLOW)
        formula.scale(1.5)
        formula.to_edge(UP)
        formula.add_background_rectangle_to_submobjects()

        plane = ComplexPlane(
            axis_config={"unit_size": 2}
        )

        self.play(FadeInFromDown(formula))
        self.wait()
        self.add(plane, formula)
        self.play(
            formula.scale, 0.7,
            formula.to_corner, UL,
            ShowCreation(plane)
        )

        self.formula = formula
        self.plane = plane

    def pull_out_complex_exponent(self):
        formula = self.formula

        c_exp = OldTex("e^{it}")
        c_exp[0][2].set_color(LIGHT_PINK)
        c_exp.set_stroke(BLACK, 3, background=True)
        c_exp.move_to(formula.get_part_by_tex("e^"), DL)
        c_exp.set_opacity(0)

        dot = Dot()
        circle = Circle(radius=2)
        circle.set_color(YELLOW)
        dot.add_updater(lambda d: d.move_to(circle.get_end()))

        self.play(
            c_exp.set_opacity, 1,
            c_exp.scale, 1.5,
            c_exp.next_to, dot, UR, SMALL_BUFF,
            GrowFromCenter(dot),
        )
        c_exp.add_updater(
            lambda m: m.next_to(dot, UR, SMALL_BUFF)
        )
        self.play(
            ShowCreation(circle),
            run_time=4,
        )
        self.wait()

        self.c_exp = c_exp
        self.circle = circle
        self.dot = dot

    def show_matrix_exponent(self):
        c_exp = self.c_exp
        formula = self.formula
        circle = self.circle
        dot = self.dot

        m_exp = OldTex(
            "\\text{exp}\\left("
            "\\left[ \\begin{array}{cc}0 & -1 \\\\ 1 & 0 \\end{array} \\right]",
            "{t} \\right)",
            "=",
            "\\left[ \\begin{array}{cc}"
            "\\cos(t) & -\\sin(t) \\\\ \\sin(t) & \\cos(t)"
            "\\end{array} \\right]",
        )
        VGroup(
            m_exp[1][0],
            m_exp[3][5],
            m_exp[3][12],
            m_exp[3][18],
            m_exp[3][24],
        ).set_color(LIGHT_PINK)
        m_exp.to_corner(UL)
        m_exp.add_background_rectangle_to_submobjects()

        vector_field = VectorField(
            lambda p: rotate_vector(p, TAU / 4),
            max_magnitude=7,
            delta_x=0.5,
            delta_y=0.5,
            length_func=lambda norm: 0.35 * sigmoid(norm),
        )
        vector_field.sort(get_norm)

        self.play(
            FadeInFromDown(m_exp),
            FadeOut(formula, UP),
            FadeOut(c_exp)
        )
        self.add(vector_field, circle, dot, m_exp)
        self.play(
            ShowCreation(
                vector_field,
                lag_ratio=0.001,
            )
        )
        self.play(Rotating(circle, run_time=TAU))
        self.wait()
