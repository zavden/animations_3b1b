# ==============================================================================
# Scene:      IndicatorScalingScene
# Source:     videos/_2018/basel/basel.py (lines 1613-1648)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IndicatorScalingScene.py IndicatorScalingScene -w -m --fps 15
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


class IndicatorScalingScene(Scene):

    def construct(self):

        unit_intensity = 0.6

        indicator1 = LightIndicator(show_reading = False, color = LIGHT_COLOR)
        indicator1.set_intensity(unit_intensity)
        reading1 = OldTex("1")
        reading1.move_to(indicator1)
        

        indicator2 = LightIndicator(show_reading = False, color = LIGHT_COLOR)
        indicator2.shift(2*RIGHT)
        indicator2.set_intensity(unit_intensity/4)
        reading2 = OldTex("{1\over 4}").scale(0.8)
        reading2.move_to(indicator2)

        indicator3 = LightIndicator(show_reading = False, color = LIGHT_COLOR)
        indicator3.shift(4*RIGHT)
        indicator3.set_intensity(unit_intensity/9)
        reading3 = OldTex("{1\over 9}").scale(0.8)
        reading3.move_to(indicator3)

        
        self.play(FadeIn(indicator1))
        self.play(FadeIn(reading1))
        self.wait()
        self.play(FadeOut(reading1))
        self.play(Transform(indicator1, indicator2))
        self.play(FadeIn(reading2))
        self.wait()
        self.play(FadeOut(reading2))
        self.play(Transform(indicator1, indicator3))
        self.play(FadeIn(reading3))
        self.wait()
