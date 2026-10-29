# ==============================================================================
# Scene:      SumToIntegral
# Source:     videos/_2020/beta/beta2.py (lines 1674-1914)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl SumToIntegral.py SumToIntegral -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy.stats


# ----- From _2020/beta/helpers.py -----

def get_beta_dist_axes(y_max=20, y_unit=2, label_y=False, **kwargs):
    config = {
        "x_min": 0,
        "x_max": 1,
        "x_axis_config": {
            "unit_size": 0.1,
            "tick_frequency": 0.1,
            "include_tip": False,
        },
        "y_min": 0,
        "y_max": y_max,
        "y_axis_config": {
            "unit_size": 1,
            "tick_frequency": y_unit,
            "include_tip": False,
        },
    }
    result = Axes(**config)
    origin = result.c2p(0, 0)
    kw = {
        "about_point": origin,
        "stretch": True,
    }
    result.x_axis.set_width(11, **kw)
    result.y_axis.set_height(6, **kw)

    x_vals = np.arange(0, 1, 0.2) + 0.2
    result.x_axis.add_numbers(
        *x_vals,
        num_decimal_places=1
    )

    if label_y:
        result.y_axis.add_numbers(
            *np.arange(y_unit, y_max, y_unit)
        )
        label = OldTexText("Probability density")
        label.scale(0.5)
        label.next_to(result.y_axis.get_top(), UR, SMALL_BUFF)
        label.next_to(result.y_axis, UP, SMALL_BUFF)
        label.align_to(result.y_axis.numbers, LEFT)
        result.add(label)
        result.y_axis_label = label

    result.to_corner(DR, LARGE_BUFF)

    return result



# ----- From _2020/beta/beta2.py -----

