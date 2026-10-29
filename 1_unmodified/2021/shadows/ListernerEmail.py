# ==============================================================================
# Scene:      ListernerEmail
# Source:     videos/_2021/shadows.py (lines 6240-6318)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ListernerEmail.py ListernerEmail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ListernerEmail(Scene):
    def construct(self):
        # Letter
        rect = Rectangle(4, 7)
        rect.set_stroke(WHITE, 2)
        rect.set_fill("#060606", 1)
        lines = Line(LEFT, RIGHT).get_grid(15, 1)
        lines.set_width(0.8 * rect.get_width())
        lines.arrange(DOWN)
        lines.set_height(0.7 * rect.get_height(), stretch=True)
        for n in [3, 8, -1]:
            lines[n].stretch(0.5, 0, about_edge=LEFT)
            if n > 0:
                lines[n + 1].set_opacity(0)
        lines.move_to(rect)

        salutation = Text("Hi Prof. Kontorovich,", font_size=30)
        salutation.next_to(lines, UP, aligned_edge=LEFT)
        lines.shift(0.2 * DOWN)

        letter = VGroup(rect, lines, salutation)

        self.add(rect)
        self.play(
            Write(salutation, run_time=1),
            ShowCreation(lines, rate_func=linear, run_time=3, lag_ratio=0.5),
        )
        self.add(letter)
        self.wait()
        self.play(letter.animate.to_edge(LEFT))

        # Phrases
        phrases = VGroup(
            Text("I’m a PhD student..."),
            Text(
                "...I had noticed my mathematical capabilities\n"
                "starting to fade (to which I attributed getting\n"
                "older and not being as sharp)..."
            ),
            Text(
                "...I realized that the entire problem, for me at least,\n"
                "was entirely about my lack of problems and drills."
            ),
        )

        phrases.arrange(DOWN, buff=2.0, aligned_edge=LEFT)
        phrases.set_width(8)
        phrases.next_to(letter, RIGHT, LARGE_BUFF)

        highlights = VGroup()
        for i, w in [(0, 1), (5, 3), (11, 2.5)]:
            hrect = Rectangle(w, 0.1)
            hrect.set_stroke(width=0)
            hrect.set_fill(YELLOW, 0.5)
            hrect.move_to(lines[i], LEFT)
            highlights.add(hrect)

        highlights[0].shift(1.5 * RIGHT)
        highlights[2].align_to(lines, RIGHT)

        hlines = VGroup()

        for highlight, phrase in zip(highlights, phrases):
            hlines.add(VGroup(
                DashedLine(highlight.get_corner(UR), phrase.get_corner(UL), buff=0.1),
                DashedLine(highlight.get_corner(DR), phrase.get_corner(DL), buff=0.1),
            ))
        hlines.set_stroke(YELLOW, 1)

        for i in range(3):
            self.play(
                FadeIn(highlights[i]),
                *map(ShowCreation, hlines[i]),
                GrowFromPoint(phrases[i], highlights[i].get_right())
            )
            self.wait(2)

        # Embed
        self.embed()
