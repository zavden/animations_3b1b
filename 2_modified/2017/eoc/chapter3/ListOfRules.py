# ==============================================================================
# Scene:      ListOfRules
# Source:     videos/_2017/eoc/chapter3.py (lines 180-206)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ListOfRules.py ListOfRules -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
# ==============================================================================

from manim_imports_ext import *

class ListOfRules(PiCreatureScene):
    CONFIG = {
        "use_morty" : False,
    }
    def construct(self):
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        rules = VGroup(*list(map(OldTex, [
            "\\frac{d}{dx} x^n = nx^{n-1}",
            "\\frac{d}{dx} \\sin(x) = \\cos(x)",
            "\\frac{d}{dx} \\cos(x) = -\\sin(x)",
            "\\frac{d}{dx} a^x = \\ln(a) a^x",
            "\\vdots"
        ])))
        rules.arrange(
            DOWN, buff = MED_LARGE_BUFF,
            aligned_edge = LEFT,
        )
        rules[-1].shift(MED_LARGE_BUFF*RIGHT)
        rules.set_height(FRAME_HEIGHT-1)
        rules.next_to(self.pi_creature, RIGHT)
        rules.to_edge(DOWN)

        self.play(
            Write(rules),
            self.pi_creature.change_mode, "pleading",
        )
        self.change_mode("tired")
        self.wait()
