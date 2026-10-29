# ==============================================================================
# Scene:      IMODetailsV2
# Source:     videos/_2026/2025_P6/p6.py (lines 3892-4036)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IMODetailsV2.py IMODetailsV2 -w -m --fps 15
#
# Notes:
#   IMO_logo: the code asks for 'IMO_logo' (case does not matter on macOS) and the actual file in the repo is imo_logo.png; _lib/manim_imports_ext.py retries the lookup ignoring case, so the real logo is used.
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

class IMODetailsV2(InteractiveScene):
    def construct(self):
        # Write "International Math Olympiad"
        imo_logo = ImageMobject("IMO_logo").set_opacity(0.9)
        imo_text = TexText("International Math Olympiad", font_size=160).set_opacity(0.9).set_stroke(width=7, color=BLACK, behind=True).next_to(imo_logo, DOWN)
        Group(imo_logo, imo_text).scale(0.3).to_edge(UP, buff=0.3)
        imo_text_shortened = TexText("2025 IMO", font_size=30).set_stroke(width=7, color=BLACK, behind=True).move_to(imo_text)
        self.play(FadeIn(imo_logo, shift=OUT * 2), Write(imo_text, stroke_color=WHITE))

        # Fade in boxes for the problems underneath
        problems = VGroup()
        for i in range(6):
            rect = Rectangle(width=6, height=1.5, fill_opacity=1, fill_color=TEAL_A, stroke_width=0).round_corners(0.2)
            label = TexText(R"\text{Problem }" + str(i + 1)).set_color(BLACK)
            label.set_z_index(1)
            problem = VGroup(rect, label)
            problems.add(problem)
        problems.arrange_in_grid(n_cols=2, h_buff=2, v_buff=0.5, fill_rows_first=False).set_width(10).to_edge(DOWN, buff=0.7)
        day1_label = TexText("Day 1").next_to(problems[:3], UP, buff=0.4)
        day2_label = TexText("Day 2").next_to(problems[3:], UP, buff=0.4)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    TransformMatchingShapes(imo_text, imo_text_shortened, run_time=1),
                    LaggedStartMap(FadeIn, problems, shift=UP * 0.2, lag_ratio=0.1)
                ),
                AnimationGroup(
                    Write(day1_label),
                    Write(day2_label)
                ), lag_ratio=0.3)
        )
        self.wait(1)

        # Highlight problem 6
        self.play(problems[-1][0].animate.set_fill(color=RED).set_stroke(width=4, color=YELLOW))
        self.wait(2)

        # Arrange the problems on the left
        imo_text_shortened.generate_target()
        imo_logo.generate_target()
        Group(imo_logo.target, imo_text_shortened.target).scale(1.5).set_y(0).to_edge(RIGHT, buff=1)
        imo_logo.set_z_index(0)
        imo_text_shortened.set_z_index(1)

        for problem in problems:
            problem.generate_target()
        VGroup(*[problem.target for problem in problems]).scale(0.9).arrange(DOWN, buff=0.2).to_edge(LEFT, buff=0.6)

        self.play(
            MoveToTarget(imo_text_shortened, run_time=2),
            MoveToTarget(imo_logo, run_time=2),
            AnimationGroup(*[
                MoveToTarget(problem, path_arc=PI * 0.3 if problem.target.get_y() > 0 else -PI * 0.3)
                for problem in problems
            ], lag_ratio=0.06, run_time=2),
            FadeOut(VGroup(day1_label, day2_label))
        )

        # Show scores
        total_participants = 630
        scores_data = [368, 253, 102, 342, 215, 6]
        score_bars = VGroup()
        master_bar_width_tracker = ValueTracker(0)
        for score, problem in zip(scores_data, problems):
            skeleton = Rectangle(
                width=4,
                height=0.5,
                fill_opacity=0.1,
                fill_color=WHITE,
                stroke_width=3,
                stroke_color=WHITE,
                stroke_opacity=1
            ).round_corners(0.08).set_z_index(1)

            def get_bar(score=score, skeleton=skeleton):
                fraction = master_bar_width_tracker.get_value() * score / total_participants
                return Rectangle(
                    fill_opacity=1,
                    fill_color=TEAL_E,
                    stroke_width=0
                ).match_height(
                    skeleton
                ).stretch_to_fit_width(
                    skeleton.get_width() * fraction
                ).move_to(
                    skeleton
                ).align_to(
                    skeleton, LEFT
                ).round_corners(min(0.08, fraction)).set_z_index(0)
            bar = always_redraw(get_bar)
            score_bars.add(VGroup(bar, skeleton).next_to(problem, RIGHT, buff=0.5))
        self.add(score_bars)

        scores = VGroup(*[
            Integer(score, font_size=30).set_color(TEAL).next_to(bar, RIGHT)
            for score, bar in zip(scores_data, score_bars)
        ])

        def update_scores(s):
            for score_value, score_display in zip(scores_data, scores):
                score_display.set_value(
                    int(score_value * master_bar_width_tracker.get_value())
                ).set_opacity(
                    master_bar_width_tracker.get_value() * 3
                )
        scores.add_updater(update_scores)
        self.add(scores)
        arrow = Arrow(ORIGIN, LEFT * 1.5).set_color(YELLOW).next_to(scores[-1], RIGHT)
        bars_label = TexText("Number of perfect scores", font_size=30).next_to(score_bars[0], UP)
        self.play(
            FadeIn(bars_label, run_time=1.4),
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(*[
                        FadeIn(skeleton)
                        for (_, skeleton) in score_bars
                    ], run_time=1),
                    master_bar_width_tracker.animate(run_time=2).set_value(1), lag_ratio=0.02), lag_ratio=0.2)
        )
        score_bars.clear_updaters()
        scores.clear_updaters()
        self.wait(1)
        self.play(GrowArrow(arrow))
        self.wait(2)

        # Add text: "The Last IMO Problem that AI could not solve"
        checkx_and_xs = VGroup(*[
            (Checkmark().set_color(PURE_GREEN) if i < 5 else Exmark().set_color(PURE_RED)).next_to(problems[i], RIGHT)
            for i in range(6)
        ])
        self.play(
            FadeOut(Group(bars_label, score_bars, scores, arrow, imo_logo, imo_text_shortened), shift=RIGHT * 2),
            AnimationGroup(*[
                FadeIn(check_or_x, shift=UP * 0.1)
                for check_or_x in checkx_and_xs
            ], lag_ratio=0.1), run_time=2)
        last_imo_problem_text = """
            The last IMO problem that
            AI could not solve
        """
        last_imo_problem = Text(last_imo_problem_text, font_size=50).set_x(0.5 * (FRAME_WIDTH * 0.5 + checkx_and_xs.get_right()[0]))
        for word in last_imo_problem_text.split():
            self.add(last_imo_problem[word])
            self.wait(0.06 * len(word))
        self.wait(2)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
