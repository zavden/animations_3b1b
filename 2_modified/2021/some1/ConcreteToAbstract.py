# ==============================================================================
# Scene:      ConcreteToAbstract
# Source:     videos/_2021/some1.py (lines 788-868)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ConcreteToAbstract.py ConcreteToAbstract -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
# ==============================================================================

from manim_imports_ext import *

def get_h_line():
    line = DashedLine(ORIGIN, FRAME_WIDTH * RIGHT)
    line.center()
    return line


class ConcreteToAbstract(Scene):
    def construct(self):
        self.add(
            get_h_line().move_to(FRAME_HEIGHT * UP / 6),
            get_h_line().move_to(FRAME_HEIGHT * DOWN / 6),
        )

        labels = VGroup(
            Text("Algebra"),
            Text("Numbers"),
            Text("Quantities"),
        )
        for i, label in enumerate(labels):
            label.scale(30 / label.font_size)
            label.to_corner(UL, buff=SMALL_BUFF)
            label.shift(i * FRAME_HEIGHT * DOWN / 3)

        self.add(labels)

        # Algebra
        expr = OldTex(
            "x^2 - y^2 = (x + y)(x - y)",
            tex_to_color_map={"x": BLUE_D, "y": BLUE_B}
        )
        expr.scale(1.5)
        expr.move_to(FRAME_HEIGHT * UP / 3)
        expr.to_edge(LEFT, buff=LARGE_BUFF)
        self.add(expr)

        # Numbers
        tricks = VGroup(
            OldTex("143 = (12 + 1)(12 - 1) = 13 \\cdot 11"),
            OldTex("3{,}599 = (60 + 1)(60 - 1) = 61 \\cdot 59"),
            OldTex("9{,}991 = (100 + 3)(100 - 3) = 103 \\cdot 97"),
        )
        tricks.arrange(DOWN, aligned_edge=LEFT)
        tricks[0].shift((tricks[1][0][5].get_x() - tricks[0][0][3].get_x()) * RIGHT)
        tricks.set_height(FRAME_HEIGHT / 3 - 1)
        tricks.center()
        brace = Brace(tricks, LEFT)
        words = OldTexText("Factoring\\\\tricks", font_size=30)
        words.set_color(GREY_A)
        words.next_to(brace, LEFT)
        VGroup(tricks, brace, words).to_edge(LEFT, buff=MED_LARGE_BUFF)

        self.add(tricks, brace, words)
        self.wait()

        # Arrows
        # CHANGE: Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
        arrow = FillArrow(
            ORIGIN, FRAME_HEIGHT * UP / 3,
            path_arc=60 * DEGREES,
            thickness=0.15,
            fill_color=YELLOW,
            stroke_color=YELLOW,
        )
        up_arrows = VGroup(arrow.copy().shift(FRAME_HEIGHT * DOWN / 3), arrow)
        up_arrows.to_edge(RIGHT, buff=1.5)

        self.play(Write(up_arrows, lag_ratio=0.5))
        self.wait()

        top_words = Text("Once you understand\n algebra...")
        top_words.next_to(up_arrows, UP)
        top_words.shift_onto_screen()
        top_words.set_color(YELLOW)

        self.play(FadeIn(top_words, lag_ratio=0.05))
        self.play(LaggedStartMap(Rotate, up_arrows, angle=PI, axis=RIGHT))
        self.wait()

        new_top_words = Text("If you're learning\n algebra.")
        new_top_words.move_to(top_words)
        new_top_words.match_color(top_words)
        self.play(
            FadeTransform(top_words, new_top_words),
            LaggedStartMap(Rotate, up_arrows, angle=PI, axis=RIGHT)
        )
        self.wait()

        self.embed()
