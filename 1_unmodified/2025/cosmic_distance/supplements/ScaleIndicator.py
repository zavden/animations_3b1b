# ==============================================================================
# Scene:      ScaleIndicator
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 1199-1257)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ScaleIndicator.py ScaleIndicator -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ScaleIndicator(InteractiveScene):
    def construct(self):
        # Test
        power_tracker = ValueTracker(0)
        indicator = always_redraw(lambda: self.get_indicator(power_tracker.get_value()))

        self.add(indicator)
        max_tim = 27
        self.play(
            power_tracker.animate.set_value(max_tim),
            run_time=3 * max_tim,
            rate_func=linear
        )

    def get_indicator(self, exponent, ref_width=2.0):
        low_power = int(exponent)
        high_power = int(exponent + 1)
        pieces = VGroup(
            self.get_piece(width=(10**(low_power - exponent)) * ref_width),
            self.get_piece(width=(10**(high_power - exponent)) * ref_width),
        )
        labels = VGroup(
            self.get_label(low_power),
            self.get_label(high_power),
        )
        opacities = [
            self.get_opacity(low_power - exponent),
            self.get_opacity(high_power - exponent),
        ]
        for piece, label, opacity in zip(pieces, labels, opacities):
            piece.move_to(4 * LEFT, DL)
            label.set_height(0.25)
            label.set_max_width(0.8 * piece.get_width())
            label.next_to(piece, DOWN, buff=SMALL_BUFF)
            width_diff = abs(ref_width - piece.get_width())
            piece.set_stroke(opacity=opacity)
            label.set_fill(opacity=opacity).set_stroke(opacity=opacity)

        return VGroup(pieces, labels)

    def get_piece(self, width):
        line = UnitInterval(width=1, tick_size=0.075)
        line.set_width(width, stretch=True)
        line.center()
        for tick in line.ticks:
            tick.align_to(ORIGIN, DOWN)

        return VGroup(line.copy().set_stroke(BLACK, width=3), line)

    def get_label(self, power):
        if power <= 14:
            result = Integer(10**power, unit="km")
        else:
            result = Tex(fR"10^{{{power}}} \text{{ km}}")
        result.set_backstroke(BLACK, 4)
        return result

    def get_opacity(self, exp_diff):
        return 1.0 - clip(inverse_interpolate(0.25, 0.75, abs(exp_diff)), 0, 1)
