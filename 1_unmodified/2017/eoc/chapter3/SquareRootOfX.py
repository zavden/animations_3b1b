# ==============================================================================
# Scene:      SquareRootOfX
# Source:     videos/_2017/eoc/chapter3.py (lines 2009-2123)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SquareRootOfX.py SquareRootOfX -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SquareRootOfX(Scene):
    CONFIG = {
        "square_color_kwargs" : {
            "stroke_color" : WHITE,
            "stroke_width" : 1,
            "fill_color" : BLUE_E,
            "fill_opacity" : 1,
        },
        "bigger_square_color_kwargs" : {
            "stroke_color" : WHITE,
            "stroke_width" : 1,
            "fill_color" : YELLOW,
            "fill_opacity" : 0.7,
        },
        "square_corner" : 6*LEFT+3*UP,
        "square_width" : 3,
        "d_sqrt_x" : 0.3,
    }
    def construct(self):
        self.add_title()
        self.introduce_square()
        self.nudge_square()

    def add_title(self):
        title = OldTex("f(x) = \\sqrt{x}")
        title.next_to(ORIGIN, RIGHT)
        title.to_edge(UP)
        self.add(title)

    def introduce_square(self):
        square = Square(
            side_length = self.square_width,
            **self.square_color_kwargs
        )
        square.move_to(self.square_corner, UP+LEFT)
        area_label = OldTexText("Area $ = x$")
        area_label.move_to(square)

        bottom_brace, right_brace = braces = VGroup(*[
            Brace(square, vect)
            for vect in (DOWN, RIGHT)
        ])
        for brace in braces:
            brace.add(brace.get_text("$\\sqrt{x}$"))


        self.play(
            DrawBorderThenFill(square),
            Write(area_label)
        )
        self.play(*list(map(FadeIn, braces)))
        self.wait()

        self.square = square
        self.area_label = area_label
        self.braces = braces

    def nudge_square(self):
        square = self.square
        area_label = self.area_label
        bottom_brace, right_brace = self.braces

        bigger_square = Square(
            side_length = self.square_width + self.d_sqrt_x,
            **self.bigger_square_color_kwargs
        )
        bigger_square.move_to(self.square_corner, UP+LEFT)

        square_copy = square.copy()

        lines = VGroup(*[
            DashedLine(
                ORIGIN,
                (self.square_width + MED_LARGE_BUFF)*vect,
                color = WHITE,
                stroke_width = 3
            ).shift(s.get_corner(corner))
            for corner, vect in [(DOWN+LEFT, RIGHT), (UP+RIGHT, DOWN)]
            for s in [square, bigger_square]
        ])
        little_braces = VGroup(*[
            Brace(VGroup(*line_pair), vect, buff = 0)
            for line_pair, vect in [(lines[:2], RIGHT), (lines[2:], DOWN)]
        ])
        for brace in little_braces:
            tex = brace.get_text("$d\\sqrt{x}$", buff = SMALL_BUFF)
            tex.scale(0.8)
            brace.add(tex)

        area_increase = OldTexText("$dx$ = New area")
        area_increase.set_color(bigger_square.get_color())
        area_increase.next_to(square, RIGHT, 4)

        question = OldTex("\\frac{d\\sqrt{x}}{dx} = ???")
        VGroup(*question[5:7]).set_color(bigger_square.get_color())
        question.next_to(
            area_increase, DOWN, 
            aligned_edge = LEFT, 
            buff = LARGE_BUFF
        )
        
        self.play(
            Transform(square_copy, bigger_square),
            Animation(square),
            Animation(area_label),
            bottom_brace.next_to, bigger_square, DOWN, SMALL_BUFF, LEFT,
            right_brace.next_to, bigger_square, RIGHT, SMALL_BUFF, UP,
        )
        self.play(Write(area_increase))
        self.play(*it.chain(
            list(map(ShowCreation, lines)),
            list(map(FadeIn, little_braces))
        ))
        self.play(Write(question))
        self.wait()
