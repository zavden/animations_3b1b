# ==============================================================================
# Scene:      ReplaceXWithPiX
# Source:     videos/_2022/borwein/main.py (lines 1218-1313)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReplaceXWithPiX.py ReplaceXWithPiX -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def sinc(x):
    return np.sinc(x / PI)


class ReplaceXWithPiX(InteractiveScene):
    def construct(self):
        # Setup graphs
        axes = Axes((-int(8 * PI), int(8 * PI)), (-0.5, 1.0, 0.5), width=FRAME_WIDTH * PI + 1, height=4)
        axes.shift(DOWN)
        axes.x_axis.add_numbers(num_decimal_places=0, font_size=20)
        axes.y_axis.add_numbers(num_decimal_places=1, font_size=20)
        sinc_graph = axes.get_graph(sinc)
        sinc_graph.set_stroke(BLUE, 1)
        sinc_pi_graph = sinc_graph.copy().stretch(1 / PI, 0, about_point=axes.get_origin())

        dx = 0.01
        sinc_area = axes.get_riemann_rectangles(
            sinc_graph,
            dx=dx,
            colors=(BLUE_E, BLUE_E),
            negative_color=RED_E,
            fill_opacity=1.0,
        )
        sinc_area.sort(lambda p: abs(p[0]))
        sinc_pi_area = sinc_area.copy().stretch(1 / PI, 0, about_point=axes.get_origin())

        partial_area = sinc_area[:len(sinc_area) // 3]
        self.add(partial_area, axes, sinc_graph)

        # Setup labels
        sinc_label = Tex(R"\int_{-\infty}^\infty \frac{\sin(x)}{x} dx = \pi")
        sinc_label.next_to(axes, UP).to_edge(LEFT)
        kw = dict(tex_to_color_map={R"\pi": TEAL})
        sinc_pi_label = Tex(
            R"\int_{-\infty}^\infty \frac{\sin(\pi x)}{\pi x} dx = 1.0",
            **kw
        )
        sinc_pi_label.move_to(sinc_label).to_edge(RIGHT)

        eq_pi = sinc_label[-2:]
        eq_one = sinc_pi_label[-4:]

        pi_rect = SurroundingRectangle(eq_pi).set_stroke(BLUE, 2)
        one_rect = SurroundingRectangle(eq_one).set_stroke(BLUE, 2)
        want_to_show = Text("want to show", font_size=36)
        want_to_show.next_to(pi_rect, DOWN, aligned_edge=LEFT)
        want_to_show.set_color(BLUE)

        instead_of = Text("Instead of", color=YELLOW, font_size=60)
        instead_of.next_to(sinc_label, UP, buff=0.7, aligned_edge=LEFT)
        focus_on = Text("Focus on", color=YELLOW, font_size=60)
        focus_on.next_to(sinc_pi_label, UP, buff=0.7, aligned_edge=LEFT)

        self.add(instead_of, sinc_label)
        self.play(Write(partial_area, stroke_width=1.0))
        self.add(sinc_area, axes, sinc_graph)
        self.wait()
        self.play(
            ShowCreation(pi_rect),
            FadeIn(want_to_show, 0.5 * DOWN)
        )
        self.wait()

        # Squish
        x_to_pix = Tex(R"x \rightarrow \pi x", **kw)
        x_to_pix.match_y(instead_of)

        squish_arrows = VGroup(Vector(RIGHT), Vector(LEFT))
        squish_arrows.arrange(RIGHT, buff=1.5)
        squish_arrows.move_to(axes.c2p(0, 0.5))

        rect_kw = dict(buff=MED_SMALL_BUFF, stroke_width=1.5)
        rect = SurroundingRectangle(sinc_pi_label, **rect_kw)
        sinc_graph.save_state()
        sinc_area.save_state()

        self.play(LaggedStart(
            FadeIn(x_to_pix),
            TransformMatchingShapes(sinc_label.copy(), sinc_pi_label),
            FadeTransform(instead_of.copy(), focus_on)
        ))
        self.wait()
        self.play(
            Transform(sinc_graph, sinc_pi_graph),
            Transform(sinc_area, sinc_pi_area),
            FadeIn(squish_arrows, scale=0.35),
            run_time=2
        )
        self.wait()
        self.play(ShowCreation(one_rect))
        self.wait()
        self.play(ShowCreation(rect))
        self.wait()
        self.play(
            FadeOut(squish_arrows, scale=3),
            sinc_area.animate.restore(),
            sinc_graph.animate.restore(),
            rect.animate.become(SurroundingRectangle(VGroup(sinc_label, want_to_show), **rect_kw)),
        )
        self.wait()
