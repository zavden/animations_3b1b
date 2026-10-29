# ==============================================================================
# Scene:      ScalingProperty
# Source:     videos/_2023/clt_proof/main.py (lines 609-647)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ScalingProperty.py ScalingProperty -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ScalingProperty(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(t2c={"c": YELLOW, "t": PINK, "X": WHITE, "Y": WHITE})
        equation = VGroup(
            Tex(R"M_{cX}(t) = ", **kw),
            Tex(R"\mathds{E}[e^{tcX}] = ", **kw),
            Tex(R"M_X(ct)", **kw),
        )
        equation.arrange(RIGHT)

        self.add(equation[0])
        self.wait()
        for i in [0, 1]:
            self.play(TransformMatchingTex(
                equation[i].copy(), equation[i + 1],
                path_arc=-45 * DEGREES
            ))
            self.wait()

        # Equation 2
        equation.generate_target()
        equation.target[1].scale(0).set_opacity(0)
        equation.target.arrange(RIGHT, buff=0.05)

        equation2 = Tex(R"M_{X+Y}(t) = M_X(t)M_Y(t)", **kw)
        equation2.next_to(equation.target, UP, buff=LARGE_BUFF)
        VGroup(equation.target, equation2).center()

        self.play(
            MoveToTarget(equation),
            FadeIn(equation2, UP),
        )
        self.wait()
        self.play(
            FadeOut(equation),
            equation2.animate.to_edge(UP),
        )
        self.wait()
