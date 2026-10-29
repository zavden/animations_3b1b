# ==============================================================================
# Scene:      IPTScene2
# Source:     videos/_2018/basel/basel.py (lines 2248-2297)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IPTScene2.py IPTScene2 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - numpy 2: `array != None` is elementwise (ambiguous truth value); use `is not None`
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


LIGHT_COLOR = YELLOW


INDICATOR_STROKE_WIDTH = 1


INDICATOR_STROKE_COLOR = WHITE


INDICATOR_TEXT_COLOR = WHITE


LIGHT_COLOR = YELLOW


class LightIndicator(VMobject):
    CONFIG = {
        "radius": 0.5,
        "intensity": 0,
        "opacity_for_unit_intensity": 1,
        "precision": 3,
        "show_reading": True,
        "measurement_point": ORIGIN,
        "light_source": None
    }

    def init_points(self):
        self.background = Circle(color=BLACK, radius = self.radius)
        self.background.set_fill(opacity=1.0)
        self.foreground = Circle(color=self.color, radius = self.radius)
        self.foreground.set_stroke(color=INDICATOR_STROKE_COLOR,width=INDICATOR_STROKE_WIDTH)

        self.add(self.background, self.foreground)
        self.reading = DecimalNumber(self.intensity,num_decimal_places = self.precision)
        self.reading.set_fill(color=INDICATOR_TEXT_COLOR)
        self.reading.move_to(self.get_center())
        if self.show_reading:
            self.add(self.reading)

    def set_intensity(self, new_int):
        self.intensity = new_int
        new_opacity = min(1, new_int * self.opacity_for_unit_intensity)
        self.foreground.set_fill(opacity=new_opacity)
        ChangeDecimalToValue(self.reading, new_int).update(1)
        return self

    def get_measurement_point(self):
        # CHANGE: numpy 2: `array != None` is elementwise (ambiguous truth value); use `is not None`
        if self.measurement_point is not None:
            return self.measurement_point
        else:
            return self.get_center()


    def measured_intensity(self):
        distance = get_norm(self.get_measurement_point() - 
            self.light_source.get_source_point())
        intensity = self.light_source.opacity_function(distance) / self.opacity_for_unit_intensity
        return intensity

    def update_mobjects(self):
        if self.light_source == None:
            print("Indicator cannot update, reason: no light source found")
        self.set_intensity(self.measured_intensity())


class IPTScene2(Scene):

    def construct(self):

        intensity1 = 0.3
        intensity2 = 0.2
        formula_scale = 01.2
        indy_radius = 1

        indy1 = LightIndicator(color = LIGHT_COLOR, show_reading = False, radius = indy_radius)
        indy1.set_intensity(intensity1)
        reading1 = OldTex("{1\over a^2}").scale(formula_scale).move_to(indy1)
        indy1.add(reading1)

        indy2 = LightIndicator(color = LIGHT_COLOR, show_reading = False, radius = indy_radius)
        indy2.set_intensity(intensity2)
        reading2 = OldTex("{1\over b^2}").scale(formula_scale).move_to(indy2)
        indy2.add(reading2)

        indy3 = LightIndicator(color = LIGHT_COLOR, show_reading = False, radius = indy_radius)
        indy3.set_intensity(intensity1 + intensity2)
        reading3 = OldTex("{1\over h^2}").scale(formula_scale).move_to(indy3)
        indy3.add(reading3)

        plus_sign = OldTex("+").scale(formula_scale)
        equals_sign = OldTex("=").scale(formula_scale)

        plus_sign.next_to(indy1, RIGHT)
        indy2.next_to(plus_sign, RIGHT)
        equals_sign.next_to(indy2, RIGHT)
        indy3.next_to(equals_sign, RIGHT)
        

        formula = VGroup(
            indy1, plus_sign, indy2, equals_sign, indy3
        )

        formula.move_to(ORIGIN)

        self.play(FadeIn(indy1))
        self.play(FadeIn(plus_sign), FadeIn(indy2))
        self.play(FadeIn(equals_sign), FadeIn(indy3))

        buffer = 1.5
        box = Rectangle(width = formula.get_width() * buffer,
            height = formula.get_height() * buffer)
        box.move_to(formula)
        text = OldTexText("Inverse Pythagorean Theorem").scale(formula_scale)
        text.next_to(box,UP)
        self.play(ShowCreation(box),Write(text))
