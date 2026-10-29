# ==============================================================================
# Scene:      WatchingVideo
# Source:     videos/_2017/eoc/chapter4.py (lines 2082-2126)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WatchingVideo.py WatchingVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WatchingVideo(PiCreatureScene):
    def construct(self):
        laptop = Laptop()
        laptop.scale(2)
        laptop.to_corner(UP+RIGHT)
        randy = self.get_primary_pi_creature()
        randy.move_to(laptop, DOWN+LEFT)
        randy.shift(MED_SMALL_BUFF*UP)
        randy.look_at(laptop.screen)


        formulas = VGroup(*[
            OldTex("\\frac{d}{dx}\\left( %s \\right)"%s)
            for s in [
                "e^x \\sin(x)",
                "\\sin(x) \\cdot  \\frac{1}{\\cos(x)}",
                "\\cos(3x)^2",
                "e^x(x^2 + 3x + 2)",
            ]
        ])
        formulas.arrange(
            DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        formulas.next_to(randy, LEFT, buff = MED_LARGE_BUFF)
        formulas.shift_onto_screen()

        self.add(randy, laptop)
        self.wait()
        self.play(randy.change_mode, "erm")
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change_mode, "maybe")
        self.wait()
        self.play(Blink(randy))
        for formula in formulas:
            self.play(
                Write(formula, run_time = 2),
                randy.change_mode, "thinking"
            )
            self.wait()

    def create_pi_creatures(self):
        return [Randolph().shift(DOWN+RIGHT)]
