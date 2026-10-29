# ==============================================================================
# Scene:      OneInOneThousandHaveDisease
# Source:     videos/_2018/eop/bayes_footnote.py (lines 233-268)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneInOneThousandHaveDisease.py OneInOneThousandHaveDisease -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


class OneInOneThousandHaveDisease(Scene):
    def construct(self):
        title = OldTexText("1 in 1{,}000")
        title.to_edge(UP)
        creature = PiCreature()
        all_creatures = VGroup(*[
            VGroup(*[
                creature.copy()
                for y in range(25)
            ]).arrange(DOWN, SMALL_BUFF)
            for x in range(40)
        ]).arrange(RIGHT, SMALL_BUFF)
        all_creatures.set_width(FRAME_WIDTH - 4)
        all_creatures.next_to(title, DOWN)
        randy = all_creatures[0][0]
        all_creatures[0].remove(randy)
        randy.change_mode("sick")
        randy.set_color(SICKLY_GREEN)
        randy.save_state()
        randy.set_height(3)
        randy.center()
        randy.change_mode("plain")
        randy.set_color(BLUE)

        self.add(randy)
        self.play(
            randy.change_mode, "sick",
            randy.set_color, SICKLY_GREEN
        )
        self.play(Blink(randy))
        self.play(randy.restore)
        self.play(
            Write(title),
            LaggedStartMap(FadeIn, all_creatures, run_time = 3)
        )
        self.wait()
