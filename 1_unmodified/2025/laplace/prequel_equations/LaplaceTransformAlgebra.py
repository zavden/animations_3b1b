# ==============================================================================
# Scene:      LaplaceTransformAlgebra
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1446-1557)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LaplaceTransformAlgebra.py LaplaceTransformAlgebra -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LaplaceTransformAlgebra(InteractiveScene):
    def construct(self):
        # Add equation
        colors = color_gradient([TEAL, RED], 3, interp_by_hsl=True)
        t2c = {
            R"x(t)": colors[0],
            R"x'(t)": colors[1],
            R"x''(t)": colors[2],
            "{s}": YELLOW,
        }
        equation = Tex(
            R"{m} x''(t) + \mu x'(t) + k x(t) = F_0 \cos(\omega_l t)",
            t2c=t2c
        )
        equation.to_edge(UP, buff=1.5)

        arrow = Vector(1.25 * DOWN, thickness=6)
        arrow.next_to(equation, DOWN)
        arrow_label = Tex(R"\mathcal{L}", font_size=72)
        arrow_label.next_to(arrow, RIGHT, buff=SMALL_BUFF)

        self.add(equation)
        self.wait()
        self.play(
            GrowArrow(arrow),
            FadeIn(arrow_label, shift=0.5 * DOWN)
        )

        # Make transformed
        transformed_eq = Tex(
            R"{m} {s}^2 X({s}) + \mu {s} X({s}) + k X({s}) = \frac{F_0 {s}}{{s}^2 + \omega_l^2}",
            t2c=t2c
        )
        transformed_eq.next_to(arrow, DOWN)

        xt_texs = ["x(t)", "x'(t)", "x''(t)"]
        Xs_texs = ["X({s})", "{s} X({s})", "{s}^2 X({s})"]

        rects = VGroup()
        srcs = VGroup()
        trgs = VGroup()
        for t1, t2, color in zip(xt_texs, Xs_texs, colors):
            src = equation[t1][0]
            trg = transformed_eq[t2][-1]
            rect = SurroundingRectangle(src, buff=0.05)
            rect.set_stroke(color, 2)
            rect.target = rect.generate_target()
            rect.target.surround(trg, buff=0.05)

            rects.add(rect)
            srcs.add(src.copy())
            trgs.add(trg)

        self.play(LaggedStartMap(ShowCreation, rects, lag_ratio=0.25, run_time=1.5))
        self.play(
            LaggedStart(
                *(FadeTransform(src, trg)
                for src, trg in zip(srcs, trgs)),
                lag_ratio=0.25,
                group_type=Group,
                run_time=1.5
            ),
            LaggedStartMap(MoveToTarget, rects, lag_ratio=0.25, run_time=1.5)
        )
        self.play(
            LaggedStart(*(
                TransformFromCopy(equation[tex], transformed_eq[tex][:2])
                for tex in ["{m}", "+", R"\mu", "k", "="]
            )),
            TransformMatchingParts(
                equation[R"F_0 \cos(\omega_l t)"].copy(),
                transformed_eq[R"\frac{F_0 {s}}{{s}^2 + \omega_l^2}"]
            )
        )
        self.wait()

        # Factor it
        factored = Tex(
            R"X({s}) \left({m} {s}^2+ \mu {s} + k\right) = \frac{F_0 {s}}{{s}^2 + \omega_l^2}",
            t2c=t2c
        )
        factored.move_to(transformed_eq)
        left_rect = SurroundingRectangle(factored["X({s})"], buff=0.05)
        left_rect.set_stroke(YELLOW, 2)

        self.play(
            TransformMatchingTex(
                transformed_eq,
                factored,
                matched_keys=["X({s})"],
                path_arc=30 * DEG
            ),
            ReplacementTransform(rects, VGroup(left_rect), path_arc=30 * DEG),
            run_time=2
        )
        self.play(FadeOut(left_rect))
        self.wait()

        # Rearrange
        rearranged = Tex(
            R"X({s}) = \frac{F_0 {s}}{{s}^2 + \omega_l^2} \frac{1}{{m} {s}^2+ \mu {s} + k}",
            t2c=t2c
        )
        rearranged.next_to(factored, DOWN, LARGE_BUFF)

        self.play(
            TransformMatchingTex(
                factored.copy(),
                rearranged,
                matched_keys=["X({s})"],
            )
        )
