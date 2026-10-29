# ==============================================================================
# Scene:      FirstThoughtsOnCombination
# Source:     videos/_2022/wordle/scenes.py (lines 3349-3425)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FirstThoughtsOnCombination.py FirstThoughtsOnCombination -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FirstThoughtsOnCombination(Scene):
    def construct(self):
        morty = Mortimer(height=2)
        morty.flip()
        morty.to_corner(DL)

        example = VGroup(
            Text("dorms", font="Consolas"),
            DecimalNumber(1.08, color=TEAL),
            DecimalNumber(0.31, color=BLUE),
        )
        word, n1, n2 = example
        example.arrange(RIGHT, buff=1.5)
        example[0].shift(0.5 * RIGHT)
        example.to_corner(UR)
        example.shift(DOWN)

        example_titles = VGroup(
            OldTex("E[\\text{Info.}]", color=TEAL),
            OldTex("p(\\text{word})", color=BLUE),
        )
        for title, ex in zip(example_titles, example[1:]):
            title.next_to(ex, UP, MED_LARGE_BUFF)
            title.add(Underline(title, buff=-0.05).set_stroke(GREY, 1))

        self.add(example_titles)
        self.add(example)
        self.add(morty)

        self.play(PiCreatureBubbleIntroduction(
            morty,
            OldTexText("How should I measure\\\\guess quality?", font_size=36),
            look_at=example,
            target_mode="pondering",
            bubble_type=ThoughtBubble,
            bubble_config={"width": 4, "height": 3},
        ))
        self.play(Blink(morty))
        self.wait()

        attempt = example.copy()
        attempt.generate_target()
        arrow = OldTex("\\rightarrow")
        plus = OldTex("+")
        group = VGroup(
            attempt.target[0],
            arrow,
            attempt.target[1],
            plus,
            attempt.target[2],
        )
        group.arrange(RIGHT, buff=0.2)
        group.next_to(example, DOWN, buff=2)

        self.play(
            MoveToTarget(attempt),
            morty.change("shruggie", attempt),
            FadeIn(arrow), FadeIn(plus),
        )
        self.wait()
        self.play(Blink(morty))

        cross = Cross(group)
        cross.insert_n_curves(100)
        better_words = OldTexText("We can do\\\\better!")
        better_words.next_to(cross, DOWN)
        better_words.set_color(RED)

        self.play(ShowCreation(cross))
        self.play(
            Write(better_words, run_time=1),
            morty.change("pondering", cross),
        )
        self.play(Blink(morty))
        self.wait()

        self.embed()
