# ==============================================================================
# Scene:      GiveShapeAndPonder
# Source:     videos/_2017/fractal_dimension.py (lines 2162-2182)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GiveShapeAndPonder.py GiveShapeAndPonder -w -m --fps 15
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


class GiveShapeAndPonder(Scene):
    def construct(self):
        morty = Mortimer()
        randy = Randolph()
        morty.next_to(ORIGIN, DOWN).shift(3*RIGHT)
        randy.next_to(ORIGIN, DOWN).shift(3*LEFT)

        norway = Norway(fill_opacity = 0, stroke_width = 1)
        norway.set_width(2)
        norway.next_to(morty, UP+LEFT, buff = -MED_SMALL_BUFF)

        self.play(
            morty.change_mode, "raise_right_hand",
            morty.look_at, norway,
            randy.look_at, norway,
            ShowCreation(norway)
        )
        self.play(Blink(morty))
        self.play(randy.change_mode, "pondering")
        self.play(Blink(randy))
        self.wait()
