# ==============================================================================
# Scene:      IllustrationUseVennDiagram
# Source:     videos/_2018/div_curl.py (lines 2338-2413)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IllustrationUseVennDiagram.py IllustrationUseVennDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IllustrationUseVennDiagram(Scene):
    def construct(self):
        title = Title("Divergence \\& Curl")
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        useful_for = OldTexText("Useful for")
        useful_for.next_to(title, DOWN)
        useful_for.set_color(BLUE)

        fluid_flow = OldTexText("Fluid \\\\ flow")
        fluid_flow.next_to(ORIGIN, UL)
        ff_circle = Circle(color=YELLOW)
        ff_circle.surround(fluid_flow, stretch=True)
        fluid_flow.match_color(ff_circle)

        big_circle = Circle(
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_color=BLUE,
        )
        big_circle.stretch_to_fit_width(9)
        big_circle.stretch_to_fit_height(6)
        big_circle.next_to(useful_for, DOWN, SMALL_BUFF)

        illustrated_by = OldTexText("Illustrated by")
        illustrated_by.next_to(
            big_circle.point_from_proportion(3. / 8), UL
        )
        illustrated_by.match_color(ff_circle)
        illustrated_by_arrow = Arrow(
            illustrated_by.get_bottom(),
            ff_circle.get_left(),
            path_arc=90 * DEGREES,
            color=YELLOW,
        )
        illustrated_by_arrow.pointwise_become_partial(
            illustrated_by_arrow, 0, 0.95
        )

        examples = VGroup(
            OldTexText("Electricity"),
            OldTexText("Magnetism"),
            OldTexText("Phase flow"),
            OldTexText("Stokes' theorem"),
        )
        points = [
            2 * RIGHT + 0.5 * UP,
            2 * RIGHT + 0.5 * DOWN,
            2 * DOWN,
            2 * LEFT + DOWN,
        ]
        for example, point in zip(examples, points):
            example.move_to(point)

        self.play(Write(title), run_time=1)
        self.play(
            Write(illustrated_by),
            ShowCreation(illustrated_by_arrow),
            run_time=1,
        )
        self.play(
            ShowCreation(ff_circle),
            FadeIn(fluid_flow),
        )
        self.wait()
        self.play(
            Write(useful_for),
            DrawBorderThenFill(big_circle),
            Animation(fluid_flow),
            Animation(ff_circle),
        )
        self.play(LaggedStartMap(
            FadeIn, examples,
            run_time=3,
        ))
        self.wait()
