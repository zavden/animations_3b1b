# ==============================================================================
# Scene:      RenameAllInTermsOfSine
# Source:     videos/_2017/tattoo.py (lines 698-777)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RenameAllInTermsOfSine.py RenameAllInTermsOfSine -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
# ==============================================================================

from manim_imports_ext import *

class RenameAllInTermsOfSine(Scene):
    def construct(self):
        texs = [
            "\\sin(\\theta)",
            "\\cos(\\theta)",
            "\\tan(\\theta)",
            "\\csc(\\theta)",
            "\\sec(\\theta)",
            "\\cot(\\theta)",
        ]
        shift_vals = [
            4*LEFT+3*UP,
            4*LEFT+UP,
            4*LEFT+DOWN,
            4*RIGHT+3*UP,
            4*RIGHT+UP,
            4*RIGHT+DOWN,
        ]
        equivs = [
            "",
            "= \\sin(90^\\circ - \\theta)",
            "= \\frac{\\sin(\\theta)}{\\sin(90^\\circ - \\theta)}",
            "= \\frac{1}{\\sin(\\theta)}",
            "= \\frac{1}{\\sin(90^\\circ - \\theta)}",
            "= \\frac{\\sin(90^\\circ - \\theta)}{\\sin(\\theta)}",
        ]
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        mobs = VGroup(*list(map(OldTex, texs)))
        sin, cos, tan = mobs[:3]
        sin.target_color = YELLOW
        cos.target_color = GREEN
        tan.target_color = RED

        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        rhs_mobs = VGroup(*list(map(OldTex, equivs)))
        rhs_mobs.submobjects[0] = VectorizedPoint()
        for mob, shift_val in zip(mobs, shift_vals):
            mob.shift(shift_val)
        self.play(Write(mobs))
        self.wait()
        for mob, rhs_mob in zip(mobs, rhs_mobs):
            rhs_mob.next_to(mob)
            rhs_mob.set_color(sin.target_color)
            mob.save_state()
            mob.generate_target()
            VGroup(mob.target, rhs_mob).move_to(mob)
        sin.target.set_color(sin.target_color)
        self.play(*it.chain(*[
            list(map(MoveToTarget, mobs)),
            [Write(rhs_mobs)]
        ]))
        self.wait(2)

        anims = []
        for mob, rhs_mob in list(zip(mobs, rhs_mobs))[1:3]:
            anims += [
                FadeOut(rhs_mob),
                mob.restore,
                mob.set_color, mob.target_color,
            ]
        self.play(*anims)
        self.wait()

        new_rhs_mobs = [
            OldTex("=\\frac{1}{\\%s(\\theta)}"%s).set_color(color)
            for s, color in [
                ("cos", cos.target_color),
                ("tan", tan.target_color),
            ]
        ]
        anims = []
        for mob, rhs, new_rhs in zip(mobs[-2:], rhs_mobs[-2:], new_rhs_mobs):
            new_rhs.next_to(mob)
            VGroup(mob.target, new_rhs).move_to(
                VGroup(mob, rhs)
            )
            anims += [
                MoveToTarget(mob),
                Transform(rhs, new_rhs)
            ]
        self.play(*anims)
        self.wait(2)
