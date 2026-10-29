# ==============================================================================
# Scene:      IMODetails
# Source:     videos/_2026/2025_P6/p6.py (lines 3730-3889)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IMODetails.py IMODetails -w -m --fps 15
#
# Notes:
#   IMO_logo: the code asks for 'IMO_logo' (case does not matter on macOS) and the actual file in the repo is imo_logo.png; _lib/manim_imports_ext.py retries the lookup ignoring case, so the real logo is used.
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

class IMODetails(InteractiveScene):
    def construct(self):
        # Write "International Math Olympiad"
        imo_text = TexText("International Math Olympiad", font_size=70).set_opacity(0.9).set_stroke(width=7, color=BLACK, behind=True)
        imo_logo = ImageMobject("IMO_logo").set_opacity(0.9)
        self.play(FadeIn(imo_logo, shift=OUT * 2), Write(imo_text, stroke_color=WHITE))
        self.wait(2)
        imo_text_shortened = TexText("IMO", font_size=100).set_stroke(width=7, color=BLACK, behind=True)
        self.play(TransformMatchingShapes(imo_text, imo_text_shortened), run_time=1.5)
        self.wait(2)

        # Shift it up to the top
        self.play(Group(imo_logo, imo_text_shortened).animate.scale(0.3).to_edge(UP, buff=0.4))
        self.wait(1)

        # Fade in boxes for the problems underneath
        problems = VGroup()
        for i in range(6):
            rect = Rectangle(width=6, height=1.5, fill_opacity=1, fill_color=TEAL_A, stroke_width=0).round_corners(0.2)
            label = TexText(R"\text{Problem }" + str(i + 1)).set_color(BLACK)
            label.set_z_index(1)
            problem = VGroup(rect, label)
            problems.add(problem)
        problems.arrange_in_grid(n_cols=2, h_buff=2, v_buff=0.5, fill_rows_first=False).set_width(10).to_edge(DOWN, buff=1)
        self.play(LaggedStartMap(FadeIn, problems, shift=UP * 0.2, lag_ratio=0.1))

        # Write labels for days underneath
        day1_label = TexText("Day 1").next_to(problems[:3], UP, buff=0.4)
        day2_label = TexText("Day 2").next_to(problems[3:], UP, buff=0.4)
        self.play(Write(day1_label), Write(day2_label))
        self.wait(2)

        # Pi Creatures react to each one's difficulty
        creatures = VGroup(*[
            PiCreature("pondering").match_height(problem).next_to(problem, LEFT).look_at(problem)
            for problem in problems
        ])
        self.play(LaggedStartMap(FadeIn, creatures, shift=RIGHT * 0.2, lag_ratio=0.1))
        self.wait(2)

        expressions = ["pondering", "confused", "horrified"]
        colors = [RED_B, interpolate_color(RED_B, RED_E, 0.5), RED_E]
        hard = TexText("Hard").set_color(colors[0]).match_y(problems[0])
        brutal = TexText("Brutal").set_color(colors[2]).match_y(problems[2])
        arrow = Arrow(ORIGIN, DOWN * 2.2, thickness=3).move_to(VGroup(hard, brutal))
        VGroup(hard, arrow, brutal).next_to(problems, RIGHT)
        self.play(
            AnimationGroup(*[
                creature.change(expressions[i % 3]).look_at(problem)
                for i, (creature, problem) in enumerate(zip(creatures, problems))
            ]),
            AnimationGroup(
                Write(hard),
                GrowArrow(arrow),
                Write(brutal), lag_ratio=0.4),
            AnimationGroup(*[
                problem[0].animate.set_color(colors[i % 3])
                for i, problem in enumerate(problems)
            ], run_time=2)
        )
        self.wait(2)

        # Change the label to "2025 IMO" and arrange the problems on the left
        year_label = TexText(
            "2025"
        ).match_height(
            imo_text_shortened
        ).set_stroke(
            width=7, color=BLACK, behind=True
        ).set_opacity(
            0
        ).next_to(
            imo_text_shortened, LEFT, buff=0.1
        )
        year_label.generate_target()
        year_label.target.set_opacity(1)
        imo_text_shortened.generate_target()
        imo_logo.generate_target()
        VGroup(year_label.target, imo_text_shortened.target).arrange(buff=0.1).move_to(imo_logo.target)
        Group(imo_logo.target, year_label.target, imo_text_shortened.target).scale(1.5).set_y(0).to_edge(RIGHT, buff=1)
        imo_logo.set_z_index(0)
        imo_text_shortened.set_z_index(1)
        year_label.set_z_index(1)

        for problem in problems:
            problem.generate_target()
        VGroup(*[problem.target for problem in problems]).scale(0.9).arrange(DOWN, buff=0.2).to_edge(LEFT, buff=0.6)
        problems[-1].target[0].set_fill(color=PURE_RED).set_stroke(width=4, color=YELLOW)

        self.play(
            MoveToTarget(imo_text_shortened, run_time=2),
            MoveToTarget(imo_logo, run_time=2),
            MoveToTarget(year_label, run_time=2),
            AnimationGroup(*[
                MoveToTarget(problem, path_arc=PI * 0.3 if problem.target.get_y() > 0 else -PI * 0.3)
                for problem in problems
            ], lag_ratio=0.06, run_time=2),
            FadeOut(creatures, shift=LEFT, run_time=1),
            FadeOut(day1_label),
            FadeOut(day2_label),
            FadeOut(VGroup(hard, arrow, brutal), shift=RIGHT)
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
        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(*[
                        FadeIn(skeleton)
                        for (_, skeleton) in score_bars
                    ], run_time=1),
                    master_bar_width_tracker.animate(run_time=2).set_value(1), lag_ratio=0.02),
                AnimationGroup(*[
                    FadeIn(score)
                    for score in scores
                ], lag_ratio=0.1, run_time=2), lag_ratio=0.2)
        )
        score_bars.clear_updaters()

        # Draw attention to the last bar
        arrow = Arrow(ORIGIN, LEFT * 1.5).set_color(YELLOW).next_to(scores[-1], RIGHT)
        self.play(GrowArrow(arrow))


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
