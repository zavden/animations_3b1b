# ==============================================================================
# Scene:      AskWhatsOnTest
# Source:     videos/_2019/windmill.py (lines 1035-1131)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AskWhatsOnTest.py AskWhatsOnTest -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class ShowTest(Scene):
    def construct(self):
        self.introduce_test()

    def introduce_test(self):
        test = self.get_test()
        test.generate_target()
        test.target.to_edge(UP)

        # Time label
        time_labels = VGroup(
            OldTexText("Day 1", ": 4.5 hours"),
            OldTexText("Day 2", ": 4.5 hours"),
        )
        time_labels.scale(1.5)
        day_labels = VGroup()
        hour_labels = VGroup()
        for label, page in zip(time_labels, test.target):
            label.next_to(page, DOWN)
            label[0].save_state()
            label[0].next_to(page, DOWN)
            label[1][1:].set_color(YELLOW)
            day_labels.add(label[0])
            hour_labels.add(label[1])

        # Problem descriptions
        problem_rects = self.get_problem_rects(test.target[0])
        proof_words = VGroup()
        for rect in problem_rects:
            word = OldTexText("Proof")
            word.scale(2)
            word.next_to(rect, RIGHT, buff=3)
            word.set_color(BLUE)
            proof_words.add(word)

        proof_words.space_out_submobjects(2)

        proof_arrows = VGroup()
        for rect, word in zip(problem_rects, proof_words):
            arrow = Arrow(word.get_left(), rect.get_right())
            arrow.match_color(word)
            proof_arrows.add(arrow)

        scores = VGroup()
        for word in proof_words:
            score = VGroup(Integer(0), OldTex("/"), Integer(7))
            score.arrange(RIGHT, buff=SMALL_BUFF)
            score.scale(2)
            score.move_to(word)
            score.to_edge(RIGHT)
            scores.add(score)
            score[0].add_updater(lambda m: m.set_color(
                interpolate_color(RED, GREEN, m.get_value() / 7)
            ))

        # Introduce test
        self.play(
            LaggedStart(
                FadeIn(test[0], 2 * RIGHT),
                FadeIn(test[1], 2 * LEFT),
                lag_ratio=0.3,
            )
        )
        self.wait()
        self.play(
            MoveToTarget(test, lag_ratio=0.2),
            FadeIn(day_labels, UP, lag_ratio=0.2),
        )
        self.wait()
        self.play(
            *map(Restore, day_labels),
            FadeIn(hour_labels, LEFT),
        )
        self.wait()

        # Discuss problems
        self.play(
            FadeOut(test[1]),
            FadeOut(time_labels[1]),
            LaggedStartMap(ShowCreation, problem_rects),
            run_time=1,
        )
        self.play(
            LaggedStart(*[
                FadeIn(word, LEFT)
                for word in proof_words
            ]),
            LaggedStart(*[
                GrowArrow(arrow)
                for arrow in proof_arrows
            ]),
        )
        self.wait()
        self.play(FadeIn(scores))
        self.play(
            LaggedStart(*[
                ChangeDecimalToValue(score[0], 7)
                for score in scores
            ], lag_ratio=0.2, rate_func=rush_into)
        )
        self.wait()

        self.scores = scores
        self.proof_arrows = proof_arrows
        self.proof_words = proof_words
        self.problem_rects = problem_rects
        self.test = test
        self.time_labels = time_labels

    def get_test(self):
        group = Group(
            ImageMobject("imo_2011_p1"),
            ImageMobject("imo_2011_p2"),
        )
        group.set_height(6)
        group.arrange(RIGHT, buff=LARGE_BUFF)
        for page in group:
            rect = SurroundingRectangle(page, buff=0.01)
            rect.set_stroke(WHITE, 1)
            page.add(rect)
            # page.pixel_array[:, :, :3] = 255 - page.pixel_array[:, :, :3]
        return group

    def get_problem_rects(self, page):
        pw = page.get_width()
        rects = VGroup(*[Rectangle() for x in range(3)])
        rects.set_stroke(width=2)
        rects.set_color_by_gradient([BLUE_E, BLUE_C, BLUE_D])

        rects.set_width(pw * 0.75)
        for factor, rect in zip([0.095, 0.16, 0.1], rects):
            rect.set_height(factor * pw, stretch=True)
        rects.arrange(DOWN, buff=0.08)
        rects.move_to(page)
        rects.shift(0.09 * pw * DOWN)
        return rects


class AskWhatsOnTest(ShowTest, MovingCameraScene):
    def construct(self):
        self.force_skipping()
        self.introduce_test()
        self.revert_to_original_skipping_status()

        self.ask_about_questions()

    def ask_about_questions(self):
        scores = self.scores
        arrows = self.proof_arrows
        proof_words = self.proof_words

        question = OldTexText("What kind \\\\ of problems?")
        question.scale(1.5)
        question.move_to(proof_words, LEFT)

        research = OldTexText("Research-lite")
        research.scale(1.5)
        research.move_to(question, LEFT)
        research.shift(MED_SMALL_BUFF * RIGHT)
        research.set_color(BLUE)

        arrows.generate_target()
        for arrow in arrows.target:
            end = arrow.get_end()
            start = arrow.get_start()
            arrow.put_start_and_end_on(
                interpolate(question.get_left(), start, 0.1),
                end
            )

        self.play(
            FadeOut(scores),
            FadeOut(proof_words),
            MoveToTarget(arrows),
            Write(question),
        )
        self.wait()
        self.play(
            FadeIn(research, DOWN),
            question.shift, 2 * UP,
        )
        self.wait()

        # Experience
        randy = Randolph(height=2)
        randy.move_to(research.get_corner(UL), DL)
        randy.shift(SMALL_BUFF * RIGHT)
        clock = Clock()
        clock.set_height(1)
        clock.next_to(randy, UR)

        self.play(
            FadeOut(question),
            FadeIn(randy),
            FadeInFromDown(clock),
        )
        self.play(
            randy.change, "pondering",
            ClockPassesTime(clock, run_time=5, hours_passed=5),
        )
        self.play(
            ClockPassesTime(clock, run_time=2, hours_passed=2),
            VFadeOut(clock),
            Blink(randy),
            VFadeOut(randy),
            LaggedStartMap(
                FadeOut,
                VGroup(
                    research,
                    *arrows,
                    *self.problem_rects,
                    self.time_labels[0]
                )
            ),
        )

        # Second part
        big_rect = FullScreenFadeRectangle()
        lil_rect = self.problem_rects[1].copy()
        lil_rect.reverse_points()
        big_rect.append_vectorized_mobject(lil_rect)
        frame = self.camera_frame
        frame.generate_target()
        frame.target.scale(0.35)
        frame.target.move_to(lil_rect)

        self.play(
            FadeInFromDown(self.test[1]),
        )
        self.wait()
        self.play(
            FadeIn(big_rect),
            MoveToTarget(frame, run_time=6),
        )
        self.wait()
