# ==============================================================================
# Scene:      ZoomInOnFractal
# Source:     videos/_2017/fractal_dimension.py (lines 65-128)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ZoomInOnFractal.py ZoomInOnFractal -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Mobject.show() would open an image viewer (debug call of the original): removed
# ==============================================================================

from manim_imports_ext import *

class ZoomInOnFractal(PiCreatureScene):
    CONFIG = {
        "fractal_order" : 6,
        "num_zooms" : 5,
        "fractal_class" : DiamondFractal,
        "index_to_replace" : 0,
    }
    def construct(self):
        morty = self.pi_creature

        fractal = self.fractal_class(order = self.fractal_order)
        # CHANGE: Mobject.show() would open an image viewer (debug call of the original): removed
        pass

        fractal = self.introduce_fractal()
        self.change_mode("thinking")
        self.blink()
        self.zoom_in(fractal)


    def introduce_fractal(self):
        fractal = self.fractal_class(order = 0)
        self.play(FadeIn(fractal))
        for order in range(1, self.fractal_order+1):
            new_fractal = self.fractal_class(order = order)
            self.play(
                Transform(fractal, new_fractal, run_time = 2),
                self.pi_creature.change_mode, "hooray"
            )
        return fractal

    def zoom_in(self, fractal):
        grower = fractal[self.index_to_replace]
        grower_target = fractal.copy()

        for x in range(self.num_zooms):
            self.tweak_fractal_subpart(grower_target)
            grower_family = grower.family_members_with_points()
            everything = VGroup(*[
                submob
                for submob in fractal.family_members_with_points()
                if not submob.is_off_screen()
                if submob not in grower_family
            ])
            everything.generate_target()
            everything.target.shift(
                grower_target.get_center()-grower.get_center()
            )
            everything.target.scale(
                grower_target.get_height()/grower.get_height()
            )

            self.play(
                Transform(grower, grower_target),
                MoveToTarget(everything),
                self.pi_creature.change_mode, "thinking",
                run_time = 2
            )
            self.wait()
            grower_target = grower.copy()
            grower = grower[self.index_to_replace]


    def tweak_fractal_subpart(self, subpart):
        subpart.rotate(np.pi/4)
