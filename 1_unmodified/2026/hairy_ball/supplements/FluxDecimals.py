# ==============================================================================
# Scene:      FluxDecimals
# Source:     videos/_2026/hairy_ball/supplements.py (lines 603-630)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FluxDecimals.py FluxDecimals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FluxDecimals(InteractiveScene):
    def construct(self):
        # Test
        label = TexText("Flux: +1.000 L/s", font_size=60)
        dec = label.make_number_changeable("+1.000", include_sign=True)
        label.to_corner(UR)
        dec.set_value(1)

        def update_color(dec, epsilon=1e-4):
            value = dec.get_value()
            if value > epsilon:
                dec.set_color(GREEN)
            elif abs(value) < epsilon:
                dec.set_color(YELLOW)
            else:
                dec.set_color(RED)

        dec.add_updater(update_color)

        self.add(label)
        self.wait()
        for value in [0.014, -0.014, 0.014]:
            self.play(ChangeDecimalToValue(dec, value))
            self.wait()
        self.play(ChangeDecimalToValue(dec, 1.0), run_time=3)
        self.wait()
        dec.set_value(0)
        self.wait()
