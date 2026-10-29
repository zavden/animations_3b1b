# ==============================================================================
# Scene:      QuadraticPolynomials
# Source:     videos/_2021/quick_eigen.py (lines 2464-2646)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuadraticPolynomials.py QuadraticPolynomials -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

EIGEN_COLORS = [TEAL_A, TEAL_D]


PROD_COLOR = BLUE_D


class QuadraticPolynomials(Scene):
    def construct(self):
        # Set up equation
        kw = {
            "tex_to_color_map": {
                "\\lambda_1": EIGEN_COLORS[0],
                "\\lambda_2": EIGEN_COLORS[1],
                "=": WHITE,
            }
        }
        equation = VGroup(
            OldTex("x^2 - 10x + 9", **kw)[0],
            OldTex("=").rotate(PI / 2),
            OldTex("x^2 - (\\lambda_1 + \\lambda_2)x + \\lambda_1 \\lambda_2", **kw),
            OldTex("=").rotate(PI / 2),
            OldTex("(x - \\lambda_1)(x - \\lambda_2)", **kw),
        )
        equation.arrange(DOWN)
        equation.to_edge(LEFT)
        line1, eq1, line2, eq2, line3 = equation
        for line in line2, line3:
            line.set_submobjects(line.family_members_with_points())

        line3.save_state()
        line3.move_to(line2)

        # Graph
        axes = Axes(
            (-5, 10),
            (-20, 20),
            height=7,
            width=FRAME_WIDTH / 2,
        )
        axes.y_axis.ticks.stretch(0.75, 0)
        axes.to_edge(RIGHT)
        graph = axes.get_graph(lambda x: x**2 - 10 * x + 9)
        graph.set_color(BLUE)
        graph_label = line1.copy()
        graph_label.set_color(BLUE)
        graph_label.next_to(graph.get_end(), UP)
        graph_label.to_edge(RIGHT)

        root_dots = VGroup()
        root_labels = VGroup()
        for i, n, vect in zip((0, 1), (1, 9), (RIGHT, LEFT)):
            dot = Dot(axes.c2p(n, 0), color=EIGEN_COLORS[i])
            label = OldTex(f"\\lambda_{i + 1}")
            label.match_color(dot)
            label.next_to(dot, UP + vect, buff=0.05)
            root_dots.add(dot)
            root_labels.add(label)
        root_dots.set_stroke(BLACK, 5, background=True)

        self.play(Write(axes))
        self.play(
            ShowCreation(graph, run_time=3),
            FadeIn(graph_label, UP)
        )
        self.play(
            LaggedStartMap(GrowFromCenter, root_dots),
            LaggedStart(
                GrowFromPoint(root_labels[0], root_dots[0].get_center()),
                GrowFromPoint(root_labels[1], root_dots[1].get_center()),
            )
        )
        self.wait()

        # Animate to equation
        self.play(TransformFromCopy(graph_label, line1))
        self.play(
            Write(eq1),
            TransformMatchingShapes(root_labels.copy(), line3)
        )
        self.wait()
        self.play(Restore(line3))
        xs = VGroup(line3[1], line3[7])
        self.play(TransformFromCopy(xs, line2[:2]))  # x^2
        self.play(LaggedStart(  # x
            AnimationGroup(
                TransformFromCopy(line3[1], line2[10].copy()),
                TransformFromCopy(line3[9:11], line2[7:9]),
                FadeIn(line2[2])
            ),
            AnimationGroup(
                TransformFromCopy(line3[7], line2[10].copy(), remover=True),
                TransformFromCopy(line3[3:5], line2[4:6]),
                FadeIn(VGroup(line2[3], line2[6], line2[9]))
            ),
        ))
        self.play(
            TransformFromCopy(
                VGroup(*line3[3:5], *line3[9:11]),
                VGroup(*line2[12:16]),
            ),
            FadeIn(line2[11]),
            FadeIn(eq2),
        )
        self.wait()

        # Highlight sum and product
        for i, j, k, l in [(3, 5, 3, 10), (7, 8, 12, 16)]:
            self.play(
                FadeIn(SurroundingRectangle(line1[i:j])),
                FadeIn(SurroundingRectangle(line2[k:l])),
                run_time=2,
                rate_func=there_and_back_with_pause,
                remover=True
            )

        # Show mean and product
        line2 = VGroup(*line2.family_members_with_points())
        line3 = VGroup(*line3.family_members_with_points())
        quad_terms = VGroup(line1[0:2], line2[0:2])
        lin_terms = VGroup(line1[2:5], line2[2:10])
        const_terms = VGroup(line1[6:], line2[11:])

        mean_arrow = Vector(UP)
        mean_arrow.next_to(lin_terms[0], UP, MED_SMALL_BUFF)
        times_half = OldTex("\\times -\\frac{1}{2}", font_size=24)
        times_half.next_to(mean_arrow, RIGHT, buff=0)
        m_eq = OldTex(
            "{\\lambda_1 + \\lambda_2 \\over 2}", "=", "5",
            tex_to_color_map={"\\lambda_1": EIGEN_COLORS[0], "\\lambda_2": EIGEN_COLORS[1]}
        )
        m_eq.next_to(mean_arrow, UP, SMALL_BUFF, submobject_to_align=m_eq[-1])
        m_eq[:-2].scale(0.7, about_edge=RIGHT)
        m_dot = Dot(axes.c2p(5, 0))
        m_dot.scale(0.5)
        m_label = Integer(5, font_size=30)
        m_label.next_to(m_dot, UP, SMALL_BUFF)

        p_rects = VGroup(*map(SurroundingRectangle, const_terms))
        p_rects.set_stroke(PROD_COLOR)

        fade_rect = FullScreenFadeRectangle()
        fade_rect.set_fill(BLACK, 0.75)
        fade_rect.replace(equation, stretch=True)

        self.add(fade_rect, *quad_terms)
        self.play(FadeIn(fade_rect))
        self.wait()
        self.add(fade_rect, *lin_terms)
        self.wait()
        self.play(
            GrowArrow(mean_arrow),
            FadeIn(times_half, shift=0.25 * UP, scale=2),
            FadeIn(m_eq[:-1])
        )
        self.play(Write(m_eq[-1]))
        self.play(
            FadeTransform(m_eq[-1].copy(), m_dot),
            FadeTransform(m_eq[-1].copy(), m_label),
        )
        self.wait()
        self.add(fade_rect, *const_terms)
        VGroup(mean_arrow, times_half).set_opacity(0.5)
        self.play(ShowCreation(p_rects))
        self.wait()

        # Show final roots
        d_terms = VGroup(*(
            OldTex(u, "\\sqrt{25 - 9}", font_size=24)
            for u in ["+", "-"]
        ))
        my = m_label.get_y()
        arrows = VGroup(
            Arrow(m_label.get_left(), [root_dots[0].get_left()[0], my, 0], buff=0.1),
            Arrow(m_label.get_right(), [root_dots[1].get_right()[0], my, 0], buff=0.1),
        )
        for d_term, arrow in zip(d_terms, arrows):
            d_term.next_to(arrow, UP, buff=0)

        self.play(FadeOut(p_rects))
        self.play(
            TransformMatchingShapes(equation[0][-2:].copy(), d_terms),
            FadeOut(root_labels),
            *map(GrowArrow, arrows)
        )
        self.wait()
        self.play(
            FadeOut(fade_rect),
        )
        self.wait()
