# ==============================================================================
# Scene:      DampenedSpring
# Source:     videos/_2017/eoc/chapter4.py (lines 205-241)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DampenedSpring.py DampenedSpring -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DampenedSpring(Scene):
    def construct(self):
        compact_spring, extended_spring = [
            ParametricCurve(
                lambda t : (t/denom)*RIGHT+np.sin(t)*UP+np.cos(t)*OUT,
                t_max = 12*np.pi,
                color = GREY,
            ).shift(3*LEFT)
            for denom in (12.0, 2.0)
        ]
        for spring in compact_spring, extended_spring:
            spring.scale(0.5)
            spring.rotate(np.pi/6, UP)
            spring.set_color(GREY)
            spring.shift(-spring.get_points()[0] + 3*LEFT)

        moving_spring = compact_spring.copy()

        def update_spring(spring, a):
            spring.interpolate(
                compact_spring, 
                extended_spring,
                0.5*(np.exp(-4*a)*np.cos(40*a)+1)
            )

        equation = OldTex(
            "\\text{Length} = 2 + e^{-4t}\\cos(20t)"
        )
        equation.to_edge(UP)


        self.add(moving_spring, equation)
        self.play(UpdateFromAlphaFunc(
            moving_spring, update_spring, run_time = 10,
            rate_func=linear
        ))
        self.wait()
