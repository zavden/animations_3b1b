# ==============================================================================
# Scene:      MoonSunRatios
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 912-937)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoonSunRatios.py MoonSunRatios -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoonSunRatios(InteractiveScene):
    def construct(self):
        # Write equation
        equation = Tex(
            R"{R_M \over D_M} = {R_S \over D_S} \approx \frac{1}{220}",
            t2c={
                "R_M": GREY_B,
                "D_M": GREY_B,
                "R_S": YELLOW,
                "D_S": YELLOW,
            }
        )
        equation.to_corner(UL)

        self.add(equation[R"{R_M \over D_M}"])
        self.wait()
        self.play(LaggedStart(
            Write(equation["="][0]),
            TransformFromCopy(equation["R_M"][0], equation["R_S"][0]),
            TransformFromCopy(equation[R"\over"][0], equation[R"\over"][1]),
            TransformFromCopy(equation["D_M"][0], equation["D_S"][0]),
            lag_ratio=0.35
        ))
        self.wait()
        self.play(Write(equation[R"\approx \frac{1}{220}"]))
        self.wait()
