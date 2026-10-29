# ==============================================================================
# Scene:      Eoc1Thumbnail
# Source:     videos/_2017/eoc/chapter1.py (lines 5-62)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Eoc1Thumbnail.py Eoc1Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Eoc1Thumbnail(GraphScene):
    CONFIG = {

    }

    def construct(self):
        title = OldTexText(
            "The Essence of\\\\Calculus",
            tex_to_color_map={
                "\\emph{you}": YELLOW,
            },
        )
        subtitle = OldTexText("Chapter 1")
        subtitle.match_width(title)
        subtitle.scale(0.75)
        subtitle.next_to(title, DOWN)
        # title.add(subtitle)
        title.set_width(FRAME_WIDTH - 2)
        title.to_edge(UP)
        title.set_stroke(BLACK, 8, background=True)
        # answer = OldTexText("...yes")
        # answer.to_edge(DOWN)

        axes = Axes(
            x_range=(-1, 5),
            y_range=(-1, 5),
            y_axis_config={
                "include_tip": False,
            },
            x_axis_config={
                "unit_size": 2,
            },
        )
        axes.set_width(FRAME_WIDTH - 1)
        axes.center().to_edge(DOWN)
        axes.shift(DOWN)
        self.x_axis = axes.x_axis
        self.y_axis = axes.y_axis
        self.axes = axes

        graph = self.get_graph(self.func)
        rects = self.get_riemann_rectangles(
            graph,
            x_min=0, x_max=4,
            dx=0.2,
        )
        rects.set_submobject_colors_by_gradient(BLUE, GREEN)
        rects.set_opacity(1)
        rects.set_stroke(BLACK, 1)

        self.add(axes)
        self.add(graph)
        self.add(rects)
        # self.add(title)
        # self.add(answer)

    def func(self, x):
        return 0.35 * ((x - 2)**3 - 2 * (x - 2) + 6)
