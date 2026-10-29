# ==============================================================================
# Scene:      PopularizaitonVsDoing
# Source:     videos/_2021/shadows.py (lines 5912-5975)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PopularizaitonVsDoing.py PopularizaitonVsDoing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PopularizaitonVsDoing(Scene):
    def construct(self):
        # Words
        popular = Text("Popularization of math")
        doing = Text("Doing math")
        words = VGroup(popular, doing)
        words.arrange(DOWN, buff=3)
        words.move_to(UP)

        self.play(FadeIn(popular, UP))
        self.wait()
        self.play(
            TransformFromCopy(
                popular.get_part_by_text("math"),
                doing.get_part_by_text("math"),
            ),
            Write(doing[:len("Doing")])
        )
        self.wait()

        # Bars
        width = 8
        bar = Rectangle(width, 0.5)
        bar.set_stroke(WHITE, 1)
        bar.next_to(popular, DOWN)
        left_bar, right_bar = bar.replicate(2)
        left_bar.set_fill(BLUE_E, 1)
        right_bar.set_fill(RED_E, 1)
        left_bar.stretch(0.5, 0, about_edge=LEFT)
        right_bar.stretch(0.5, 0, about_edge=RIGHT)

        left_brace = always_redraw(lambda: Brace(left_bar, DOWN, buff=SMALL_BUFF))
        right_brace = always_redraw(lambda: Brace(right_bar, DOWN, buff=SMALL_BUFF))
        left_label = Text("Insights", font_size=30, color=GREY_B)
        right_label = Text("Computations", font_size=30, color=GREY_B)
        always(left_label.next_to, left_brace, DOWN, SMALL_BUFF)
        always(right_label.next_to, right_brace, DOWN, SMALL_BUFF)

        bar_group = VGroup(
            bar,
            left_bar, right_bar,
            left_brace, right_brace,
            left_label, right_label,
        )

        def set_bar_alpha(alpha, **kwargs):
            self.play(
                left_bar.animate.set_width(alpha * width, about_edge=LEFT, stretch=True),
                right_bar.animate.set_width((1 - alpha) * width, about_edge=RIGHT, stretch=True),
                **kwargs
            )

        self.play(FadeIn(bar_group, lag_ratio=0.1))
        set_bar_alpha(0.95, run_time=2)
        self.wait()
        self.add(bar_group.deepcopy().clear_updaters())
        self.play(
            bar_group.animate.shift(doing.get_center() - popular.get_center())
        )
        set_bar_alpha(0.05, run_time=5)
        self.wait()

        # Embed
        self.embed()
