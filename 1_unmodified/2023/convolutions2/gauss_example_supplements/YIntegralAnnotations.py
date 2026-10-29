# ==============================================================================
# Scene:      YIntegralAnnotations
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 548-689)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl YIntegralAnnotations.py YIntegralAnnotations -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class YIntegralAnnotations(InteractiveScene):
    def construct(self):
        # Setup
        kw = dict(
            t2c={
                "{s}": RED,
                "{y}": YELLOW,
                "{x}": BLUE,
                R"\text{Area}": TEAL
            }
        )
        integrals = VGroup(
            Tex(R"\text{Area} = \int_{\text{-}\infty}^\infty e^{-{x}^2} \cdot e^{-{y}^2} \, d{y}", **kw),
            Tex(R"\text{Area} = \int_{\text{-}\infty}^\infty e^{-({s} / \sqrt{2})^2} \cdot e^{-{y}^2} \, d{y}", **kw),
            Tex(R"\text{Area} = e^{-({s} / \sqrt{2})^2} \int_{\text{-}\infty}^\infty e^{-{y}^2} \, d{y}", **kw),
            Tex(R"\text{Area} = e^{-({s} / \sqrt{2})^2} \sqrt{\pi}", **kw),
        )
        for integral in integrals:
            integral.to_edge(UP)

        x_rect = SurroundingRectangle(integrals[0]["e^{-{x}^2}"], buff=0.05)
        s_rect1 = SurroundingRectangle(integrals[1][R"e^{-({s} / \sqrt{2})^2}"], buff=0.05)
        s_rect2 = SurroundingRectangle(integrals[2][R"e^{-({s} / \sqrt{2})^2}"], buff=0.05)
        y_int = integrals[2][R"\int_{\text{-}\infty}^\infty e^{-{y}^2} \, d{y}"]
        y_int_rect = SurroundingRectangle(y_int, buff=0.05)

        x_rect.set_stroke(BLUE, 2)
        s_rect1.set_stroke(RED, 2)
        s_rect2.set_stroke(RED, 2)
        y_int_rect.set_stroke(YELLOW, 2)
        const_word = Text("Constant!", font_size=36)
        const_word.next_to(x_rect, DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        const_word.shift(SMALL_BUFF * RIGHT)

        # Replace x
        self.play(Write(integrals[0]))
        self.wait()
        self.play(
            ShowCreation(x_rect),
            FadeIn(const_word, scale=0.7),
        )
        self.wait()

        self.play(
            TransformMatchingTex(*integrals[:2]),
            ReplacementTransform(x_rect, s_rect1),
            const_word.animate.match_x(s_rect1).set_anim_args(run_time=2),
        )
        self.wait()

        # Factor out
        self.play(
            FadeOut(const_word, 0.5 * DOWN),
            VShowPassingFlash(
                s_rect1.copy().insert_n_curves(100).set_stroke(width=5),
                run_time=2,
            ),
            ShowCreation(s_rect1, run_time=2)
        )
        self.wait()
        s_rect2.set_stroke(opacity=0)
        self.play(
            TransformMatchingTex(*integrals[1:3], path_arc=45 * DEGREES),
            ReplacementTransform(s_rect1, s_rect2, path_arc=45 * DEGREES),
            run_time=2
        )
        self.wait()

        # Emphasize separation
        s_rect2.set_stroke(RED, 2, 1)
        self.play(ShowCreation(s_rect2))
        self.wait()
        self.play(ReplacementTransform(s_rect2, y_int_rect))
        self.wait()

        y_int_group = VGroup(y_int_rect, y_int.copy())
        y_int.set_opacity(0)
        int_eq = Tex("=").rotate(90 * DEGREES)
        pi_term = integrals[3][R"\sqrt{\pi}"]
        int_eq.next_to(pi_term, DOWN, SMALL_BUFF)

        self.play(
            TransformMatchingTex(*integrals[2:4]),
            y_int_group.animate.scale(0.5).next_to(int_eq, DOWN, SMALL_BUFF),
            Write(int_eq),
        )
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(int_eq, *y_int_group)))
        self.wait()

        # Area expression
        area_eq = Tex(R"\text{Area} = e^{-{s}^2 / 2} \sqrt{\pi}", **kw)
        area_eq.to_edge(UP)
        area_eq.save_state()
        twos = area_eq["2"]
        twos_copies = twos.copy()
        twos[0].become(twos_copies[1])
        twos[1].become(twos_copies[0])

        self.play(
            TransformMatchingTex(integrals[3], area_eq)
        )
        area_eq.restore()
        self.wait()

        # From area to convolution
        conv_eqs = VGroup(
            Tex(R"[f * g]({s}) = \text{Area} / \sqrt{2}", **kw),
            Tex(R"[f * g]({s}) = \text{Area} / \sqrt{2} = e^{-{s}^2 / 2} \sqrt{\pi} / \sqrt{2}", **kw),
            Tex(R"[f * g]({s}) = \text{Area} / \sqrt{2} = e^{-{s}^2 / 2} \sqrt{\pi \over 2}", **kw),
        )
        conv_eqs[0].next_to(ORIGIN, LEFT, LARGE_BUFF).to_edge(UP)
        conv_eqs[1].move_to(area_eq)
        conv_eqs[2].move_to(area_eq)

        self.play(
            Write(conv_eqs[0]),
            Transform(area_eq["Area"].copy(), conv_eqs[0]["Area"].copy(), remover=True),
            area_eq.animate.next_to(ORIGIN, RIGHT, LARGE_BUFF).to_edge(UP),
        )
        self.wait()
        self.play(
            LaggedStart(*(
                FadeTransform(src[tex][-1], conv_eqs[1][tex][-1])
                for src, tex in [
                    (conv_eqs[0], conv_eqs[0].get_tex()),
                    (area_eq, R"e^{-{s}^2 / 2} \sqrt{\pi}"),
                    (conv_eqs[0], R"/ \sqrt{2}"),
                ]
            )),
            Write(conv_eqs[1]["="][1]),
            FadeOut(area_eq[R"\text{Area} ="][0]),
        )
        self.clear()
        self.add(conv_eqs[1])
        self.wait()
        self.play(TransformMatchingTex(
            *conv_eqs[1:3],
            key_map={R"\sqrt{\pi} / \sqrt{2}": R"\sqrt{\pi \over 2}"},
            run_time=1.5,
        ))
        self.wait()
