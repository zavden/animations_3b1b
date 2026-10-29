# ==============================================================================
# Scene:      BasicIdea
# Source:     videos/_2026/cross_entropy/language_tree_visualization/language_tree.py (lines 470-572)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BasicIdea.py BasicIdea -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

PURE_MAGENTA = "#FF00FF"


class BasicIdea(InteractiveScene):
    def construct(self):
        # Add two documents
        document1 = VGroup(*[
            Rectangle(
                width=5,
                height=1,
                fill_opacity=1,
                fill_color=interpolate_color(LIGHT_PINK, PURE_MAGENTA, random.random()),
                stroke_width=1,
                stroke_color=WHITE
            )
            for _ in range(8)
        ]).arrange(DOWN, buff=0)
        document1_label = TexText("Document A", font_size=80).next_to(document1, UP, buff=0.4)
        document2 = document1.copy()
        for rect in document2:
            rect.set_fill(color=interpolate_color(GREEN_B, GREEN_E, random.random()))
        document2_label = TexText("Document B", font_size=80).next_to(document2, UP, buff=0.4)
        document1_group = VGroup(document1, document1_label)
        document2_group = VGroup(document2, document2_label)
        documents = VGroup(document1_group, document2_group)
        documents.arrange(buff=2).set_height(4)
        self.play(
            AnimationGroup(*[
                FadeIn(doc, shift=UP * 0.5)
                for doc in documents
            ], lag_ratio=0.4)
        )
        self.play(documents.animate.scale(0.9).to_edge(LEFT, buff=2.3))

        # Take a small snippet of B and append it to a copy of A
        a_copy = document1.copy()
        snippet = document2[4:7].copy()
        new_doc = VGroup(a_copy, snippet).arrange(DOWN, buff=0).set_x(0.5 * (FRAME_WIDTH * 0.5 + document2.get_right()[0]))
        self.play(
            AnimationGroup(
                TransformFromCopy(document2[4:7], snippet, path_arc=PI * 0.3),
                TransformFromCopy(document1, a_copy, path_arc=-PI * 0.3), lag_ratio=0.9), run_time=4)

        # "Compress" it
        new_doc.generate_target()
        new_doc.target.set_stroke(width=0)
        new_doc.target[0].stretch(0.15, 1)
        new_doc.target[1].stretch(0.4, 1)
        new_doc.target.arrange(DOWN, buff=0).set_width(2.2).move_to(new_doc)
        gzip_ab = TexText("GZIP(AB)", font_size=35, tex_to_color_map={"A": PINK, "B": GREEN}).next_to(new_doc.target, UP)
        self.play(AnimationGroup(MoveToTarget(new_doc), Write(gzip_ab), lag_ratio=0.8))
        self.wait(1)

        # Compress A on its own
        a_copy_2 = document1.copy().match_x(new_doc).to_edge(DOWN, buff=1)
        self.play(
            VGroup(new_doc, gzip_ab).animate.to_edge(UP, buff=2),
            TransformFromCopy(document1, a_copy_2, path_arc=PI * 0.3), run_time=2)
        self.wait(0.5)
        a_copy_2.generate_target()
        a_copy_2.target.set_stroke(width=0).stretch(0.15, 1).set_width(2.2)
        gzip_a = TexText("GZIP(A)", font_size=35, tex_to_color_map={"A": PINK, "B": GREEN}).next_to(a_copy_2.target, UP)
        self.play(AnimationGroup(MoveToTarget(a_copy_2), Write(gzip_a), lag_ratio=0.8))
        self.wait(2)

        # Compare the sizes
        compressed_docs_group = VGroup(VGroup(gzip_ab, new_doc), VGroup(gzip_a, a_copy_2))
        compressed_docs_group.generate_target()
        compressed_docs_group.target.scale(1.3).arrange(buff=3)
        compressed_docs_group.target[1].align_to(compressed_docs_group.target[0], UP)
        self.play(
            FadeOut(VGroup(document1_group, document2_group), shift=LEFT * 4),
            MoveToTarget(compressed_docs_group, path_arc=PI * 0.3), run_time=1.5)
        difference_equation = VGroup(
            Line(ORIGIN, UP * 4).next_to(compressed_docs_group[0], LEFT, buff=0.35),
            Line(ORIGIN, UP * 4).next_to(compressed_docs_group[0], RIGHT, buff=0.35),
            Tex("-", font_size=90),
            Line(ORIGIN, UP * 4).next_to(compressed_docs_group[1], LEFT, buff=0.35).set_y(0),
            Line(ORIGIN, UP * 4).next_to(compressed_docs_group[1], RIGHT, buff=0.35).set_y(0)
        )
        self.play(Write(difference_equation))
        self.wait(2)

        # Highlight the snippet of B
        self.play(AnimationGroup(*[Indicate(rect, scale_factor=1.05) for rect in new_doc[1]], lag_ratio=0.1), run_time=2)
        self.wait(1)

        # Highlight the main part of A
        self.play(AnimationGroup(*[Indicate(rect, scale_factor=1.05) for rect in new_doc[0]], lag_ratio=0.1), run_time=2)
        self.wait(1)

        # Decrease the "linguistic difference"
        new_doc.generate_target()
        new_doc.target[1].stretch(0.75, 1).next_to(new_doc.target[0], DOWN, buff=0)
        for rect in new_doc.target[1]:
            rect.set_fill(color=interpolate_color(RED_A, RED_E, random.random()))
        self.play(MoveToTarget(new_doc), gzip_ab["B"].animate.set_fill(color=RED), run_time=2)
        self.wait(2)

        # Increase the "linguistic difference"
        new_doc.generate_target()
        new_doc.target[1].stretch(2.5, 1).next_to(new_doc.target[0], DOWN, buff=0)
        for rect in new_doc.target[1]:
            rect.set_fill(color=interpolate_color(PURE_GREEN, "#296633", random.random()))
        self.play(MoveToTarget(new_doc), gzip_ab["B"].animate.set_fill(color=PURE_GREEN), run_time=2)
        self.wait(2)
