# ==============================================================================
# Scene:      MoreModestDirichlet
# Source:     videos/_2019/spirals.py (lines 4215-4254)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreModestDirichlet.py MoreModestDirichlet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoreModestDirichlet(Scene):
    def construct(self):
        ed = OldTexText(
            "Each (coprime) residue class ",
            "is equally dense with ",
            "primes."
        )
        inf = OldTexText(
            "Each (coprime) residue class ",
            "has infinitely many ",
            "primes."
        )
        ed[1].set_color(BLUE)
        inf[1].set_color(GREEN)

        for mob in [*ed, *inf]:
            mob.save_state()

        cross = Cross(ed[1])
        c_group = VGroup(ed[1], cross)

        self.add(ed)
        self.wait()
        self.play(ShowCreation(cross))
        self.play(
            c_group.shift, DOWN,
            c_group.set_opacity, 0.5,
            ReplacementTransform(ed[::2], inf[::2]),
            FadeIn(inf[1])
        )
        self.wait()
        self.remove(*inf)
        self.play(
            inf[1].shift, UP,
            Restore(ed[0]),
            Restore(ed[1]),
            Restore(ed[2]),
            FadeOut(cross),
        )
        self.wait()
