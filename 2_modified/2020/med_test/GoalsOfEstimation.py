# ==============================================================================
# Scene:      GoalsOfEstimation
# Source:     videos/_2020/med_test.py (lines 1966-2114)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GoalsOfEstimation.py GoalsOfEstimation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ShowCreationThenFadeAround no longer accepts surrounding_rectangle_config; stroke_color is used
# ==============================================================================

from manim_imports_ext import *

class GoalsOfEstimation(TeacherStudentsScene):
    def construct(self):
        # Goal
        goal = OldTexText("Goal: Quick estimations")
        goal.to_edge(UP)
        goal_line = Underline(goal)

        self.look_at(goal, added_anims=[FadeIn(goal, shift=0.5 * UP)])
        self.play(
            ShowCreation(goal_line),
            self.change_students(
                *3 * ["pondering"],
                look_at=goal_line,
            )
        )
        self.wait()

        # Generators
        def generate_stats(prev, sens, spec, bottom=self.hold_up_spot):
            stats = VGroup(
                OldTexText("Prevalence: ", f"{prev}\\%"),
                OldTexText("Sensitivity: ", f"{sens}\\%"),
                OldTexText("Specificity: ", f"{spec}\\%"),
            )
            stats.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            for stat, color in zip(stats, [YELLOW, GREEN_B, GREY_B]):
                stat[0].set_color(color)
                stat[1].align_to(stats[0][1], LEFT)

            rect = SurroundingRectangle(stats, buff=0.2)
            rect.set_fill(BLACK, 1)
            rect.set_stroke(GREY_B, 2)
            stats.add_to_back(rect)
            stats.move_to(bottom, DOWN)
            return stats

        def generate_answer(ans_tex):
            return OldTex(
                "P(\\text{Cancer} \\,|\\, {+})", ans_tex,
                tex_to_color_map={
                    "\\text{Cancer}": YELLOW,
                    "{+}": GREEN,
                }
            )

        stats = [
            generate_stats(1, 90, 91),
            generate_stats(10, 90, 91),
            generate_stats(0.1, 90, 91),
            generate_stats(1, 90, 99),
        ]

        # Question and answer
        self.teacher_holds_up(stats[0])
        self.wait()
        self.student_says(
            generate_answer("\\approx \\frac{1}{11}"),
            target_mode="hooray",
            index=0,
            run_time=1,
        )
        self.wait(3)

        stats[1].to_edge(RIGHT)
        self.play(
            FadeOut(stats[0]),
            self.teacher.change, "raise_left_hand", stats[1],
            FadeIn(stats[1], shift=0.5 * UP),
            RemovePiCreatureBubble(self.students[0]),
        )
        self.play(ShowCreationThenFadeAround(stats[1][1][1]))
        self.play_student_changes(
            "pondering", "thinking", "confused",
            look_at=stats[1]
        )
        self.wait()

        self.student_says(
            generate_answer("\\text{ is} \\\\ \\text{a little over } 50\\%"),
            bubble_config={"width": 4, "height": 3},
            index=1,
            target_mode="speaking",
            run_time=1,
            added_anims=[
                self.students[2].change, "erm", goal,
                self.teacher.change, "happy", self.students[1].eyes,
            ]
        )
        self.wait(2)

        self.play(
            FadeOut(stats[1], 0.5 * UP),
            FadeIn(stats[2], 0.5 * UP),
            RemovePiCreatureBubble(self.students[1]),
            self.teacher.change, "raise_right_hand", stats[2],
            self.change_students(*3 * ["pondering"], look_at=stats[2])
        )
        self.play(ShowCreationThenFadeAround(stats[2][1][1]))
        self.wait(2)

        self.student_says(
            generate_answer("\\approx \\frac{1}{100}"),
            bubble_config={"width": 4, "height": 3},
            index=0,
            target_mode="tease",
            run_time=1,
        )
        self.look_at(self.students[0].bubble.content)
        self.wait(2)

        stats[3].to_edge(RIGHT)
        self.play(
            FadeOut(stats[2], 0.5 * UP),
            FadeIn(stats[3], 0.5 * UP),
            self.teacher.change, "raise_left_hand",
            RemovePiCreatureBubble(self.students[0]),
            *(ApplyMethod(pi.look_at, stats[3]) for pi in self.pi_creatures)
        )
        self.play(ShowCreationThenFadeAround(stats[3][1][1]))
        self.play(
            ShowCreationThenFadeAround(
                stats[3][3][1],
                # CHANGE: ShowCreationThenFadeAround no longer accepts surrounding_rectangle_config; stroke_color is used
                stroke_color=TEAL,
            ),
            self.teacher.change, "tease", stats[3]
        )
        self.play_student_changes(
            "pondering", "thinking", "confused",
            look_at=self.teacher.get_bottom(),
        )
        self.wait(2)
        self.student_says(
            generate_answer("\\text{ is} \\\\ \\text{a little below } 50\\%"),
            bubble_config={"width": 4, "height": 3},
            index=1,
            target_mode="speaking",
            run_time=1,
            added_anims=[
                self.students[0].change, "erm", goal,
                self.students[2].change, "confused", goal,
                self.teacher.change, "happy", self.students[1].eyes,
            ]
        )
        self.wait(2)
        self.play_student_changes(
            "thinking", "hooray", "thinking",
            look_at=self.students[1].bubble.content,
        )
        self.wait(3)
