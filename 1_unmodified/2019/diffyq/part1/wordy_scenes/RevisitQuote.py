# ==============================================================================
# Scene:      RevisitQuote
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 684-724)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RevisitQuote.py RevisitQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StrogatzQuote(Scene):
    def construct(self):
        quote = self.get_quote()
        movers = VGroup(*quote[:-1].family_members_with_points())
        for mover in movers:
            mover.save_state()
            disc = Circle(radius=0.05)
            disc.set_stroke(width=0)
            disc.set_fill(BLACK, 0)
            disc.move_to(mover)
            mover.become(disc)
        self.play(
            FadeIn(quote.author_part, LEFT),
            LaggedStartMap(
                # FadeInFromLarge,
                # quote[:-1].family_members_with_points(),
                Restore, movers,
                lag_ratio=0.005,
                run_time=2,
            )
            # FadeInFromDown(quote[:-1]),
            # lag_ratio=0.01,
        )
        self.wait()
        self.play(
            Write(quote.law_part.copy().set_color(YELLOW)),
            run_time=1,
        )
        self.wait()
        self.play(
            Write(quote.language_part.copy().set_color(BLUE)),
            run_time=1.5,
        )
        self.wait(2)

    def get_quote(self):
        law_words = "laws of physics"
        language_words = "language of differential equations"
        author = "-Steven Strogatz"
        quote = OldTexText(
            """
            \\Large
            ``Since Newton, mankind has come to realize
            that the laws of physics are always expressed
            in the language of differential equations.''\\\\
            """ + author,
            alignment="",
            arg_separator=" ",
            isolate=[law_words, language_words, author]
        )
        quote.law_part = quote.get_part_by_tex(law_words)
        quote.language_part = quote.get_part_by_tex(language_words)
        quote.author_part = quote.get_part_by_tex(author)
        quote.set_width(12)
        quote.to_edge(UP)
        quote[-2].shift(SMALL_BUFF * LEFT)
        quote.author_part.shift(RIGHT + 0.5 * DOWN)
        quote.author_part.scale(1.2, about_edge=UL)

        return quote


class RevisitQuote(StrogatzQuote, PiCreatureScene):
    def construct(self):
        quote = self.get_quote()
        quote.law_part.set_color(YELLOW)
        quote.language_part.set_color(BLUE)
        quote.set_stroke(BLACK, 6, background=True)
        quote.scale(0.8, about_edge=UL)

        new_langauge_part = OldTexText(
            "\\Large Language of differential equations"
        )
        new_langauge_part.to_edge(UP)
        new_langauge_part.match_style(quote.language_part)

        randy = self.pi_creature

        self.play(
            FadeIn(quote[:-1], DOWN),
            FadeIn(quote[-1:], LEFT),
            randy.change, "raise_right_hand",
        )
        self.play(Blink(randy))
        self.play(randy.change, "angry")
        self.play(
            Blink(randy),
            VFadeOut(randy, run_time=3)
        )
        mover = VGroup(quote.language_part)
        self.add(quote, mover)
        self.play(
            ReplacementTransform(
                mover, new_langauge_part,
            ),
            *[
                FadeOut(part)
                for part in quote
                if part is not quote.language_part
            ],
            run_time=2,
        )
        self.wait()
