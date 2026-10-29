# ==============================================================================
# Scene:      OldBayesFactorCode
# Source:     videos/_2020/med_test.py (lines 5550-5674)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl OldBayesFactorCode.py OldBayesFactorCode -w -m --fps 15
#
# Why it does not render:
#   Fragment of Grant's code without definitions: it uses `post_group`, `boxes` and other objects that are created in another scene (med_test.py:2728) and not in OldBayesFactorCode. It is old material discarded from the video; it cannot be reconstructed without inventing the previous scene.
# ==============================================================================

from manim_imports_ext import *

class OldBayesFactorCode(Scene):
    def construct(self):
        # Show test statistics
        def get_prob_bars(p_positive):
            rects = VGroup(Square(), Square())
            rects.set_width(0.2, stretch=True)
            rects.set_stroke(WHITE, 2)
            rects[0].stretch(p_positive, 1, about_edge=UP)
            rects[1].stretch(1 - p_positive, 1, about_edge=DOWN)
            rects[0].set_fill(GREEN, 1)
            rects[1].set_fill(RED_E, 1)

            braces = VGroup(*[
                Brace(rect, LEFT, buff=SMALL_BUFF)
                for rect in rects
            ])
            positive_percent = int(p_positive * 100)
            percentages = VGroup(
                OldTexText(f"{positive_percent}\\% +", color=GREEN),
                OldTexText(f"{100 - positive_percent}\\% $-$", color=RED),
            )
            percentages.scale(0.7)
            for percentage, brace in zip(percentages, braces):
                percentage.next_to(brace, LEFT, SMALL_BUFF)

            result = VGroup(
                rects,
                braces,
                percentages,
            )

            return result

        boxes = VGroup(
            Square(color=YELLOW),
            Square(color=GREY_B)
        )
        boxes.set_height(3)
        labels = VGroup(
            OldTexText("With cancer"),
            OldTexText("Without cancer"),
        )
        for box, label in zip(boxes, labels):
            label.next_to(box, UP)
            label.match_color(box)
            box.push_self_into_submobjects()
            box.add(label)

        boxes.arrange(DOWN, buff=0.5)
        boxes.to_edge(RIGHT)

        sens_bars = get_prob_bars(0.9)
        spec_bars = get_prob_bars(0.09)
        bar_groups = VGroup(sens_bars, spec_bars)
        for bars, box in zip(bar_groups, boxes):
            bars.shift(box[0].get_right() - bars[0].get_center())
            bars.shift(0.75 * LEFT)
            box.add(bars)

        self.play(
            FadeIn(boxes[0], lag_ratio=0.1),
            post_group.scale, 0.1, {"about_point": FRAME_HEIGHT * DOWN / 2}
        )
        self.wait()
        self.play(
            FadeIn(boxes[1], lag_ratio=0.1)
        )
        self.wait()

        # Pull out Bayes factor
        ratio = VGroup(
            sens_bars[2][0].copy(),
            OldTex("\\phantom{90\\%+} \\over \\phantom{9\\%+}"),
            spec_bars[2][0].copy(),
            *Tex("=", "10"),
        )
        ratio.generate_target()
        ratio.target[:3].arrange(DOWN, buff=0.2)
        ratio.target[3:].arrange(RIGHT, buff=0.2)
        ratio.target[3:].next_to(ratio.target[:3], RIGHT, buff=0.2)
        ratio.target.center()

        ratio[1].scale(0)
        ratio[3:].scale(0)

        new_boxes = VGroup(boxes[0][0], boxes[1][0]).copy()
        new_boxes.generate_target()
        for box, part in zip(new_boxes.target, ratio.target[::2]):
            box.replace(part, stretch=True)
            box.scale(1.2)
            box.set_stroke(width=2)

        self.play(
            MoveToTarget(ratio),
            MoveToTarget(new_boxes),
        )
        self.wait()

        for part, box in zip(ratio[0:3:2], new_boxes):
            part.add(box)

        self.remove(new_boxes)
        self.add(ratio)

        bayes_factor_label = OldTexText("``Bayes factor''")
        bayes_factor_label.next_to(ratio, UP, LARGE_BUFF)
        self.play(Write(bayes_factor_label))
        self.wait()

        # Show updated result
        bayes_factor_label.generate_target()
        bayes_factor_label.target.scale(0.8)
        bayes_factor_label.target.next_to(
            post_group.saved_state[0], DOWN,
            buff=LARGE_BUFF,
        )

        self.play(
            MoveToTarget(bayes_factor_label),
            ratio.scale, 0.8,
            ratio.next_to, bayes_factor_label.target, DOWN,
            Restore(post_group),
            FadeOut(boxes, shift=2 * RIGHT),
        )
        self.wait()
