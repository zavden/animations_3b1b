# ==============================================================================
# Scene:      HighlightReviewParts
# Source:     videos/_2020/beta/beta1.py (lines 145-240)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HighlightReviewParts.py HighlightReviewParts -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - append_points requires an even length; add_subpath starts the cutout subpath correctly
# ==============================================================================

from manim_imports_ext import *

class HighlightReviewParts(Scene):
    CONFIG = {
        "reverse_order": False,
    }

    def construct(self):
        # Setup up rectangles
        rects = VGroup(*[Rectangle() for x in range(3)])
        rects.set_stroke(width=0)
        rects.set_fill(GREY, 0.5)

        rects.set_height(1.35, stretch=True)
        rects.set_width(9.75, stretch=True)

        rects[0].move_to([-0.2, 0.5, 0])
        rects[1].next_to(rects[0], DOWN, buff=0)
        rects[2].next_to(rects[1], DOWN, buff=0)

        rects[2].set_height(1, stretch=True, about_edge=UP)

        inv_rects = VGroup()
        for rect in rects:
            fsr = FullScreenFadeRectangle()
            # CHANGE: append_points requires an even length; add_subpath starts the cutout subpath correctly
            fsr.add_subpath(rect.get_points()[::-1])
            inv_rects.add(fsr)

        inv_rects.set_fill(BLACK, 0.85)

        # Set up labels
        ratings = [100, 96, 93]
        n_reviews = [10, 50, 200]
        colors = [PINK, BLUE, YELLOW]

        review_labels = VGroup()
        for rect, rating, nr, color in zip(rects, ratings, n_reviews, colors):
            label = OldTex(
                f"{nr}", "\\text{ reviews }",
                f"{rating}", "\\%",
            )
            label[2:].set_color(color)
            label.set_height(1)
            label.next_to(rect, UP, aligned_edge=RIGHT)
            label.set_stroke(BLACK, 4, background=True)
            fix_percent(label[3][0])
            review_labels.add(label)

        # Animations
        curr_fsr = inv_rects[0]
        curr_label = None

        tuples = list(zip(inv_rects, review_labels))
        if self.reverse_order:
            tuples = reversed(tuples)
            curr_fsr = inv_rects[-1]

        for fsr, label in tuples:
            if curr_fsr is fsr:
                self.play(VFadeIn(fsr))
            else:
                self.play(
                    Transform(curr_fsr, fsr),
                    MoveToTarget(curr_label),
                )

            first, second = label[2:], label[:2]
            if self.reverse_order:
                first, second = second, first

            self.add(first)
            self.wait(2)
            self.add(second)
            self.wait(2)

            label.generate_target()
            label.target.scale(0.3)
            if curr_label is None:
                label.target.to_corner(UR)
                label.target.shift(MED_LARGE_BUFF * LEFT)
            else:
                label.target.next_to(curr_label, DOWN)

            curr_label = label
        self.play(MoveToTarget(curr_label))
        self.wait()

        br = BackgroundRectangle(review_labels, buff=0.25)
        br.set_fill(BLACK, 0.85)
        br.set_width(FRAME_WIDTH)
        br.set_height(FRAME_HEIGHT, stretch=True)
        br.center()
        self.add(br, review_labels)
        self.play(
            FadeOut(curr_fsr),
            FadeIn(br),
        )
        self.wait()
