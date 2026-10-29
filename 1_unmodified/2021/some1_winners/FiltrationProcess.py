# ==============================================================================
# Scene:      FiltrationProcess
# Source:     videos/_2021/some1_winners.py (lines 365-425)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FiltrationProcess.py FiltrationProcess -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FiltrationProcess(Scene):
    def construct(self):
        total = OldTexText("$>1{,}200(!)$ submissions")

        hundred = OldTexText("$\\sim 100$")
        hundred.next_to(total, RIGHT, buff=4)
        arrow = Arrow(total, hundred, stroke_width=5)
        VGroup(total, arrow, hundred).center().to_edge(UP)

        peer_words = Text("Peer review process", font_size=36)
        peer_words.set_color(BLUE)
        peer_words.next_to(arrow, DOWN, buff=SMALL_BUFF)
        peer_subwords = OldTexText(
            "(actually quite interesting\\\\see the blog post)",
            font_size=24,
            fill_color=GREY_B,
        )
        peer_subwords.next_to(peer_words, DOWN, MED_SMALL_BUFF)

        self.play(FadeIn(total, lag_ratio=0.1))
        self.wait()
        self.play(
            ShowCreation(arrow),
            FadeIn(peer_words, lag_ratio=0.1)
        )
        self.play(
            FadeIn(hundred),
            FadeIn(peer_subwords, 0.25 * DOWN)
        )
        self.wait()

        # Guest judges
        guest_words = Text("Guest judges:")
        guest_words.next_to(peer_subwords, DOWN, buff=LARGE_BUFF)
        guest_words.add(Underline(guest_words))
        guest_words.to_edge(RIGHT, buff=1.5)

        guests = VGroup(
            Text("Alex Kontorovich"),
            Text("Henry Reich"),
            Text("Nicky Case"),
            Text("Tai-Danae Bradley"),
            Text("Bukard Polster"),
            Text("Mithuna Yoganathan"),
            Text("Steven Strogatz"),
        )
        guests.scale(0.75)
        guests.set_color(GREY_B)
        guests.arrange(DOWN, aligned_edge=LEFT)
        guests.next_to(guest_words, DOWN, aligned_edge=LEFT)

        self.play(
            FadeIn(guest_words),
            LaggedStartMap(
                FadeIn, guests,
                shift=0.25 * DOWN,
                lag_ratio=0.5,
                run_time=4,
            )
        )
        self.wait()
