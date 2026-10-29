# ==============================================================================
# Scene:      PiAndCircleAnalogy2
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 568-647)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiAndCircleAnalogy2.py PiAndCircleAnalogy2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiAndCircleAnalogy2(InteractiveScene):
    def construct(self):
        # Show sum
        sum_expr = Tex(R"\sqrt{6 \sum_{n = 1}^{100} \frac{1}{n^2}}", isolate=["100"])
        rhs = Tex(R"= 3.1415926\dots")
        VGroup(sum_expr, rhs).arrange(RIGHT, buff=SMALL_BUFF).center()
        top_bound = sum_expr.make_number_changeable("100", group_with_commas=True, edge_to_fix=ORIGIN)
        top_bound.set_color(YELLOW)
        rhs_value = rhs.make_number_changeable("3.1415926", edge_to_fix=LEFT)
        sigma = sum_expr[7]
        sigma_width = sigma.get_width()

        n_tracker = ValueTracker(1)
        get_n = n_tracker.get_value
        top_bound.f_always.set_value(n_tracker.get_value)
        top_bound.always.set_max_width(sigma_width)
        rhs_value.add_updater(lambda m: m.set_value(
            math.sqrt(6 * sum(1 / n**2 for n in range(1, int(get_n()))))
        ))
        inf = Tex(R"\infty", font_size=36)
        inf.move_to(top_bound).set_color(YELLOW)

        circle = Circle(radius=0.49 * FRAME_HEIGHT)
        circle.rotate(45 * DEG)
        circle.set_stroke(WHITE, 3, 0.5)
        lights = Group(
            Group(
                GlowDot(circle.pfp(a), glow_factor=1, radius=radius, opacity=0.8 / (n + 2)**2)
                for n, radius in enumerate(np.arange(0.25, 5.25, 0.25))
            )
            for a in np.arange(0, 1, 1 / 16)
        )

        self.add(sum_expr, rhs)
        self.play(
            n_tracker.animate.set_value(10000).set_anim_args(run_time=6),
            FadeIn(circle, time_span=(3, 5)),
            FadeIn(lights, time_span=(4, 6)),
        )
        rhs_value.clear_updaters()
        self.play(
            n_tracker.animate.set_value(20000),
            VFadeOut(top_bound),
            FadeIn(inf),
            ChangeDecimalToValue(rhs_value, PI),
        )
        self.wait()

        # Transition to cross-entropy
        ce_formula = Tex(R"\sum_i p_i (-\log q_i)", t2c={"p_i": GREEN, "q_i": PINK}, font_size=60)
        compression_rects = Rectangle().get_grid(15, 1, buff=0)
        compression_rects.set_shape(3, 8)
        compression_rects.next_to(ce_formula, RIGHT, LARGE_BUFF)
        compression_rects.set_stroke(WHITE, 1, 0.25)
        compression_rects.set_z_index(-1)
        for rect in compression_rects:
            rect.set_fill(random_bright_color(hue_range=(0.1, 0.2)), 0.2)
        big_rect = SurroundingRectangle(compression_rects, buff=0)
        big_rect.set_stroke(WHITE, 2, 0)
        arrows = VGroup(Vector(0.5 * DOWN, thickness=5), Vector(0.5 * UP, thickness=5))
        arrows.set_fill(YELLOW)
        arrows[0].always.next_to(compression_rects, UP, SMALL_BUFF)
        arrows[1].always.next_to(compression_rects, DOWN, SMALL_BUFF)

        sum_expr.remove(sigma)
        sum_expr.remove(top_bound)
        sum_expr.add(inf)
        self.play(
            FadeOut(sum_expr, 0.2 * LEFT, lag_ratio=0.05),
            FadeOut(rhs, 0.2 * RIGHT, lag_ratio=0.05),
            ReplacementTransform(sigma, ce_formula[0]),
            Write(ce_formula[1:], time_span=(0.5, 2.0), stroke_color=WHITE),
            ReplacementTransform(circle, big_rect),
            FadeIn(compression_rects),
            FadeOut(lights),
        )
        self.wait()
        self.add(arrows)
        self.play(compression_rects.animate.stretch(0.3, 1), run_time=3)
        self.play(FadeOut(arrows))
