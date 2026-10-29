# ==============================================================================
# Scene:      StrogatzMention
# Source:     videos/_2019/diffyq/part2/staging.py (lines 661-748)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl StrogatzMention.py StrogatzMention -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class StrogatzMention(PiCreatureScene):
    def construct(self):
        self.show_book()
        self.show_motives()
        self.show_pages()

    def show_book(self):
        morty = self.pi_creature
        book = ImageMobject("InfinitePowers")
        book.set_height(5)
        book.to_edge(LEFT)

        steve = ImageMobject("Strogatz_by_bricks")
        steve.set_height(5)
        steve.to_edge(LEFT)

        name = OldTexText("Steven Strogatz")
        name.match_width(steve)
        name.next_to(steve, DOWN)

        self.think(
            "Hmm...many good\\\\lessons here...",
            run_time=1
        )
        self.wait()
        self.play(FadeInFromDown(steve))
        self.wait()
        self.play(
            FadeIn(book, DOWN),
            steve.shift, 4 * RIGHT,
            RemovePiCreatureBubble(
                morty, target_mode="thinking"
            )
        )
        self.wait(3)
        self.play(
            FadeOut(steve),
            FadeOut(morty),
        )

        self.book = book

    def show_motives(self):
        motives = VGroup(
            OldTexText("1) Scratch and itch"),
            OldTexText("2) Make people love math"),
        )
        motives.scale(1.5)
        motives.arrange(
            DOWN, LARGE_BUFF,
            aligned_edge=LEFT,
        )
        motives.move_to(
            Line(
                self.book.get_right(),
                FRAME_WIDTH * RIGHT / 2
            )
        )
        motives.to_edge(UP)

        for motive in motives:
            self.play(FadeInFromDown(motive))
            self.wait(2)
        self.play(FadeOut(motives))

    def show_pages(self):
        book = self.book
        pages = Group(*[
            ImageMobject("IP_Sample_Page{}".format(i))
            for i in range(1, 4)
        ])
        for page in pages:
            page.match_height(book)
            page.next_to(book, RIGHT)

        last_page = VectorizedPoint()
        for page in pages:
            self.play(
                FadeOut(last_page),
                FadeIn(page)
            )
            self.wait()
            last_page = page

        self.play(FadeOut(last_page))

    def create_pi_creature(self):
        return Mortimer().to_corner(DR)
