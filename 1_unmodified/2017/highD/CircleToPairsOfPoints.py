# ==============================================================================
# Scene:      CircleToPairsOfPoints
# Source:     videos/_2017/highD.py (lines 376-499)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircleToPairsOfPoints.py CircleToPairsOfPoints -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CircleToPairsOfPoints(Scene):
    def construct(self):
        plane = NumberPlane(written_coordinate_height = 0.3)
        plane.scale(2)
        plane.add_coordinates(y_vals = [-1, 1])
        background_plane = plane.copy()
        background_plane.set_color(GREY)
        background_plane.fade()
        circle = Circle(radius = 2, color = YELLOW)

        x, y = [np.sqrt(2)/2]*2
        dot = Dot(2*x*RIGHT + 2*y*UP, color = GREY_B)

        equation = OldTex("x", "^2", "+", "y", "^2", "=", "1")
        equation.set_color_by_tex("x", GREEN)
        equation.set_color_by_tex("y", RED)
        equation.to_corner(UP+LEFT)
        equation.add_background_rectangle()

        coord_pair = OldTex("(", "-%.02f"%x, ",", "-%.02f"%y, ")") 
        fixed_numbers = coord_pair.get_parts_by_tex("-")
        fixed_numbers.set_fill(opacity = 0)
        coord_pair.add_background_rectangle()
        coord_pair.next_to(dot, UP+RIGHT, SMALL_BUFF)
        numbers = VGroup(*[
            DecimalNumber(val).replace(num, dim_to_match = 1)
            for val, num in zip([x, y], fixed_numbers)
        ])
        numbers[0].set_color(GREEN)
        numbers[1].set_color(RED)

        def get_update_func(i):
            return lambda t : dot.get_center()[i]/2.0


        self.add(background_plane, plane)
        self.play(ShowCreation(circle))
        self.play(
            FadeIn(coord_pair),
            Write(numbers, run_time = 1),
            ShowCreation(dot),
        )
        self.play(
            Write(equation),
            *[
                Transform(
                    number.copy(),
                    equation.get_parts_by_tex(tex),
                    remover = True
                )
                for tex, number in zip("xy", numbers)
            ]
        )
        self.play(FocusOn(dot, run_time = 1))
        self.play(
            Rotating(
                dot, run_time = 7, in_place = False,
                rate_func = smooth,
            ),
            MaintainPositionRelativeTo(coord_pair, dot),
            *[
                ChangingDecimal(
                    num, get_update_func(i),
                    tracked_mobject = fixed_num
                )
                for num, i, fixed_num in zip(
                    numbers, (0, 1), fixed_numbers
                )
            ]
        )
        self.wait()

        ######### Rotation equations ##########

        rot_equation = OldTex(
            "\\Rightarrow"
            "\\big(\\cos(\\theta)x - \\sin(\\theta)y\\big)^2 + ",
            "\\big(\\sin(\\theta)x + \\cos(\\theta)y\\big)^2 = 1",
        )
        rot_equation.scale(0.9)
        rot_equation.next_to(equation, RIGHT)
        rot_equation.add_background_rectangle()

        words = OldTexText("Rotational \\\\ symmetry")
        words.next_to(ORIGIN, UP)
        words.to_edge(RIGHT)
        words.add_background_rectangle()

        arrow = Arrow(
            words.get_left(), rot_equation.get_bottom(),
            path_arc = -np.pi/6
        )
        randy = Randolph(color = GREY_BROWN)
        randy.to_corner(DOWN+LEFT)

        self.play(
            Write(rot_equation, run_time = 2),
            FadeOut(coord_pair),
            FadeOut(numbers),
            FadeOut(dot),
            FadeIn(randy)
        )
        self.play(randy.change, "confused", rot_equation)
        self.play(Blink(randy))
        self.play(
            Write(words, run_time = 1),
            ShowCreation(arrow),
            randy.look_at, words
        )
        plane.remove(*plane.coordinate_labels)
        self.play(
            Rotate(
                plane, np.pi/3, 
                run_time = 4,
                rate_func = there_and_back
            ),
            Animation(equation),
            Animation(rot_equation),
            Animation(words),
            Animation(arrow),
            Animation(circle),
            randy.change, "hooray"
        )
        self.wait()
