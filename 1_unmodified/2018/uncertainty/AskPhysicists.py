# ==============================================================================
# Scene:      AskPhysicists
# Source:     videos/_2018/uncertainty.py (lines 3202-3268)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskPhysicists.py AskPhysicists -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class AskPhysicists(PiCreatureScene):
    def construct(self):
        morty, physy1, physy2, physy3 = self.pi_creatures
        formula = OldTex("p", "=", "h", "\\xi")
        formula.set_color_by_tex_to_color_map({
            "p" : BLUE,
            "\\xi" : YELLOW,
        })
        formula.scale(1.5)

        formula.to_edge(UP)
        formula.save_state()
        formula.shift(DOWN)
        formula.fade(1)
        self.play(formula.restore)
        self.pi_creature_says(
            morty, "So...why?",
            target_mode = "maybe"
        )
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(morty),
            PiCreatureSays(
                physy2,
                "Take the Schrödinger equation \\\\ with $H = \\frac{p^2}{2m}+V(x)$",
                bubble_config = {"fill_opacity" : 0.9},
            ),
        )
        self.play(
            PiCreatureSays(
                physy1,
                "Even classically position and \\\\ momentum are conjugate",
                target_mode = "surprised",
                bubble_config = {"fill_opacity" : 0.9},
            ),
        )
        self.play(
            PiCreatureSays(
                physy3,
                "Consider special relativity \\\\ together with $E = hf$",
                target_mode = "hooray",
                bubble_config = {"fill_opacity" : 0.9},
            ),
            morty.change, "guilty"
        )
        self.wait(2)



    ###

    def create_pi_creatures(self):
        scale_factor = 0.85
        morty = Mortimer().flip()
        morty.scale(scale_factor)
        morty.to_corner(DOWN+LEFT)

        physies = VGroup(*[
            PiCreature(color = c).flip()
            for c in (GREY, GREY_B, GREY_D)
        ])
        physies.arrange(RIGHT, buff = MED_SMALL_BUFF)
        physies.scale(scale_factor)
        physies.to_corner(DOWN+RIGHT)

        self.add(physies)
        return VGroup(morty, *physies)
