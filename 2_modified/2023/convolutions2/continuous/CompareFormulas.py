# ==============================================================================
# Scene:      CompareFormulas
# Source:     videos/_2023/convolutions2/continuous.py (lines 234-355)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CompareFormulas.py CompareFormulas -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - DiscreteDistributionSum.png: placeholder diagram (two dice and their sum) at the root of _lib/assets/raster_images/ (make_convolutions2_assets.py); the scene asks for it by Grant's Dropbox path and manim_imports_ext finds it by name
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def wedge_func(x):
    return np.clip(-np.abs(x) + 1, 0, 1)


def double_lump(x):
    return 0.45 * np.exp(-6 * (x - 0.5)**2) + np.exp(-6 * (x + 0.5)**2)


def get_conv_graph(axes, f, g, dx=0.1):
    dx = 0.1
    x_min, x_max = axes.x_range[:2]
    x_samples = np.arange(x_min, x_max + dx, dx)
    f_samples = np.array([f(x) for x in x_samples])
    g_samples = np.array([g(x) for x in x_samples])
    full_conv = np.convolve(f_samples, g_samples)
    x0 = len(x_samples) // 2 - 1  # TODO, be smarter about this
    conv_samples = full_conv[x0:x0 + len(x_samples)]
    conv_graph = VMobject()
    conv_graph.set_stroke(TEAL, 2)
    conv_graph.set_points_smoothly(axes.c2p(x_samples, conv_samples * dx))
    return conv_graph


class CompareFormulas(InteractiveScene):
    def construct(self):
        # Setup division
        v_line = Line(DOWN, UP).set_height(FRAME_HEIGHT)
        kw = dict(font_size=60)
        disc_title, cont_title = titles = VGroup(
            Text("Discrete case", **kw),
            Text("Continuous case", **kw),
        )
        for vect, title in zip([LEFT, RIGHT], titles):
            title.move_to(vect * FRAME_WIDTH * 0.25)
            title.to_edge(UP, buff=MED_SMALL_BUFF)
            underline = Underline(title, stretch_factor=1.5)
            underline.set_stroke(GREY_B)
            title.add(underline)

        self.add(v_line, titles)

        # Discrete diagram (pre-made image)
        discrete_diagram = ImageMobject("/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2023/convolutions2/dice/DiscreteDistributionSum.png")
        discrete_diagram.set_height(5)
        discrete_diagram.match_x(disc_title)
        discrete_diagram.to_edge(DOWN, buff=0.5)
        self.add(discrete_diagram)

        # Continuous diagrams
        kw = dict(y_range=(0, 1, 0.5), width=5, height=1.5)
        all_axes = VGroup(
            Axes((-2, 2), **kw),
            Axes((-2, 2), **kw),
            Axes((-3, 3), **kw),
        )
        all_axes[:2].arrange(RIGHT, buff=1.5)
        all_axes[2].set_width(10)
        all_axes[2].next_to(all_axes[:2], UP, buff=1.5)
        all_axes.set_width(FRAME_WIDTH * 0.5 - 0.5)
        all_axes.match_x(cont_title)
        all_axes.to_edge(DOWN, buff=0.75)

        graphs = VGroup(
            all_axes[0].get_graph(
                wedge_func,
                use_smoothing=False
            ).set_stroke(BLUE),
            all_axes[1].get_graph(double_lump).set_stroke(RED),
            get_conv_graph(all_axes[2], wedge_func, double_lump).set_stroke(TEAL)
        )
        graphs.set_stroke(width=2)

        tex_kw = dict()
        labels = VGroup(
            Tex("f(x)", font_size=24),
            Tex("g(y)", font_size=24),
            Tex("[f * g](s)", font_size=36),
        )
        for label, axes in zip(labels, all_axes):
            label.move_to(midpoint(axes.get_corner(UR), axes.get_top()), UP)

        plots = VGroup(*(
            VGroup(*tup)
            for tup in zip(all_axes, graphs, labels)
        ))

        self.add(plots)

        # Formulae
        disc_formula = Tex(
            R"\big[P_X * P_Y\big](s) = \sum_{x = 1}^N P_X(x) \cdot P_Y(s - x)",
            font_size=36,
            t2c={"X": BLUE, "Y": RED},
        )
        disc_formula.next_to(disc_title, DOWN, MED_LARGE_BUFF)

        cont_formula = Tex(
            R"\big[f * g \big](s) = \int_{-\infty}^\infty f(x) g(s - x) \, dx",
            font_size=36,
        )
        cont_formula.match_x(cont_title)
        cont_formula.match_y(disc_formula)

        self.play(
            FadeIn(disc_formula, run_time=2, lag_ratio=0.1),
            FlashAround(disc_formula, time_width=1.5, run_time=2),
        )
        self.wait()

        rect = SurroundingRectangle(disc_formula)
        rect.set_stroke(YELLOW, 2, opacity=0)
        target_rects = VGroup(*(
            SurroundingRectangle(disc_formula[s][0])
            for s in ["P_X", "P_Y", "P_X * P_Y", re.compile(R"\\sum.*")]
        ))
        target_rects.set_stroke(YELLOW, 2)
        for target_rect in target_rects:
            self.play(rect.animate.become(target_rect), run_time=0.5)
            self.wait()
        self.play(FadeOut(rect))
        self.play(
            TransformMatchingTex(
                disc_formula.copy(), cont_formula,
                lag_ratio=-0.001,
                path_arc=-0.1 * PI
            )
        )
        self.wait()

        # Out of context
        fade_rect = FullScreenFadeRectangle()
        randy = Randolph()
        randy.next_to(cont_formula, DL, LARGE_BUFF)

        self.add(fade_rect, cont_formula)
        self.play(
            FadeIn(fade_rect),
            VFadeIn(randy),
            randy.change("horrified", cont_formula),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("pondering", cont_formula))
        self.play(Blink(randy))
        self.wait()
