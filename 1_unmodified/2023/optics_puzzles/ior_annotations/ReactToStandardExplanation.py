# ==============================================================================
# Scene:      ReactToStandardExplanation
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 269-372)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactToStandardExplanation.py ReactToStandardExplanation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReactToStandardExplanation(InteractiveScene):
    samples = 4

    def construct(self):
        # Phrases
        phrases = VGroup(
            Text("Light slows down in glass\ndifferent amounts for different colors", alignment="LEFT"),
            TexText(R"Slowing down $\Rightarrow$ bending"),
            TexText(R"Therefore colors refract at different angles"),
        )
        phrases.set_fill(border_width=0)

        for phrase, y in zip(phrases, [1, 0, -1]):
            phrase.set_y(y * FRAME_HEIGHT / 3)
            phrase.set_x(-2.0, LEFT)

        self.add(phrases)
        self.wait()

        # Ask question
        p1 = phrases[0]["Light slows down in glass"]
        p2 = phrases[0]["different amounts for different colors"]
        slows_down = phrases[0]["slows down"]

        rect = SurroundingRectangle(p1, buff=0.05)
        rect.set_stroke(YELLOW, 2)

        why = Text("Why?!")
        why.set_color(YELLOW)
        why.next_to(rect, RIGHT)
        how = Text("How?")
        how.match_style(why)
        how.next_to(slows_down, UP)
        discovered = Text("This should feel discovered")
        discovered.match_style(why)
        discovered.next_to(phrases[0], DOWN, buff=0.5)

        morty = Mortimer(height=2)
        morty.to_edge(RIGHT)

        self.play(
            ShowCreation(rect),
            Write(why),
            p2.animate.set_opacity(0.25),
            phrases[1:].animate.set_opacity(0.25),
            VFadeIn(morty),
            morty.change("maybe", rect),
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            FadeTransform(why, how),
            rect.animate.surround(slows_down),
            morty.change("angry", rect),
        )
        self.play(Blink(morty))
        self.wait()
        why.next_to(p2, DOWN)
        self.play(
            rect.animate.surround(p2),
            p2.animate.set_opacity(1),
            p1.animate.set_opacity(0.25),
            FadeTransform(how, why),
            morty.change("confused", rect),
        )
        self.play(Blink(morty))
        self.wait()

        self.remove(why)
        self.play(
            rect.animate.surround(phrases[0], buff=0.25),
            phrases[0].animate.set_opacity(1),
            FadeTransformPieces(why.copy(), discovered, remover=True),
            morty.change("tease", rect),
        )
        self.add(discovered)
        self.play(Blink(morty))
        self.wait()

        # Ask for better explanation of bending
        new_why = Text("Better explanation?")
        new_why.match_style(why)
        new_why.next_to(phrases[1], UP)
        self.play(
            phrases[0].animate.set_opacity(0.25),
            phrases[1].animate.set_opacity(1),
            rect.animate.surround(phrases[1]),
            FadeTransform(discovered, new_why),
            morty.change("pondering", phrases[1]),
        )
        self.play(Blink(morty))
        self.wait()

        # Back to central question
        why.next_to(p1, UP)
        self.play(
            rect.animate.surround(p1),
            p1.animate.set_opacity(1),
            phrases[1].animate.set_opacity(0.25),
            FadeTransform(new_why, why),
            morty.change("raise_right_hand")
        )
        self.play(Blink(morty))
        self.wait()
