# ==============================================================================
# Scene:      Proof3Slide
# Source:     videos/_2022/visual_proofs/lies.py (lines 1708-1738)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Proof3Slide.py Proof3Slide -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Proof3Slide(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle())
        title = OldTexText("``Proof'' \\#3", font_size=60)
        subtitle = Text("All triangles are isosceles", font_size=60, color=BLUE)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)
        self.add(title, subtitle)

        # Triangle
        tri = Triangle()
        tri.set_fill(BLUE_E)
        tri.set_stroke(WHITE, 1)
        tri.stretch(2, 1)
        tri.to_corner(DL, buff=LARGE_BUFF).shift(RIGHT)
        A, B, C = tri.get_top(), tri.get_corner(DL), tri.get_corner(DR)
        AB = Line(A, B, color=YELLOW)
        AC = Line(A, C, color=TEAL)
        eq = OldTex("\\overline{AB}", " = ", "\\overline{AC}")
        eq.next_to(tri, UP)
        eq[0].match_color(AB)
        eq[2].match_color(AC)

        self.add(tri)
        self.play(ShowCreation(AB), Write(eq[0]))
        self.play(
            TransformFromCopy(AB, AC),
            FadeTransform(eq[0].copy(), eq[2]),
            Write(eq[1]),
        )
        self.wait()
