# ==============================================================================
# Scene:      Graph15Case
# Source:     videos/_2022/borwein/main.py (lines 1829-1841)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Graph15Case.py Graph15Case -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def sinc(x):
    return np.sinc(x / PI)


def multi_sinc(x, n):
    return np.prod([sinc(x / (2 * k + 1)) for k in range(n)])


def get_fifteenth_frac_tex():
    return R"{467{,}807{,}924{,}713{,}440{,}738{,}696{,}537{,}864{,}469 \over 467{,}807{,}924{,}720{,}320{,}453{,}655{,}260{,}875{,}000}"


class ShowIntegrals(InteractiveScene):
    # add_axis_labels = True
    add_axis_labels = False

    def construct(self):
        # Setup axes
        axes = self.get_axes()

        graph = axes.get_graph(sinc, color=BLUE)
        graph.set_stroke(width=3)
        points = graph.get_anchors()
        right_sinc = VMobject().set_points_smoothly(points[len(points) // 2:])
        left_sinc = VMobject().set_points_smoothly(points[:len(points) // 2]).reverse_points()
        VGroup(left_sinc, right_sinc).match_style(graph).make_jagged()

        func_label = Tex(R"{\sin(x) \over x}")
        func_label.move_to(axes, UP).to_edge(LEFT)

        self.add(axes)
        self.play(
            Write(func_label),
            ShowCreation(right_sinc, remover=True, run_time=3),
            ShowCreation(left_sinc, remover=True, run_time=3),
        )
        self.add(graph)
        self.wait()

        # Discuss sinc function?
        sinc_label = OldTex(R"\text{sinc}(x)")
        sinc_label.next_to(func_label, UR, buff=LARGE_BUFF)
        arrow = Arrow(func_label, sinc_label)

        one_over_x_graph = axes.get_graph(lambda x: 1 / x, x_range=(0.1, 8 * PI))
        one_over_x_graph.set_stroke(YELLOW, 2)
        one_over_x_label = OldTex("1 / x")
        one_over_x_label.next_to(axes.i2gp(1, one_over_x_graph), RIGHT)
        sine_wave = axes.get_graph(np.sin, x_range=(0, 8 * PI)).set_stroke(TEAL, 3)
        half_sinc = axes.get_graph(sinc, x_range=(0, 8 * PI)).set_stroke(BLUE, 3)

        self.play(
            GrowArrow(arrow),
            FadeIn(sinc_label, UR)
        )
        self.wait()

        self.play(
            ShowCreation(sine_wave, run_time=2),
            graph.animate.set_stroke(width=1, opacity=0.5)
        )
        self.wait()
        self.play(
            ShowCreation(one_over_x_graph),
            FadeIn(one_over_x_label),
            Transform(sine_wave, half_sinc),
        )
        self.wait()
        self.play(
            FadeOut(one_over_x_graph),
            FadeOut(one_over_x_label),
            FadeOut(sine_wave),
            graph.animate.set_stroke(width=3, opacity=1),
        )

        # At 0
        hole = Dot()
        hole.set_stroke(BLUE, 2)
        hole.set_fill(BLACK, 1)
        hole.move_to(axes.c2p(0, 1))

        zero_eq = OldTex(R"{\sin(0) \over 0} = ???")
        zero_eq.next_to(hole, UR)
        lim = OldTex(R"\lim_{x \to 0} {\sin(x) \over x} = 1")
        lim.move_to(zero_eq, LEFT)
        x_tracker = ValueTracker(1.5 * PI)
        get_x = x_tracker.get_value
        dots = GlowDot().replicate(2)
        dots.add_updater(lambda d: d[0].move_to(axes.i2gp(-get_x(), graph)))
        dots.add_updater(lambda d: d[1].move_to(axes.i2gp(get_x(), graph)))
        dots.update()

        self.play(Write(zero_eq), FadeIn(hole, scale=0.35))
        self.wait()
        self.play(FadeTransform(zero_eq, lim))
        self.add(dots)
        self.play(
            x_tracker.animate.set_value(0).set_anim_args(run_time=2),
            UpdateFromAlphaFunc(dots, lambda m, a: m.set_opacity(a)),
        )
        self.wait()
        self.play(FadeOut(dots), FadeOut(hole), FadeOut(lim))
        self.play(FadeOut(arrow), FadeOut(sinc_label))

        # Area under curve
        area = self.get_area(axes, graph)
        int1 = self.get_integral(1)
        rhs = OldTex(R"=\pi")
        rhs.next_to(int1, RIGHT)

        origin = axes.get_origin()
        pos_area = VGroup(*(r for r in area if r.get_center()[1] > origin[1]))
        neg_area = VGroup(*(r for r in area if r.get_center()[1] < origin[1]))

        self.add(area, axes, graph)
        area.set_fill(opacity=1)
        self.play(
            Write(area, stroke_color=WHITE, lag_ratio=0.01, run_time=4),
            ReplacementTransform(func_label, int1[1]),
            Write(int1[::2]),
            graph.animate.set_stroke(width=1),
        )
        self.add(int1)
        self.wait()
        self.play(FadeOut(neg_area))
        self.wait()
        self.play(FadeIn(neg_area), FadeOut(pos_area))
        self.wait()
        self.play(FadeIn(pos_area))
        self.add(area)
        self.wait()
        self.play(Write(rhs))
        self.play(FlashAround(rhs, run_time=2))
        self.wait()

        # Show sin(x / 3) / (x / 3)
        frame = self.camera.frame
        midpoint = 1.5 * DOWN
        top_group = VGroup(axes, graph, area)
        top_group.generate_target().next_to(midpoint, UP)
        low_axes = self.get_axes(height=2.5)
        low_axes.next_to(midpoint, DOWN, buff=MED_LARGE_BUFF)
        low_sinc = low_axes.get_graph(sinc)
        low_sinc.set_stroke(BLUE, 2)
        low_graph = low_axes.get_graph(lambda x: sinc(x / 3))
        low_graph.set_stroke(WHITE, 2)
        low_label = OldTex(R"{\sin(x / 3) \over x / 3}")
        low_label.match_x(int1[1]).shift(1.75 * LEFT).match_y(low_axes.get_top())

        self.play(
            MoveToTarget(top_group),
            FadeTransform(axes.copy(), low_axes),
            FadeIn(low_label),
            frame.animate.set_height(10),
            VGroup(int1, rhs).animate.shift(UP + 1.75 * LEFT),
        )
        self.wait()
        self.play(TransformFromCopy(graph, low_sinc))
        self.play(low_sinc.animate.stretch(3, 0).match_style(low_graph), run_time=2)
        self.remove(low_sinc)
        self.add(low_graph)
        self.wait()

        # Sequence of integrals
        curr_int = int1
        for n in range(2, 9):
            new_int = self.get_integral(n)
            if n == 4:
                new_int.scale(0.9)
            elif n == 5:
                new_int.scale(0.8)
            elif n > 5:
                new_int.scale(0.7)
            new_int.move_to(curr_int, LEFT)
            if n < 8:  # TODO
                new_rhs = Tex(R"=\pi")
            else:
                new_rhs = Tex(R"\approx \pi - 4.62 \times 10^{-11}")
            new_rhs.next_to(new_int, RIGHT)

            new_graph = axes.get_graph(lambda x, n=n: multi_sinc(x, n))
            new_graph.set_stroke(BLUE, 2)
            new_area = self.get_area(axes, new_graph)

            self.play(
                ReplacementTransform(curr_int[:n], new_int[:n]),
                TransformFromCopy(low_label[0], new_int[n]),
                ReplacementTransform(curr_int[-1], new_int[-1]),
                FadeOut(rhs),
                FadeOut(area),
                ReplacementTransform(graph, new_graph),
                TransformFromCopy(low_graph, new_graph.copy(), remover=True),
            )
            self.play(Write(new_area, stroke_color=WHITE, stroke_width=1, lag_ratio=0.01))
            self.wait(0.25)
            self.play(FadeIn(new_rhs, scale=0.7))
            self.play(FlashAround(new_rhs))
            self.wait()

            if n < 8:
                new_low_graph = low_axes.get_graph(lambda x, n=n: sinc(x / (2 * n + 1)))
                new_low_graph.match_style(low_graph)
                new_low_label = OldTex(fR"{{\sin(x / {2 * n + 1}) \over x / {2 * n + 1}}}")
                new_low_label.move_to(low_label)
                if n == 4:
                    new_low_label.shift(0.5 * UP)

                self.play(
                    FadeOut(low_label, UP),
                    FadeIn(new_low_label, UP),
                    ReplacementTransform(low_graph, new_low_graph),
                )
                self.wait(0.25)

            curr_int = new_int
            rhs = new_rhs
            graph = new_graph
            area = new_area
            low_graph = new_low_graph
            low_label = new_low_label

        # More accurate rhs
        new_rhs = OldTex(Rf"= {get_fifteenth_frac_tex()} \pi")
        new_rhs.next_to(curr_int, DOWN, buff=LARGE_BUFF)

        self.play(
            FadeOut(VGroup(low_axes, low_graph, low_label), DOWN),
            VGroup(axes, graph, area).animate.shift(2 * DOWN),
            Write(new_rhs)
        )
        self.wait()

    def get_axes(self,
                 x_range=(-10 * PI, 10 * PI, PI),
                 y_range=(-0.5, 1, 0.5),
                 width=1.3 * FRAME_WIDTH,
                 height=3.5,
                 ):
        axes = Axes(x_range, y_range, width=width, height=height)
        axes.center()
        if self.add_axis_labels:
            axes.y_axis.add_numbers(num_decimal_places=1, font_size=20)
            for u in -1, 1:
                axes.x_axis.add_numbers(
                    u * np.arange(PI, 15 * PI, PI),
                    unit=PI,
                    unit_tex=R"\pi",
                    font_size=20
                )
        return axes

    def get_area(self, axes, graph, dx=0.01 * PI, fill_opacity=0.5):
        rects = axes.get_riemann_rectangles(
            graph, dx=dx,
            colors=(BLUE_D, BLUE_D),
            negative_color=RED,
        )
        rects.set_fill(opacity=fill_opacity)
        rects.set_stroke(width=0)
        rects.sort(lambda p: abs(p[0]))
        return rects

    def get_integral(self, n):
        return OldTex(
            R"\int_{-\infty}^\infty",
            R"{\sin(x) \over x}",
            *(
                Rf"{{\sin(x/{k}) \over x / {k} }}"
                for k in range(3, 2 * n + 1, 2)
            ),
            "dx"
        ).to_corner(UL)


class Graph15Case(ShowIntegrals):
    def construct(self):
        # Test
        axes = self.get_axes(
            x_range=(-3 * PI, 3 * PI, PI),
            y_range=(0, 1),
            width=1.0 * FRAME_WIDTH,
        )
        graph = axes.get_graph(lambda x: multi_sinc(x, 8))
        graph.set_stroke(width=1)
        area = self.get_area(axes, graph, dx=0.005 * PI)
        area.set_fill(opacity=0.9)
        self.add(axes, area, graph)
