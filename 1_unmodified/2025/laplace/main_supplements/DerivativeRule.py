# ==============================================================================
# Scene:      DerivativeRule
# Source:     videos/_2025/laplace/main_supplements.py (lines 793-827)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DerivativeRule.py DerivativeRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DerivativeRule(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"t": BLUE, "s": YELLOW}
        kw = dict(t2c=t2c, font_size=96)
        in_texs = VGroup(
            Tex(R"x(t)", **kw),
            Tex(R"x'(t)", **kw),
        )
        out_texs = VGroup(
            Tex(R"X(s)", **kw),
            Tex(R"s X(s) - x(0)", **kw),
        )
        arrows = Vector(3 * RIGHT, thickness=7).replicate(2)

        in_texs.arrange(DOWN, buff=2)
        in_texs.to_edge(LEFT, buff=2)

        for in_tex, arrow, output in zip(in_texs, arrows, out_texs):
            arrow.next_to(in_tex, RIGHT)
            output.next_to(arrow, RIGHT)
            fancy_L = Tex(R"\mathcal{L}")
            fancy_L.next_to(arrow, UP, SMALL_BUFF)
            arrow.add(fancy_L)

        self.add(in_texs[0], arrows[0], out_texs[0])
        self.wait()
        self.play(
            TransformMatchingTex(in_texs[0].copy(), in_texs[1]),
            TransformMatchingTex(out_texs[0].copy(), out_texs[1]),
            TransformFromCopy(*arrows),
            run_time=1.5
        )
        self.wait()
        SpeechBubble
