# ==============================================================================
# Scene:      PInfectionSlider
# Source:     videos/_2020/sir.py (lines 2746-2764)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PInfectionSlider.py PInfectionSlider -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ValueSlider(NumberLine):
    CONFIG = {
        "x_min": 0,
        "x_max": 1,
        "tick_frequency": 0.1,
        "big_tick_numbers": [],
        "numbers_to_show": np.linspace(0, 1, 6),
        "decimal_number_config": {
            "num_decimal_places": 1,
        },
        "stroke_width": 5,
        "width": 8,
        "marker_color": BLUE,
    }

    def __init__(self, name, value, **kwargs):
        super().__init__(**kwargs)
        self.set_width(self.width, stretch=True)
        self.add_numbers()

        self.marker = ArrowTip(start_angle=-90 * DEGREES)
        self.marker.move_to(self.n2p(value), DOWN)
        self.marker.set_color(self.marker_color)
        self.add(self.marker)

        # self.label = DecimalNumber(value)
        # self.label.next_to(self.marker, UP)
        # self.add(self.label)

        self.name = OldTexText(name)
        self.name.scale(1.25)
        self.name.next_to(self, DOWN)
        self.name.match_color(self.marker)
        self.add(self.name)

    def get_change_anim(self, new_value, **kwargs):
        start_value = self.p2n(self.marker.get_bottom())
        # m2l = self.label.get_center() - self.marker.get_center()

        def update(mob, alpha):
            interim_value = interpolate(start_value, new_value, alpha)
            mob.marker.move_to(mob.n2p(interim_value), DOWN)
            # mob.label.move_to(mob.marker.get_center() + m2l)
            # mob.label.set_value(interim_value)

        return UpdateFromAlphaFunc(self, update, **kwargs)


class PInfectionSlider(Scene):
    def construct(self):
        slider = ValueSlider(
            "Probability of infection",
            0.2,
            x_min=0,
            x_max=0.2,
            numbers_to_show=np.arange(0.05, 0.25, 0.05),
            decimal_number_config={
                "num_decimal_places": 2,
            },
            tick_frequency=0.05,
        )
        self.add(slider)
        self.wait()
        self.play(slider.get_change_anim(0.1))
        self.wait()
        self.play(slider.get_change_anim(0.05))
        self.wait()
