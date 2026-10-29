# ==============================================================================
# Scene:      IncrementTest
# Source:     videos/_2017/eoc/chapter2.py (lines 39-44)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IncrementTest.py IncrementTest -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IncrementNumber(Succession):
    CONFIG = {
        "start_num" : 0,
        "changes_per_second" : 1,
        "run_time" : 11,
    }
    def __init__(self, num_mob, **kwargs):
        digest_config(self, kwargs)
        n_iterations = int(self.run_time * self.changes_per_second)
        new_num_mobs = [
            OldTex(str(num)).move_to(num_mob, LEFT)
            for num in range(self.start_num, self.start_num+n_iterations)
        ]
        transforms = [
            Transform(
                num_mob, new_num_mob, 
                run_time = 1.0/self.changes_per_second,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            for new_num_mob in new_num_mobs
        ]
        Succession.__init__(
            self, *transforms, **{
                "rate_func" : None,
                "run_time" : self.run_time,
            }
        )


class IncrementTest(Scene):
    def construct(self):
        num = OldTex("0")
        num.shift(UP)
        self.play(IncrementNumber(num))
        self.wait()
