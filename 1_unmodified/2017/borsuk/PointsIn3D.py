# ==============================================================================
# Scene:      PointsIn3D
# Source:     videos/_2017/borsuk.py (lines 1014-1054)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PointsIn3D.py PointsIn3D -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PointsIn3D(Scene):
    CONFIG = {
        # "colors" : [RED, GREEN, BLUE],
        "colors" : color_gradient([GREEN, BLUE], 3),
    }
    def construct(self):
        sphere_def = OldTexText(
            "\\doublespacing Sphere in 3D: All", "$(x_1, x_2, x_3)$\\\\", 
            "such that", "$x_1^2 + x_2^2 + x_3^2 = 1$",
            alignment = "",
        )
        sphere_def.next_to(ORIGIN, DOWN)
        for index, subindex_list in (1, [1, 2, 4, 5, 7, 8]), (3, [0, 2, 4, 6, 8, 10]):
            colors = np.repeat(self.colors, 2)
            for subindex, color in zip(subindex_list, colors):
                sphere_def[index][subindex].set_color(color)

        point_ex = OldTexText(
            "For example, ", 
            "(", "0.41", ", ", "-0.58", ", ", "0.71", ")",
            arg_separator = ""
        )
        for index, color in zip([2, 4, 6], self.colors):
            point_ex[index].set_color(color)
        point_ex.scale(0.8)
        point_ex.next_to(
            sphere_def[1], UP+RIGHT,
            buff = 1.5*LARGE_BUFF
        )
        point_ex.shift_onto_screen()
        arrow = Arrow(sphere_def[1].get_top(), point_ex.get_bottom())

        self.play(Write(sphere_def[1]))
        self.play(ShowCreation(arrow))
        self.play(Write(point_ex))
        self.wait()
        self.play(
            Animation(sphere_def[1].copy(), remover = True),
            Write(sphere_def),
        )
        self.wait()
