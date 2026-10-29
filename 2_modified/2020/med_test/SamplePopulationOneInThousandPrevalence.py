# ==============================================================================
# Scene:      SamplePopulationOneInThousandPrevalence
# Source:     videos/_2020/med_test.py (lines 2442-2601)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SamplePopulationOneInThousandPrevalence.py SamplePopulationOneInThousandPrevalence -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - manimgl bug: with draw_together the render fails with "min_storage_buffer_offset_alignment" (member offsets of a run not aligned to 32); each mobject is drawn separately
# ==============================================================================

from manim_imports_ext import *

# CHANGE: manimgl bug: with draw_together the render fails with "min_storage_buffer_offset_alignment" (member offsets of a run not aligned to 32); each mobject is drawn separately
class SamplePopulationOneInThousandPrevalence(Scene):
    default_camera_config = {"draw_together": False}

    def construct(self):
        # Add prevalence title
        titles = VGroup(*(
            OldTexText(
                f"What if prevalence is {n} in {k}?",
                tex_to_color_map={
                    n: YELLOW,
                    k: GREY_B,
                }
            )
            for n, k in [("{1}", "{1,000}"), ("{10}", "{10,000}")]
        ))
        titles.to_edge(UP)

        self.add(titles[0])

        # Show population
        dots1k, dots10k = [
            VGroup(*(Dot() for x in range(n))).set_fill(GREY_D)
            for n in [1000, 10000]
        ]
        dots1k[:1].set_fill(YELLOW)
        dots10k[:10].set_fill(YELLOW)

        for dots, n, m in [(dots1k, 20, 50), (dots10k, 100, 100)]:
            sorter = VGroup(*dots)
            sorter.shuffle()
            sorter.arrange_in_grid(n, m, buff=SMALL_BUFF)
            sorter.set_width(FRAME_WIDTH - 1)
            if sorter.get_height() > 6:
                sorter.set_height(6)
            sorter.to_edge(DOWN)

        self.play(FadeIn(dots1k, lag_ratio=0.05, run_time=2))
        self.wait()
        self.play(
            Transform(dots1k, dots10k[0::10]),
        )
        self.play(
            FadeIn(dots10k),
            ReplacementTransform(titles[0][0::2], titles[1][0::2]),
            FadeOut(titles[0][1::2], 0.5 * UP),
            FadeIn(titles[1][1::2], 0.5 * UP),
        )
        self.remove(dots1k)

        # Split the group
        cancer_cases = dots10k[:10]
        cancer_cases.generate_target()
        cancer_cases.target.arrange_in_grid(
            buff=cancer_cases[0].get_width() / 2,
        )
        cancer_cases.target.set_height(2)
        cancer_cases.target.set_y(0)
        cancer_cases.target.to_edge(LEFT, buff=LARGE_BUFF)

        non_cancer_cases = dots10k[10:]
        non_cancer_cases.generate_target()
        non_cancer_cases.target.to_edge(RIGHT)

        c_count = titles[1][1].copy()
        c_count.generate_target()
        c_count.target.next_to(cancer_cases.target, UP, MED_LARGE_BUFF)
        nc_count = Integer(9990)
        nc_count.set_color(GREY_B)
        nc_count.set_opacity(0)
        nc_count.move_to(titles[1][3])

        self.play(
            MoveToTarget(cancer_cases),
            MoveToTarget(non_cancer_cases),
            MoveToTarget(c_count),
            nc_count.set_opacity, 1,
            nc_count.next_to, non_cancer_cases.target, UP,
            FadeOut(titles[1]),
        )
        self.wait()

        # Show test results
        tp_cases = cancer_cases[:9]
        fp_cases = VGroup(*random.sample(list(non_cancer_cases), 900))
        for case in it.chain(tp_cases, fp_cases):
            box = SurroundingRectangle(
                case, buff=0.1 * case.get_width()
            )
            box.set_stroke(GREEN, 3)
            case.box = box

        tn_cases = VGroup(*(
            case for case in non_cancer_cases if case not in fp_cases
        ))

        tp_label = OldTexText("$9$ True Positives")
        tp_label.set_color(GREEN)
        tp_label.move_to(c_count)
        tp_label.shift_onto_screen()

        fp_label = OldTexText("$\\sim 900$ False Positives")
        fp_label.set_color(GREEN_D)
        fp_label.move_to(nc_count)

        self.play(
            FadeOut(c_count),
            FadeIn(tp_label),
            LaggedStart(*(
                ShowCreation(case.box)
                for case in tp_cases
            )),
            cancer_cases[9].set_opacity, 0.25
        )
        self.wait()
        self.play(
            FadeOut(nc_count),
            FadeIn(fp_label),
            LaggedStart(*(
                ShowCreation(case.box)
                for case in fp_cases
            ), lag_ratio=0.001),
            tn_cases.set_opacity, 0.25,
            run_time=2,
        )
        self.wait()

        for case in it.chain(tp_cases, fp_cases):
            case.add(case.box)

        # Organize false positives
        center = fp_cases.get_center()
        fp_cases.sort(lambda p: get_norm(p - center))
        fp_cases.generate_target()
        fp_cases.target.arrange_in_grid(
            buff=fp_cases[0].get_width() / 4,
        )
        fp_cases.target.set_height(6)
        fp_cases.target.to_corner(DR)
        new_center = fp_cases.target.get_center()
        fp_cases.target.sort(lambda p: get_norm(p - new_center))

        self.play(
            MoveToTarget(fp_cases, run_time=4),
            FadeOut(tn_cases, run_time=1),
            FadeOut(cancer_cases[9]),
        )
        self.wait()

        # Final fraction
        final_frac = OldTex(
            "{{9} \\over {9} + {900}} \\approx 0.01",
            tex_to_color_map={
                "{9}": GREEN,
                "{900}": GREEN_D,
            }
        )
        final_frac.scale(1.5)
        final_frac.next_to(tp_cases, DOWN, LARGE_BUFF)
        final_frac.to_edge(LEFT, LARGE_BUFF)

        self.play(FadeIn(final_frac, lag_ratio=0.2))
        self.wait()
