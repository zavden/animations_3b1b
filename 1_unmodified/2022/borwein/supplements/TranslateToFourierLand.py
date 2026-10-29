# ==============================================================================
# Scene:      TranslateToFourierLand
# Source:     videos/_2022/borwein/supplements.py (lines 445-542)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TranslateToFourierLand.py TranslateToFourierLand -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TranslateToFourierLand(InteractiveScene):
    def construct(self):
        # Setup right side
        right_rect = FullScreenRectangle()
        right_rect.set_fill(TEAL, 0.2)
        right_rect.set_stroke(width=0)
        right_rect.stretch(0.5, 0, about_edge=RIGHT)
        ft_label = Text("Fourier Land", font_size=60)
        ft_label.next_to(right_rect.get_top(), DOWN, MED_SMALL_BUFF)
        ft_label.set_backstroke(width=5)
        ft_label.set_fill(TEAL)
        self.add(right_rect, ft_label)

        # Break up a wave?
        left_rect = right_rect.copy().to_edge(LEFT, buff=0)
        axes_kw = dict(width=FRAME_WIDTH - 2, height=3)
        left_axes = VGroup(*(
            Axes((0, 12, 1), (-2, 2), **axes_kw).scale(0.5)
            for x in range(3)
        ))
        left_axes.arrange(DOWN, buff=0.7)
        left_axes.move_to(left_rect).to_edge(DOWN, buff=SMALL_BUFF)

        left_graphs = VGroup(
            left_axes[0].get_graph(lambda x: math.sin(3 * x)),
            left_axes[1].get_graph(lambda x: math.sin(4 * x)),
            left_axes[2].get_graph(lambda x: math.sin(3 * x) + math.sin(4 * x)),
        )
        left_graphs.set_submobject_colors_by_gradient(BLUE, YELLOW, GREEN)

        left_symbols = VGroup(OldTex("+"), OldTex("=").rotate(PI / 2)).scale(1.5)
        left_symbols[0].move_to(left_axes[0:2])
        left_symbols[1].move_to(left_axes[1:3])

        # Peaks in Fourier land
        right_axes = VGroup(*(
            Axes((0, 5), (0, 3), **axes_kw).scale(0.5)
            for x in range(3)
        ))
        for a1, a2 in zip(left_axes, right_axes):
            a2.match_y(a1).match_x(right_rect)

        def bell(x, n):
            return 3 * np.exp(-40 * (x - n)**2)

        right_graphs = VGroup(
            right_axes[0].get_graph(lambda x: bell(x, 3)),
            right_axes[1].get_graph(lambda x: bell(x, 4)),
            right_axes[2].get_graph(lambda x: bell(x, 3) + bell(x, 4)),
        )
        right_graphs.match_style(left_graphs)
        right_symbols = left_symbols.copy().match_x(right_rect).shift(0.5 * DOWN)

        self.play(
            LaggedStartMap(FadeIn, left_axes, lag_ratio=0.7),
            LaggedStartMap(ShowCreation, left_graphs, lag_ratio=0.7),
            LaggedStartMap(Write, left_symbols, lag_ratio=0.7),
            run_time=3
        )
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(left_axes, right_axes),
            TransformFromCopy(left_graphs, right_graphs),
            TransformFromCopy(left_symbols, right_symbols),
        ))
        self.wait(3)

        # Other properties
        to_fade = VGroup(
            left_axes, left_graphs, left_symbols,
            right_axes, right_graphs, right_symbols,
        )

        property_pairs = [
            VGroup(
                OldTex(R"\int_{-\infty}^\infty f(t) dt"),
                OldTex(R"\hat f(0)"),
            ),
            VGroup(
                OldTex(R"f(t) \cdot g(t)"),
                # OldTex(R"\hat f(\omega) * \hat g(\omega)", tex_to_color_map={R"\omega": YELLOW}),
                OldTex(R"\int_{-\infty}^\infty \hat f(\xi) \hat g(\omega - \xi) d\xi", tex_to_color_map={R"\omega": YELLOW}),
            ),
            VGroup(
                OldTex(R"\sum_{n = -\infty}^\infty f(n)"),
                OldTex(R"\sum_{k = -\infty}^\infty \hat f(k)"),
            ),
        ]

        for pair in property_pairs:
            pair.scale(1.5)
            m1, m2 = pair
            m1.move_to(left_rect)
            m2.move_to(right_rect)

            self.play(FadeOut(to_fade), FadeIn(pair))
            self.wait(3)
            to_fade = pair
