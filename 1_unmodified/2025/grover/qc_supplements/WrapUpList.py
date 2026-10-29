# ==============================================================================
# Scene:      WrapUpList
# Source:     videos/_2025/grover/qc_supplements.py (lines 1092-1135)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WrapUpList.py WrapUpList -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WrapUpList(InteractiveScene):
    def construct(self):
        # List
        morty = Mortimer()
        morty.to_corner(DR)

        items = BulletedList(
            "The Lie",
            R"Why $\sqrt{\quad}$",
            "A suprising analogy",
            buff=0.75
        )
        items[1][-2:].shift(SMALL_BUFF * UP)
        items[1][1:].shift(0.5 * SMALL_BUFF * DOWN)
        items.scale(1.25)
        items.to_edge(UP, LARGE_BUFF)

        morty.body.insert_n_curves(100)

        self.play(
            morty.change("raise_right_hand", items),
            FadeInFromPoint(items[0], morty.get_corner(UL), lag_ratio=0.01)
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change("pondering", items[1]),
            Write(items[1]),
        )
        self.wait()
        self.play(
            morty.change("tease", 5 * UR),
            FadeIn(items[2], DOWN),
        )
        self.play(Blink(morty))
        self.wait()

        for n, mode in enumerate(["guilty", "tease", "surprised"]):
            self.play(
                items.animate.fade_all_but(n, scale_factor=0.5),
                morty.change(mode, items[n]),
            )
            self.play(Blink(morty))
            self.wait()
