# ==============================================================================
# Scene:      MentionPart2
# Source:     videos/_2020/med_test.py (lines 5511-5541)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionPart2.py MentionPart2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MentionPart2(Scene):
    def construct(self):
        self.add(FullScreenFadeRectangle(fill_color=GREY_E, fill_opacity=1))

        tweet = ImageMobject("twitter_covid_test_poll")
        tweet.set_height(5)
        tweet.to_edge(LEFT)

        words = OldTexText(
            "Possible follow-up\\\\breaking this down",
            alignment="",
            font_size=60
        )
        words.to_edge(RIGHT)
        words.align_to(tweet, UP)
        arrow = Arrow(words.get_bottom() + SMALL_BUFF * DOWN, tweet.get_right(), path_arc=-45 * DEGREES)

        low_words = OldTexText("How would you answer?")
        low_words.match_x(words)
        low_words.align_to(tweet, DOWN)
        low_words.set_color(BLUE)

        self.add(words)

        self.play(
            FadeIn(tweet, shift=LEFT, scale=1.2),
            DrawBorderThenFill(arrow),
        )
        self.wait()
        self.play(Write(low_words, run_time=1))
        self.wait()
