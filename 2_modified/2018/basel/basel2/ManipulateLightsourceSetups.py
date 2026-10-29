# ==============================================================================
# Scene:      ManipulateLightsourceSetups
# Source:     videos/_2018/basel/basel2.py (lines 1929-2039)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ManipulateLightsourceSetups.py ManipulateLightsourceSetups -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
# ==============================================================================

# CHANGE: import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


INDICATOR_STROKE_WIDTH = 1


INDICATOR_STROKE_COLOR = WHITE


INDICATOR_TEXT_COLOR = WHITE


AMBIENT_FULL = 0.5


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint, scale, cutoff: inverse_power_law(maxint,scale,cutoff,2)


class LightIndicator(Mobject):
    CONFIG = {
        "radius": 0.5,
        "reading_height" : 0.25,
        "intensity": 0,
        "opacity_for_unit_intensity": 1,
        "fill_color" : YELLOW,
        "precision": 3,
        "show_reading": True,
        "measurement_point": ORIGIN,
        "light_source": None
    }

    def init_points(self):
        self.background = Circle(color=BLACK, radius = self.radius)
        self.background.set_fill(opacity = 1.0)
        self.foreground = Circle(color=self.color, radius = self.radius)
        self.foreground.set_stroke(
            color=INDICATOR_STROKE_COLOR,
            width=INDICATOR_STROKE_WIDTH
        )
        self.foreground.set_fill(color = self.fill_color)

        self.add(self.background, self.foreground)
        self.reading = DecimalNumber(self.intensity,num_decimal_places = self.precision)
        self.reading.set_fill(color=INDICATOR_TEXT_COLOR)
        self.reading.set_height(self.reading_height)
        self.reading.move_to(self.get_center())
        if self.show_reading:
            self.add(self.reading)

    def set_intensity(self, new_int):
        self.intensity = new_int
        new_opacity = min(1, new_int * self.opacity_for_unit_intensity)
        self.foreground.set_fill(opacity=new_opacity)
        ChangeDecimalToValue(self.reading, new_int).update(1)
        if new_int > 1.1:
            self.reading.set_fill(color = BLACK)
        else:
            self.reading.set_fill(color = WHITE)
        return self

    def get_measurement_point(self):
        if self.measurement_point is not None:
            return self.measurement_point
        else:
            return self.get_center()

    def measured_intensity(self):
        distance = get_norm(
            self.get_measurement_point() - 
            self.light_source.get_source_point()
        )
        intensity = self.light_source.opacity_function(distance) / self.opacity_for_unit_intensity
        return intensity

    def update_mobjects(self):
        if self.light_source == None:
            print("Indicator cannot update, reason: no light source found")
        self.set_intensity(self.measured_intensity())


class ManipulateLightsourceSetups(PiCreatureScene):
    CONFIG = {
        "num_levels" : 100,
        "radius" : 10,
        "pi_creature_point" : 2*LEFT + 2*DOWN,
    }
    def construct(self):
        unit_distance = 3

        # Morty
        morty = self.pi_creature
        observer_point = morty.eyes[1].get_center()

        bubble = ThoughtBubble(height = 3, width = 4, direction = RIGHT)
        bubble.set_fill(BLACK, 1)
        bubble.pin_to(morty)

        # Indicator
        light_indicator = LightIndicator(
            opacity_for_unit_intensity = 0.5,
            fill_color = YELLOW,
            radius = 0.4,
            reading_height = 0.2,
        )
        light_indicator.move_to(bubble.get_bubble_center())
        def update_light_indicator(light_indicator):
            distance = get_norm(light_source.get_source_point()-observer_point)
            light_indicator.set_intensity((unit_distance/distance)**2)

        #Light source
        light_source = LightSource(
            opacity_function = inverse_quadratic(1,2,1),
            num_levels = self.num_levels,
            radius = self.radius,
            max_opacity_ambient = AMBIENT_FULL,
        )
        light_source.move_to(observer_point + unit_distance*RIGHT)

        #Light source copies
        light_source_copies = VGroup(*[light_source.copy() for x in range(2)])
        for lsc, vect in zip(light_source_copies, [RIGHT, UP]):
            lsc.move_to(observer_point + np.sqrt(2)*unit_distance*vect)

        self.add(light_source)
        self.add_foreground_mobjects(morty, bubble, light_indicator)
        self.add(Mobject.add_updater(light_indicator, update_light_indicator))
        self.play(
            ApplyMethod(
                light_source.shift, 0.66*unit_distance*LEFT,
                rate_func = wiggle,
                run_time = 5,
            ),
            morty.change, "erm",
        )
        self.play(
            UpdateFromAlphaFunc(
                light_source, 
                lambda ls, a : ls.move_to(
                    observer_point + rotate_vector(
                        unit_distance*RIGHT, (1+1./8)*a*TAU
                    )
                ),
                run_time = 6,
                rate_func = bezier([0, 0, 1, 1])
            ),
            morty.change, "pondering",
            UpdateFromFunc(morty, lambda m : m.look_at(light_source))
        )
        self.wait()

        plus = OldTex("+")
        point = light_indicator.get_center()
        plus.move_to(point)
        light_indicator_copy = light_indicator.copy()
        self.add_foreground_mobjects(plus, light_indicator_copy)
        self.play(
            ReplacementTransform(
                light_source, light_source_copies[0]
            ),
            ReplacementTransform(
                light_source.copy().fade(1), 
                light_source_copies[1]
            ),
            FadeIn(plus),
            UpdateFromFunc(
                light_indicator_copy,
                lambda li : update_light_indicator(li),
            ),
            UpdateFromAlphaFunc(
                light_indicator, lambda m, a : m.move_to(
                    point + a*0.75*RIGHT,
                )
            ),
            UpdateFromAlphaFunc(
                light_indicator_copy, lambda m, a : m.move_to(
                    point + a*0.75*LEFT,
                )
            ),
            run_time = 2
        )
        self.play(morty.change, "hooray")
        self.wait(2)

    ##

    def create_pi_creature(self):
        morty = Mortimer()
        morty.flip()
        morty.scale(0.5)
        morty.move_to(self.pi_creature_point)
        return morty
