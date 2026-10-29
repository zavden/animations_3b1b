# ==============================================================================
# Scene:      IntroduceSierpinskiTriangle
# Source:     videos/_2017/fractal_dimension.py (lines 234-261)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceSierpinskiTriangle.py IntroduceSierpinskiTriangle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceSierpinskiTriangle(PiCreatureScene):
    CONFIG = {
        "order" : 7,
    }
    def construct(self):
        sierp = Sierpinski(order = self.order)
        sierp.save_state()

        self.play(FadeIn(
            sierp,
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait()
        self.play(
            self.pi_creature.change_mode, "pondering",
            *[
                ApplyMethod(submob.shift, submob.get_center())
                for submob in sierp
            ]
        )
        self.wait()
        for submob in sierp:
            self.play(sierp.shift, -submob.get_center())
            self.wait()
        self.play(sierp.restore)
        self.change_mode("happy")
        self.wait()
