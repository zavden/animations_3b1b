# ==============================================================================
# Scene:      Confessions
# Source:     videos/_2022/wordle/footnote.py (lines 57-105)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Confessions.py Confessions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Confessions(Scene):
    def construct(self):
        titles = VGroup(*(
            Text(f"Confession {n}", font_size=60)
            for n in range(1, 4)
        ))
        titles.arrange(DOWN, buff=2, aligned_edge=LEFT)
        titles.center()
        for title in titles:
            title.save_state()
            title.generate_target()

        phrases = VGroup(
            OldTexText("Bug in the code", font_size=48),
            OldTexText("About the opening scene...", font_size=48),
            OldTexText("Maybe don't use entropy?", font_size=48),
        )

        self.play(LaggedStart(*(
            FadeIn(title, RIGHT)
            for title in titles
        ), lag_ratio=0.3))
        self.wait()

        last_phrase = VMobject()
        for title, phrase in zip(titles, phrases):
            others = VGroup(*(
                t for t in titles
                if t is not title
            ))
            others_target = VGroup(*(t.target for t in others))
            for t in others_target:
                t.set_height(0.2)
                t.set_opacity(0.5)
            others_target.arrange(DOWN, buff=0.75)
            others_target.to_edge(LEFT)

            phrase.set_color(BLUE)
            phrase.to_edge(UP, buff=1.5)

            self.play(
                FadeOut(last_phrase),
                title.animate.restore().set_height(0.5).center().to_edge(UP),
                *map(MoveToTarget, others),
            )
            self.play(FadeIn(phrase))
            self.wait(2)

            last_phrase = phrase
