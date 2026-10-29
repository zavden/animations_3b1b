# ==============================================================================
# Scene:      Linearity
# Source:     videos/_2025/laplace/main_equations.py (lines 1777-1804)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Linearity.py Linearity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Linearity(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"f": GREEN, "g": BLUE, R"\mathcal{L}": GREY_A, R"\big\{": WHITE, R"\big\}": WHITE, "a": GREEN_A, "b": BLUE_A}
        lhs = Tex(R"\mathcal{L}\big\{a \cdot f(t) + b \cdot g(t) \big\}", t2c=t2c)
        rhs = Tex(R"a \cdot \mathcal{L} \big\{ f(t) \big\} + b \cdot \mathcal{L} \big\{ g(t) \big\}", t2c=t2c)
        arrow = Vector(RIGHT, thickness=4)
        group = VGroup(lhs, arrow, rhs)
        group.arrange(RIGHT)

        self.add(lhs)
        self.wait()
        self.play(
            GrowArrow(arrow),
            LaggedStart(
                AnimationGroup(*(
                    TransformFromCopy(lhs[tex][0], rhs[tex][0], path_arc=45 * DEG)
                    for tex in [R"\mathcal{L}", R"\big\{", R"a \cdot", "f(t)", R"\big\}"]
                )),
                AnimationGroup(*(
                    TransformFromCopy(lhs[tex][0], rhs[tex][-1], path_arc=-45 * DEG)
                    for tex in ["+", R"\mathcal{L}", R"\big\{", R"b \cdot", "g(t)", R"\big\}"]
                )),
                lag_ratio=0.75,
                run_time=3
            ),
        )
        self.wait()
