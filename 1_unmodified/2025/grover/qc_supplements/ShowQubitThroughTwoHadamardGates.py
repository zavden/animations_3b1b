# ==============================================================================
# Scene:      ShowQubitThroughTwoHadamardGates
# Source:     videos/_2025/grover/qc_supplements.py (lines 735-788)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowQubitThroughTwoHadamardGates.py ShowQubitThroughTwoHadamardGates -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowQubitThroughTwoHadamardGates(InteractiveScene):
    def construct(self):
        # Add the line
        line = Line(4 * LEFT, 4 * RIGHT)
        h_box = Square(1)
        h_box.set_fill(BLACK, 1).set_stroke(WHITE)
        h_box.add(Text("H", font_size=60))
        h_boxes = h_box.replicate(2)
        h_boxes.arrange(RIGHT, buff=3)

        self.add(line, Point(), h_boxes)

        # Symbols
        symbols = VGroup(
            Tex(R"|0\rangle", font_size=60),
            Tex(R"\frac{1}{\sqrt{2}}\left(|0\rangle + |1\rangle\right)"),
            Tex(R"|0\rangle", font_size=60),
        )
        symbols[0].next_to(line, LEFT, MED_SMALL_BUFF)
        symbols[1].next_to(line, UP, LARGE_BUFF)
        symbols[2].next_to(line, RIGHT, MED_SMALL_BUFF)

        mid_sym_rect = SurroundingRectangle(symbols[1], buff=0.2)
        mid_sym_lines = VGroup(
            Line(line.pfp(0.5 + 0.01 * u), mid_sym_rect.get_corner(DOWN + u * RIGHT))
            for u in [-1, 1]
        )
        VGroup(mid_sym_lines, mid_sym_rect).set_stroke(BLUE, 2)

        # Show progression
        dot = GlowDot(color=BLUE, radius=0.5)
        dot.move_to(line.get_left())
        dot.set_opacity(0)

        cover = FullScreenFadeRectangle()
        cover.set_fill(BLACK, 1)
        cover.stretch(0.45, 0, about_edge=RIGHT)

        self.add(line, dot, h_boxes, cover)

        self.play(FadeIn(symbols[0], 0.5 * UR, run_time=1))
        self.play(dot.animate.set_opacity(1))
        self.wait()
        self.play(dot.animate.move_to(line.get_center()))
        self.play(
            ShowCreation(mid_sym_lines, lag_ratio=0),
            GrowFromPoint(mid_sym_rect, dot.get_center()),
            GrowFromPoint(symbols[1], dot.get_center()),
        )
        self.wait()
        self.play(FadeOut(cover))
        self.play(dot.animate.move_to(line.get_end()))
        self.play(FadeIn(symbols[2], 0.25 * RIGHT, rate_func=rush_from))
        self.wait()
