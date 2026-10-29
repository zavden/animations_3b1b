# ==============================================================================
# Scene:      WriteAntipodalCoordinates
# Source:     videos/_2017/borsuk.py (lines 1098-1112)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteAntipodalCoordinates.py WriteAntipodalCoordinates -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WritePointCoordinates(Scene):
    CONFIG = {
        "colors" : color_gradient([GREEN, BLUE], 3),
        "corner" : DOWN+RIGHT,
    }
    def construct(self):
        coords = self.get_coords()
        arrow = Arrow(
            -self.corner, self.corner, 
            stroke_width = 8,
            color = MAROON_B
        )
        x_component = self.corner[0]*RIGHT
        y_component = self.corner[1]*UP
        arrow.next_to(
            coords.get_edge_center(y_component), 
            y_component, 
            aligned_edge = -x_component,
            buff = MED_SMALL_BUFF
        )

        group = VGroup(coords, arrow)
        group.scale(2)        
        group.to_corner(self.corner)


        self.play(FadeIn(coords))
        self.play(ShowCreation(arrow))
        self.wait()

    def get_coords(self):
        coords = OldTex(
            "(", "0.41", ", ", "-0.58", ", ", "0.71", ")",
            arg_separator = ""
        )
        for index, color in zip([1, 3, 5], self.colors):
            coords[index].set_color(color)
        return coords


class WriteAntipodalCoordinates(WritePointCoordinates):
    CONFIG = {
        "corner" : UP+LEFT,
        "sign_color" : RED,
    }

    def get_coords(self):
        coords = OldTex(
            "(", "-", "0.41", ", ", "+", "0.58", ", ", "-", "0.71", ")",
            arg_separator = ""
        )
        for index, color in zip([2, 5, 8], self.colors):
            coords[index].set_color(color)
            coords[index-1].set_color(self.sign_color)
        return coords
