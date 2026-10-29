# ==============================================================================
# Scene:      AntiDerivative
# Source:     videos/_2023/gauss_int/integral.py (lines 208-280)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AntiDerivative.py AntiDerivative -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import scipy.signal
import scipy.stats

class AntiDerivative(InteractiveScene):
    def construct(self):
        # Add both planes
        x_min, x_max = (-3, 3)
        planes = VGroup(*(
            NumberPlane(
                (x_min, x_max), (0, 2),
                width=5.5, height=2.75,
                background_line_style=dict(stroke_color=GREY, stroke_width=1, stroke_opacity=1.0),
                faded_line_ratio=3,
            )
            for x in range(2)
        ))
        planes.arrange(DOWN, buff=LARGE_BUFF)
        planes.to_corner(UL)
        self.add(planes)

        # Titles
        titles = VGroup(
            Tex("f(x) = e^{-x^2}", font_size=66),
            Tex(R"F(x) = \int_0^x e^{-t^2} dt"),
        )
        for title, plane in zip(titles, planes):
            title.next_to(plane, RIGHT)

        ad_word = Text("Antiderivative")
        ad_word.next_to(titles[1], UP, MED_LARGE_BUFF)
        VGroup(ad_word, titles[1]).match_y(planes[1])

        self.add(titles)
        self.add(ad_word)

        # High graph
        x_tracker = ValueTracker(0)
        get_x = x_tracker.get_value
        high_graph = planes[0].get_graph(lambda x: np.exp(-x**2))
        high_graph.set_stroke(BLUE, 3)

        high_area = high_graph.copy()

        def update_area(area: VMobject):
            x = get_x()
            area.become(high_graph)
            area.set_stroke(width=0)
            area.set_fill(BLUE, 0.5)
            area.pointwise_become_partial(
                high_graph, 0, inverse_interpolate(x_min, x_max, x)
            )
            area.add_line_to(planes[0].c2p(x, 0))
            area.add_line_to(planes[0].c2p(x_min, 0))
            return area

        high_area.add_updater(update_area)

        self.add(high_graph, high_area)

        # Low graph
        dist = scipy.stats.norm(0, 1)
        low_graph = planes[1].get_graph(lambda x: math.sqrt(PI) * dist.cdf(x))
        low_graph.set_stroke(YELLOW, 2)
        low_dot = GlowDot()
        low_dot.add_updater(lambda m: m.move_to(planes[1].i2gp(get_x(), low_graph)))

        low_line = always_redraw(lambda: DashedLine(
            planes[1].c2p(get_x(), 0), planes[1].i2gp(get_x(), low_graph),
        ).set_stroke(WHITE, 2))

        self.add(low_graph, low_dot, low_line)

        # Animations
        for value in [1.5, -2, -1, 1, -0.5, 0.5, 3.0, -1.5]:
            self.play(x_tracker.animate.set_value(value), run_time=3)
            self.wait()
