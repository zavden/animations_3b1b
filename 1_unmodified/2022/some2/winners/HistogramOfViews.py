# ==============================================================================
# Scene:      HistogramOfViews
# Source:     videos/_2022/some2/winners.py (lines 333-449)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HistogramOfViews.py HistogramOfViews -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HistogramOfViews(InteractiveScene):
    data = [
        628083,
        396785,
        359233,
        301850,
        245930,
        243370,
        231732,
        212708,
        209343,
        208586,
        167442,
        153613,
        145692,
        135465,
        130783,
        126159,
        101919,
        93069,
        92110,
        89790,
        82160,
        81311,
        79598,
        67092,
        63373,
        63239,
        62246,
        56242,
        52840,
        47267,
        45942,
        43032,
        42558,
        41618,
        41201,
        39059,
        36675,
        36138,
        35999,
        35999,
        35805,
        34057,
        33137,
        33009,
        31064,
        30855,
        30616,
        30122,
        30016,
        28817,
    ]

    def construct(self):
        # Add axes
        axes = Axes((0, 50, 50), (0, 6e5, 1e5), width=12, height=6)
        axes.to_corner(DR)

        y_step = 100000
        axes.add_coordinate_labels(
            x_values=range(0),
            y_values=range(y_step, 7 * y_step, y_step),
        )
        self.add(axes)

        # Bars
        bars = VGroup(*(
            Rectangle(
                width=axes.x_axis.get_width() / len(self.data),
                height=value * axes.y_axis.unit_size,
            )
            for value in self.data
        ))
        bars.arrange(RIGHT, aligned_edge=DOWN, buff=0)
        bars.set_fill(opacity=1)
        bars.set_submobject_colors_by_gradient(BLUE_D, TEAL)
        bars.set_stroke(BLACK, 2)
        bars.move_to(axes.get_origin(), DL)
        bars.shift(0.01 * UR)
        self.add(bars)

        # Title
        title = Text(
            "Distribution of SoME2 views (top 50 shown)"
        )
        title.move_to(axes, UP)
        subtitle = Text("7,000,000+ total", font_size=36, fill_color=GREY_B)
        subtitle.next_to(title, DOWN)

        self.add(title, subtitle)

        # Animate bars
        self.remove(bars)
        bars.sort(lambda p: -p[0])
        self.play(LaggedStart(*(
            ReplacementTransform(bar.copy().stretch(0, 1, about_edge=DOWN), bar)
            for bar in bars
        )), lag_ratio=0.2)
        self.add(bars)

        # SoME1
        some1_words = Text("""
            2,000,000+
            Additional SoME1 views
            during this time
        """, font_size=36)
        box = SurroundingRectangle(some1_words, buff=MED_LARGE_BUFF)
        box.set_fill(GREY_E, 1)
        box.set_stroke(WHITE, 1)
        VGroup(box, some1_words).to_edge(RIGHT)

        self.play(
            FadeIn(box),
            Write(some1_words),
        )
        self.wait()
