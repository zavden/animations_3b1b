# ==============================================================================
# Scene:      CleverProofExample
# Source:     videos/_2021/shadows.py (lines 6074-6230)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CleverProofExample.py CleverProofExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CleverProofExample(Scene):
    def construct(self):
        initial_sum = OldTex("1^2 + 2^2 + 3^2 + \\cdots + n^2")
        tripple_tris, final_tri = self.get_triangle_sums()

        initial_sum.set_width(10)
        self.play(FadeIn(initial_sum, lag_ratio=0.1))
        self.wait()

        tripple_tris.set_width(10)
        tripple_tris.to_edge(DOWN, buff=2)
        tris = tripple_tris[0]
        tri = tris[0]
        tri.save_state()
        tri.set_height(4)
        tri.center().to_edge(DOWN, buff=1)
        self.play(
            initial_sum.animate.set_width(8).to_edge(UP),
            FadeIn(tri, lag_ratio=0.1)
        )
        self.wait()
        self.play(
            Restore(tri),
            FadeIn(tripple_tris[1:])
        )
        for i in (0, 1):
            bt1 = tris[i].copy()
            bt1.generate_target()
            bt1.target.rotate(120 * DEGREES)
            bt1.target.replace(tris[i + 1])
            bt1.target.set_opacity(0)
            tris[i + 1].save_state()
            tris[i + 1].rotate(-120 * DEGREES)
            tris[i + 1].replace(tris[i])
            tris[i + 1].set_opacity(0)
            self.play(
                MoveToTarget(bt1, remover=True),
                Restore(tris[i + 1])
            )
        self.wait()

        final_tri.set_height(3)
        final_tri.move_to(tripple_tris, UP)
        initial_sum.generate_target()
        eq = OldTex("=").scale(2)
        tripple_tris.generate_target()
        top_row = VGroup(initial_sum.target, eq, tripple_tris.target)
        top_row.arrange(RIGHT, buff=0.5)
        top_row.set_width(FRAME_WIDTH - 1)
        top_row.center().to_edge(UP)

        self.play(
            MoveToTarget(initial_sum),
            FadeIn(eq),
            MoveToTarget(tripple_tris),
            FadeTransform(tripple_tris.copy(), final_tri)
        )
        self.wait()

        final1 = OldTex("= \\frac{2n + 1}{3} (1 + 2 + 3 + \\cdots + n)")
        final2 = OldTex("= \\frac{2n + 1}{3} \\frac{(n + 1)n}{2}")
        final3 = OldTex("= \\frac{(2n + 1)(n + 1)(n)}{6}")
        final_tri.generate_target()
        final_tri.target.set_height(2).to_edge(LEFT)
        for final in (final1, final2, final3):
            final.next_to(final_tri.target, RIGHT)

        self.play(
            MoveToTarget(final_tri),
            Write(final1),
        )
        self.wait()
        self.play(
            FadeOut(final1, UP),
            FadeIn(final2, UP),
        )
        self.wait()
        self.play(
            FadeOut(final2, UP),
            FadeIn(final3, UP),
        )
        self.play(VGroup(final_tri, final3).animate.set_x(0))
        self.wait()

        # Embed
        self.embed()

    def get_triangle_sums(self):
        dl_dots = OldTex("\\vdots").rotate(-30 * DEGREES)
        dr_dots = OldTex("\\vdots").rotate(30 * DEGREES)
        blank = Integer(0).set_opacity(0)
        n = OldTex("n")
        np1 = OldTex("(2n + 1)")
        dots = OldTex("\\dots")
        tri1 = VGroup(
            Integer(1).replicate(1),
            Integer(2).replicate(2),
            Integer(3).replicate(3),
            VGroup(dl_dots, blank.copy(), blank.copy(), dr_dots),
            VGroup(n.copy(), n.copy(), dots, n.copy(), n.copy()),
        )
        tri2 = VGroup(
            n.replicate(1),
            VGroup(dl_dots, n).copy(),
            VGroup(Integer(3), blank, dr_dots).copy(),
            VGroup(Integer(2), Integer(3), dots, n).copy(),
            VGroup(Integer(1), Integer(2), Integer(3), dots, n).copy(),
        )
        tri3 = VGroup(
            n.replicate(1),
            VGroup(n, dr_dots).copy(),
            VGroup(dl_dots, blank, Integer(3)).copy(),
            VGroup(n, dots, Integer(3), Integer(2)).copy(),
            VGroup(n, dots, Integer(3), Integer(2), Integer(1)).copy(),
        )

        sum_tri = VGroup(
            np1.replicate(1),
            np1.replicate(2),
            np1.replicate(3),
            VGroup(dl_dots, *blank.replicate(6), dr_dots).copy(),
            VGroup(np1.copy(), np1.copy(), dots.copy(), np1.copy(), np1.copy()),
        )

        tris = VGroup(tri1, tri2, tri3)
        for tri in (*tris, sum_tri):
            for row in tri:
                row.arrange(RIGHT, buff=0.5)
            tri.arrange(DOWN, buff=0.5)
        tris.arrange(RIGHT, buff=2.0)
        tris.set_width(6)
        plusses = VGroup(
            OldTex("+").move_to(tris[:2]),
            OldTex("+").move_to(tris[1:]),
        )
        parens = OldTex("()")[0]
        parens.stretch(2, 1)
        parens.match_height(tris)
        parens[0].next_to(tris, LEFT)
        parens[1].next_to(tris, RIGHT)

        frac = OldTex("\\frac{1}{3}")
        frac.next_to(parens, LEFT)

        lhs = VGroup(tris, frac, parens, plusses)

        parens_copy = parens.copy()
        sum_tri.match_height(lhs)
        sum_tri.move_to(tris, LEFT)
        parens_copy[1].next_to(sum_tri, RIGHT)

        rhs = VGroup(frac.copy(), sum_tri, parens_copy)
        rhs.next_to(lhs, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        # eq = OldTex("=")
        # eq.next_to(rhs, LEFT)

        return VGroup(lhs, rhs)
