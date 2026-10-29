# ==============================================================================
# Scene:      TryAssigningProbabilitiesToSpecificValues
# Source:     videos/_2020/beta/beta2.py (lines 454-595)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryAssigningProbabilitiesToSpecificValues.py TryAssigningProbabilitiesToSpecificValues -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryAssigningProbabilitiesToSpecificValues(Scene):
    def construct(self):
        # To get "P(s = .7000001) = ???" type labels
        def get_p_label(value):
            result = OldTex(
                # "P(", "{s}", "=", value, "\\%", ")",
                "P(", "{h}", "=", value, ")",
            )
            # fix_percent(result.get_part_by_tex("\\%")[0])
            result.set_color_by_tex("{h}", YELLOW)
            return result

        labels = VGroup(
            get_p_label("0.70000000"),
            get_p_label("0.70000001"),
            get_p_label("0.70314159"),
            get_p_label("0.70271828"),
            get_p_label("0.70466920"),
            get_p_label("0.70161803"),
        )
        labels.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        labels.set_height(4.5)
        labels.to_edge(DOWN, buff=LARGE_BUFF)

        q_marks = VGroup()
        gt_zero = VGroup()
        eq_zero = VGroup()
        for label in labels:
            qm = OldTex("=", "\\,???")
            qm.next_to(label, RIGHT)
            qm[1].set_color(TEAL)
            q_marks.add(qm)

            gt = OldTex("> 0")
            gt.next_to(label, RIGHT)
            gt_zero.add(gt)

            eqz = OldTex("= 0")
            eqz.next_to(label, RIGHT)
            eq_zero.add(eqz)

        v_dots = OldTex("\\vdots")
        v_dots.next_to(q_marks[-1][0], DOWN, MED_LARGE_BUFF)

        # Animations
        self.play(FadeInFromDown(labels[0]))
        self.play(FadeIn(q_marks[0], LEFT))
        self.wait()
        self.play(*[
            TransformFromCopy(m1, m2)
            for m1, m2 in [
                (q_marks[0], q_marks[1]),
                (labels[0][:3], labels[1][:3]),
                (labels[0][-1], labels[1][-1]),
            ]
        ])
        self.play(ShowIncreasingSubsets(
            labels[1][3],
            run_time=3,
            int_func=np.ceil,
            rate_func=linear,
        ))
        self.add(labels[1])
        self.wait()
        self.play(
            LaggedStartMap(
                FadeInFrom, labels[2:],
                lambda m: (m, UP),
            ),
            LaggedStartMap(
                FadeInFrom, q_marks[2:],
                lambda m: (m, UP),
            ),
            Write(v_dots, rate_func=squish_rate_func(smooth, 0.5, 1))
        )
        self.add(labels, q_marks)
        self.wait()

        self.play(
            ReplacementTransform(q_marks, gt_zero, lag_ratio=0.05),
            run_time=2,
        )
        self.wait()

        # Show sum
        group = VGroup(labels, gt_zero, v_dots)
        sum_label = OldTex(
            "\\sum_{0 \\le {h} \\le 1}", "P(", "{h}", ")", "=",
            tex_to_color_map={"{h}": YELLOW},
        )
        # sum_label.set_color_by_tex("{s}", YELLOW)
        sum_label[0].set_color(WHITE)
        sum_label.scale(1.75)
        sum_label.next_to(ORIGIN, RIGHT, buff=1)
        sum_label.shift(LEFT)

        morty = Mortimer()
        morty.set_height(2)
        morty.to_corner(DR)

        self.play(group.to_corner, DL)
        self.play(
            Write(sum_label),
            VFadeIn(morty),
            morty.change, "confused", sum_label,
        )

        infty = OldTex("\\infty")
        zero = OldTex("0")
        for mob in [infty, zero]:
            mob.scale(2)
            mob.next_to(sum_label[-1], RIGHT)
        zero.set_color(RED)
        zero.shift(SMALL_BUFF * RIGHT)

        self.play(
            Write(infty),
            morty.change, "horrified", infty,
        )
        self.play(Blink(morty))
        self.wait()

        # If equal to zero
        eq_zero.move_to(gt_zero)
        eq_zero.set_color(RED)
        self.play(
            ReplacementTransform(
                gt_zero, eq_zero,
                lag_ratio=0.05,
                run_time=2,
                path_arc=30 * DEGREES,
            ),
            morty.change, "pondering", eq_zero,
        )
        self.wait()
        self.play(
            FadeIn(zero, DOWN),
            FadeOut(infty, UP),
            morty.change, "sad", zero
        )
        self.play(Blink(morty))
        self.wait()
