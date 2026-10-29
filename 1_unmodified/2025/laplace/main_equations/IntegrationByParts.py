# ==============================================================================
# Scene:      IntegrationByParts
# Source:     videos/_2025/laplace/main_equations.py (lines 2155-2196)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntegrationByParts.py IntegrationByParts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntegrationByParts(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"{s}": YELLOW, "{t}": BLUE, R"\omega": PINK}
        steps = VGroup(
            Tex(R"X = \int^\infty_0 \cos(\omega{t}) e^{\minus {s}{t}}d{t}", t2c=t2c),
            Tex(R"X = \left[\frac{1}{\omega} \sin(\omega{t}) e^{\minus {s}{t}} \right]_0^\infty - \int^\infty_0 \frac{1}{\omega} \sin(\omega {t}) \left(\minus {s} e^{\minus{s}{t}} \right) d{t}", t2c=t2c),
            Tex(R"X = \frac{s}{\omega} \int^\infty_0 \sin(\omega{t}) e^{\minus{s}{t}} d{t}", t2c=t2c),
            Tex(R"X = \frac{s}{\omega} \left(\left[\frac{\minus 1}{\omega} \cos(\omega{t}) e^{\minus {s}{t}} \right]_0^\infty - \int^\infty_0 \frac{\minus 1}{\omega} \cos(\omega{t}) \left(\minus {s} e^{\minus{s}{t}} \right) d{t} \right)", t2c=t2c),
            Tex(R"X = \frac{s}{\omega} \left(\frac{1}{\omega} - \frac{s}{\omega} \int^\infty_0 \cos(\omega{t}) e^{\minus{s}{t}} d{t} \right)", t2c=t2c),
            Tex(R"X = \frac{s}{\omega^2} \left(1 - {s} X \right)", t2c=t2c),
            Tex(R"X\left(\omega^2 + {s}^2 \right) = {s}", t2c=t2c),
            Tex(R"X = \frac{s}{\omega^2 + {s}^2}", t2c=t2c),
        )
        steps.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        steps.to_edge(LEFT, buff=LARGE_BUFF)

        randy = Randolph(mode="raise_left_hand")
        randy.to_edge(DOWN)
        steps[0].save_state()
        steps[0].next_to(randy, UL, MED_LARGE_BUFF)
        randy.look_at(steps[0])

        ibp = Tex(R"\int u \, dv = uv - \int v \, du", t2c={"u": RED, "v": PINK})
        ibp.next_to(randy, UR, MED_LARGE_BUFF)

        self.add(randy, steps[0])
        self.play(Blink(randy))
        self.play(
            randy.change("raise_right_hand", ibp),
            FadeIn(ibp, UP)
        )
        self.wait()
        self.play(
            self.frame.animate.set_height(steps.get_height() + 3, about_edge=LEFT),
            Restore(steps[0]),
            Write(steps[1:], run_time=2),
            randy.change("pondering", 5 * UL).shift(6 * RIGHT + 2 * DOWN),
            ibp.animate.shift(6 * RIGHT + 3 * DOWN),
        )
        self.play(randy.animate.look_at(steps[-1]))
        self.wait()
