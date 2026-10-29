# ==============================================================================
# Scene:      FalseEuclidProofAnnotation
# Source:     videos/_2022/visual_proofs/lies.py (lines 1904-2033)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FalseEuclidProofAnnotation.py FalseEuclidProofAnnotation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - white braces and outline of triangle ABC as a stand-in for the unavailable Dropbox image (with black braces on a black background the video came out empty)
# ==============================================================================

from manim_imports_ext import *

class FalseEuclidProofAnnotation(InteractiveScene):
    def construct(self):
        # path = "/Users/grant/Dropbox/3Blue1Brown/videos/2022/visual_proofs/lies/images/FalseEuclidProof.jpg"
        # self.add(ImageMobject(path).set_width(FRAME_WIDTH))

        # Points
        A = np.array([-1.94444444, 1.44444444, 0.])
        B = np.array([-4.44444444, -0.02777778, 0.])
        C = np.array([-1.09722222, -0.48611111, 0.])
        D = np.array([-2.63888889, -0.27777778, 0.])
        E = np.array([-1.56944444, 0.55555556, 0.])
        F = np.array([-3.01388889, 0.83555556, 0.])
        P = np.array([-2.58333333, 0.122222, 0.])
        # dots = Group(*(GlowDot(point, color=RED) for point in [A, B, C, D, E, F, P]))

        AFP = Polygon(A, F, P)
        AEP = Polygon(A, E, P)
        BPD = Polygon(B, P, D)
        CPD = Polygon(C, P, D)
        BFP = Polygon(B, F, P)
        CEP = Polygon(C, E, P)

        tris = VGroup(AFP, AEP, BPD, CPD, BFP, CEP)
        tris.set_stroke(BLACK, 1)
        tris[:2].set_fill(BLUE)
        tris[2:4].set_fill(GREEN)
        tris[4:].set_fill(RED)
        tris.set_fill(opacity=0.8)

        # Final sum
        AF = Line(A, F)
        FB = Line(F, B)
        AB = Line(A, B)
        AE = Line(A, E)
        EC = Line(E, C)
        AC = Line(A, C)
        lines = VGroup(AF, FB, AB, AE, EC, AC)
        for line in lines:
            brace = Brace(Line(ORIGIN, line.get_length() * RIGHT), UP)
            brace.next_to(ORIGIN, UP, buff=0.1)
            angle = line.get_angle()
            angle = (angle + PI / 2) % PI - PI / 2
            brace.rotate(angle, about_point=ORIGIN)
            brace.shift(line.get_center())
            # CHANGE: the braces were black to go over the Dropbox image (not available); on a black background they were not visible: they are drawn white
            brace.set_fill(WHITE, 1)
            line.brace = brace

        # CHANGE: placeholder instead of the image FalseEuclidProof.jpg (not available): outline of triangle ABC with the lines AF, FB, AE, EC
        self.add(Polygon(A, B, C, stroke_color=GREY_B, stroke_width=2), AF, FB, AE, EC)
        VGroup(AF, FB, AE, EC).set_stroke(GREY_B, 2)
        self.play(GrowFromCenter(AF.brace), run_time=1)
        self.play(GrowFromCenter(FB.brace), run_time=1)
        self.wait()
        self.play(
            Transform(AF.brace, AB.brace, path_arc=45 * DEGREES),
            Transform(FB.brace, AB.brace, path_arc=45 * DEGREES),
        )
        self.wait()
        self.play(GrowFromCenter(AE.brace), run_time=1)
        self.play(GrowFromCenter(EC.brace), run_time=1)
        self.wait()
        self.play(
            Transform(AE.brace, AC.brace, path_arc=45 * DEGREES),
            Transform(EC.brace, AC.brace, path_arc=45 * DEGREES),
        )
        self.wait()
        return

        # Lines for final triangles
        BP = Line(B, P)
        CP = Line(C, P)
        PF = Line(P, F)
        PE = Line(P, E)
        BF = Line(B, F)
        CE = Line(C, E)

        VGroup(BP, CP).set_stroke(BLUE_E, 5)
        VGroup(PF, PE).set_stroke(TEAL, 5)
        VGroup(BF, CE).set_stroke(RED, 5)

        self.play(*map(ShowCreation, [BP, CP]))
        self.play(*map(ShowCreation, [PF, PE]))
        self.wait()
        self.play(
            TransformFromCopy(PF, BF, path_arc=90 * DEGREES),
            TransformFromCopy(PE, CE, path_arc=-90 * DEGREES),
        )
        self.wait()

        # Compare AB to BC
        AB = Line(A, B).set_stroke(RED, 3)
        AC = Line(A, C).set_stroke(BLUE, 3)

        self.play(ShowCreation(AB))
        self.play(ShowCreation(AC))
        self.wait()
        self.add(AB.copy(), AC.copy())
        self.play(
            AB.animate.set_angle(-90 * DEGREES).next_to(A, RIGHT, aligned_edge=UP, buff=2),
            AC.animate.set_angle(-90 * DEGREES).next_to(A, RIGHT, aligned_edge=UP, buff=2.5),
        )
        self.wait()
        self.play(FadeOut(AB), FadeOut(AC))

        # Bisector labels
        perp = Text("Perpendicular\nbisector", font_size=30, color=BLACK, stroke_width=0)
        perp.next_to(F, UL, buff=0.5)
        perp.set_color(BLUE_E)
        perp_arrow = Arrow(perp, midpoint(D, P), buff=0.1, stroke_width=2)
        perp_arrow.match_color(perp)

        ang_b = Text("Angle\nbisector", font_size=30, color=BLACK, stroke_width=0)
        ang_b.next_to(F, UL, buff=0.5)
        ang_b.set_color(RED_E)
        ang_b_arrow = Arrow(ang_b, midpoint(A, P), buff=0.1, stroke_width=2)
        ang_b_arrow.match_color(ang_b)

        self.play(Write(perp), ShowCreation(perp_arrow), run_time=1)
        self.wait()
        self.play(FadeOut(perp), FadeOut(perp_arrow))
        self.wait()
        self.play(Write(ang_b), ShowCreation(ang_b_arrow), run_time=1)
        self.wait()
        self.play(FadeOut(ang_b), FadeOut(ang_b_arrow))
        self.wait()

        # Similar triangles
        for pair in [(AFP, AEP), (BPD, CPD), (BFP, CEP)]:
            self.play(DrawBorderThenFill(pair[0]))
            self.play(TransformFromCopy(pair[0], pair[1]))
            self.wait()
            self.play(LaggedStartMap(FadeOut, VGroup(*pair)))
            self.wait()
