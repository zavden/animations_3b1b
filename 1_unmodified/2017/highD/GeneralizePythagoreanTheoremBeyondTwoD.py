# ==============================================================================
# Scene:      GeneralizePythagoreanTheoremBeyondTwoD
# Source:     videos/_2017/highD.py (lines 1771-1842)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralizePythagoreanTheoremBeyondTwoD.py GeneralizePythagoreanTheoremBeyondTwoD -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralizePythagoreanTheoremBeyondTwoD(ThreeDScene):
    def construct(self):
        tex_to_color_map = {
            "x" : GREEN,
            "y" : RED,
            "z" : BLUE,
        }
        rect = Rectangle(
            height = 4, width = 5,
            fill_color = WHITE,
            fill_opacity = 0.2,
        )
        diag = Line(
            rect.get_corner(DOWN+LEFT),
            rect.get_corner(UP+RIGHT),
            color = YELLOW
        )
        bottom = Line(rect.get_left(), rect.get_right())
        bottom.move_to(rect.get_bottom())
        bottom.set_color(tex_to_color_map["x"])
        side = Line(rect.get_bottom(), rect.get_top())
        side.move_to(rect.get_right())
        side.set_color(tex_to_color_map["y"])

        x = OldTex("x")
        x.next_to(rect.get_bottom(), UP, SMALL_BUFF)
        y = OldTex("y")
        y.next_to(rect.get_right(), LEFT, SMALL_BUFF)
        hyp = OldTex("\\sqrt", "{x", "^2 + ", "y", "^2}")
        hyp.set_color_by_tex_to_color_map(tex_to_color_map)
        hyp.next_to(ORIGIN, UP)
        hyp.rotate(diag.get_angle())
        hyp.shift(diag.get_center())
        group = VGroup(rect, bottom, side, diag, x, y, hyp)

        self.add(rect)
        for line, tex in (bottom, x), (side, y), (diag, hyp):
            self.play(
                ShowCreation(line),
                Write(tex, run_time = 1)
            )
        self.wait()
        self.play(
            group.rotate, 0.45*np.pi, LEFT,
            group.shift, 2*DOWN
        )

        corner = diag.get_end()
        z_line = Line(corner, corner + 3*UP)
        z_line.set_color(tex_to_color_map["z"])
        z = OldTex("z")
        z.set_color(tex_to_color_map["z"])
        z.next_to(z_line, RIGHT)
        dot = Dot(z_line.get_end())
        three_d_diag = Line(diag.get_start(), z_line.get_end())
        three_d_diag.set_color(MAROON_B)

        self.play(
            ShowCreation(z_line),
            ShowCreation(dot),
            Write(z, run_time = 1)
        )
        self.play(ShowCreation(three_d_diag))
        self.wait()

        full_group = VGroup(group, z_line, z, three_d_diag, dot)
        self.play(Rotating(
            full_group, radians = -np.pi/6,
            axis = UP, 
            run_time = 10,
        ))
        self.wait()
