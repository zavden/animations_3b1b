# ==============================================================================
# Scene:      ReversePuzzleAndInsight
# Source:     videos/_2024/puzzles/supplements.py (lines 567-604)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReversePuzzleAndInsight.py ReversePuzzleAndInsight -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReversePuzzleAndInsight(InteractiveScene):
    def construct(self):
        # Add
        bulb = SVGMobject("light_bulb").set_color(YELLOW)
        puzzle = SVGMobject("puzzle_piece").set_color(BLUE_D)
        icons = VGroup(puzzle, bulb)
        icons.scale(0.75)
        titles = VGroup(Text("Puzzle"), Text("Insight"))
        titles.scale(1.25)
        objs = VGroup(VGroup(*pair) for pair in zip(titles, icons))
        for obj in objs:
            obj[1].set_height(1.5)
            obj.arrange(UP)
        objs.arrange(RIGHT, buff=3.5)
        puzzle.match_y(bulb).align_to(titles[0], LEFT)
        arrow = Arrow(puzzle, bulb, thickness=8, buff=0.3)

        self.play(LaggedStart(
            AnimationGroup(
                FadeIn(titles[0], lag_ratio=0.1),
                FadeIn(puzzle, 0.5 * UP),
            ),
            GrowArrow(arrow),
            AnimationGroup(
                FadeIn(titles[1], lag_ratio=0.1),
                FadeIn(bulb, scale=2),
            ),
            lag_ratio=0.7
        ))
        self.wait()

        # Swap
        self.play(LaggedStart(
            objs[0].animate.next_to(arrow, RIGHT, buff=0.3).shift(0.2 * DOWN).set_anim_args(path_arc=PI / 2),
            objs[1].animate.next_to(arrow, LEFT, buff=0.3).shift(0.2 * DOWN).set_anim_args(path_arc=PI / 2),
            lag_ratio=0.15
        ))
        self.wait()
