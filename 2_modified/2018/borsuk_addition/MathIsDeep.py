# ==============================================================================
# Scene:      MathIsDeep
# Source:     videos/_2018/borsuk_addition.py (lines 201-263)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl MathIsDeep.py MathIsDeep -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - inner contour of letter math[1] removed by keeping only its largest subpath (GL glyphs have no submobjects for holes)
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class MathIsDeep(PiCreatureScene):
    def construct(self):
        words = OldTexText(
            "Math", "is", "deep"
        )
        words.scale(2)
        words.to_edge(UP)
        math = words[0].copy()
        # CHANGE: GL glyphs have no submobjects for their holes; Cairo's math[1].remove(math[1][1]) dropped the inner contour of the letter, so keep only its largest subpath
        math[1].set_points(max(math[1].get_subpaths(), key = lambda p : np.ptp(p[:, 0]) * np.ptp(p[:, 1])))
        math.set_fill(opacity=0)
        math.set_stroke(width=0, background=True)
        numbers = [13, 1, 20, 8]
        num_mobs = VGroup(*[Integer(d) for d in numbers])
        num_mobs.arrange(RIGHT, buff=MED_LARGE_BUFF)
        num_mobs.next_to(math, DOWN, buff=1.5)
        num_mobs.set_color(YELLOW)
        top_arrows = VGroup(*[
            Arrow(c.get_bottom(), n.get_top())
            for c, n in zip(math, num_mobs)
        ])
        n_sum = Integer(sum(numbers))
        n_sum.scale(1.5)
        n_sum.next_to(num_mobs, DOWN, buff=1.5)
        low_arrows = VGroup(*[
            Arrow(n.get_bottom(), n_sum.get_top())
            for n in num_mobs
        ])
        VGroup(top_arrows, low_arrows).set_color(WHITE)

        n_sum_border = n_sum.deepcopy()
        n_sum_border.set_fill(opacity=0)
        n_sum_border.set_stroke(YELLOW, width=1)
        n_sum_border.set_stroke(width=0, background=True)

        # pre_num_mobs = num_mobs.copy()
        # for pn, letter in zip(pre_num_mobs, math):
        #     pn.fade(1)
        #     pn.set_color(RED)
        #     pn.move_to(letter)
        # num_mobs[1].add_subpath(num_mobs[1].get_points())

        self.play(
            LaggedStartMap(
                FadeInFromLarge, words,
                scale_factor=1.5,
                run_time=0.6,
                lag_ratio=0.6,
            ),
            self.pi_creature.change, "pondering"
        )
        self.play(
            TransformFromCopy(math, num_mobs),
            *map(GrowArrow, top_arrows),
        )
        self.wait()
        self.play(
            TransformFromCopy(num_mobs, VGroup(n_sum)),
            self.pi_creature.change, "thinking",
            *map(GrowArrow, low_arrows),
        )
        self.play(LaggedStartMap(ShowCreationThenDestruction, n_sum_border))
        self.play(Blink(self.pi_creature))
        self.wait()
