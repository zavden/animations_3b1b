# ==============================================================================
# Scene:      AskAboutSome
# Source:     videos/_2023/moser_reboot/main.py (lines 1314-1365)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutSome.py AskAboutSome -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutSome(InteractiveScene):
    def construct(self):
        randy = Randolph()
        morty = Mortimer()
        randy.next_to(ORIGIN, LEFT, LARGE_BUFF).to_edge(DOWN)
        morty.next_to(ORIGIN, RIGHT, LARGE_BUFF).to_edge(DOWN)

        morty.to_corner(DR)
        randy.next_to(morty, LEFT, LARGE_BUFF)
        self.add(morty)

        # SoME
        words = Text("The 3rd Summer of\nMath Exposition", font_size=72)
        words.next_to(randy, UP)
        words.to_edge(RIGHT)

        small_words = Text("SoME3", font_size=72)
        small_words.move_to(words, UP)
        small_words_copy = small_words.copy()
        small_words_copy.next_to(morty.get_corner(UL), UP)
        three_some = Text("3SoME", font_size=72)
        three_some.next_to(randy.get_corner(UR), UP)

        self.play(
            morty.change("raise_left_hand", words),
            FadeIn(words, 0.25 * UP, lag_ratio=0.01)
        )
        self.play(Blink(morty))
        self.wait(3)

        self.play(
            TransformMatchingStrings(words, small_words, path_arc=45 * DEGREES),
            morty.change("raise_right_hand")
        )
        self.play(Blink(morty))
        self.wait(2)
        self.play(
            VFadeIn(randy),
            randy.change("shruggie", three_some),
            morty.change("sassy", randy.eyes),
            TransformMatchingStrings(small_words, three_some, path_arc=45 * DEGREES)
        )
        self.play(morty.change("angry", randy.eyes))
        self.play(Blink(morty))
        self.play(
            TransformMatchingStrings(three_some, small_words_copy, run_time=1),
            morty.change("raise_right_hand"),
            randy.change("sassy")
        )
        self.play(Blink(morty))
        self.play(Blink(randy))
        self.wait(2)
