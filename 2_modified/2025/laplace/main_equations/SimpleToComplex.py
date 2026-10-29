# ==============================================================================
# Scene:      SimpleToComplex
# Source:     videos/_2025/laplace/main_equations.py (lines 1276-1373)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SimpleToComplex.py SimpleToComplex -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - self.play(frame.reorient(...)) -> self.play(frame.animate.reorient(...))
# ==============================================================================

from manim_imports_ext import *

class SimpleToComplex(InteractiveScene):
    def construct(self):
        # Add key expressions
        t2c = {"{t}": BLUE, "{s}": YELLOW}
        terms = VGroup(
            Tex(R"f({t}) = 1", t2c=t2c),
            Tex(R"f({t}) = e^{at}", t2c=t2c),
            Tex(R"f({t}) = \sum_{n=1}^N c_n e^{s_n {t}}", t2c=t2c),
        )
        terms.scale(1.5)
        terms.arrange(DOWN, buff=1.5)
        arrows = VGroup(
            Arrow(*pair, buff=0.25, thickness=5)
            for pair in zip(terms, terms[1:])
        )
        terms[2].shift(SMALL_BUFF * DOWN)

        self.add(terms[0])
        for arrow, term1, term2 in zip(arrows, terms, terms[1:]):
            self.play(
                TransformMatchingTex(
                    term1.copy(),
                    term2,
                    key_map={"1": "e^{at}", "a": "s_n"}
                ),
                GrowArrow(arrow),
                run_time=1
            )
            self.wait()

        # Set up Laplace Transforms
        lt_left_x = terms.get_x(RIGHT) + 3
        lt_arrows = VGroup(
            Arrow(
                term.get_right(),
                lt_left_x * RIGHT + term.get_y() * UP,
                buff=0.5,
                thickness=6
            )
            for term in terms
        )
        lt_arrows.set_color(GREY_A)
        lt_arrow_labels = VGroup(
            Tex(R"\mathcal{L}").next_to(arrow, UP, buff=0)
            for arrow in lt_arrows
        )
        lt_integrals = VGroup(
            Tex(
                R"\int^\infty_0 " + tex + R"\cdot e^{\minus{s}{t}}d{t}",
                t2c=t2c
            )
            for tex in ["1", "e^{a{t}}", R"\sum_{n=1}^N c_n e^{s_n {t}}"]
        )
        lt_rhss = VGroup(
            Tex(R"= \frac{1}{{s}}", t2c=t2c),
            Tex(R"= \frac{1}{{s} - a}", t2c=t2c),
            Tex(R"= \sum_{n=1}^N \frac{c_n}{{s} - s_n}", t2c=t2c),
        )
        for integral, arrow, rhs in zip(lt_integrals, lt_arrows, lt_rhss):
            integral.next_to(arrow, RIGHT)
            rhs.scale(1.25)
            rhs.next_to(integral, RIGHT)

        # Show laplace transforms
        frame = self.frame

        self.play(
            LaggedStart(
                GrowArrow(lt_arrows[0]),
                Write(lt_arrow_labels[0]),
                FadeIn(lt_integrals[0], RIGHT),
                lag_ratio=0.3
            ),
            terms[1:].animate.set_fill(opacity=0.1),
            arrows.animate.set_fill(opacity=0.1),
            frame.animate.set_x(4),
            run_time=2
        )
        self.wait()
        self.play(Write(lt_rhss[0]))
        self.wait()
        for index in [1, 2]:
            self.play(
                arrows[index - 1].animate.set_fill(opacity=1),
                terms[index].animate.set_fill(opacity=1),
            )
            self.play(
                LaggedStart(
                    GrowArrow(lt_arrows[index]),
                    Write(lt_arrow_labels[index]),
                    FadeIn(lt_integrals[index], RIGHT),
                    lag_ratio=0.3
                ),
            )
            self.wait()
            self.play(Write(lt_rhss[index]))
            self.wait()
        # CHANGE: the camera is animated with frame.animate.reorient(...); the original passed frame.reorient(...) (which returns the frame) to play.
        self.play(frame.animate.reorient(0, 0, 0, (5.5, 0.04, 0.0), 10), run_time=2)
