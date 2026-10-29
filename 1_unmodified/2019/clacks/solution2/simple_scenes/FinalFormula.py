# ==============================================================================
# Scene:      FinalFormula
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 495-535)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FinalFormula.py FinalFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FinalFormula(Scene):
    def construct(self):
        text = OldTexText("Final answer: ")
        t2c_map = {
            "\\theta": BLUE,
            "m_1": GREEN,
            "m_2": RED,
        }

        formula = OldTex(
            "\\left\\lfloor",
            "{\\pi", "\\over", "\\theta}",
            "\\right\\rfloor"
        )
        formula.set_color_by_tex_to_color_map(t2c_map)
        group = VGroup(text, formula)
        group.arrange(RIGHT)
        group.scale(1.5)
        group.to_edge(UP)

        self.play(Write(text))
        self.play(FadeIn(formula))
        self.play(ShowCreationThenFadeAround(formula))
        self.wait()

        theta_eq = OldTex(
            "\\theta", "=", "\\arctan", "\\left(",
            "\\sqrt",
            "{{m_2", "\\over", "m_1}}",
            "\\right)"
        )
        theta_eq.set_color_by_tex_to_color_map(t2c_map)
        theta_eq.scale(1.5)
        theta_eq.next_to(group, DOWN, MED_LARGE_BUFF)

        self.play(TransformFromCopy(
            formula.get_part_by_tex("\\theta"),
            theta_eq.get_part_by_tex("\\theta"),
        ))
        self.play(Write(theta_eq[1:]))
        self.wait()
