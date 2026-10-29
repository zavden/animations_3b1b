# ==============================================================================
# Scene:      ShowCurrAndTarget
# Source:     videos/_2020/chess.py (lines 4447-4504)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowCurrAndTarget.py ShowCurrAndTarget -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowCurrAndTarget(Scene):
    CONFIG = {
        "bit_strings": [
            "011010",
            "110001",
            "101011",
        ]
    }

    def construct(self):
        words = VGroup(
            OldTexText("Current: "),
            OldTexText("Need to\\\\change:"),
            OldTexText("Target: "),
        )
        words.arrange(DOWN, buff=0.75, aligned_edge=RIGHT)
        words.to_corner(UL)

        def get_bit_aligned_bit_string(bit_coords):
            result = VGroup(*[Integer(int(b)) for b in bit_coords])
            for i, bit in enumerate(result):
                bit.move_to(ORIGIN, LEFT)
                bit.shift(i * RIGHT * 0.325)
            result.set_stroke(BLACK, 4, background=True)
            return result

        bit_strings = VGroup(*[
            get_bit_aligned_bit_string(bs)
            for bs in self.bit_strings
        ])
        for word, bs in zip(words, bit_strings):
            bs.next_to(word.family_members_with_points()[-1], RIGHT, aligned_edge=DOWN)

        words[1].set_fill(YELLOW)
        bit_strings[1].set_fill(YELLOW)

        self.add(words[::2])
        self.add(bit_strings[::2])
        self.wait()
        self.play(FadeIn(words[1]))

        curr_rect = None
        for n in reversed(range(6)):
            rect = SurroundingRectangle(Group(
                bit_strings[0][n],
                bit_strings[2][n],
                buff=0.05,
            ))
            rect.stretch(0.9, 0)
            rect.set_stroke(WHITE, 1)
            if curr_rect is None:
                curr_rect = rect
                self.play(ShowCreation(curr_rect))
            else:
                self.play(Transform(curr_rect, rect, run_time=0.25))
                self.wait(0.75)
            self.play(FadeIn(bit_strings[1][n]))
        self.play(FadeOut(curr_rect))
