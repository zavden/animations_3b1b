# ==============================================================================
# Scene:      RantPage
# Source:     videos/outside_videos/for_site.py (lines 169-218)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RantPage.py RantPage -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - PiCreature no longer has .pupils: each eye is a VGroup(iris, pupil) with eye.pupil and eye.iris
# ==============================================================================

from manim_imports_ext import *

class RantPage(Scene):
    CONFIG = {
    }

    def construct(self):
        squares = VGroup(Square(), Square())
        squares.arrange(DOWN, buff=MED_SMALL_BUFF)
        squares.set_height(FRAME_HEIGHT - 0.5)
        squares.set_width(5, stretch=True)
        squares.set_stroke(WHITE, 2)
        squares.set_fill(BLACK, opacity=0.75)
        s1, s2 = squares

        # Group1
        morty = Mortimer(mode="maybe")
        # CHANGE: PiCreature no longer has .pupils: each eye is a VGroup(iris, pupil) with eye.pupil and eye.iris
        for eye in morty.eyes:
            eye.pupil.move_to(eye.iris)
        morty.shift(MED_SMALL_BUFF * UL)
        words = OldTexText(
            "What were you\\\\expecting to be here?"
        )
        bubble = SpeechBubble(direction=RIGHT)
        bubble.match_style(s1)
        bubble.add_content(words)
        bubble.resize_to_content()
        bubble.add(bubble.content)
        bubble.pin_to(morty)
        group1 = VGroup(morty, bubble)
        group1.set_height(s1.get_height() - MED_SMALL_BUFF)
        group1.next_to(s1.get_corner(DR), UL, SMALL_BUFF)

        # Group 2
        morty = Mortimer(mode="surprised")
        morty.shift(MED_SMALL_BUFF * UL)
        words = OldTexText(
            "Go on!\\\\Give the rant!"
        )
        bubble = SpeechBubble(direction=RIGHT)
        bubble.match_style(s1)
        bubble.add_content(words)
        bubble.resize_to_content()
        bubble.add(bubble.content)
        bubble.pin_to(morty)
        group2 = VGroup(morty, bubble)
        group2.set_height(s2.get_height() - MED_SMALL_BUFF)
        group2.next_to(s2.get_corner(DR), UL, SMALL_BUFF)

        self.add(squares)
        self.add(group1)
        self.add(group2)
