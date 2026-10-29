# ==============================================================================
# Scene:      CompressionIsIntellgenceWords
# Source:     videos/_2026/cross_entropy/supplements.py (lines 322-412)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompressionIsIntellgenceWords.py CompressionIsIntellgenceWords -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CompressionIsIntellgenceWords(InteractiveScene):
    def construct(self):
        # Intro
        words = ["Compression", "is", "Intelligence"]
        colors = ["#0BFCB7", WHITE, YELLOW]
        phrase_mob = Text(" ".join(words), font_size=90)
        compression, is_, intelligence = mobs = VGroup(
            phrase_mob[word][0]
            for word in words
        )
        for mob, color in zip(mobs, colors):
            mob.set_color(color)

        compression.shift(0.5 * LEFT)
        intelligence.shift(0.5 * RIGHT)
        phrase_mob.to_edge(UP)

        self.play(ShowIncreasingSubsets(mobs, run_time=3))
        self.wait()

        # Conservative phrasing
        phrase_mob.save_state()
        theory_of = Text("The mathematical theory of")
        theory_of.set_color(TEAL_D)
        theory_of.match_width(compression)
        compression.refresh_bounding_box()
        theory_of.move_to(compression, UP)

        compression.target = compression.generate_target()
        compression.target.next_to(theory_of, DOWN, SMALL_BUFF)

        rightarrow = Tex(R"\longrightarrow", font_size=60)
        rightarrow.match_x(is_)
        rightarrow.match_y(VGroup(compression.target, theory_of))
        rightarrow.scale(1.5, about_edge=LEFT)
        useful = Text("is useful for")
        useful.match_width(rightarrow)
        useful.next_to(rightarrow, UP, buff=SMALL_BUFF)

        ai = Text("Artificial\nIntelligence", font_size=72)
        ai.set_color(YELLOW_D)
        ai.match_x(intelligence).match_y(rightarrow)

        self.play(LaggedStart(
            AnimationGroup(
                FadeTransformPieces(compression.copy(), theory_of),
                MoveToTarget(compression),
            ),
            Transform(is_, rightarrow),
            AnimationGroup(
                Transform(intelligence, ai["Intelligence"][0]),
                FadeIn(ai["Artificial"][0], lag_ratio=0.2, shift=0.1 * UP),
            ),
            lag_ratio=0.7
        ))
        self.wait()
        self.play(
            Restore(phrase_mob),
            FadeOut(theory_of, 0.5 * UP),
            FadeOut(ai["Artificial"][0], 0.5 * UP),
        )
        self.wait()

        # Trio of videos
        background = FullScreenFadeRectangle()
        background.set_fill(GREY_E, 0.5)
        videos = ScreenRectangle().replicate(3)
        videos.arrange(RIGHT, buff=LARGE_BUFF)
        videos.set_width(FRAME_WIDTH - 1)
        videos.set_fill(BLACK, 1)
        videos.set_stroke(WHITE, 2)
        brace = Brace(videos, UP, SMALL_BUFF)

        clean_phrase = Text("Compression is Intelligence")
        clean_phrase.next_to(brace, UP)

        phrase_mob.set_z_index(1)
        self.play(LaggedStart(
            FadeIn(background),
            Transform(phrase_mob, clean_phrase),
            GrowFromCenter(brace),
            LaggedStartMap(FadeIn, videos),
            lag_ratio=0.25
        ))
        self.wait()
        self.play(
            FadeOut(phrase_mob, 0.5 * RIGHT, lag_ratio=0.1),
            FadeOut(brace, scale=0.5, shift=0.25 * brace.get_width() * RIGHT),
            FadeOut(videos),
        )
        self.wait()
