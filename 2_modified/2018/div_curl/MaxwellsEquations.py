# ==============================================================================
# Scene:      MaxwellsEquations
# Source:     videos/_2018/div_curl.py (lines 2416-2562)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MaxwellsEquations.py MaxwellsEquations -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - dropped lag_range=0.4: not a parameter of GL Animation/LaggedStartMap (it was silently ignored by sep19 Cairo too)
# ==============================================================================

from manim_imports_ext import *

class MaxwellsEquations(Scene):
    CONFIG = {
        "faded_opacity": 0.3,
    }

    def construct(self):
        self.add_equations()
        self.circle_gauss_law()
        self.circle_magnetic_divergence()
        self.circle_curl_equations()

    def add_equations(self):
        title = Title("Maxwell's equations")
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        tex_to_color_map = {
            "\\textbf{E}": BLUE,
            "\\textbf{B}": YELLOW,
            "\\rho": WHITE,
        }

        equations = self.equations = VGroup(*[
            OldTex(
                tex, tex_to_color_map=tex_to_color_map
            )
            for tex in [
                """
                    \\text{div} \\, \\textbf{E} =
                    {\\rho \\over \\varepsilon_0}
                """,
                """\\text{div} \\, \\textbf{B} = 0""",
                """
                    \\text{curl} \\, \\textbf{E} =
                    -{\\partial \\textbf{B} \\over \\partial t}
                """,
                """
                    \\text{curl} \\, \\textbf{B} =
                    \\mu_0 \\left(
                        \\textbf{J} + \\varepsilon_0
                        {\\partial \\textbf{E} \\over \\partial t}
                    \\right)
                """,
            ]
        ])
        equations.arrange(
            DOWN, aligned_edge=LEFT,
            buff=MED_LARGE_BUFF
        )

        field_definitions = VGroup(*[
            OldTex(text, tex_to_color_map=tex_to_color_map)
            for text in [
                "\\text{Electric field: } \\textbf{E}",
                "\\text{Magnetic field: } \\textbf{B}",
            ]
        ])
        field_definitions.arrange(
            RIGHT, buff=MED_LARGE_BUFF
        )
        field_definitions.next_to(title, DOWN, MED_LARGE_BUFF)
        equations.next_to(field_definitions, DOWN, MED_LARGE_BUFF)
        field_definitions.shift(MED_SMALL_BUFF * UP)

        self.add(title)
        self.add(field_definitions)
        self.play(LaggedStartMap(
            FadeIn, equations,
            # CHANGE: dropped lag_range=0.4: not a parameter of GL Animation/LaggedStartMap (it was silently ignored by sep19 Cairo too)
            run_time=3,
        ))
        self.wait()

    def circle_gauss_law(self):
        equation = self.equations[0]
        rect = SurroundingRectangle(equation)
        rect.set_color(RED)
        rho = equation.get_part_by_tex("\\rho")
        sub_rect = SurroundingRectangle(rho)
        sub_rect.match_color(rect)
        rho_label = OldTexText("Charge density")
        rho_label.next_to(sub_rect, RIGHT)
        rho_label.match_color(sub_rect)
        gauss_law = OldTexText("Gauss's law")
        gauss_law.next_to(rect, RIGHT)

        self.play(
            ShowCreation(rect),
            Write(gauss_law, run_time=1),
            self.equations[1:].set_fill, {"opacity": self.faded_opacity}
        )
        self.wait(2)
        self.play(
            ReplacementTransform(rect, sub_rect),
            FadeOut(gauss_law),
            FadeIn(rho_label),
            rho.match_color, sub_rect,
        )
        self.wait()
        self.play(
            self.equations.to_edge, LEFT,
            MaintainPositionRelativeTo(rho_label, equation),
            MaintainPositionRelativeTo(sub_rect, equation),
            VFadeOut(rho_label),
            VFadeOut(sub_rect),
        )
        self.wait()

    def circle_magnetic_divergence(self):
        equations = self.equations
        rect = SurroundingRectangle(equations[1])

        self.play(
            equations[0].set_fill, {"opacity": self.faded_opacity},
            equations[1].set_fill, {"opacity": 1.0},
        )
        self.play(ShowCreation(rect))
        self.wait(3)
        self.play(FadeOut(rect))

    def circle_curl_equations(self):
        equations = self.equations
        rect = SurroundingRectangle(equations[2:])
        randy = Randolph(height=2)
        randy.flip()
        randy.next_to(rect, RIGHT, aligned_edge=DOWN)
        randy.look_at(rect)

        self.play(
            equations[1].set_fill, {"opacity": self.faded_opacity},
            equations[2:].set_fill, {"opacity": 1.0},
        )
        self.play(ShowCreation(rect))
        self.play(
            randy.change, "confused",
            VFadeIn(randy),
        )
        self.play(Blink(randy))
        self.play(randy.look_at, 2 * RIGHT)
        self.wait(3)
        self.play(
            FadeOut(rect),
            randy.change, "pondering",
            randy.look_at, rect,
        )
        self.wait()
        self.play(Blink(randy))
        self.wait()
