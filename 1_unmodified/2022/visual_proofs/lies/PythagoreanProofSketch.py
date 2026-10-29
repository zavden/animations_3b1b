# ==============================================================================
# Scene:      PythagoreanProofSketch
# Source:     videos/_2022/visual_proofs/lies.py (lines 2208-2329)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PythagoreanProofSketch.py PythagoreanProofSketch -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PythagoreanProofSketch(InteractiveScene):
    def construct(self):
        # First orientation
        tri = Polygon(ORIGIN, UP, 2 * RIGHT)
        tri.set_stroke(WHITE, 1)
        tri.set_fill(BLUE_E, 1)

        verts = tri.get_vertices()
        tris = VGroup(tri, tri.copy().rotate(PI, about_point=midpoint(*verts[1:])))
        tris.add(*tris.copy().rotate(PI, axis=UL, about_point=tris.get_corner(DL)))
        tris[2:4].flip(UP)
        big_square = SurroundingRectangle(tris, buff=0)
        big_square.set_stroke(WHITE, 2)
        VGroup(tris, big_square).center().set_height(5)

        A, B = tri.get_height(), tri.get_width()
        a_square = Square(A)
        a_square.move_to(big_square, UL)
        a_square.set_fill(RED_C, 0.75)
        b_square = Square(B)
        b_square.move_to(big_square, DR)
        b_square.set_fill(RED_D, 0.75)

        a_square_label = Tex("a^2").move_to(a_square)
        b_square_label = Tex("b^2").move_to(b_square)

        # Pre triangle
        pre_tri = tris[0].copy()
        pre_tri.scale(1.5)
        pre_tri.shift(-pre_tri.get_center_of_mass())
        side_labels = Tex("abc")
        side_labels[0].next_to(pre_tri, LEFT)
        side_labels[1].next_to(pre_tri, DOWN)
        side_labels[2].next_to(pre_tri.get_center(), UR)

        self.add(pre_tri)
        self.add(side_labels)

        # Equation
        equation = Tex("a^2 + b^2 = c^2", isolate=["a^2", "+", "b^2", "=", "c^2"])
        equation.next_to(big_square, UP).to_edge(UP)

        # A^2 and B^2
        scale_factor = tris[0].get_height() / pre_tri.get_height()
        shift_vect = tris[0].get_center() - pre_tri.get_center()
        self.play(
            ReplacementTransform(pre_tri, tris[0]),
            side_labels.animate.scale(scale_factor, about_point=pre_tri.get_center()).shift(shift_vect)
        )
        self.add(tris[1], side_labels)
        self.play(LaggedStart(
            TransformFromCopy(tris[0], tris[1], path_arc=PI),
            TransformFromCopy(tris[0], tris[2]),
            TransformFromCopy(tris[0], tris[3]),
            FadeIn(big_square),
            Animation(side_labels),
            lag_ratio=0.3
        ))
        self.play(
            FadeIn(a_square),
            FadeTransform(side_labels[0], a_square_label),
            FadeIn(b_square),
            FadeTransform(side_labels[1], b_square_label),
        )
        self.play(
            FadeOut(a_square),
            FadeOut(b_square),
            TransformFromCopy(a_square_label, equation.select_parts("a^2")),
            TransformFromCopy(b_square_label, equation.select_parts("b^2")),
            Write(equation.select_parts("+")),
        )
        self.wait()

        # Second orientation
        tris.save_state()
        tris2 = tris.copy()

        tris2[0].rotate(PI / 2, OUT, about_point=tris2[0].get_corner(DR))
        tris2[3].rotate(-PI / 2).move_to(big_square, DL)
        tris2[2].move_to(big_square, UL)

        c_square = Square(math.sqrt(A**2 + B**2))
        c_square.rotate(math.atan(B / A))
        c_square.move_to(big_square)
        c_square.set_fill(RED_D, 0.7)
        c_square_label = Tex("c^2").move_to(c_square)

        self.play(LaggedStart(
            FadeOut(a_square_label),
            FadeOut(b_square_label),
            *(Transform(tris[i], tris2[i]) for i in (0, 2, 3)),
            lag_ratio=0.5
        ))
        self.wait()

        self.play(
            FadeIn(c_square),
            FadeIn(c_square_label),
        )
        self.play(
            FadeTransform(c_square_label.copy(), equation.select_parts("c^2")),
            Write(equation.select_parts("=")),
            c_square.animate.set_fill(opacity=0.5)
        )
        self.wait()
        self.play(FadeOut(c_square))

        # Final gif
        self.play(
            Transform(tris, tris.saved_state, lag_ratio=0.2, run_time=3, path_arc=45 * DEGREES),
            FadeOut(c_square_label),
            FadeIn(a_square_label, time_span=(1.5, 2.5)),
            FadeIn(b_square_label, time_span=(2, 3)),
        )
        self.wait()
        self.play(
            Transform(tris, tris2, lag_ratio=0.2, run_time=3, path_arc=45 * DEGREES),
            FadeIn(c_square_label, time_span=(2, 3)),
            FadeOut(a_square_label, time_span=(0, 1)),
            FadeOut(b_square_label, time_span=(0.5, 1.5)),
        )
        self.wait()
