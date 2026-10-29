# ==============================================================================
# Scene:      SeekIdealized
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 179-264)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeekIdealized.py SeekIdealized -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SeekIdealized(Scene):
    def construct(self):
        phrases = VGroup(*[
            OldTexText(
                "Seek", text, "problems",
                tex_to_color_map={
                    "realistic": GREEN,
                    "{idealized}": YELLOW,
                    "over-idealized": YELLOW,
                    "general": BLUE,
                }
            )
            for text in [
                "realistic",
                "{idealized}",
                "over-idealized",
                "general",
            ]
        ])
        phrases.scale(2)
        words = VGroup()
        for phrase in phrases:
            phrase.center()
            word = phrase[1]
            words.add(word)
            phrase.remove(word)
        arrow = Vector(DOWN)
        arrow.set_stroke(WHITE, 6)
        arrow.next_to(words[3], UP)
        low_arrow = arrow.copy()
        low_arrow.next_to(words[3], DOWN)

        solutions = OldTexText("solutions")
        solutions.scale(2)
        solutions.move_to(phrases[3][1], UL)
        models = OldTexText("models")
        models.scale(2)
        models.next_to(
            words[0], RIGHT, buff=0.35,
            aligned_edge=DOWN
        )

        phrases.center()
        phrase = phrases[0]

        self.add(phrase)
        self.add(words[0])
        self.wait()
        words[0].save_state()
        self.play(
            words[0].to_edge, DOWN,
            words[0].set_opacity, 0.5,
            Transform(phrase, phrases[1]),
            FadeIn(words[1], UP)
        )
        self.wait()
        # self.play(
        #     words[1].move_to, words[2], RIGHT,
        #     FadeIn(words[2]),
        #     Transform(phrase, phrases[2])
        # )
        # self.wait()
        self.play(
            words[1].next_to, arrow, UP,
            ShowCreation(arrow),
            MaintainPositionRelativeTo(
                phrase, words[1]
            ),
            FadeIn(solutions, LEFT),
            FadeIn(words[3]),
        )
        self.wait()

        words[0].generate_target()
        words[0].target.next_to(low_arrow, DOWN)
        words[0].target.set_opacity(1)
        models.shift(
            words[0].target.get_center() -
            words[0].saved_state.get_center()
        )
        self.play(
            MoveToTarget(words[0]),
            ShowCreation(low_arrow),
            FadeIn(models, LEFT)
        )
        self.wait()
