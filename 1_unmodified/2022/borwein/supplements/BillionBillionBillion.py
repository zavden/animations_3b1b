# ==============================================================================
# Scene:      BillionBillionBillion
# Source:     videos/_2022/borwein/supplements.py (lines 155-166)
# Category:   1 · Renders unmodified
# Includes code copied from: _2022/borwein/main.py
#
# Run from this folder:
#     manimgl BillionBillionBillion.py BillionBillionBillion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/borwein/main.py -----

def get_fifteenth_frac_tex():
    return R"{467{,}807{,}924{,}713{,}440{,}738{,}696{,}537{,}864{,}469 \over 467{,}807{,}924{,}720{,}320{,}453{,}655{,}260{,}875{,}000}"



# ----- From _2022/borwein/supplements.py -----

class BillionBillionBillion(InteractiveScene):
    def construct(self):
        fraction = OldTex(get_fifteenth_frac_tex())[0]
        # self.add(fraction)

        for x in (4, 16, 28):
            part = VGroup(*fraction[x:x + 11], *fraction[x + 40:x + 40 + 11])
            vh = VHighlight(part, color_bounds=(YELLOW, BLACK), max_stroke_addition=8)
            self.add(vh, part)
            self.wait(0.5)
            self.remove(vh, part)
        self.wait()
