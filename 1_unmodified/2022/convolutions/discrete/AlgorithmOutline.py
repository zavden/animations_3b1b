# ==============================================================================
# Scene:      AlgorithmOutline
# Source:     videos/_2022/convolutions/discrete.py (lines 2534-2759)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AlgorithmOutline.py AlgorithmOutline -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AlgorithmOutline(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Fast(?) convolution algorithm")
        title.to_edge(UP, buff=0.35)
        title.set_backstroke(BLACK, 3)
        underline = Underline(title, buff=-0.05).scale(1.5)
        underline.insert_n_curves(20)
        underline.set_stroke(GREY, (0, 3, 3, 3, 0))
        self.add(underline, title)

        # Arrays
        t2c = {
            tex: BLUE
            for tex in [R"\textbf{a}", "a_0", "a_1", "a_2", "a_{n - 1}"]
        }
        t2c.update({
            tex: TEAL
            for tex in [R"\textbf{b}", "b_0", "b_1", "b_2", "b_{m - 1}"]
        })
        tex_kw = dict(tex_to_color_map=t2c, font_size=36)
        lists = VGroup(
            Tex(R"\textbf{a} = [a_0, a_1, a_2, \dots, a_{n - 1}]", **tex_kw),
            Tex(R"\textbf{b} = [b_0, b_1, b_2, \dots, b_{m - 1}]", **tex_kw),
            Tex(R"""\textbf{a} * \textbf{b} = \left[\begin{array}{l}
                    a_0 b_0, \\
                    a_0 b_1 + a_1 b_0, \\
                    a_0 b_2 + a_1 b_1  + a_2 b_0, \\
                    \quad \vdots \\
                    a_{n - 1} b_{m - 1}
            \end{array}\right]""", **tex_kw),
        )
        lists.arrange(DOWN, buff=1.7, aligned_edge=LEFT)
        lists.next_to(underline, DOWN, LARGE_BUFF)
        lists.to_edge(LEFT)
        lists[2][4:].scale(0.7, about_edge=LEFT)
        lists[2].refresh_bounding_box()
        lists[2].to_edge(DOWN, buff=MED_SMALL_BUFF)
        conv_rect = SurroundingRectangle(lists[2], buff=SMALL_BUFF)
        conv_rect.set_stroke(YELLOW, 2)
        q_marks = Text("???", color=YELLOW)
        q_marks.next_to(conv_rect, RIGHT, MED_SMALL_BUFF)

        self.add(lists[:2])
        self.play(ShowCreation(underline))
        self.play(
            TransformMatchingShapes(VGroup(*lists[0], *lists[1]).copy(), lists[2]),
            FadeIn(conv_rect),
            FadeIn(q_marks),
        )
        self.wait()

        # Show polynomials
        polys = VGroup(
            Tex(R"f(x) = a_0 + a_1 x + a_2 x^2 + \cdots + a_{n - 1}x^{n - 1}", **tex_kw),
            Tex(R"g(x) = b_0 + b_1 x + b_2 x^2 + \cdots + b_{m - 1}x^{m - 1}", **tex_kw),
        )
        for poly, listy in zip(polys, lists):
            poly.next_to(listy, DOWN, aligned_edge=LEFT)

        axes = VGroup(*(
            Axes((-3, 3), (-2, 2), width=5, height=1.5)
            for x in range(3)
        ))
        axes.to_edge(RIGHT)
        axes[0].match_y(polys[0])
        axes[1].match_y(polys[1])
        axes[2].move_to(2 * axes[1].get_origin() - axes[0].get_origin())

        def f(x):
            return 0.2 * (x + 3) * (x + 1) * (x - 2)

        def g(x):
            return 0.1 * (x + 2) * (x + 0) * (x - 3.25)

        graphs = VGroup(
            axes[0].get_graph(f, color=BLUE),
            axes[1].get_graph(g, color=TEAL),
            axes[2].get_graph(lambda x: f(x) * g(x), color=YELLOW),
        )
        graphs.set_stroke(width=2)

        label_kw = dict(font_size=24)
        graph_labels = VGroup(
            Tex("f(x)", **label_kw).move_to(axes[0], UL),
            Tex("g(x)", **label_kw).move_to(axes[1], UL),
            Tex(R"f(x) \cdot g(x)", **label_kw).move_to(axes[2], UL),
        )

        self.play(
            LaggedStart(*(
                TransformFromCopy(listy.copy(), poly)
                for listy, poly in zip(lists, polys)
            )),
            LaggedStartMap(FadeIn, axes[:2]),
            LaggedStartMap(ShowCreation, graphs[:2]),
            LaggedStartMap(FadeIn, graph_labels[:2]),
            lag_ratio=0.5,
        )
        self.wait()

        # Show samples
        x_samples = np.arange(-3, 3.5, 0.5)
        f_points, g_points, fg_points = all_points = [
            [ax.i2gp(x, graph) for x in x_samples]
            for ax, graph in zip(axes, graphs)
        ]

        f_dots, g_dots, fg_dots = all_dots = Group(*(
            Group(*(GlowDot(point, color=WHITE, glow_factor=0.8, radius=0.07) for point in points))
            for points in all_points
        ))

        self.play(
            FadeIn(f_dots, lag_ratio=0.7),
            FadeIn(g_dots, lag_ratio=0.7),
            run_time=5
        )
        self.wait()
        self.play(
            TransformFromCopy(axes[1], axes[2]),
            TransformMatchingShapes(graph_labels[:2].copy(), graph_labels[2]),
            LaggedStart(*(
                Transform(Group(fd, gd).copy(), Group(fgd), remover=True)
                for fd, gd, fgd in zip(*all_dots)
            ), lag_ratio=0.5, run_time=5)
        )
        self.add(fg_dots)
        self.play(ShowCreation(graphs[2], run_time=2))
        self.wait()

        # Show arrow
        final_arrow = Arrow(graph_labels[2], conv_rect.get_corner(UR), path_arc=PI / 5)
        final_arrow.set_color(RED)

        self.play(Write(final_arrow))
        self.wait()

        # Erase graphs
        crosses = VGroup(*map(Cross, axes[:2]))
        for cross in crosses:
            cross.insert_n_curves(20)
            cross.set_stroke(RED, (0, 10, 10, 10, 0))

        self.play(
            LaggedStartMap(ShowCreation, crosses, lag_ratio=0.5, run_time=2),
            polys[0].animate.scale(0.5, about_edge=DL),
            polys[1].animate.scale(0.5, about_edge=DL),
            LaggedStartMap(FadeOut, Group(
                final_arrow, axes[2], graph_labels[2], fg_dots, graphs[2], q_marks,
            ))
        )
        self.play(
            LaggedStartMap(FadeOut, Group(
                axes[0], graphs[0], graph_labels[0], f_dots, crosses[0],
                axes[1], graphs[1], graph_labels[1], g_dots, crosses[1],
            ), shift=0.2 * RIGHT)
        )

        # Show FFTs
        t2c = {
            tex: RED
            for tex in [R"\hat{\textbf{a}}", R"\hat{a}_0", R"\hat{a}_1", R"\hat{a}_2", R"\hat{a}_{m + n - 1}"]
        }
        t2c.update({
            tex: MAROON_C
            for tex in [R"\hat{\textbf{b}}", R"\hat{b}_0", R"\hat{b}_1", R"\hat{b}_2", R"\hat{b}_{m + n - 1}"]
        })
        fft_kw = dict(tex_to_color_map=t2c, font_size=36, isolate=["="])
        fft_lists = VGroup(
            Tex(R"\hat{\textbf{a}} = [\hat{a}_0, \hat{a}_1, \hat{a}_2, \dots, \hat{a}_{m + n - 1}]", **fft_kw),
            Tex(R"\hat{\textbf{b}} = [\hat{b}_0, \hat{b}_1, \hat{b}_2, \dots, \hat{b}_{m + n - 1}]", **fft_kw),
            Tex(R"""\hat{\textbf{a}} \cdot \hat{\textbf{b}} = [
                    \hat{a}_0 \hat{b}_0,
                    \hat{a}_1 \hat{b}_1,
                    \hat{a}_2 \hat{b}_2,
                    \dots,
            ]""", **fft_kw),
        )
        for fft_list in fft_lists:
            fft_list.shift(-fft_list.select_part("=").get_center())
        fft_lists.to_edge(RIGHT)

        arrows = VGroup()
        arrow_labels = VGroup()
        for orig_list, fft_list, n in zip(lists, fft_lists, it.count()):
            fft_list.match_y(orig_list)
            arrow = Arrow(orig_list, fft_list, buff=0.3)
            arrow.label = Text("Inverse FFT" if n == 2 else "FFT", font_size=36)
            arrow.label.next_to(arrow, UP)
            arrow_labels.add(arrow.label)
            arrows.add(arrow)
        arrows[2].rotate(PI)

        mult_arrow = Vector(2 * DOWN).move_to(VGroup(fft_lists[1], fft_lists[2]).get_center())
        mult_arrow.label = Text("Multiply\n(pointwise)", font_size=36)
        mult_arrow.label.next_to(mult_arrow, RIGHT)

        kw = dict(lag_ratio=0.75, run_time=2)
        self.play(
            title[:4].animate.match_x(title[4:7], RIGHT),
            FadeOut(title[4:7], 0.1 * DOWN, lag_ratio=0.1),
        )
        self.play(
            LaggedStartMap(FadeIn, fft_lists[:2], shift=1.5 * RIGHT, **kw),
            LaggedStartMap(GrowArrow, arrows[:2], **kw),
            LaggedStartMap(FadeIn, arrow_labels[:2], shift=0.5 * RIGHT, **kw),
        )
        self.wait()
        self.play(LaggedStart(
            polys[0].animate.scale(1.5, about_edge=DL),
            polys[1].animate.scale(1.5, about_edge=DL),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(
            FadeIn(fft_lists[2], DOWN),
            GrowArrow(mult_arrow),
            FadeIn(mult_arrow.label, 0.5 * DOWN)
        )
        self.wait()
        self.play(
            GrowArrow(arrows[2]),
            FadeIn(arrow_labels[2], shift=LEFT),
        )
        self.wait()
