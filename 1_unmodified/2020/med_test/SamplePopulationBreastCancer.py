# ==============================================================================
# Scene:      SamplePopulationBreastCancer
# Source:     videos/_2020/med_test.py (lines 816-1275)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SamplePopulationBreastCancer.py SamplePopulationBreastCancer -w -m --fps 15
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


class SamplePopulationBreastCancer(Scene):
    def construct(self):
        # Introduce population
        title = OldTexText(
            "Sample of ", "$1{,}000$", " women",
            font_size=72,
        )
        title.add(Underline(title, color=GREY_B))
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        self.add(title)

        woman = WomanIcon()
        globals()['woman'] = woman
        population = VGroup(*[woman.copy() for x in range(1000)])
        population.arrange_in_grid(
            25, 40,
            buff=LARGE_BUFF,
            fill_rows_first=False,
        )
        population.set_height(6)
        population.next_to(title, DOWN)

        counter = Integer(1000, edge_to_fix=UL)
        counter.replace(title[1])
        counter.set_value(0)

        title[1].set_opacity(0)
        self.play(
            ShowIncreasingSubsets(population),
            ChangeDecimalToValue(counter, 1000),
            run_time=5
        )
        self.remove(counter)
        title[1].set_opacity(1)
        self.wait()

        # Show true positives
        rects = VGroup(Rectangle(), Rectangle())
        rects.set_height(6)
        rects[0].set_width(4, stretch=True)
        rects[1].set_width(8, stretch=True)
        rects[0].set_stroke(YELLOW, 3)
        rects[1].set_stroke(GREY, 3)
        rects.arrange(RIGHT)
        rects.center().to_edge(DOWN, buff=MED_SMALL_BUFF)

        positive_cases = population[:10]
        negative_cases = population[10:]

        positive_cases.generate_target()
        positive_cases.target.move_to(rects[0])
        positive_cases.target.set_color(YELLOW)

        negative_cases.generate_target()
        negative_cases.target.set_height(rects[1].get_height() * 0.8)
        negative_cases.target.move_to(rects[1])

        positive_words = OldTexText(r"1\% ", "Have breast cancer", font_size=36)
        positive_words.set_color(YELLOW)
        positive_words.next_to(rects[0], UP, SMALL_BUFF)

        negative_words = OldTexText(r"99\% ", "Do not have cancer", font_size=36)
        negative_words.set_color(GREY_B)
        negative_words.next_to(rects[1], UP, SMALL_BUFF)

        self.play(
            MoveToTarget(positive_cases),
            MoveToTarget(negative_cases),
            Write(positive_words, run_time=1),
            Write(negative_words, run_time=1),
            FadeIn(rects),
        )
        self.wait()

        # Show screening
        scan_lines = VGroup(*(
            Line(
                # FRAME_WIDTH * LEFT / 2,
                FRAME_HEIGHT * DOWN / 2,
                icon.get_center(),
                stroke_width=1,
                stroke_color=interpolate_color(BLUE, GREEN, random.random())
            )
            for icon in population
        ))
        self.play(
            LaggedStartMap(
                ShowCreationThenFadeOut, scan_lines,
                lag_ratio=1 / len(scan_lines),
                run_time=3,
            )
        )
        self.wait()

        # Test results on cancer population
        tpr_words = OldTexText("9 True positives", font_size=36)
        fnr_words = OldTexText("1 False negative", font_size=36)
        tnr_words = OldTexText("901 True negatives", font_size=36)
        fpr_words = OldTexText("89 False positives", font_size=36)

        tpr_words.set_color(GREEN_B)
        fnr_words.set_color(RED_D)
        tnr_words.set_color(RED_B)
        fpr_words.set_color(GREEN_D)

        tp_cases = positive_cases[:9]
        fn_cases = positive_cases[9:]

        tpr_words.next_to(tp_cases, UP)
        fnr_words.next_to(fn_cases, DOWN)

        signs = VGroup()
        for woman in tp_cases:
            sign = OldTex("+")
            sign.set_color(GREEN_B)
            sign.match_height(woman)
            sign.next_to(woman, RIGHT, SMALL_BUFF)
            woman.sign = sign
            signs.add(sign)
        for woman in fn_cases:
            sign = OldTex("-")
            sign.set_color(RED)
            sign.match_width(signs[0])
            sign.next_to(woman, RIGHT, SMALL_BUFF)
            woman.sign = sign
            signs.add(sign)

        boxes = VGroup()
        for n, woman in enumerate(positive_cases):
            box = SurroundingRectangle(woman, buff=0)
            box.set_stroke(width=2)
            if woman in tp_cases:
                box.set_color(GREEN)
            else:
                box.set_color(RED)
            woman.box = box
            boxes.add(box)

        self.play(
            FadeIn(tpr_words, shift=0.2 * UP),
            ShowIncreasingSubsets(signs[:9]),
            ShowIncreasingSubsets(boxes[:9]),
        )
        self.wait()
        self.play(
            FadeIn(fnr_words, shift=0.2 * DOWN),
            Write(signs[9:]),
            ShowCreation(boxes[9:]),
        )
        self.wait()

        # Test results on cancer-free population
        negative_cases.sort(lambda p: -p[1])

        num_fp = int(len(negative_cases) * 0.09)
        fp_cases = negative_cases[:num_fp]
        tn_cases = negative_cases[num_fp:]

        new_boxes = VGroup()
        for n, woman in enumerate(negative_cases):
            box = SurroundingRectangle(woman, buff=0)
            box.set_stroke(width=2)
            if woman in fp_cases:
                box.set_color(GREEN)
            else:
                box.set_color(RED)
            woman.box = box
            new_boxes.add(box)

        fpr_words.next_to(fp_cases, UP, buff=SMALL_BUFF)
        tnr_words.next_to(tn_cases, DOWN, buff=0.2)

        self.play(
            FadeIn(fpr_words, shift=0.2 * UP),
            ShowIncreasingSubsets(new_boxes[:num_fp])
        )
        self.wait()
        self.play(
            FadeIn(tnr_words, shift=0.2 * DOWN),
            ShowIncreasingSubsets(new_boxes[num_fp:])
        )
        self.wait()

        # Consolidate boxes
        self.remove(boxes, new_boxes, population)
        for woman in population:
            woman.add(woman.box)
        self.add(population)

        # Limit view to positive cases
        for cases, nr, rect in zip([tp_cases, fp_cases], [3, 7], rects):
            cases.save_state()
            cases.generate_target()
            for case in cases.target:
                case[-1].set_stroke(width=3)
                case[-1].scale(1.1)
            cases.target.arrange_in_grid(
                n_rows=nr,
                buff=0.5 * cases[0].get_width()
            )
            cases.target.scale(0.5 / cases.target[0].get_height())
            cases.target.move_to(rect)

        fp_cases.target.shift(0.4 * DOWN)
        positive_words.save_state()
        negative_words.save_state()
        tpr_words.save_state()
        fpr_words.save_state()

        self.play(
            MoveToTarget(tp_cases),
            MoveToTarget(fp_cases),
            tpr_words.next_to, tp_cases.target, UP,
            fpr_words.next_to, fp_cases.target, UP,
            FadeOut(signs),
            positive_words[0].set_opacity, 0,
            negative_words[0].set_opacity, 0,
            positive_words[1].match_x, rects[0],
            negative_words[1].match_x, rects[1],
            LaggedStart(
                FadeOut(fn_cases, shift=DOWN),
                FadeOut(fnr_words, shift=DOWN),
                FadeOut(tn_cases, shift=DOWN),
                FadeOut(tnr_words, shift=DOWN),
            ),
        )
        self.wait()

        # Emphasize groups counts
        self.play(
            ShowCreationThenFadeOut(SurroundingRectangle(
                tpr_words[0][:1],
                stroke_width=2,
                stroke_color=WHITE,
                buff=0.05,
            )),
            LaggedStartMap(Indicate, tp_cases, color=YELLOW, lag_ratio=0.3, run_time=1),
        )
        self.wait()
        self.play(
            ShowCreationThenFadeOut(SurroundingRectangle(
                fpr_words[0][:2],
                stroke_width=2,
                stroke_color=WHITE,
                buff=0.05,
            )),
            LaggedStartMap(
                Indicate, fp_cases,
                color=GREEN_A,
                lag_ratio=0.05,
                run_time=3
            )
        )
        self.wait()

        # Final equation
        equation = OldTex(
            "P(",
            "\\text{Have cancer }",
            "|",
            "\\text{ positive test})",
            "\\approx",
            "\\frac{9}{9 + 89}",
            "\\approx \\frac{1}{11}"
        )
        equation.set_color_by_tex("cancer", YELLOW)
        equation.set_color_by_tex("positive", GREEN)
        equation.to_edge(UP, buff=SMALL_BUFF)

        self.play(
            FadeIn(equation[:-1], shift=UP),
            FadeOut(title, shift=UP),
        )
        self.wait()
        self.play(Write(equation[-1]))
        self.wait()

        # Label PPV
        frame = self.camera.frame
        frame.save_state()

        ppv_words = OldTexText(
            "Positive\\\\",
            "Predictive\\\\",
            "Value\\\\",
            alignment="",
        )
        ppv_words.next_to(equation, RIGHT, LARGE_BUFF, DOWN)
        for word in ppv_words:
            word[0].set_color(BLUE)

        ppv_rhs = OldTex(
            "={\\text{TP} \\over \\text{TP} + \\text{FP}}",
            tex_to_color_map={
                "\\text{TP}": GREEN_B,
                "\\text{FP}": GREEN_C,
            }
        )
        ppv_rhs.next_to(ppv_words, RIGHT)
        ppv_rhs.shift(1.5 * LEFT)

        self.play(frame.scale, 1.1, {"about_edge": DL})
        self.play(ShowIncreasingSubsets(ppv_words))
        self.wait()

        self.play(
            equation.shift, 1.5 * LEFT + 0.5 * UP,
            ppv_words.shift, 1.5 * LEFT,
            FadeIn(ppv_rhs, lag_ratio=0.1),
            frame.scale, 1.1, {"about_edge": DL},
        )
        self.wait()

        # Go back to earlier state
        self.play(
            frame.restore,
            frame.shift, 0.5 * DOWN,
            LaggedStartMap(FadeOut, VGroup(equation, ppv_words, ppv_rhs)),
            LaggedStartMap(Restore, VGroup(
                tpr_words, tp_cases,
                fpr_words, fp_cases,
            )),
            run_time=3,
        )
        self.play(
            LaggedStartMap(FadeIn, VGroup(
                fnr_words, fn_cases,
                tnr_words, tn_cases,
            )),
        )
        self.wait()

        # Fade rects
        fade_rects = VGroup(*(
            BackgroundRectangle(
                VGroup(rect, words),
                fill_opacity=0.9,
                fill_color=BLACK,
                buff=SMALL_BUFF,
            )
            for rect, words in zip(rects, [positive_words, negative_words])
        ))

        # Sensitivity
        sens_eq = OldTex(
            "\\text{Sensitivity}",
            "= {9 \\over 10}",
            "= 90\\%"
        )
        sens_eq.next_to(rects[0], LEFT, MED_LARGE_BUFF, aligned_edge=UP)
        sens_eq.shift(DOWN)

        fnr_eq = OldTex(
            "\\text{False Negative Rate}", "= 10\\%"
        )
        fnr_eq.set_color(RED)
        fnr_eq.scale(0.9)
        equiv = OldTex("\\Leftrightarrow")
        equiv.scale(1.5)
        equiv.rotate(90 * DEGREES)
        equiv.next_to(sens_eq, DOWN, MED_LARGE_BUFF)
        fnr_eq.next_to(equiv, DOWN, MED_LARGE_BUFF)

        self.play(
            frame.shift, 5 * LEFT,
            FadeIn(fade_rects[1]),
            Write(sens_eq[0]),
        )
        self.wait()
        self.play(
            TransformFromCopy(tpr_words[0][0], sens_eq[1][1]),
            Write(sens_eq[1][0]),
            Write(sens_eq[1][2:]),
        )
        self.play(Write(sens_eq[2]))
        self.wait()

        self.play(
            FadeIn(equiv, shift=0.5 * DOWN),
            FadeIn(fnr_eq, shift=1.0 * DOWN),
        )
        self.wait()

        # Transition to right side
        fade_rects[0].stretch(5, 0, about_edge=RIGHT)
        self.play(
            ApplyMethod(frame.shift, 10 * RIGHT, run_time=4),
            FadeIn(fade_rects[0], run_time=2),
            FadeOut(fade_rects[1], run_time=2),
        )

        # Specificity
        spec_eq = OldTex(
            "\\text{Specificity}",
            "= {901 \\over 990}",
            "\\approx 91\\%"
        )
        spec_eq.next_to(rects[1], RIGHT, MED_LARGE_BUFF, aligned_edge=DOWN)
        spec_eq.shift(UP)

        fpr_eq = OldTex(
            "\\text{False Positive Rate}", "= 9\\%"
        )
        fpr_eq.set_color(GREEN)
        fpr_eq.scale(0.9)
        equiv2 = OldTex("\\Leftrightarrow")
        equiv2.scale(1.5)
        equiv2.rotate(90 * DEGREES)
        equiv2.next_to(spec_eq, UP, MED_LARGE_BUFF)
        fpr_eq.next_to(equiv2, UP, MED_LARGE_BUFF)

        self.play(Write(spec_eq[0]))
        self.wait()
        self.play(
            Write(spec_eq[1][0]),
            TransformFromCopy(
                tnr_words[0][:3],
                spec_eq[1][1:4],
                run_time=2,
                path_arc=30 * DEGREES,
            ),
            Write(spec_eq[1][4:]),
        )
        self.wait()
        self.play(Write(spec_eq[2]))
        self.wait()

        self.play(
            FadeIn(equiv2, shift=0.5 * UP),
            FadeIn(fpr_eq, shift=1.0 * UP),
        )
        self.wait()

        # Reset to show both kinds of accuracy
        eqs = [sens_eq, spec_eq]
        for eq, word in zip(eqs, [positive_words, negative_words]):
            eq.generate_target()
            eq.target[1].set_opacity(0)
            eq.target[2].move_to(eq.target[1], LEFT),
            eq.target.next_to(word, UP, buff=0.3)

        self.play(
            FadeOut(fade_rects[0]),
            frame.shift, 5 * LEFT,
            frame.scale, 1.1, {"about_edge": DOWN},
            MoveToTarget(sens_eq),
            MoveToTarget(spec_eq),
            *map(FadeOut, (fnr_eq, fpr_eq, equiv, equiv2)),
            run_time=2,
        )
        self.wait()

        self.play(
            VGroup(
                fn_cases, fnr_words,
                fp_cases, fpr_words,
            ).set_opacity, 0.2,
            rate_func=there_and_back_with_pause,
            run_time=3
        )
