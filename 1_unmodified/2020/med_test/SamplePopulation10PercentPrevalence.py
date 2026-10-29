# ==============================================================================
# Scene:      SamplePopulation10PercentPrevalence
# Source:     videos/_2020/med_test.py (lines 2231-2423)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SamplePopulation10PercentPrevalence.py SamplePopulation10PercentPrevalence -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WomanIcon(SVGMobject):
    CONFIG = {
        "fill_color": GREY_B,
        "stroke_width": 0,
    }

    def __init__(self, **kwargs):
        super().__init__("woman_icon", **kwargs)
        self.remove(self[0])


class SamplePopulation10PercentPrevalence(Scene):
    def construct(self):
        # Setup test accuracy figures
        accuracy_figures = VGroup(
            OldTexText(
                "90\\% Sensitivity,", " 10\\% False negative rate",
                font_size=36
            ),
            OldTexText(
                "91\\% Specificity,", " 9\\% False positive rate",
                font_size=36
            ),
        )
        accuracy_figures.arrange(RIGHT, buff=LARGE_BUFF)
        accuracy_figures.to_edge(UP)

        for color, text in zip([YELLOW, GREY], accuracy_figures):
            text.add(Underline(text, color=color, stroke_width=2))

        # Show population
        population = VGroup(*[WomanIcon() for x in range(100)])
        population.arrange_in_grid(fill_rows_first=False)
        population.set_height(5)
        population.next_to(accuracy_figures, DOWN, LARGE_BUFF)
        cancer_cases = population[:10]
        healthy_cases = population[10:]
        cancer_cases.set_fill(YELLOW)
        healthy_cases.set_fill(GREY)

        population.generate_target()
        reordered_pop = VGroup(*population)
        reordered_pop.shuffle()
        for m1, m2 in zip(reordered_pop, population.target):
            m1.move_to(m2)
        population.target[:10].next_to(accuracy_figures[0], DOWN, MED_LARGE_BUFF)
        population.target[10:].next_to(accuracy_figures[1], DOWN, MED_LARGE_BUFF)

        pop_words = OldTexText("100", " patients")
        wc_words = OldTexText("10", " with cancer")
        wo_words = OldTexText("90", " without cancer")

        pop_words.next_to(population, DOWN)
        wc_words.next_to(population.target[:10], DOWN)
        wo_words.next_to(population.target[10:], DOWN)
        for words in wc_words, wo_words:
            words.save_state()
            words[0].replace(pop_words[0], stretch=True)
            words[1].replace(pop_words[1], stretch=True)
            words.set_opacity(0)

        title = OldTexText("Picture a concrete population", font_size=72)
        title.to_edge(UP)
        self.add(title)

        self.play(
            FadeIn(population, lag_ratio=0.05, run_time=3),
            FadeIn(pop_words),
        )
        self.wait()
        self.play(
            MoveToTarget(population, run_time=2),
            Restore(wc_words),
            Restore(wo_words),
            FadeOut(pop_words),
            title.shift, 0.25 * UP,
        )
        self.wait()

        # Show test stats
        self.play(
            FadeOut(title, shift=UP),
            FadeIn(accuracy_figures[0], 0.5 * UP)
        )

        # Show test results
        c_boxes = VGroup(*(
            SurroundingRectangle(icon, buff=0)
            for icon in cancer_cases
        ))
        h_boxes = VGroup(*(
            SurroundingRectangle(icon, buff=0)
            for icon in healthy_cases
        ))
        all_boxes = VGroup(c_boxes, h_boxes)
        all_boxes.set_stroke(width=3)

        c_boxes[:9].set_stroke(GREEN)
        c_boxes[9:].set_stroke(RED)
        h_boxes.set_stroke(RED)

        false_positives = healthy_cases[0:80:10]
        false_positive_boxes = h_boxes[0:80:10]
        false_positive_boxes.set_stroke(GREEN)

        for n, box in enumerate(c_boxes):
            tex = "+" if n < 9 else "-"
            sign = OldTex(tex, font_size=36)
            sign.next_to(box, RIGHT, SMALL_BUFF)
            sign.match_color(box)
            box.add(sign)

        for box in false_positive_boxes:
            sign = OldTex("+", font_size=36)
            sign.next_to(box, UP, SMALL_BUFF)
            sign.match_color(box)
            box.add(sign)

        for i, boxes in (0, c_boxes), (1, h_boxes):
            if i == 1:
                self.play(FadeIn(accuracy_figures[1]))
            self.play(ShowCreationThenFadeOut(SurroundingRectangle(
                accuracy_figures[i][i],
                buff=SMALL_BUFF,
                stroke_color=GREEN,
            )))
            self.wait()
            self.play(ShowIncreasingSubsets(boxes))
            self.wait()

        for icon, box in zip(cancer_cases, c_boxes):
            icon.add(box)
        for icon, box in zip(healthy_cases, h_boxes):
            icon.add(box)

        self.remove(all_boxes)
        self.add(population)

        # Filter down to positive cases
        new_wc_words = OldTexText("9 ", "with cancer")
        new_wo_words = OldTexText("8 ", "without cancer")
        for nw, w in (new_wc_words, wc_words), (new_wo_words, wo_words):
            nw[0].set_color(GREEN)
            nw.move_to(w)

        self.play(
            cancer_cases[:9].move_to, cancer_cases,
            FadeOut(cancer_cases[9:]),
            ReplacementTransform(wc_words, new_wc_words),
        )
        self.wait()
        self.play(
            false_positives.move_to, healthy_cases,
            FadeOut(VGroup(*(
                case for case in healthy_cases
                if case not in false_positives
            ))),
            ReplacementTransform(wo_words, new_wo_words),
        )
        self.wait()

        # Rearrange true positives
        false_positives.generate_target()
        false_positives.target.shift(DOWN)
        true_positives = cancer_cases[:9]
        true_positives.generate_target()
        for case in true_positives.target:
            box = case[-1]
            sign = box[-1]
            sign.next_to(case[:-1], UP, SMALL_BUFF)
        true_positives.target.arrange(
            RIGHT,
            buff=get_norm(false_positives[0].get_right() - false_positives[1].get_left()),
        )
        true_positives.target.match_y(false_positives.target)
        true_positives.target.match_x(new_wc_words)

        self.play(
            MoveToTarget(true_positives),
            MoveToTarget(false_positives),
            new_wc_words.next_to, true_positives.target, DOWN,
            new_wo_words.next_to, false_positives.target, DOWN,
        )
        self.wait()

        # Show final fraction
        answer = OldTex(
            "{9 \\over 9 + 8} \\approx 0.53",
            font_size=72,
        )[0]
        answer.next_to(accuracy_figures, DOWN, LARGE_BUFF)
        nine1 = new_wc_words[0].copy()
        nine2 = new_wc_words[0].copy()
        eight = new_wo_words[0].copy()

        self.play(
            nine1.replace, answer[0],
            nine2.replace, answer[2],
            eight.replace, answer[4],
            Write(answer[1:5:2]),
        )
        self.wait()
        self.play(Write(answer[5:]))
        self.wait()
