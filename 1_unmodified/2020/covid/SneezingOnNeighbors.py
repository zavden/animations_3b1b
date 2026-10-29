# ==============================================================================
# Scene:      SneezingOnNeighbors
# Source:     videos/_2020/covid.py (lines 1342-1390)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SneezingOnNeighbors.py SneezingOnNeighbors -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


class SneezingOnNeighbors(Scene):
    def construct(self):
        randys = VGroup(*[PiCreature() for x in range(3)])
        randys.set_height(1)
        randys.arrange(RIGHT)

        self.add(randys)
        self.play(
            randys[1].change, "sick",
            randys[1].set_color, SICKLY_GREEN,
        )
        self.play(
            Flash(
                randys[1],
                color=SICKLY_GREEN,
                flash_radius=0.8,
            ),
            randys[0].change, "sassy", randys[1],
            randys[2].change, "angry", randys[1],
        )
        self.play(
            randys[0].change, "sick",
            randys[0].set_color, SICKLY_GREEN,
            randys[2].change, "sick",
            randys[2].set_color, SICKLY_GREEN,
        )
        self.play(
            Flash(
                randys[1],
                color=SICKLY_GREEN,
                flash_radius=0.8,
            )
        )
        self.play(
            randys[0].change, "sad", randys[1],
            randys[2].change, "tired", randys[1],
        )
        self.play(
            Flash(
                randys[1],
                color=SICKLY_GREEN,
                flash_radius=0.8,
            )
        )
        self.play(
            randys[0].change, "angry", randys[1],
            randys[2].change, "angry", randys[1],
        )
        self.wait()
