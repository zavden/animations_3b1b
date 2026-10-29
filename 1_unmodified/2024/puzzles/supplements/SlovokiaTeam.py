# ==============================================================================
# Scene:      SlovokiaTeam
# Source:     videos/_2024/puzzles/supplements.py (lines 329-351)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SlovokiaTeam.py SlovokiaTeam -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SlovokiaTeam(InteractiveScene):
    def construct(self):
        # Test
        talker = PiCreature(color=RED_E)
        talker.to_edge(DOWN).shift(3 * LEFT)
        flag = ImageMobject("flags/sk.png")
        flag.set_height(1)
        flag.next_to(talker, LEFT)
        name = Text("Akos Zahorsky", font_size=24)
        name.next_to(flag, DOWN, buff=SMALL_BUFF)

        morty = Mortimer()
        morty.to_edge(DOWN).shift(3 * RIGHT)

        self.play(
            talker.says("You can save\nthis proof.", mode="speaking", look_at=morty.eyes),
            morty.change("pondering", talker.eyes)
        )
        self.play(FadeIn(flag, UP), morty.change("tease"))
        self.play(Write(name))
        self.play(Blink(morty))
        self.play(Blink(talker))
        self.wait()
