# ==============================================================================
# Scene:      MonsterQuotes
# Source:     videos/_2020/monster.py (lines 4254-4297)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MonsterQuotes.py MonsterQuotes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_named_image(name, height=3):
    image = ImageMobject(name)
    image.set_height(height)

    name = OldTexText(name)
    name.match_width(image)
    name.next_to(image, DOWN)
    group = Group(image, name)
    return group


class MonsterQuotes(Scene):
    def construct(self):
        images = [
            get_named_image("John Conway"),
            get_named_image("Richard Borcherds"),
        ]

        quotes = [
            OldTexText(
                """
                ``Nothing has given me the feeling\\\\
                that I understand why the monster\\\\
                is there.''\\\\
                """,
                alignment="",
            ),
            OldTexText(
                """
                ``The monster simple group . . . appears\\\\
                to rely on numerous bizarre coincidences\\\\
                to exist.''\\\\
                """,
                alignment="",
            ),
        ]
        faders = []
        self.clear()
        for image, quote, color in zip(images, quotes, [YELLOW, WHITE]):
            quote[0].set_color(color)

            image.set_height(5)
            image.to_edge(LEFT)
            image[1].set_color(GREY_B)
            quote.next_to(image, RIGHT, buff=1, aligned_edge=UP)
            quote.shift(DOWN)
            quote.shift_onto_screen()

            self.play(
                FadeIn(image, DOWN),
                FadeIn(quote, lag_ratio=0.1, run_time=3),
                *faders,
            )
            self.wait(4)
            faders = [FadeOut(image, UP), FadeOut(quote)]