class SumToIntegral(Scene):
    def construct(self):
        # Titles
        titles = VGroup(
            OldTexText("Discrete context"),
            OldTexText("Continuous context"),
        )
        titles.set_height(0.5)
        for title, vect in zip(titles, [LEFT, RIGHT]):
            title.move_to(vect * FRAME_WIDTH / 4)
            title.to_edge(UP, buff=MED_SMALL_BUFF)

        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.next_to(titles, DOWN)
        h_line.set_x(0)
        v_line.center()

        self.play(
            ShowCreation(VGroup(h_line, v_line)),
            LaggedStartMap(
                FadeInFrom, titles,
                lambda m: (m, -0.2 * m.get_center()[0] * RIGHT),
                run_time=1,
                lag_ratio=0.1,
            ),
        )
        self.wait()

        # Sum and int
        kw = {"tex_to_color_map": {"S": BLUE}}
        s_sym = OldTex("\\sum", "_{x \\in S} P(x)", **kw)
        i_sym = OldTex("\\int_{S} p(x)", "\\text{d}x", **kw)
        syms = VGroup(s_sym, i_sym)
        syms.scale(2)
        for sym, title in zip(syms, titles):
            sym.shift(-sym[-1].get_center())
            sym.match_x(title)

        arrow = Arrow(
            s_sym[0].get_corner(UP),
            i_sym[0].get_corner(UP),
            path_arc=-90 * DEGREES,
        )
        arrow.set_color(YELLOW)

        self.play(Write(s_sym, run_time=1))
        anims = [ShowCreation(arrow)]
        for i, j in [(0, 0), (2, 1), (3, 2)]:
            source = s_sym[i].deepcopy()
            target = i_sym[j]
            target.save_state()
            source.generate_target()
            target.replace(source, stretch=True)
            source.target.replace(target, stretch=True)
            target.set_opacity(0)
            source.target.set_opacity(0)
            anims += [
                Restore(target, path_arc=-60 * DEGREES),
                MoveToTarget(source, path_arc=-60 * DEGREES),
            ]
        self.play(LaggedStart(*anims))
        self.play(FadeInFromDown(i_sym[3]))
        self.add(i_sym)
        self.wait()
        self.play(
            FadeOut(arrow, UP),
            syms.next_to, h_line, DOWN, {"buff": MED_LARGE_BUFF},
            syms.match_x, syms,
        )

        # Add curve area in editing
        # Add bar chart
        axes = Axes(
            x_min=0,
            x_max=10,
            y_min=0,
            y_max=7,
            y_axis_config={
                "unit_size": 0.75,
            }
        )
        axes.set_width(0.5 * FRAME_WIDTH - 1)
        axes.next_to(s_sym, DOWN)
        axes.y_axis.add_numbers(2, 4, 6)

        bars = VGroup()
        for x, y in [(1, 1), (4, 3), (7, 2)]:
            bar = Rectangle()
            bar.set_stroke(WHITE, 1)
            bar.set_fill(BLUE_D, 1)
            line = Line(axes.c2p(x, 0), axes.c2p(x + 2, y))
            bar.replace(line, stretch=True)
            bars.add(bar)

        addition_formula = OldTex(*"1+3+2")
        addition_formula.space_out_submobjects(2.1)
        addition_formula.next_to(bars, UP)

        for bar in bars:
            bar.save_state()
            bar.stretch(0, 1, about_edge=DOWN)

        self.play(
            Write(axes),
            LaggedStartMap(Restore, bars),
            LaggedStartMap(FadeInFromDown, addition_formula),
        )
        self.wait()

        # Confusion
        morty = Mortimer()
        morty.to_corner(DR)
        morty.look_at(i_sym)
        self.play(
            *map(FadeOut, [axes, bars, addition_formula]),
            FadeIn(morty)
        )
        self.play(morty.change, "maybe")
        self.play(Blink(morty))
        self.play(morty.change, "confused", i_sym.get_right())
        self.play(Blink(morty))
        self.wait()

        # Focus on integral
        self.play(
            Uncreate(VGroup(v_line, h_line)),
            FadeOut(titles, UP),
            FadeOut(morty, RIGHT),
            FadeOut(s_sym, LEFT),
            i_sym.center,
            i_sym.to_edge, LEFT
        )

        arrows = VGroup()
        for vect in [UP, DOWN]:
            corner = i_sym[-1].get_corner(RIGHT + vect)
            arrows.add(Arrow(
                corner,
                corner + 2 * RIGHT + 2 * vect,
                path_arc=-np.sign(vect[1]) * 60 * DEGREES,
            ))

        self.play(*map(ShowCreation, arrows))

        # Types of integration
        dist = scipy.stats.beta(7 + 1, 3 + 1)
        axes_pair = VGroup()
        graph_pair = VGroup()
        for arrow in arrows:
            axes = get_beta_dist_axes(y_max=5, y_unit=1)
            axes.set_width(4)
            axes.next_to(arrow.get_end(), RIGHT)
            graph = axes.get_graph(dist.pdf)
            graph.set_stroke(BLUE, 2)
            graph.set_fill(BLUE_E, 0)
            graph.make_smooth()
            axes_pair.add(axes)
            graph_pair.add(graph)

        r_axes, l_axes = axes_pair
        r_graph, l_graph = graph_pair
        r_name = OldTexText("Riemann\\\\Integration")
        r_name.next_to(r_axes, RIGHT)
        l_name = OldTexText("Lebesgue\\\\Integration$^*$")
        l_name.next_to(l_axes, RIGHT)
        footnote = OldTexText("*a bit more complicated than\\\\these bars make it look")
        footnote.match_width(l_name)
        footnote.next_to(l_name, DOWN)

        self.play(LaggedStart(
            FadeIn(r_axes),
            FadeIn(r_graph),
            FadeIn(r_name),
            FadeIn(l_axes),
            FadeIn(l_graph),
            FadeIn(l_name),
            run_time=1,
        ))

        # Approximation bars
        def get_riemann_rects(dx, axes=r_axes, func=dist.pdf):
            bars = VGroup()
            for x in np.arange(0, 1, dx):
                bar = Rectangle()
                line = Line(
                    axes.c2p(x, 0),
                    axes.c2p(x + dx, func(x)),
                )
                bar.replace(line, stretch=True)
                bar.set_stroke(BLUE_E, width=10 * dx, opacity=1)
                bar.set_fill(BLUE, 0.5)
                bars.add(bar)
            return bars

        def get_lebesgue_bars(dy, axes=l_axes, func=dist.pdf, mx=0.7, y_max=dist.pdf(0.7)):
            bars = VGroup()
            for y in np.arange(dy, y_max + dy, dy):
                x0 = binary_search(func, y, 0, mx) or mx
                x1 = binary_search(func, y, mx, 1) or mx
                line = Line(axes.c2p(x0, y - dy), axes.c2p(x1, y))
                bar = Rectangle()
                bar.set_stroke(RED_E, 0)
                bar.set_fill(RED_E, 0.5)
                bar.replace(line, stretch=True)
                bars.add(bar)
            return bars

        r_bar_groups = []
        l_bar_groups = []
        Ns = [10, 20, 40, 80, 160]
        Ms = [2, 4, 8, 16, 32]
        for N, M in zip(Ns, Ms):
            r_bar_groups.append(get_riemann_rects(dx=1 / N))
            l_bar_groups.append(get_lebesgue_bars(dy=1 / M))
        self.play(
            FadeIn(r_bar_groups[0], lag_ratio=0.1),
            FadeIn(l_bar_groups[0], lag_ratio=0.1),
            FadeIn(footnote),
        )
        self.wait()
        for rbg0, rbg1, lbg0, lbg1 in zip(r_bar_groups, r_bar_groups[1:], l_bar_groups, l_bar_groups[1:]):
            self.play(
                ReplacementTransform(
                    rbg0, rbg1,
                    lag_ratio=1 / len(rbg0),
                    run_time=2,
                ),
                ReplacementTransform(
                    lbg0, lbg1,
                    lag_ratio=1 / len(lbg0),
                    run_time=2,
                ),
            )
            self.wait()
        self.play(
            FadeOut(r_bar_groups[-1]),
            FadeOut(l_bar_groups[-1]),
            r_graph.set_fill, BLUE_E, 1,
            l_graph.set_fill, RED_E, 1,
        )
