# ==============================================================================
# Scene:      UniqueCharacterization
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 468-487)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UniqueCharacterization.py UniqueCharacterization -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class UniqueCharacterization(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(t2c={"{x}": BLUE, "{y}": YELLOW})
        group = VGroup(
            TexText("Rotational symmetry of $f({x})f({y})$", font_size=36, **kw),
            Tex(R"\Downarrow"),
            Tex(R"f({x}) = Ae^{-c {x}^2}", **kw),
        )
        group.arrange(DOWN)
        group.to_corner(UR)

        self.add(group[0])
        self.wait()
        self.play(
            Write(group[1]),
            FadeInFromPoint(group[2], group[0]["f({x})"].get_center()),
            run_time=1
        )
        self.wait()
