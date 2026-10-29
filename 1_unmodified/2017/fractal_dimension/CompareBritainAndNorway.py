# ==============================================================================
# Scene:      CompareBritainAndNorway
# Source:     videos/_2017/fractal_dimension.py (lines 2703-2748)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareBritainAndNorway.py CompareBritainAndNorway -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Britain(SVGMobject):
    CONFIG = {
        "file_name" : "Britain.svg",
        "stroke_width" : 0,
        "fill_color" : BLUE_D,
        "fill_opacity" : 1,
        "height" : 5,
        "mark_paths_closed" : True,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.set_points(self[0].get_points())
        self.submobjects = []
        self.set_height(self.height)
        self.center()


class Norway(Britain):
    CONFIG = {
        "file_name" : "Norway",
        "mark_paths_closed" : False
    }


class CompareBritainAndNorway(Scene):
    def construct(self):
        norway = Norway(
            fill_opacity = 0,
            stroke_width = 2,
        )
        norway.to_corner(UP+RIGHT, buff = 0)
        fractalify(norway, order = 1, dimension = 1.5)
        anchors = list(norway.get_anchors())
        anchors.append(FRAME_X_RADIUS*RIGHT+FRAME_Y_RADIUS*UP)
        norway.set_points_as_corners(anchors)

        britain = Britain(
            fill_opacity = 0,
            stroke_width = 2
        )
        britain.shift(FRAME_X_RADIUS*LEFT/2)
        britain.to_edge(UP)
        fractalify(britain, order = 1, dimension = 1.21)

        britain_label = OldTexText("""
            Britain coast:
            1.21-dimensional
        """)
        norway_label = OldTexText("""
            Norway coast:
            1.52-dimensional
        """)
        britain_label.next_to(britain, DOWN)
        norway_label.next_to(britain_label, RIGHT, aligned_edge = DOWN)
        norway_label.to_edge(RIGHT)

        self.add(britain_label, norway_label)
        self.play(
            *list(map(ShowCreation, [norway, britain])),
            run_time = 3
        )
        self.wait()
        self.play(*it.chain(*[
            [
                mob.set_stroke, None, 0,
                mob.set_fill, BLUE, 1
            ]
            for mob in (britain, norway)
        ]))
        self.wait(2)
