# ==============================================================================
# Scene:      ThreeBodyEquation
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 602-641)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeBodyEquation.py ThreeBodyEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeBodyEquation(Scene):
    def construct(self):
        x1 = "\\vec{\\textbf{x}}_1"
        x2 = "\\vec{\\textbf{x}}_2"
        x3 = "\\vec{\\textbf{x}}_3"
        kw = {
            "tex_to_color_map": {
                x1: RED,
                x2: GREEN,
                x3: BLUE,
            }
        }
        equations = VGroup(*[
            OldTex(
                "{d^2", t1, "\\over dt^2}", "=",
                "G", "\\left("
                "{" + m2, "(", t2, "-", t1, ")"
                "\\over"
                "||", t2, "-", t1, "||^3}",
                "+",
                "{" + m3, "(", t3, "-", t1, ")"
                "\\over"
                "||", t3, "-", t1, "||^3}",
                "\\right)",
                **kw
            )
            for t1, t2, t3, m1, m2, m3 in [
                (x1, x2, x3, "m_1", "m_2", "m_3"),
                (x2, x3, x1, "m_2", "m_3", "m_1"),
                (x3, x1, x2, "m_3", "m_1", "m_2"),
            ]
        ])
        equations.arrange(DOWN, buff=LARGE_BUFF)

        self.play(LaggedStartMap(
            FadeInFrom, equations,
            lambda m: (m, UP),
            lag_ratio=0.2,
        ))
        self.wait()
