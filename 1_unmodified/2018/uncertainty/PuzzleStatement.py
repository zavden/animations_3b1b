# ==============================================================================
# Scene:      PuzzleStatement
# Source:     videos/_2018/uncertainty.py (lines 4525-4547)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PuzzleStatement.py PuzzleStatement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class PuzzleStatement(Scene):
    def construct(self):
        aops_logo = AoPSLogo()
        url = OldTexText("AoPS.com/3b1b")
        url.next_to(aops_logo, UP)
        group = VGroup(aops_logo, url)
        group.to_edge(UP)
        self.add(group)

        words = OldTexText("""
            AoPS must choose one of 20 people to send to a 
            tug-of-war tournament.  We don't care who we send, 
            as long as we don't send our weakest person. \\\\ \\\\

            Each person has a different strength, but we don't know 
            those strengths.  We get 10 intramural 10-on-10 matches 
            to determine who we send.  Can we make sure we don't send
             the weakest person?
        """, alignment = "")
        words.set_width(FRAME_WIDTH - 2)
        words.next_to(group, DOWN, LARGE_BUFF)
        self.play(LaggedStartMap(FadeIn, words, run_time = 5, lag_ratio = 0.2))
        self.wait(2)
