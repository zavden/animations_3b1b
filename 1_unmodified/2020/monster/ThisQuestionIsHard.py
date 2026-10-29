# ==============================================================================
# Scene:      ThisQuestionIsHard
# Source:     videos/_2020/monster.py (lines 3082-3159)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisQuestionIsHard.py ThisQuestionIsHard -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThisQuestionIsHard(Scene):
    def construct(self):
        # Setup line
        line = NumberLine(x_range=(0, 1, 0.1), width=12)
        line.shift(UP)
        arrows = VGroup(
            Arrow(line.n2p(0.5), line.n2p(0), fill_color=GREEN),
            Arrow(line.n2p(0.5), line.n2p(1), fill_color=RED),
        )
        arrows.shift(2.5 * DOWN)
        words = VGroup(OldTexText("Easier"), OldTexText("Harder"))
        for word, arrow in zip(words, arrows):
            word.match_color(arrow)
            word.next_to(arrow, DOWN, SMALL_BUFF)

        self.add(line)
        self.add(arrows)
        self.add(words)

        # Add problems
        problems = VGroup(
            OldTex("1 + 1"),
            VGroup(
                OldTex("\\frac{2^{289}+1}{2^{17}+1}=2^{a_{1}}+\\ldots+2^{a_{k}}"),
                OldTex("a_1 < \\ldots < a_k"),
                OldTex("a_1, \\dots, a_k \\in \\mathds{Z}^+"),
            ),
            VGroup(
                OldTex("{a \\over b + c} + {b \\over c + a} + {c \\over b + c} = 4"),
                OldTex("a, b, c \\in \\mathds{Z}^+"),
            ),
            VGroup(
                OldTex("x^n + y^n = z^n"),
                OldTex("x, y, z \\in \\mathds{Z}"),
            ),
        )
        colors = Color(GREEN).range_to(RED, 4)
        for prob, x, color in zip(problems, [0, 0.3, 0.7, 1], colors):
            triangle = Triangle()
            triangle.set_height(0.2)
            triangle.set_stroke(width=0)
            triangle.set_fill(color, 1)
            triangle.move_to(line.n2p(x), UP)
            prob.arrange(DOWN)
            prob.scale(0.5)
            prob.next_to(triangle, DOWN)
            prob.add(triangle)
            prob.set_color(color)

        self.add(problems)

        # Group question
        tri = Triangle(start_angle=-90 * DEGREES)
        tri.set_height(0.3)
        tri.set_stroke(width=0)
        tri.set_fill(GREY_B, 1)
        tri.move_to(line.n2p(0.5), DOWN)
        question = OldTexText("What are all\\\\the groups?")
        question.next_to(tri, UP)

        ext_line = line.copy()
        ext_line.move_to(line.get_right(), LEFT)

        frame = self.camera.frame

        self.play(
            DrawBorderThenFill(tri),
            FadeIn(question, DOWN)
        )
        question.add(tri)
        self.play(question.move_to, line.n2p(0.9), DOWN)
        self.wait()
        self.play(
            ShowCreation(ext_line),
            question.move_to, line.n2p(1.3), DOWN,
            ApplyMethod(frame.scale, 1.3, {"about_edge": LEFT}, run_time=2)
        )
        self.wait()
